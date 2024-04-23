import itertools
from typing import (
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
    TypeVar,
    Union,
    cast,
)
from uuid import UUID

import gtirb
import more_itertools
from typing_extensions import Literal

from .integral_symbols import assign_integral_symbols

T = TypeVar("T")


class LayoutError(Exception):
    """
    Layout was attempted, but the module could not be laid out.
    """


def _sliding_pair(iterable: Iterable[T]) -> Iterator[Tuple[T, Optional[T]]]:
    """
    Iterate over every item in an iterable, along with the next item in the
    iterable (or None if we're at the last item).
    """
    for a, b in more_itertools.pairwise(itertools.chain(iterable, (None,))):
        yield cast(T, a), b


def _address_sort_key(
    obj: Union[gtirb.Section, gtirb.ByteInterval]
) -> Tuple[bool, int, bool, int, UUID]:
    """
    Sorts objects by address in the same way as the C++ AddressLess does.
    """
    return (
        obj.address is not None,
        obj.address or 0,
        obj.size is not None,
        obj.size or 0,
        obj.uuid,
    )


def _block_sort_key(
    b: gtirb.ByteBlock,
) -> Tuple[int, int, int, gtirb.CodeBlock.DecodeMode, UUID]:
    """
    Sorts byte blocks in the same way as the C++ API does.
    """
    if isinstance(b, gtirb.CodeBlock):
        return (b.offset, b.size, 0, b.decode_mode, b.uuid)
    else:
        return (
            b.offset,
            b.size,
            1,
            gtirb.CodeBlock.DecodeMode.Default,
            b.uuid,
        )


def _first_code_block(bi: gtirb.ByteInterval) -> Optional[gtirb.CodeBlock]:
    """
    Gets the first code block in the byte interval at offset zero.
    """
    targets = sorted(
        (
            block
            for block in bi.blocks
            if isinstance(block, gtirb.CodeBlock) and block.offset == 0
        ),
        key=_block_sort_key,
    )
    return targets[0] if targets else None


def _get_predecessor_byte_interval(
    target_bi: gtirb.ByteInterval,
) -> Optional[gtirb.ByteInterval]:
    """
    Find the ByteInterval, if any, that falls through to the given interval.

    Assumes that at most one fallthrough edge from another byte interval to
    the given interval exists, that the source of that edge is the last block
    in its byte interval, and that the target of that edge is the first block
    in the given byte interval. Also assumes that both byte intervals are in
    the same section. Violating these assumptions will raise a
    LayoutException.

    :param target_bi: ByteInterval to find the predecessor for.

    :returns: a ByteInterval that contains the source of a fallthrough edge
    that targets the given ByteInterval, or None if no such source could be
    found.
    """
    target = _first_code_block(target_bi)
    if not target:
        return None

    for edge in target.incoming_edges:
        if edge.label and edge.label.type == gtirb.EdgeType.Fallthrough:
            if not isinstance(edge.source, gtirb.CodeBlock):
                raise LayoutError(
                    "Code block has fallthrough edge from proxy block!"
                )

            source_bi = edge.source.byte_interval
            if not source_bi or source_bi.section != target_bi.section:
                raise LayoutError(
                    "Block has fallthrough edge from a block in another "
                    "section!"
                )

            if edge.source.offset + edge.source.size < source_bi.size:
                raise LayoutError(
                    "fallthrough edge exists, but source is not at end of "
                    "interval"
                )

            return source_bi

    return None


def is_module_layout_required(
    module: gtirb.Module, skip_sections: Set[str] = set()
) -> bool:
    """
    Determine if a module needs to layout to run.
    """

    sorted_sections = sorted(module.sections, key=_address_sort_key)

    # If the module has no sections, we don't care that it has no address.
    for sect, next_sect in _sliding_pair(sorted_sections):
        if sect.name in skip_sections:
            continue

        # The pretty-printer requires that every section must have an address.
        if sect.address is None:
            return True

        if (
            next_sect
            and next_sect.address is not None
            and next_sect.address < (sect.address + cast(int, sect.size))
        ):
            return True

        # Because the section has an address, we know it has at least one byte
        # interval and each of its byte intervals has an address.
        sorted_intervals = sorted(sect.byte_intervals, key=_address_sort_key)
        for bi, next_bi in _sliding_pair(sorted_intervals):
            if next_bi and cast(int, next_bi.address) < (
                cast(int, bi.address) + bi.size
            ):
                return True

    # TODO: Should we also check that blocks are aligned according to the
    # "alignment" AuxData?
    # TODO: Should we ensure CodeBlocks with fallthrough edges are correct?
    return False


def _default_alignment(addr: Optional[int]) -> Literal[None, 2, 4, 8, 16]:
    """
    Compute the largest power of two (up to 16) that an address can be
    considered aligned to.

    :param addr: address to get alignment from.
    :returns: the largest power of 2 that the address is aligned to, or None
    if there is no address or it is unaligned to any power of two between 2
    and 16.
    """
    if addr is None:
        return None

    if addr & 0xF == 0:
        return 16

    if addr & 0x7 == 0:
        return 8

    if addr & 0x3 == 0:
        return 4

    if addr & 0x1 == 0:
        return 2

    return None


def _get_alignments(m: gtirb.Module) -> Dict[gtirb.ByteBlock, int]:
    """
    Collect the required alignments for blocks in a module.

    Uses the module's "alignment" AuxData, if present. For any ByteIntervals
    with addresses that do not contain blocks with user-defined alignment, the
    blocks in that ByteInterval will be assumed to be aligned to the largest
    power of two that is consistent with their current alignment.

    :param m: module to gather alignments for.
    :returns: An alignment table for blocks in the module.
    """
    result: Dict[gtirb.ByteBlock, int] = {}
    user_aligned_intervals: Set[gtirb.ByteInterval] = set()

    # Start with the user-specified alignment, if possible.
    alignment_table = m.aux_data.get("alignment", None)
    if alignment_table is not None:
        for node, alignment in alignment_table.data.items():
            if isinstance(node, gtirb.ByteBlock) and node.byte_interval:
                user_aligned_intervals.add(node.byte_interval)
                result[node] = alignment

    # Compute default alignment for blocks in byte intervals that were not
    # aligned by the user.
    for bi in m.byte_intervals:
        if bi.address is None or bi in user_aligned_intervals:
            continue

        for block in bi.blocks:
            alignment = _default_alignment(block.address)
            if alignment is not None:
                result[block] = alignment

    return result


def _toposort_intervals(s: gtirb.Section) -> List[gtirb.ByteInterval]:
    """
    Sort the ByteIntervals in a Section so that the sources of fallthrough
    edges are returned before the targets of those edges.

    If the CFG is well-behaved (each interval has at most one incoming and at
    most one outgoing fallthrough edge and there are no cycles of fallthrough
    edges) the sources and targets will be adjacent in the returned list. This
    implementation does not confirm that the CFG is well-behaved.

    :param s: Section containing the ByteIntervals to sort
    :returns: a vector containing the sorted pointers to the byte intervals.
    """
    sorted = []
    visited = set()
    for bi in s.byte_intervals:
        pending = []
        pred = bi
        while pred and pred not in visited:
            visited.add(pred)
            pending.append(pred)
            pred = _get_predecessor_byte_interval(pred)
        sorted.extend(pending[::-1])

    return sorted


def layout_module(m: gtirb.Module) -> None:
    """
    Lays out a module by assigning new addresses to byte intervals.
    """

    # Fix symbols with integral referents that point to known objects, since
    # performing layout would likely change what the integral symbols refer
    # to.
    assign_integral_symbols(m)

    # Get the desired ByteInterval alignments.
    alignments = _get_alignments(m)

    addr = 0

    for s in m.sections:
        for bi in _toposort_intervals(s):
            # If this interval contains any blocks with requested alignment,
            # update the address to maintain the alignment of the first of
            # them.
            for block in sorted(bi.blocks, key=_block_sort_key):
                alignment = alignments.get(block)
                if alignment is not None:
                    mask = alignment - 1
                    block_addr = addr + block.offset
                    if block_addr & mask:
                        addr += mask - (block_addr & mask) + 1
                    break

            bi.address = addr
            addr += bi.size


def remove_module_layout(module: gtirb.Module) -> None:
    """
    Removes all address information from the module, making it require layout
    to be performed.
    """

    # Fix symbols with integral referents that point to known objects, since
    # we won't be able to recover that information once we remove addresses.
    assign_integral_symbols(module)

    # Remove addresses from all byte intervals. We can always re-layout
    # the module later, usually without loss to pretty-printability.
    for interval in module.byte_intervals:
        interval.address = None

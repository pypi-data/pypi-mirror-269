from typing import cast

import gtirb


def assign_integral_symbols(module: gtirb.Module) -> None:
    """
    Finds symbols that refer to an address instead of a block and assigns them
    to blocks if possible.
    """

    # In general, we want as many integral symbols to not be integral as
    # possible. If they point to blocks, even 0-length ones, instead of raw
    # addresses, then they automatically get moved around when we adjust
    # addresses later in the layout process. This also removes the need
    # for the pretty-printer to check if it needs to print a symbol every time
    # the program counter increments.
    for sym in module.symbols:
        if sym.referent is not None or sym.value is None:
            continue

        # If a byte interval encompasses this address, then we can redirect
        # the symbol to point to it. It might also refer to the end of a byte
        # interval.
        byte_interval = next(
            iter(module.byte_intervals_on(sym.value)), None
        ) or next(iter(module.byte_intervals_on(sym.value - 1)), None)
        if not byte_interval:
            # TODO: should we emit a warning?
            continue

        # do we have a block at this exact address?
        block = next(iter(byte_interval.byte_blocks_at(sym.value)), None)
        if block:
            sym.referent = block
            continue

        # do we have a block that ends at this exact address?
        block = next(
            (
                block
                for block in byte_interval.byte_blocks_on(sym.value - 1)
                if cast(int, block.address) + block.size == sym.value
            ),
            None,
        )
        if block:
            sym.referent = block
            sym.at_end = True
            continue

        # do we have any block that overlaps the address?
        block = next(iter(byte_interval.byte_blocks_on(sym.value)), None)
        if block:
            new_block = type(block)(
                byte_interval=byte_interval,
                offset=sym.value - cast(int, byte_interval.address),
                size=0,
            )
            sym.referent = new_block
            continue

        # if all else fails, make it a new 0-length data block.
        block = gtirb.DataBlock(
            byte_interval=byte_interval,
            offset=sym.value - cast(int, byte_interval.address),
            size=0,
        )
        sym.referent = block

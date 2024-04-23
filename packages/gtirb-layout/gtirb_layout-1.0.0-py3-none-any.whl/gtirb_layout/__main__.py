import argparse

import gtirb

from .layout import layout_module


def main():
    ap = argparse.ArgumentParser(description="lay out GTIRB modules")
    ap.add_argument("in_ir", help="input GTIRB IR")
    ap.add_argument("out_ir", help="output GTIRB IR")
    args = ap.parse_args()

    ir = gtirb.IR.load_protobuf(args.in_ir)
    for module in ir.modules:
        layout_module(module)
    ir.save_protobuf(args.out_ir)


if __name__ == "__main__":
    main()

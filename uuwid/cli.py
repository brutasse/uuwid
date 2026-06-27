#!/usr/bin/env python3
import argparse
import sys

import uuwid


def main() -> None:
    parser = argparse.ArgumentParser(description="UUWID: Encode/decode UUIDs to words")
    sub = parser.add_subparsers(dest="cmd", required=True)

    enc = sub.add_parser("encode", help="Encode a UUID to words")
    enc.add_argument("uuid", nargs="?", help="UUID to encode (default: stdin)")

    dec = sub.add_parser("decode", help="Decode words to a UUID")
    dec.add_argument("words", nargs="?", help="Words to decode (default: stdin)")

    args = parser.parse_args()

    if args.cmd == "encode":
        value = args.uuid.strip() if args.uuid else sys.stdin.read().strip()
        print(uuwid.encode(value))
    else:
        value = args.words.strip() if args.words else sys.stdin.read().strip()
        print(uuwid.decode(value))


if __name__ == "__main__":
    main()

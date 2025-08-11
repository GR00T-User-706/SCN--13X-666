#!/usr/bin/env python3

import os
import argparse
import subprocess
import sys

def shred_file(file_path, args):
    if not os.path.exists(file_path):
        print(f"Operation Failure: Target File Not Found at {file_path}")
        sys.exit(1)

    shred_command = [
        "shred",
        "-f",
        "-u",
        "-z"
    ]

    if args.iterations:
        shred_command += ["-n", str(args.iterations)]

    if args.random_source:
        shred_command += ["--random-source", args.random_source]

    if args.size:
        shred_command += ["-s", args.size]

    if args.remove:
        shred_command += ["--remove", args.remove]

    if args.verbose:
        shred_command.append("-v")

    if args.exact:
        shred_command.append("-x")

    if args.zero:
        shred_command.append("-z")

    shred_command.append(file_path)

    subprocess.run(shred_command)

    if os.path.exists(file_path):
        print(f"Operation Failure: Target File Still Remains At {file_path}. Are You Rooted?")
        sys.exit(1)
    else:
        print("Target File Neutralized")


def main():
    parser = argparse.ArgumentParser(
        description="cleanslate: Tactical Footprint Remover using GNU shred",
        usage="cleanslate [options] <target_file>"
    )
    parser.add_argument("target_file", help="The file to shred and neutralize.")
    parser.add_argument("-f", "--force", action="store_true", help="Force change permissions to allow writing if necessary.")
    parser.add_argument("-n", "--iterations", type=int, help="Overwrite N times instead of default (3).")
    parser.add_argument("--random-source", help="Get random bytes from FILE.")
    parser.add_argument("-s", "--size", help="Shred this many bytes (K,M,G accepted).")
    parser.add_argument("-u", action="store_true", help="Deallocate and remove file after overwriting.")
    parser.add_argument("--remove", choices=['unlink', 'wipe', 'wipesync'], help="Control HOW to delete.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show progress.")
    parser.add_argument("-x", "--exact", action="store_true", help="Do not round file sizes up to the next full block.")
    parser.add_argument("-z", "--zero", action="store_true", help="Add final overwrite with zeroes.")
    parser.add_argument("--version", action="version", version="cleanslate 1.0")

    args = parser.parse_args()

    shred_file(args.target_file, args)

if __name__ == "__main__":
    main()

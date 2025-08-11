#!/usr/bin/env python3

import argparse
import json
import os
from datetime import datetime
from pathlib import Path

CONFIG_PATH = Path.home() / ".forgeid" / "config.json"
DEFAULT_OUTPUT_DIR = Path.cwd() / "artifacts" / "ids"

# Initialize segment store
SEGMENTS = {
    "PID": {
        "GNS": {"length": 3, "label": "GhoulNet Sanctuary", "type": "Project Codename"},
        "Σ": {"length": 1, "label": "Sigma", "type": "Directive Core"},
        "13": {"length": 2, "label": "Thirteen", "type": "Numerical Node"},
        "X": {"length": 1, "label": "Unknown/Chaos", "type": "Wildcard Directive"},
        "706": {"length": 3, "label": "Code 706", "type": "Personal Anchor"}
    },
    "SPID": {
        "R": {"length": 1, "label": "Rituals", "type": "Subsystem"},
        "CS": {"length": 2, "label": "CleanSlate", "type": "Module"},
        "001": {"length": 3, "label": "Instance ID", "instance": True}
    }
}

def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    else:
        return SEGMENTS

def save_config(config):
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)

def generate_id(config):
    pid = ':'.join(['GNS-Σ13X706'])
    spid = 'RCS-001'
    print(f"[+] Generated ID: {pid}:{spid}")
    return pid, spid

def export_markdown(pid, spid, config, output_dir):
    output_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d")
    filename = f"{pid.replace(':', '_')}_{spid}_{now}.md"
    filepath = output_dir / filename

    def format_table(segment, data):
        rows = ["| Segment | Length | Value | Meaning / Symbolism |",
                "|---------|--------|--------|----------------------|"]
        for key, props in data.items():
            label = props.get("label", "")
            length = len(key)
            rows.append(f"| `{key}` | {length} | {label} | {props.get('type', '')} |")
        return '\n'.join(rows)

    with open(filepath, 'w') as f:
        f.write(f"# Breakdown for {pid}:{spid}\n\n")
        f.write("## PID Segments\n")
        f.write(format_table("PID", config.get("PID", {})))
        f.write("\n\n## SPID Segments\n")
        f.write(format_table("SPID", config.get("SPID", {})))

    print(f"[+] Markdown exported to {filepath}")

def list_segments(config):
    print("\n[PID Segments]")
    for key, val in config.get("PID", {}).items():
        print(f"{key}: {val}")
    print("\n[SPID Segments]")
    for key, val in config.get("SPID", {}).items():
        print(f"{key}: {val}")

def add_segment(config, target):
    target = target.upper()
    if target not in config:
        print(f"[!] Invalid target: {target}. Must be PID or SPID.")
        return
    key = input("Segment Code (e.g. GNS): ").strip()
    label = input("Label (required): ").strip()
    type_ = input("Type (optional): ").strip()
    entry = {"length": len(key), "label": label}
    if type_:
        entry["type"] = type_
    config[target][key] = entry
    save_config(config)
    print(f"[+] Segment `{key}` added to {target}.")

def parse_id(id_str):
    try:
        pid, spid = id_str.split(":")
        print(f"[✓] Valid ID\n- PID: {pid}\n- SPID: {spid}")
    except ValueError:
        print("[!] Invalid ID format. Use PID:SPID")

def main():
    parser = argparse.ArgumentParser(description="forgeid: Modular ID Generator & Parser")
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--parse")
    parser.add_argument("--new-segment", action="store_true")
    parser.add_argument("--target")
    parser.add_argument("--output", type=str, default=str(DEFAULT_OUTPUT_DIR))
    parser.add_argument("--list-segments", action="store_true")
    parser.add_argument("--export")
    args = parser.parse_args()

    config = load_config()

    if args.generate:
        pid, spid = generate_id(config)
        export_markdown(pid, spid, config, Path(args.output))
    elif args.parse:
        parse_id(args.parse)
    elif args.new_segment and args.target:
        add_segment(config, args.target)
    elif args.list_segments:
        list_segments(config)
    elif args.export:
        export_markdown(*args.export.split(":"), config=config, output_dir=Path(args.output))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

import os
import json
import argparse
from collections import OrderedDict

EXPECTED_ORDER = [
    "final_ats_score",
    "certifications",
    "education",
    "experience",
    "grammar_cleanliness",
    "leadership",
    "responsibilities",
    "skills",
    "soft_skills",
    "tools",
    "transferable_skills"
]

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def is_output_field_order_consistent(output: dict) -> bool:
    actual_keys = list(output.keys())
    return actual_keys == EXPECTED_ORDER

def check_directory(directory: str):
    mismatched_files = []
    total_files = 0

    for filename in os.listdir(directory):
        if not filename.endswith(".json"):
            continue

        full_path = os.path.join(directory, filename)
        try:
            data = load_json(full_path)
            if "output" in data and isinstance(data["output"], dict):
                total_files += 1
                if not is_output_field_order_consistent(data["output"]):
                    mismatched_files.append(filename)
        except Exception as e:
            print(f"⚠️ Error reading {filename}: {e}")

    print(f"\n🔍 Scanned {total_files} files in '{directory}'")
    if mismatched_files:
        print(f"❌ Found {len(mismatched_files)} files with inconsistent output field order:")
        for f in mismatched_files:
            print(f"  - {f}")
    else:
        print("✅ All files have consistent output field order.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check SFT JSON files for consistent output field order.")
    parser.add_argument("directory", help="Path to the directory containing SFT JSON files")
    args = parser.parse_args()
    check_directory(args.directory)

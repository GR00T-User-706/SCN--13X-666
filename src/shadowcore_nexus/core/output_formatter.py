import json
import csv
import os
from datetime import datetime

class OutputFormatter:
    def __init__(self, output_dir="artifacts/intel_dumps/"):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def save_json(self, data, entity_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}{entity_name}_intel_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as outfile:
            json.dump(data, outfile, indent=4)
        print(f"[+] JSON Intel Saved: {filename}")

    def save_csv(self, data, entity_name):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}{entity_name}_intel_{timestamp}.csv"
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(data.keys())
            writer.writerow(data.values())
        print(f"[+] CSV Intel Saved: {filename}")
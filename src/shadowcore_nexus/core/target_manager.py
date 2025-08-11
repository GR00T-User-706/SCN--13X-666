import csv
import json
import os

class TargetManager:
    def __init__(self, target_file):
        self.target_file = target_file
        self.targets = []

    def load_targets(self):
        ext = os.path.splitext(self.target_file)[1]
        if ext == ".csv":
            self._load_csv()
        elif ext == ".json":
            self._load_json()
        else:
            raise ValueError("Unsupported file format. Use CSV or JSON.")

    def _load_csv(self):
        with open(self.target_file, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.targets.append(row)

    def _load_json(self):
        with open(self.target_file, 'r', encoding='utf-8') as jsonfile:
            self.targets = json.load(jsonfile)

    def prioritize_targets(self):
        if 'ecocide_index' in self.targets[0]:
            self.targets.sort(key=lambda x: float(x['ecocide_index']), reverse=True)

    def get_targets(self):
        return self.targets
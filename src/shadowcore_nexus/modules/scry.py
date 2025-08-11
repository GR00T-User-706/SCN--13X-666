from core.target_manager import TargetManager
from core.intel_harvester import IntelHarvester
from core.output_formatter import OutputFormatter

def main():
    target_loader = TargetManager("targets.csv")
    target_loader.load_targets()
    target_loader.prioritize_targets()
    targets = target_loader.get_targets()

    harvester = IntelHarvester(targets)
    formatter = OutputFormatter()

    for intel in harvester.run_recon():
        formatter.save_json(intel, intel['entity'])
        formatter.save_csv(intel, intel['entity'])

if __name__ == "__main__":
    main()
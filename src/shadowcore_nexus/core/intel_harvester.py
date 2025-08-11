from modules.email_scraper import EmailScraper
from modules.supply_chain_mapper import SupplyChainMapper
from modules.financial_trail import FinancialTrail
from modules.legal_case_fetcher import LegalCaseFetcher

class IntelHarvester:
    def __init__(self, targets):
        self.targets = targets

    def run_recon(self):
        for entity in self.targets:
            print(f"[+] Recon: {entity['name']}")
            email_data = EmailScraper(entity).scrape()
            supply_chain = SupplyChainMapper(entity).map_supply_chain()
            financials = FinancialTrail(entity).trace_finances()
            legal_cases = LegalCaseFetcher(entity).fetch_cases()

            yield {
                'entity': entity['name'],
                'emails': email_data,
                'supply_chain': supply_chain,
                'financial_trail': financials,
                'legal_cases': legal_cases
            }
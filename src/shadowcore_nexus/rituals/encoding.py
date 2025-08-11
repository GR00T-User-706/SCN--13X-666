from core.logger import log_event, log_history

PARAMS = ['input']

def run(**kwargs):
    input_file = kwargs.get('input')
    if not input_file:
        print("[-] No input file specified.")
        log_event("Encoding Ritual Failed - No input specified.")
        log_history("encoding", "Failed - No input specified.")
        return
        
    print(f"[Encoding Ritual] Executed on {input_file}")
    log_event(f"Encoding Ritual executed on {input_file}")
    log_history("encoding", f"Executed on {input_file}")


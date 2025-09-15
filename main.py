import argparse
import asyncio
import yaml
from src.core.api_client import ApiClient
from src.core.orchestrator import BatchOrchestrator
import os
# --- RETAILER MAPPING ---
from src.retailers.ambrose_parser import AmbroseParser
from src.retailers.brooksbrothers_parser import BrooksBrothersParser
from src.retailers.croma_parser import CromaParser
from src.retailers.dillards_parser import DillardsParser
from src.retailers.evo_parser import EvoParser
from src.retailers.fashionworld_parser import FashionWorldParser
from src.retailers.jcrew_parser import JcrewParser
from src.retailers.jdwilliams_parser import JDWilliamsParser
from src.retailers.joefresh_parser import JoeFreshParser
from src.retailers.lenovo_parser import LenovoParser
from src.retailers.lenovolas_parser import LenovoLasParser
from src.retailers.napaonline_parser import NapaOnlineParser
from src.retailers.simplybe_parser import SimplyBeParser
from src.retailers.solesupplier_parser import SoleSupplierParser
from src.retailers.revzilla_parser import RevzillaParser
from src.retailers.uniquevintage_parser import UniqueVintageParser

RETAILER_PARSERS = {
    "ambrose": AmbroseParser,
    "brooksbrothers": BrooksBrothersParser,
    "croma": CromaParser,
    "dillards": DillardsParser,
    "evo": EvoParser,
    "fashionworld": FashionWorldParser,
    "jcrew": JcrewParser,
    "jdwilliams": JDWilliamsParser,
    "joefresh": JoeFreshParser,
    "lenovo": LenovoParser,
    "lenovolas": LenovoLasParser,
    "napaonline": NapaOnlineParser,
    "simplybe": SimplyBeParser,
    "solesupplier": SoleSupplierParser,
    "revzilla": RevzillaParser,
    "uniquevintage": UniqueVintageParser,
}

# (The rest of the main.py file remains unchanged)
def load_config(retailer_name):
    """Loads the YAML configuration for a given retailer."""
    config_path = f"configs/{retailer_name}.yaml"
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file not found at '{config_path}'")
        return None

def create_output_directory(retailer_name):
    """Creates a retailer-specific output directory if it doesn't exist."""
    output_dir = f"outputs/{retailer_name}"
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def main():
    parser = argparse.ArgumentParser(description="Fetch product data from e-commerce sites.")
    parser.add_argument("retailer", choices=RETAILER_PARSERS.keys(), help="The retailer to process.")
    
    parser.add_argument(
        "-f", "--files", 
        type=int, 
        default=1, 
        help="The number of output files to split the results into. Defaults to 1."
    )
    
    args = parser.parse_args()

    retailer_name = args.retailer
    print(f"--- Starting data fetch for: {retailer_name.upper()} ---")

    config = load_config(retailer_name)
    if not config:
        return
    config['num_output_files'] = args.files
    print(f"Targeting {config['num_output_files']} output file(s).")
 
    output_dir = create_output_directory(retailer_name)
    config['output_dir'] = output_dir
    config['output_filename_base'] = f"{retailer_name}_results"  # Only the base name

    ParserClass = RETAILER_PARSERS[retailer_name]
    data_parser = ParserClass(config)
    api_client = ApiClient(config['retry_settings'])
    orchestrator = BatchOrchestrator(config, api_client, data_parser)

    asyncio.run(orchestrator.run())

if __name__ == "__main__":
    main()
import streamlit as st
import asyncio
from src.core.orchestrator import BatchOrchestrator
from src.core.api_client import ApiClient
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
import os
import yaml
import tempfile
import json
from io import BytesIO
import zipfile

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

def create_zip_file(file_paths):
    """Creates a ZIP file containing all the given file paths."""
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for file_path in file_paths:
            zip_file.write(file_path, os.path.basename(file_path))  # Add file with its base name
    zip_buffer.seek(0)  # Move the pointer to the beginning of the buffer
    return zip_buffer

def create_output_directory(retailer_name):
    """Creates a retailer-specific output directory if it doesn't exist."""
    output_dir = f"outputs/{retailer_name}"
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def run_orchestrator(keywords, retailer_name, num_output_files):
    """Runs the BatchOrchestrator with the given inputs."""
    # Load the retailer-specific configuration
    config_path = f"configs/{retailer_name}.yaml"
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)

    # Create a persistent temporary directory for outputs
    temp_dir = tempfile.TemporaryDirectory()  # Keep this alive until the function ends
    config['output_dir'] = temp_dir.name
    config['output_filename_base'] = f"{retailer_name}_results"
    config['num_output_files'] = num_output_files
    config['input_csv_path'] = None  # Not used since we pass keywords directly

    # Initialize the parser, API client, and orchestrator
    ParserClass = RETAILER_PARSERS[retailer_name]
    data_parser = ParserClass(config)
    api_client = ApiClient(config['retry_settings'])
    orchestrator = BatchOrchestrator(config, api_client, data_parser)

    # Inject keywords directly into the orchestrator
    orchestrator.keywords = keywords

    # Run the orchestrator
    asyncio.run(orchestrator.run())

    # Collect the output files
    output_files = [
        os.path.join(config['output_dir'], file)
        for file in os.listdir(config['output_dir'])
        if file.endswith('.json')
    ]

    # Return the output files and the temporary directory object
    return output_files, temp_dir

# Streamlit UI
st.title("Data Fetcher for LLM Assortment Analysis")

# User inputs
retailer_name = st.selectbox("Select Retailer", options=list(RETAILER_PARSERS.keys()))
keywords_input = st.text_area("Paste Keywords (one per line)")
num_output_files = st.number_input("Number of Output Files", min_value=1, value=1, step=1)

if st.button("Run"):
    if not keywords_input.strip():
        st.error("Please paste at least one keyword.")
    else:
        # Parse keywords
        keywords = [kw.strip() for kw in keywords_input.splitlines() if kw.strip()]
        st.info(f"Processing {len(keywords)} keywords for retailer '{retailer_name}'...")

        # Run the backend process
        try:
            output_files, temp_dir = run_orchestrator(keywords, retailer_name, num_output_files)
            st.success("Processing complete! Download your files below:")

            # Display download links for each file
            for file_path in output_files:
                with open(file_path, "r") as f:
                    file_data = f.read()
                st.download_button(
                    label=f"Download {os.path.basename(file_path)}",
                    data=file_data,
                    file_name=os.path.basename(file_path),
                    mime="application/json"
                )

            # Create a ZIP file for "Download All"
            zip_buffer = create_zip_file(output_files)
            st.download_button(
                label="Download All Files as ZIP",
                data=zip_buffer,
                file_name=f"{retailer_name}_results.zip",
                mime="application/zip"
            )

            # Cleanup temporary directory after downloads
            temp_dir.cleanup()

        except Exception as e:
            st.error(f"An error occurred: {e}")
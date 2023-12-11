import os
import sys
import subprocess
from argparse import ArgumentParser, RawTextHelpFormatter
from importlib import metadata

# Automatyczna instalacja pakietu 'tqdm', jeśli nie jest zainstalowany
required_pkg = 'tqdm'
installed_pkgs = {pkg.metadata['Name'] for pkg in metadata.distributions()}
if required_pkg not in installed_pkgs:
    subprocess.check_call([sys.executable, "-m", "pip", "install", required_pkg])

from tqdm import tqdm
from config_loader import load_patterns
from file_processor import process_file
from html_generator import generate_html_start, generate_html_end
from directory_structure import create_directory_structure
from pattern_utils import should_process

def parse_arguments():
    parser = ArgumentParser(
        description="Process directory contents based on specified modes.", 
        formatter_class=RawTextHelpFormatter
    )

    parser.add_argument(
        "--mode", 
        choices=["all", "ignore", "only", "size_only"], 
        default="all", 
        help=(
            "Specify the mode of operation:\n"
            "  all       - Process all files and directories, ignoring none.\n"
            "  ignore    - Ignore files and directories matching patterns\n"
            "              defined in the configuration file.\n"
            "  only      - Process only files and directories that match patterns\n"
            "              defined in the configuration file.\n"
            "  size_only - Generate output based on the size of files and directories\n"
            "              without processing their content."
        )
    )

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_directory = os.path.join(script_dir, 'combined')

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    combined_txt_path = os.path.join(output_directory, 'combined.txt')
    combined_html_path = os.path.join(output_directory, 'combined.html')

    config_file = os.path.join(script_dir, 'configs', 'config.json')
    ignore_patterns, only_patterns = load_patterns(config_file)

    with open(combined_txt_path, 'w', encoding='utf-8') as combined_txt, \
         open(combined_html_path, 'w', encoding='utf-8') as combined_html:

        generate_html_start(combined_html, output_directory)

        input_directory = './'  # lub inna ścieżka do katalogu źródłowego
        base_directory = os.path.abspath(input_directory)
        create_directory_structure(input_directory, ignore_patterns, only_patterns, args.mode, combined_html, combined_txt)

        for root, dirs, files in tqdm(os.walk(input_directory), desc="Processing Files"):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, input_directory)
                if should_process(file_path, ignore_patterns, only_patterns, args.mode, base_directory):
                    process_file(file_path, relative_path, combined_txt, combined_html, args.mode)

        generate_html_end(combined_html)

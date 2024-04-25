# Example:
# Help:
# python -m b2bTools --help
# Version:
# python -m b2bTools --version
# Single Seq:
# python -m b2bTools -i ./b2bTools/test/input/example_toy.fasta -o ~/workspace/sandbox/hackathonjune2023/example_toy.json --output_tabular_file ~/workspace/sandbox/hackathonjune2023/example_toy.csv --metadata_file ~/workspace/sandbox/hackathonjune2023/example_toy.meta.csv
# MSA:
# python -m b2bTools --sequence-id SEQ_1 --mode msa -i ./b2bTools/test/input/small_alignment.clustal -o ~/workspace/sandbox/hackathonjune2023/small_alignment.clustal.json --output_tabular_file ~/workspace/sandbox/hackathonjune2023/small_alignment.clustal.csv --metadata_file ~/workspace/sandbox/hackathonjune2023/small_alignment.clustal.meta.csv --distribution_json_file ~/workspace/sandbox/hackathonjune2023/small_alignment.clustal.distrib.json --distribution_tabular_file ~/workspace/sandbox/hackathonjune2023/small_alignment.clustal.distrib.csv
#

import argparse
import logging
import os
import sys
import traceback
from b2bTools import constants, MultipleSeq, SingleSeq
from b2bTools_version.versioning import PYPI_VERSION

print(sys.modules[__name__])

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format=f"%(asctime)s [b2bTools {PYPI_VERSION} %(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

def run(parsed_args):
    input_file = os.path.abspath(parsed_args.input_file)
    logging.info(f"Reading sequences from: {input_file}")

    if parsed_args.sequence_id is not None:
        logging.info(f"Sequence to filter: {parsed_args.sequence_id}")
        sequence_key = parsed_args.sequence_id
    else:
        sequence_key = None

    sep = "," if parsed_args.sep == "comma" else "\t"

    if parsed_args.output_tabular_file is not None:
        output_tabular_file = os.path.abspath(parsed_args.output_tabular_file)
    else:
        output_tabular_file = None

    if parsed_args.metadata_file is not None:
        metadata_file = os.path.abspath(parsed_args.metadata_file)
    else:
        metadata_file = None

    if parsed_args.distribution_json_file is not None:
        distribution_json_file =  os.path.abspath(parsed_args.distribution_json_file)
    else:
        distribution_json_file = None

    if parsed_args.distribution_tabular_file is not None:
        distribution_tabular_file =  os.path.abspath(parsed_args.distribution_tabular_file)
    else:
        distribution_tabular_file = None

    tools = [
        constants.TOOL_DYNAMINE if parsed_args.dynamine else None,
        constants.TOOL_DISOMINE if parsed_args.disomine else None,
        constants.TOOL_EFOLDMINE if parsed_args.efoldmine else None,
        constants.TOOL_AGMATA if parsed_args.agmata else None,
        constants.TOOL_PSP if parsed_args.psper else None,
    ]
    tools = [tool_name for tool_name in tools if tool_name is not None]
    logging.info(f"Tools to execute: {tools}")

    output_json_file = os.path.abspath(parsed_args.output_json_file)

    if parsed_args.mode == 'single_seq':
        logging.info("Predicting sequence(s)")
        wrapper = SingleSeq(input_file, short_id=parsed_args.short_ids)
        wrapper.predict(tools=tools)

        if sequence_key is not None and sequence_key != '':
            logging.info(f"Saving results for {sequence_key} in JSON format in: {output_json_file}")
            wrapper.get_all_predictions_json_file(output_filepath=output_json_file, sequence_key=sequence_key)
        else:
            logging.info(f"Saving results in JSON format in: {output_json_file}")
            wrapper.get_all_predictions_json_file(output_filepath=output_json_file)

    elif parsed_args.mode == 'msa':
        logging.info("Predicting sequence(s)")
        wrapper = MultipleSeq()
        wrapper.from_aligned_file(input_file, tools=tools)

        if sequence_key is not None and sequence_key != '':
            logging.info(f"Saving results for {sequence_key} in JSON format in: {output_json_file}")
            wrapper.get_all_predictions_json_file(output_filepath=output_json_file, sequence_key=sequence_key)
        else:
            logging.info(f"Saving results in JSON format in: {output_json_file}")
            wrapper.get_all_predictions_json_file(output_filepath=output_json_file)

        if distribution_json_file:
            logging.info(f"Saving distributions in JSON format in: {distribution_json_file}", )
            wrapper.get_msa_distrib_json(distribution_json_file)

        if distribution_tabular_file:
            logging.info(f"Saving distributions in tabular format in: {distribution_tabular_file}")
            wrapper.get_msa_distrib_tabular(distribution_tabular_file)
    else:
        raise NotImplementedError(f"Invalid mode: {parsed_args.mode}")

    if output_tabular_file:
        if sequence_key is not None and sequence_key != '':
            logging.info(f"Saving results for {sequence_key} in tabular format in: {output_tabular_file}")
            wrapper.get_all_predictions_tabular(output_tabular_file, sep=sep, sequence_key=sequence_key)
        else:
            logging.info(f"Saving results in tabular format in: {output_tabular_file}")
            wrapper.get_all_predictions_tabular(output_tabular_file, sep=sep)

    if metadata_file:
        if sequence_key is not None and sequence_key != '':
            logging.info(f"Saving metadata for {sequence_key} in tabular format in: {metadata_file}")
            wrapper.get_metadata(metadata_file, sep=sep, sequence_key=sequence_key)
        else:
            logging.info(f"Saving metadata in tabular format in: {metadata_file}")
            wrapper.get_metadata(metadata_file, sep=sep)

def main():
    parser = argparse.ArgumentParser(prog='b2bTools', description='Bio2Byte Tool - Command Line Interface')
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s v3.0.6 for Python v{sys.version}')

    parser.add_argument('-i', '--input_file', required=True, help="File to process")
    parser.add_argument('-o', '--output_json_file', required=True, help="Path to JSON output file")
    parser.add_argument('-t', '--output_tabular_file', help="Path to tabular output file")
    parser.add_argument('-m', '--metadata_file', help="Path to tabular metadata file")

    # Only for MSA
    parser.add_argument('-dj', '--distribution_json_file', help="Path to distribution output JSON file")
    parser.add_argument('-dt', '--distribution_tabular_file', help="Path to distribution output JSON file")

    parser.add_argument('-s', '--sep', choices=["comma", "tab"], default="comma", help="Tabular separator")
    parser.add_argument('--short_ids', action='store_true', default=False, help="Trim sequence ids (up to 20 chars per seq)")

    parser.add_argument('--mode', choices=['single_seq', 'msa'], default="single_seq", help="Execution mode: Single Sequence or MSA Analysis")

    parser.add_argument('--dynamine', action='store_true', default=True, help="Run DynaMine predictor")
    parser.add_argument('--disomine', action='store_true', default=False, help="Run DisoMine predictor")
    parser.add_argument('--efoldmine', action='store_true', default=False, help="Run EFoldMine predictor")
    parser.add_argument('--agmata', action='store_true', default=False, help="Run AgMata predictor")
    parser.add_argument('--psper', action='store_true', default=False, help="Run PSPer predictor")

    parser.add_argument('-id', '--sequence_id', help="Sequence to extract results instead of getting all the results")

    parsed_args = None
    try:
        parsed_args = parser.parse_args()
    except SystemExit as e:
        if e.code > 0:
            logging.error('Please review your parameters and try again. Use `--help` or `-` to read docs.')
            sys.exit(2)
        elif e.code == 0:
            sys.exit(0)
        else:
            sys.exit(1)
    except BaseException as e:
        logging.error(f"An unexpected fatal error of type '{type(e).__name__}' occurred when executing predicting flow: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

    try:
        logging.info("Arguments parsed with success")
        run(parsed_args)
        logging.info("Execution finished with success")
    except FileNotFoundError as e:
        logging.error(f"File not found: {e.filename}. Please check the path is correct and try again")
        sys.exit(2)
    except Exception as e:
        logging.error(f"An unexpected error of type '{type(e).__name__}' occurred when executing predicting flow: {str(e)}")
        traceback.print_exc()
        sys.exit(1)
    except BaseException as e:
        logging.error(f"An unexpected fatal error of type '{type(e).__name__}' occurred when executing predicting flow: {str(e)}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

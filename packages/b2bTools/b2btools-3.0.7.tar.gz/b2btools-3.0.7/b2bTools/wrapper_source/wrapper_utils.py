import json
import statistics
import copy
import sys

import numpy as np
import pandas as pd

from ..singleSeq.Predictor import MineSuite
from ..multipleSeq.msa_core import predManager
from ..multipleSeq.msa_core import BlastManager
from ..multipleSeq.msa_core import MsaManager
from ..multipleSeq.msa_core import UniRef50Manager
from ..general.plotter import Plotter

from ..singleSeq import constants

from .metadata import Bio2ByteMetadata

class SingleSeq:
    """
    Stores the sequences, the filename where they were read from, tools to be executed and the result of the
    predicitons.

    Parameters:

            fileName (str): Path to the fasta file where the sequences of interest are located.
    """

    def __init__(self, fileName, short_id=False):
        """
        Constructor for the SingleSeq class. Reads the fasta file that contains the sequences, calls a function that
        reads the sequences and creates the structure to store all the information required to run and store the
        predicitons.

        Parameters:

            fileName (str): Path to the fasta file where the sequences of interest are located.


        """
        self.__mineSuite__ = MineSuite()
        self.__sequenceFileName__ = fileName
        self.__sequences__ = self.__mineSuite__.readFasta(fileName, short_id)
        self.__sequences_count__ = len(self.__sequences__)
        self.__predictor_runners__ = {
            constants.TOOL_DYNAMINE: self.__mineSuite__.dynaMine,
            constants.TOOL_EFOLDMINE: self.__mineSuite__.eFoldMine,
            constants.TOOL_DISOMINE: self.__mineSuite__.disoMine,
            constants.TOOL_AGMATA: self.__mineSuite__.agmata,
            constants.TOOL_PSP: self.__mineSuite__.psper
        }

        self.__results__ = {}

    def __str__(self):
        return f"Single Sequence Biophysical predictions: input_file={self.__sequenceFileName__}; sequences (count)={len(self.__sequences__)};"

    def __repr__(self):
        return str(self)

    # This method has the responsibility of running the asked predictions in a smart way: it omits the tools that already have a result
    def predict(self, tools=[], level = 0):
        """
        This method has the responsibility of running the asked predictions in a smart way: it omits the tools that
        already have a result and runs the remaining.

        Parameters:

            tools (list[str]) : List of tools to be ran. Any combination of the following tools is accepted:
                - "dynamine"
                - "disomine"
                - "efoldmine"
                - "agmata"
                - "psper"

        Returns:

            obj: self
        """

        if len(self.__sequences__) == 0:
            raise ValueError("Invalid input file, at least one sequence is expected")

        tools = sorted(list(set(tools)))

        if level == 0:
            self.__b2btools_metadata__ = Bio2ByteMetadata("Single Sequence", tools)

        for tool in tools:
            dependencies = constants.DEPENDENCIES[tool]

            if (len(dependencies) > 0):
                self.predict(tools=dependencies, level=level + 1)

            if self.__results__.get(tool, None) is None:
                predictor_function = self.__predictor_runners__[tool]
                predictor_function.allPredictions = self._all_predictions()

                if tool == constants.TOOL_EFOLDMINE:
                    predictor_function.predictSeqs(self.__sequences__, dynaMinePreds=predictor_function.allPredictions)
                elif tool == constants.TOOL_PSP:
                    seqs_dict = dict((key, value) for key, value in self.__sequences__)
                    predictor_function.predictSeqs(seqs_dict)
                else:
                    predictor_function.predictSeqs(self.__sequences__)

                self.__results__[tool] = predictor_function.allPredictions

        return self

    # Instead of using a list of tools as in predict method, this one uses flags to create a list of tools and call
    # the predict method:
    def semantic_predict(
            self,
            dynamics=False,
            aggregation=False,
            early_folding_propensity=False,
            disorder=False,
            phase_separating_protein=False
    ):
        """
        Instead of using a list of tools as in predict method, this one uses flags on the (high level) type of
        predictions desired to create a list of tools and call the predict method.

        Parameters:

            dynamics (bool, optional) : Whether or not dynamics predictions are to be ran
            aggregation (bool, optional) : Whether or not aggregation predictions are to be ran
            early_folding_propensity (bool, optional) : Whether or not early folding propensity predictions are to be ran
            disorder (bool, optional) : Whether or not disorder predictions are to be ran
            phase_separating_protein (bool, optional): Whether or not phase separating protein (PSP) are to be ran

        Returns:

            obj: self
        """
        tools_to_run = []

        if dynamics:
            tools_to_run.append(constants.TOOL_DYNAMINE)
        if aggregation:
            tools_to_run.append(constants.TOOL_AGMATA)
        if early_folding_propensity:
            tools_to_run.append(constants.TOOL_EFOLDMINE)
        if disorder:
            tools_to_run.append(constants.TOOL_DISOMINE)
        if phase_separating_protein:
            tools_to_run.append(constants.TOOL_PSP)

        return self.predict(tools=tools_to_run)

    def explicit_definition_predictions(self, backbone_dynamics=False,
                                        sidechain_dynamics=False,
                                        propoline_II=False,
                                        disorder_propensity=False,
                                        coil=False,
                                        beta_sheet=False,
                                        alpha_helix=False,
                                        early_folding_propensity=False,
                                        aggregation_propensity=False,
                                        protein_score=False,
                                        viterbi=False,
                                        complexity=False,
                                        arg=False,
                                        tyr=False,
                                        RRM=False):


        """

        Instead of using a list of tools as in predict method, this one uses flags on the (explicit) type of
        predictions desired to create a list of tools and call the predict method.

        Parameters:

            backbone_dynamics (bool, optional) : Whether or not backbone dynamics are to be predicted
            sidechain_dynamics (bool, optional) : Whether or not sidechain dynamics are to be predicted
            propoline_II (bool, optional) : Whether or not propoline II propensity is to be predicted
            disorder_propensity (bool, optional) : Whether or not disorder propensity is to be predicted
            coil (bool, optional) : Whether or not coil propensity is to be predicted
            beta_sheet (bool, optional) : Whether or not beta sheet propensity is to be predicted
            alpha_helix (bool, optional) : Whether or not alpha helix propensity is to be predicted
            early_folding_propensity (bool, optional) : Whether or not early folding propensity is to be predicted
            aggregation_propensity (bool, optional) : Whether or not aggregation propensity is to be predicted
            protein_score (bool, optional): Whether or not protein score from PSP is to be predicted
            viterbi (bool, optional): Whether or not Viterbi from PSP is to be predicted
            complexity (bool, optional): Whether or not complexity from PSP is to be predicted
            arg (bool, optional): Whether or not ARG from PSP is to be predicted
            tyr (bool, optional): Whether or not TYR from PSP is to be predicted
            RRM (bool, optional): Whether or not RRM from PSP is to be predicted

        Returns:

            obj: self

        """

        tools_to_run = []

        if backbone_dynamics or sidechain_dynamics or coil or beta_sheet or alpha_helix or propoline_II:
            tools_to_run.append(constants.TOOL_DYNAMINE)
        if disorder_propensity:
            tools_to_run.append(constants.TOOL_DISOMINE)
        if early_folding_propensity:
            tools_to_run.append(constants.TOOL_EFOLDMINE)
        if aggregation_propensity:
            tools_to_run.append(constants.TOOL_AGMATA)
        if protein_score or viterbi or complexity or arg or tyr or RRM:
            tools_to_run.append(constants.TOOL_PSP)

        return self.predict(tools=tools_to_run)

    def index(self, index_filepath, json_filename):
        all_predictions = self.get_all_predictions()

        with open(index_filepath, 'w') as index_file:
            index_file.write("id,json_file,residues_count\n")

            for sequence_key, prediction in all_predictions['proteins'].items():
                seq_len = len(prediction['seq'])

                index_line = "{0},{1},{2}\n".format(
                    sequence_key,
                    json_filename,
                    seq_len
                )
                index_file.write(index_line)

                index_file.flush()

        return self

    def get_metadata(self, output_filepath, sequence_key=None, sep=","):
        execution_time_df = self._get_execution_time_df(sequence_key)
        statistics_df = self._get_statistics_df(sequence_key)

        metadata_df = pd.merge(statistics_df, execution_time_df, on='sequence_id', how="outer")
        metadata_df.round(6).to_csv(output_filepath, sep=sep, index=False)

    def _get_statistics_df(self, sequence_key=None):
        stats_metadata_list = []
        results = self.get_all_predictions(sequence_key)

        # NOTES (Sophie & Adrián): Room for improvements
        # Pandas's read_json: https://pandas.pydata.org/pandas-docs/version/1.1/reference/api/pandas.read_json.html
        for sequence_id, predictions in results['proteins'].items():
            statistics_data = {}

            statistics_data["sequence_id"] = sequence_id
            statistics_data["length"] = len(predictions['seq'])
            statistics_data["protein_score"] = predictions.get('protein_score', None)

            for prediction_name in constants.PREDICTION_NAMES:
                values = predictions.get(prediction_name, None) #value of bb per residue [0.3,0.5]

                if prediction_name == "viterbi":
                    statistics_data[prediction_name + "_mean"] = None
                    statistics_data[prediction_name + "_median"] = None
                    statistics_data[prediction_name + "_variance"] = None
                    statistics_data[prediction_name + "_stdev"] = None
                    statistics_data[prediction_name + "_pvariance"] = None
                    statistics_data[prediction_name + "_pstdev"] = None
                    statistics_data[prediction_name + "_min"] = None
                    statistics_data[prediction_name + "_max"] = None
                else:
                    statistics_data[prediction_name + "_mean"] = statistics.mean(values) if values else None
                    statistics_data[prediction_name + "_median"] = statistics.median(values) if values else None
                    statistics_data[prediction_name + "_variance"] = statistics.variance(values) if values else None
                    statistics_data[prediction_name + "_stdev"] = statistics.stdev(values) if values else None
                    statistics_data[prediction_name + "_pvariance"] = statistics.pvariance(values) if values else None
                    statistics_data[prediction_name + "_pstdev"] = statistics.pstdev(values) if values else None
                    statistics_data[prediction_name + "_min"] = min(values) if values else None
                    statistics_data[prediction_name + "_max"] = max(values) if values else None

            stats_metadata_list.append(statistics_data)

        stats_metadata_df = pd.DataFrame.from_dict(stats_metadata_list)

        return stats_metadata_df

    def _get_execution_time_df(self, sequence_key=None):
        stats_metadata_list = []
        results = self.get_all_predictions(sequence_key)
        # NOTES (Sophie & Adrián): Room for improvements
        # Pandas's read_json: https://pandas.pydata.org/pandas-docs/version/1.1/reference/api/pandas.read_json.html
        for sequence_id, predictions in results['proteins'].items():
            statistics_data = { 'sequence_id': sequence_id }

            for predictor_name in constants.PREDICTOR_NAMES:
                execution_time_key = f'{predictor_name}_execution_time'
                statistics_data[execution_time_key] = predictions.get(execution_time_key, None)

            stats_metadata_list.append(statistics_data)

        stats_metadata_df = pd.DataFrame.from_dict(stats_metadata_list)
        return stats_metadata_df

    def get_all_predictions_tabular(self, output_filepath, sequence_key=None, sep=","):
        prediction_names = sorted(constants.PREDICTION_NAMES)
        tsv_column_names = ['sequence_id', 'residue', 'residue_index', *prediction_names]

        rows_list = []
        # For each sequence
        for protein_key, protein in self.get_all_predictions(sequence_key)['proteins'].items():
            residues = protein["seq"]

            for residue_index, residue_value in enumerate(residues):
                row = { 'sequence_id': protein_key, 'residue': residue_value, 'residue_index': residue_index}

                for predictor in prediction_names:
                    row[predictor] = protein[predictor][residue_index] if predictor in protein else None

                rows_list.append(row)

        sequence_df = pd.DataFrame.from_dict(rows_list)
        sequence_df.round(3).to_csv(
            output_filepath,
            header=True,
            columns=tsv_column_names,
            index=False,
            sep=sep
        )

    def _all_predictions(self):
        all_predictions = {}

        for tool in self.__predictor_runners__:
            current_tool_predictions = self.__predictor_runners__[tool].allPredictions
            for sequence_key in current_tool_predictions:
                if not sequence_key in all_predictions:
                    all_predictions[sequence_key] = current_tool_predictions[sequence_key]
                else:
                    all_predictions[sequence_key].update(current_tool_predictions[sequence_key])

        return all_predictions

    def get_all_predictions_json(self, identifier):
        """
        Outputs all available predictions in a JSON formatted string. This still needs to be written in the desired
        output channel by the user.

        Parameters:

            identifier (str) : Identifier used as the root key of the JSON output.

        Returns:

            str : JSON string with outputs
        """
        self.__mineSuite__.allPredictions = self._all_predictions()

        return self.__mineSuite__.getAllPredictionsJson(identifier=identifier)

    def get_all_predictions(self, sequence_key = None):
        """
        Returns the values in dictionary form. It also allows to select the outputs of a single sequence from the
        original fasta file instead of all of them at once.

        Parameters:

            sequence_key (str, optional) : Sequence identifier specified as the FASTA header in the input
        file. It allow the user to select the output of a single sequence.

        Returns:

            reorganized_results (dict) : Dictionary which contains the output of the predictions.

        """
        result = self._all_predictions()

        if sequence_key is not None:
            results_to_reorganize = {sequence_key: result[sequence_key]}
        else:
            results_to_reorganize = result

        reorganized_results = self._organize_predictions_in_dictionary(results_to_reorganize)

        return reorganized_results

    def _organize_predictions_in_dictionary(self, results):
        new_result = {
            'proteins': {},
            'metadata': self.__b2btools_metadata__.build_metadata_dict()
        }

        for protein_key, protein in results.items():
            new_keys = {}

            for i, prediction_key_name in enumerate(protein):
                if prediction_key_name == 'seq' and 'seq' in protein:
                    new_keys['seq'] = protein['seq']
                    continue
                elif i == 0:
                    new_keys['seq'] = [position[0] for position in protein[prediction_key_name]]

                if type(protein[prediction_key_name]) == list or type(protein[prediction_key_name]) == np.array or type(protein[prediction_key_name]) == np.ndarray:
                    new_keys[prediction_key_name] = [position[1] for position in protein[prediction_key_name]]
                else:
                    new_keys[prediction_key_name] = protein[prediction_key_name]

            new_result['proteins'][protein_key] = new_keys

        return new_result

    def get_all_predictions_json_file(self, output_filepath, sequence_key=None):
        predictions = self.get_all_predictions(sequence_key)

        with open(output_filepath, "w") as fp:
            json.dump(predictions, fp, indent=4)

class MultipleSeq:
    """
    Class to handle all the MSA related inputs, it calculates the aligned
    predictions and plots accordingly.

    """

    def __init__(self):
        """
            Instates the predManager class required for all the methods below.

        """
        self._predManager = predManager()

    def from_aligned_file(self, path_to_msa, tools=[]):
        """
        This method has the responsibility of running the asked predictions when
        the input is an MSA file.

        Parameters:

            path_to_msa (str): Path to the file where the alignment is located.

            tools (list[str]) : List of tools to be ran. Any combination of the
            following tools is accepted:
                - "dynamine"
                - "disomine"
                - "efoldmine"
                - "agmata"

        Returns:

            obj: self
        """
        self.type = "from_msa"
        self.__b2btools_metadata__ = Bio2ByteMetadata("MSA", tools)
        return self._predManager.run_predictors(path_to_msa, predTypes=tools)

    def from_two_msa(self, path_to_msa1, path_to_msa2, tools=[]):
        """
        This method has the responsibility of running the asked predictions when
        the input are two MSA files to be compared.

        Parameters:

            path_to_msa1 (str): Path to the 1st file where the alignment is
            located.

            path_to_msa2 (str): Path to the 2nd file where the alignment is
            located.

            tools (list[str]) : List of tools to be ran. Any combination of the
            following tools is accepted:
                - "dynamine"
                - "disomine"
                - "efoldmine"
                - "agmata"

        Returns:

            obj: self
        """
        self.type = "from_msa"
        self.__b2btools_metadata__ = Bio2ByteMetadata("MSA", tools)
        msa = MsaManager()
        msa.t_coffe_MSA_aligner([path_to_msa1, path_to_msa2])
        return self._predManager.run_predictors(msa.out_file_name,
                                                msa_map=msa.msa_dict,
                                                predTypes=tools)

    def from_json(self, path_to_json, tools=[], output_dir=""):
        """
        This method has the responsibility of running the asked predictions when
        the input is a json file defining sequence variants (predefined format).

        Parameters:

            path_to_json (str): Path to the json file with the sequence variants
            tools (list[str]) : List of tools to be ran. Any combination of the
            following tools is accepted:
                - "dynamine"
                - "disomine"
                - "efoldmine"
                - "agmata"
            output_dir (str): Path to the output fasta file created by reading the json file

        Returns:

            obj: self
        """
        self.type = "from_json"
        self.__b2btools_metadata__ = Bio2ByteMetadata("MSA", tools)
        return self._predManager.run_predictors_json_input(path_to_json,
                                                           predTypes=tools)

    def from_blast(self, path_to_sequence, tools=[], blast_file_name = None, mut_option = None, mut_position=None, mut_residue=None):
        """
        This method has the responsibility of running the asked predictions when
        the input is a fasta file with a single sequence from which an alignment
        is generated with the BLAST hits.

        Parameters:

            path_to_sequence (str): Path to the fasta file where the sequence of
            interest is located.

            tools (list[str]) : List of tools to be ran. Any combination of the
            following tools is accepted:
                - "dynamine"
                - "disomine"
                - "efoldmine"
                - "agmata"

        Returns:

            obj: self
        """
        self.type = "from_msa"
        self.__b2btools_metadata__ = Bio2ByteMetadata("MSA", tools)
        blast = BlastManager(path_to_sequence, file_name=blast_file_name, mut_option=mut_option, mut_position=mut_position, mut_residue=mut_residue)
        blast.run_qblast()
        return self._predManager.run_predictors(blast.aligned_file,
                                                mutation=None,
                                                predTypes=tools)

    def from_uniref(self, uniprotKB_id, tools=[]):
        """
        This method has the responsibility of running the asked predictions when
        the input is a UniprotKB identifier from which an alignment is generated
        with the UniRef hits (Top 25).

        Parameters:

            uniprotKB_id (str): UniprotKB identifier

            tools (list[str]) : List of tools to be ran. Any combination of the
            following tools is accepted:
                - "dynamine"
                - "disomine"
                - "efoldmine"
                - "agmata"

        Returns:

            obj: self
        """
        self.type = "from_msa"
        self.__b2btools_metadata__ = Bio2ByteMetadata("MSA", tools)
        uniref = UniRef50Manager(uniprotKB_id, 'uniref')
        return self._predManager.run_predictors(uniref.aligned_file,
                                                predTypes=tools)

    # Tested
    def get_all_predictions_msa(self, sequence_key=None):
        """
        This method has the responsibility of returning the predictions mapped
        to the alignment. A sequence identifier can be used to retrieve only the
        desired predictions.

        Parameters:

            sequence_key (str): Sequence identifier

        Returns:

            obj: Aligned predictions
        """

        results_dict = { 'proteins': {}, 'sequences': {} }

        aligned_predictions = self._predManager.allAlignedPredictions
        sequence_keys = [key for key in aligned_predictions.keys() if key != "sequence"]

        for current_sequence_key in sequence_keys:
            if sequence_key is None or sequence_key == current_sequence_key:
                results_dict['proteins'][current_sequence_key] = aligned_predictions[current_sequence_key]
                results_dict['sequences'][current_sequence_key] = aligned_predictions['sequence'][current_sequence_key]

        return results_dict

    # Tested
    def get_all_predictions_msa_distrib(self):
        """
        This method has the responsibility of returning the distribution of the
        predictions for all the positions in the alignment (Top-outlier, third-
        quartile, median, 1st quartile, bottom-outlier)

        Returns:

            obj: Distribution of the aligned predictions

        """
        return self._predManager.ms.getDistributions()

    # Tested
    def get_all_predictions_tabular(self, output_filepath, sequence_key = None, sep=","):
        prediction_names = sorted(constants.PREDICTION_NAMES)
        tsv_column_names = ['sequence_id', 'residue', 'residue_index', *prediction_names]

        rows_list = []
        predictions_msa =  self.get_all_predictions_msa(sequence_key)
        proteins = predictions_msa['proteins']

        # For each sequence
        for protein_key, protein in proteins.items():
            residues = predictions_msa["sequences"][protein_key]

            for residue_index, residue_value in enumerate(residues):
                row = { 'sequence_id': protein_key, 'residue': residue_value, 'residue_index': residue_index}

                for predictor in prediction_names:
                    row[predictor] = protein[predictor][residue_index] if predictor in protein else None

                rows_list.append(row)

        sequence_df = pd.DataFrame.from_dict(rows_list)
        sequence_df.round(3).to_csv(
            output_filepath,
            header=True,
            columns=tsv_column_names,
            index=False,
            sep=sep,
            decimal="."
        )

    # Tested
    def get_metadata(self, output_filepath, sequence_key=None, sep=","):
        execution_time_df = self._get_execution_time_df(sequence_key)
        statistics_df = self._get_statistics_df(sequence_key)

        metadata_df = pd.merge(statistics_df, execution_time_df, on='sequence_id', how="outer")
        metadata_df.round(6).to_csv(output_filepath, sep=sep, index=False)

    def _get_statistics_df(self, sequence_key=None):
        stats_metadata_list = []

        all_predictions = self.get_all_predictions_msa(sequence_key)
        proteins = all_predictions['proteins']

        # NOTES (Sophie & Adrián): Room for improvements
        # Pandas's read_json: https://pandas.pydata.org/pandas-docs/version/1.1/reference/api/pandas.read_json.html

        for sequence_id, predictions in proteins.items():
            statistics_data = {
                "sequence_id": sequence_id,
                "length": len([r for r in all_predictions['sequences'][sequence_id] if r != '-']),
                "aligned_length": len(all_predictions['sequences'][sequence_id]),
                "protein_score": predictions.get('protein_score', None)
            }

            for predictor_name in constants.PREDICTION_NAMES:
                values = predictions.get(predictor_name, None) #value of bb per residue [0.3,0.5]

                if predictor_name == "viterbi":
                    statistics_data[predictor_name + "_mean"] = None
                    statistics_data[predictor_name + "_median"] = None
                    statistics_data[predictor_name + "_variance"] = None
                    statistics_data[predictor_name + "_stdev"] = None
                    statistics_data[predictor_name + "_pvariance"] = None
                    statistics_data[predictor_name + "_pstdev"] = None
                    statistics_data[predictor_name + "_min"] = None
                    statistics_data[predictor_name + "_max"] = None
                else:
                    statistics_data[predictor_name + "_mean"] = statistics.mean([i for i in values if i is not None]) if values else None
                    statistics_data[predictor_name + "_median"] = statistics.median([i for i in values if i is not None]) if values else None
                    statistics_data[predictor_name + "_variance"] = statistics.variance([i for i in values if i is not None]) if values else None
                    statistics_data[predictor_name + "_stdev"] = statistics.stdev([i for i in values if i is not None]) if values else None
                    statistics_data[predictor_name + "_pvariance"] = statistics.pvariance([i for i in values if i is not None]) if values else None
                    statistics_data[predictor_name + "_pstdev"] = statistics.pstdev([i for i in values if i is not None]) if values else None
                    statistics_data[predictor_name + "_min"] = min([i for i in values if i is not None]) if values else None
                    statistics_data[predictor_name + "_max"] = max([i for i in values if i is not None]) if values else None

            stats_metadata_list.append(statistics_data)

        stats_metadata_df = pd.DataFrame.from_dict(stats_metadata_list)

        return stats_metadata_df

    def _get_execution_time_df(self, sequence_key=None):
        stats_metadata_list = []

        # NOTES (Sophie & Adrián): Room for improvements
        # Pandas's read_json: https://pandas.pydata.org/pandas-docs/version/1.1/reference/api/pandas.read_json.html

        all_sequences = self.get_all_predictions_msa(sequence_key)
        proteins = all_sequences['proteins']

        for protein_key, protein in proteins.items():
            statistics_data = { 'sequence_id': protein_key }

            for predictor_name in constants.PREDICTOR_NAMES:
                execution_time_key = f'{predictor_name}_execution_time'
                statistics_data[execution_time_key] = protein.get(execution_time_key, None)

            stats_metadata_list.append(statistics_data)

        stats_metadata_df = pd.DataFrame.from_dict(stats_metadata_list)

        return stats_metadata_df

    # Tested
    def get_msa_distrib_json(self, output_filepath):
        distrib = self.get_all_predictions_msa_distrib()
        distrib['metadata'] = self.__b2btools_metadata__.build_metadata_dict()

        with open(output_filepath, "w") as fp:
            json.dump(distrib, fp)

    def _get_msa_distrib_df(self):
        distrib = self.get_all_predictions_msa_distrib()
        results = distrib['results']

        table_dict = {}
        for prediction_name in constants.PREDICTION_NAMES:
            for distribution_key in constants.DISTRIBUTION_KEYS:
                column_name = f"{prediction_name}_{distribution_key}"

                if prediction_name in results and distribution_key in results[prediction_name]:
                    table_dict[column_name] = results[prediction_name][distribution_key]
                else:
                    table_dict[column_name] = None

        distrib_df = pd.DataFrame.from_dict(table_dict)
        distrib_df.index.name='residue_index'
        distrib_df = distrib_df.reindex(sorted(distrib_df.columns), axis=1)
        return distrib_df

    # Tested
    def get_msa_distrib_tabular(self, output_filepath, sep=","):
        distrib_df = self._get_msa_distrib_df()
        distrib_df.round(6).to_csv(output_filepath, sep=sep, index=True, index_label="residue_index")

    def get_execution_metadata(self):
        return self.__b2btools_metadata__.build_metadata_dict()

    # Testing
    def get_all_predictions_json_file(self, output_filepath, sequence_key=None):
        predictions = self.get_all_predictions_msa(sequence_key)

        predictions['metadata'] = self.__b2btools_metadata__.build_metadata_dict()

        with open(output_filepath, "w") as fp:
            json.dump(predictions, fp, indent=4)

    def plot(self):
        """
        This method has the responsibility of returning the according prediction
        plots depending on the input.

        Returns:

            obj: Plots for the selected input

        """
        plotter = Plotter()
        if self.type == "from_msa":
            return plotter.plot_msa_distrib(self._predManager.jsondata_list)

        elif self.type == "from_json":
            return plotter.plot_json(self._predManager.allAlignedPredictions)
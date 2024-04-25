<h1 align="center">
  <a href="bio2byte.be/b2btools" target="_blank" ref="noreferrer noopener">
  <img src="https://pbs.twimg.com/profile_images/1247824923546079232/B9b_Yg7n_400x400.jpg" width="224px"/>
  </a>
  <br/>
  Bio2Byte Tools
</h1>
<p align="center">This package provides you structural predictions for protein sequences made by Bio2Byte group.</p>
<p align="center">
  <a href="https://anaconda.org/Bio2Byte/b2bTools"> <img src="https://anaconda.org/Bio2Byte/b2bTools/badges/version.svg" /></a>&nbsp;
  <a href="https://anaconda.org/Bio2Byte/b2bTools"> <img src="https://anaconda.org/Bio2Byte/b2bTools/badges/latest_release_relative_date.svg" /></a>&nbsp;
  <a href="https://anaconda.org/Bio2Byte/b2bTools"> <img src="https://anaconda.org/Bio2Byte/b2bTools/badges/platforms.svg" /></a>&nbsp;
  <a href="https://anaconda.org/Bio2Byte/b2bTools"> <img src="https://anaconda.org/Bio2Byte/b2bTools/badges/downloads.svg" /></a>&nbsp;
</p>

## 🧪 About this Python package

This package, called `b2bTools`, offers biophysical feature predictors for protein sequences as well as different file parses and other utilities to help you with your protein data analysis.
If your input data consists on one or more sequences not aligned, we provide you with the Single Sequence mode. On the other hand, if your input is a Multiple Sequence Alignment (MSA), we provide the MSA mode. For NMR data, we have the predictor ShiftCrypt.

About the available predictors:

| Predictor | Usage | Bio.Tools | Online predictor |
| --------- | --------- | ----  | ----  |
| DynaMine  | Fast predictor of protein backbone dynamics using only sequence information as input. The version here also predicts side-chain dynamics and secondary structure predictors using the same principle. | [Link](https://bio.tools/Dynamine) | [Start predicting online ▶️](https://bio2byte.be/b2btools/dynamine/)|
| DisoMine  | Predicts protein disorder with recurrent neural networks not directly from the amino acid sequence, but instead from more generic predictions of key biophysical properties, here protein dynamics, secondary structure and early folding. | [Link](https://bio.tools/Disomine) | [Start predicting online ▶️](https://bio2byte.be/b2btools/disomine/)|
| EfoldMine | Predicts from the primary amino acid sequence of a protein, which amino acids are likely involved in early folding events. | [Link](https://bio.tools/b2btools) | [Start predicting online ▶️](https://bio2byte.be/b2btools/efoldmine) |
| AgMata    | Single-sequence based predictor of protein regions that are likely to cause beta-aggregation. | [Link](https://bio.tools/agmata) | [Start predicting online ▶️](https://bio2byte.be/b2btools/agmata/) |
| PSPer    | PSP (Phase Separating Protein) predicts whether a protein is likely to phase-separate with a particular mechanism involving RNA interacts (FUS-like proteins). It will highlight the regions in your protein that are involved mechanistically, and provide an overall score. | [Link](https://bio.tools/PSPer) | [Start predicting online ▶️](https://bio2byte.be/b2btools/psp/) |
| ShiftCrypt    | Auto-encoding NMR chemical shifts from their native vector space to a residue-level biophysical index | [Link](https://bio.tools/ShiftCrypt) | [Start predicting online ▶️](https://bio2byte.be/b2btools/shiftcrypt/) |

**🔗 Related link:**

- These tools are described on the Bio2Byte website inside the [Tools section](https://bio2byte.be/tool/).
- [Galaxy](https://usegalaxy.org) is an open source, web-based platform for data intensive biomedical research. There is an available version of the Single Sequence predictors on Galaxy Europe. Start predicting online using Galaxy from [this link](https://usegalaxy.eu/root?tool_id=toolshed.g2.bx.psu.edu/repos/iuc/b2btools_single_sequence/b2btools_single_sequence/3.0.5+galaxy0).

## Usage and examples

To install the latest version of this package:

```console
$ pip install b2bTools
```

**⚠️ Important notes:** [Hmmer](http://hmmer.org) and [T-Coffee](https://tcoffee.crg.eu) are required to run several features. Please install them following their official guidelines.

### Single Sequence predictions

Use this example as an entry point when you have a FASTA file containing one or more sequences. There is a live demo available on [Google Colab](https://colab.research.google.com/github/Bio2Byte/public_notebooks/blob/main/Bio2ByteTools_v3_singleseq_pypi.ipynb).

#### Predicting biophysical features in JSON format

```python
# Import necessary modules:
# 'json' for file operations
# and specific functions/classes from 'b2bTools'.
import json
from b2bTools import SingleSeq, constants

# Define the path to the input FASTA file containing the protein sequences.
input_fasta = "/path/to/example.fasta"

# Initialize a SingleSeq object with the input FASTA file.
single_seq = SingleSeq(input_fasta)

# Use the predict method of the SingleSeq object to run predictions using a predefined set of tools.
# All the available tools are specified in 'constants.PREDICTOR_NAMES', which includes 'dynamine', 'disomine', 'efoldmine', 'agmata', 'psper'.
single_seq.predict(tools=constants.PREDICTOR_NAMES)

# Retrieve all the predictions made by the previously specified tools and store them in a dictionary.
predictions = single_seq.get_all_predictions()

# Extract the protein predictions from the overall predictions dictionary.
protein_predictions = predictions['proteins']

# Iterate through the protein predictions. Each iteration provides a sequence ID and its associated prediction values.
for sequence_id, prediction_values in protein_predictions.items():
    # Open a new JSON file for each sequence ID to write the prediction values.
    # The file is named using the input FASTA file path and the sequence ID.
    with open(f"{input_fasta}_{sequence_id}.json", "w") as fp:
        # Write the prediction values to the file in a pretty-printed JSON format.
        json.dump(prediction_values, fp, indent=4)

# Additionally, save the execution metadata associated with the predictions into a CSV file.
with open(f"{input_fasta}_exec_metadata.json", "w") as fp:
    # Write the execution metadata to the file in a pretty-printed JSON format.
    json.dump(predictions['metadata'], fp, indent=4)
```

#### Predicting biophysical features in tabular formats (CSV, TSV)

```python
# Import necessary libraries:
import json
from b2bTools import SingleSeq, constants

# Define the path to the input FASTA file containing the protein sequences.
input_fasta = "/path/to/example.fasta"

single_seq = SingleSeq(input_fasta)
single_seq.predict(tools=constants.PREDICTOR_NAMES)

# Output the predictions in a tabular format to a CSV file.
# The method 'get_all_predictions_tabular' is called
# with the filename (appending '_residues.csv' to the input FASTA path) and the separator set to a comma (',')
single_seq.get_all_predictions_tabular(f"{input_fasta}_residues.csv", sep=",")

# Additionally, output the predictions in a tabular format to a TSV file.
single_seq.get_all_predictions_tabular(f"{input_fasta}_residues.tsv", sep="\t")
```

The output contains these columns:

| Predictor | Value | Data type |
| --------- | ----- | --------- |
| None      | `sequence_id` | `String` |
| None      | `residue`     | `Char` |
| None      | `residue_index` | `Integer` |
| PSPer     | `RRM` | `Float` |
| AgMata     | `agmata` | `Float` |
| PSPer     | `arg` | `Float` |
| DynaMine     | `backbone` | `Float` |
| DynaMine     | `coil` | `Float` |
| PSPer     | `complexity` | `Float` |
| DisoMine     | `disoMine` | `Float` |
| PSPer     | `disorder` | `Float` |
| EFoldMine     | `earlyFolding` | `Float` |
| DynaMine     | `helix` | `Float` |
| DynaMine     | `ppII` | `Float` |
| DynaMine     | `sheet` | `Float` |
| DynaMine     | `sidechain` | `Float` |
| PSPer     | `tyr` | `Float` |

#### Plotting biophysical features
In case you need to plot the prediction values:

```python
# Import necessary libraries.

import json
from b2bTools import SingleSeq, constants
from matplotlib import pyplot as plt

# Define the path to the input FASTA file containing the protein sequences.
input_fasta = "/path/to/example.fasta"

# Specify the ID of the sequence for which predictions are to be made.
sequence_id = "SEQ001"

# Predict features using 'DynaMine'.
single_seq = SingleSeq(input_fasta)
single_seq.predict(tools=constants.TOOL_DYNAMINE)

predictions = single_seq.get_all_predictions()
protein_predictions = predictions['proteins']

# Extract backbone and side chain predictions for the specified sequence ID. These predictions are part of the
# protein features predicted by DynaMine.
backbone_pred = protein_predictions[sequence_id]['backbone']
sidechain_pred = protein_predictions[sequence_id]['sidechain']

# Plot the backbone and sidechain predictions using matplotlib. Two lines are plotted: one for backbone predictions
# and another for side chain predictions. The x-axis represents amino acid positions, and the y-axis represents
# the prediction values.
plt.plot(range(len(backbone_pred)), backbone_pred, label = "Backbone")
plt.plot(range(len(backbone_pred)), sidechain_pred, label = "Sidechain")

# Add a legend to the plot to differentiate between the backbone and sidechain lines.
plt.legend()

# Label the x-axis as 'aa_position' to indicate amino acid positions and the y-axis as 'pred_values' to indicate
# the values of the predictions.
plt.xlabel('aa_position')
plt.ylabel('pred_values')

# Save the plot as an image file. The file path includes the input FASTA file path with a '.png' extension,
# indicating the plot is saved in PNG format.
plt.savefig("/path/to/example.fasta.png")
```

#### Extracting metadata

For extracting metadata from the prediction values in tabular format when analyzing Single Sequence input:

```python
# Import necessary libraries.
from b2bTools import SingleSeq, constants

# Define the path to the input FASTA file containing the protein sequences.
input_fasta = "/path/to/example.fasta"

single_seq = SingleSeq(input_fasta)

# Predict features using 'dynamine', 'disomine', 'efoldmine', 'agmata', 'psper'.
single_seq.predict(tools=constants.PREDICTOR_NAMES)

# Retrieve and save the metadata associated with the predictions to a CSV file.
single_seq.get_metadata(f"{input_fasta}.csv")
```

### Multiple Sequences Alignment predictions

Use the following example as an entry point when you have a MSA file input. There is a live demo available on Google Colab: [link](https://colab.research.google.com/github/Bio2Byte/public_notebooks/blob/main/Bio2ByteTools_v3_multipleseq_pypi.ipynb)

#### Predicting biophysical features in JSON format

```python
# Import necessary modules: 'json' for handling JSON data, and functionalities from 'b2bTools'.
import json
from b2bTools import MultipleSeq, constants

# Define the path to the input MSA (Multiple Sequence Alignment) file.
input_msa = "/path/to/example.afa"

# Create an instance of the MultipleSeq class, which is designed to handle operations on multiple sequences.
multiple_seq = MultipleSeq()

# Load the MSA file and specify the prediction tools to use. The 'from_aligned_file' method is used to read
# the alignment from the specified file, and 'constants.PREDICTOR_NAMES' defines the list of available tools.
multiple_seq.from_aligned_file(input_msa, tools=constants.PREDICTOR_NAMES)

# Retrieve the predictions for the MSA.
predictions = multiple_seq.get_all_predictions_msa()

# Extract the predictions specific to proteins from the overall predictions.
proteins_predictions = predictions['proteins']

# Iterate over the protein predictions.
for sequence_id, prediction_values in proteins_predictions.items():
    with open(f"{input_msa}_{sequence_id}_from_msa.json", "w") as fp:
        json.dump(prediction_values, fp, indent=4)

# Retrieve distribution data for all predictions made on the MSA.
distributions_dict = multiple_seq.get_all_predictions_msa_distrib()
distributions = distributions_dict['results']

# Save the distribution data to a JSON file.
with open(f"{input_msa}_distributions.json", "w") as fp:
    json.dump(distributions, fp, indent=4)

# Save the execution metadata to a JSON file.
execution_metadata = multiple_seq.get_execution_metadata()
with open(f"{input_msa}_execution_metadata.json", "w") as fp:
    json.dump(execution_metadata, fp, indent=4)
```

#### Predicting biophysical features in tabular formats (CSV, TSV)

```python
# Import the MultipleSeq class and constants from the b2bTools package.
from b2bTools import MultipleSeq, constants

# Specify the path to the input MSA file.
input_msa = "/path/to/example.afa"

# Instantiate a MultipleSeq object.
multiple_seq = MultipleSeq()
multiple_seq.from_aligned_file(input_msa, tools=constants.PREDICTOR_NAMES)

# Output the prediction results in a tabular format as a CSV file.
multiple_seq.get_all_predictions_tabular(f"{input_msa}_residues.csv", sep=",")

# Similarly, output the prediction results in a tabular format as a TSV file.
multiple_seq.get_all_predictions_tabular(f"{input_msa}_residues.tsv", sep="\t")
```

#### Extracting metadata
For extracting metadata from the prediction values in tabular format when analyzing MSA input:

```python
# Import the MultipleSeq class and a constants module from the b2bTools package.
from b2bTools import MultipleSeq, constants

# Specify the file path to the input MSA file.
input_msa = "/path/to/example.afa"

# Create an instance of the MultipleSeq class.
multiple_seq = MultipleSeq()
multiple_seq.from_aligned_file(input_msa, tools=constants.PREDICTOR_NAMES)

# Extract and save the metadata associated with the analysis of the MSA file.
multiple_seq.get_metadata(f"{input_msa}_metadata.csv")
```

## 💻 Installation

From the official documentation:

> [`pip`](https://pypi.org/) is the package installer for Python. You can use pip to install packages from the Python Package Index and other indexes.


To install the b2bTools package in your local environment:

```console
$ pip install b2bTools
```

**💡 Notes:** If you are using [Jupyter Notebook](https://jupyter.org) or [Google Colab](https://colab.research.google.com), install the package directly from `pip` inside a _code block_ cell:

```python
!pip install b2bTools
```

## 📦  Package content

### 🔍 General Tools

Besides the prediction tools, this package includes general bioinformatics tools useful to manipulate files.

#### 📄 Single Sequences files (FASTA format)

The class `FastaIO` provides the following static methods:

- `read_fasta_from_file`
- `read_fasta_from_string`
- `write_fasta`

Usage:

```python
from b2bTools.general.parsers.fasta import FastaIO
```

#### 📄 Multiple Sequences Alignments files

The class `AlignmentsIO` provides the following static methods:

- `read_alignments`
- `read_alignments_fasta`
- `read_alignments_A3M`
- `read_alignments_blast`
- `read_alignments_balibase`
- `read_alignments_clustal`
- `read_alignments_psi`
- `read_alignments_phylip`
- `read_alignments_stockholm`
- `write_fasta_from_alignment`
- `write_fasta_from_seq_alignment_dict`
- `json_preds_to_csv_singleseq`
- `json_preds_to_csv_msa`

Usage:

```python
from b2bTools.general.parsers.alignments import AlignmentsIO
```

#### 📄 NEF files

The class `NefIO` provides the following static methods:

- `read_nef_file`
- `read_nef_file_sequence_shifts`

Usage:

```python
from b2bTools.general.parsers.nef import NefIO
```

#### 📄 NMR-STAR files

The class `NMRStarIO` provides the following static methods:

- `read_nmr_star_project`
- `read_nmr_star_sequence_shifts`

Usage:

```python
from b2bTools.general.parsers.nmr_star import NMRStarIO
```

### 🔍 Biophysical features predictors

Given a predictor might be built on top of other, it is usual to get more output predictions than the expected:

| Predictor | Depends on            |
| --------- | --------------------- |
| Dynamine  | -                     |
| EfoldMine | Dynamine              |
| Disomine  | EfoldMine, Dynamine   |
| AgMata    | EfoldMine, Dynamine   |

These are all the available options to use inside the tools array parameter:

| Predictor | constant value              | literal value |
| --------- | ----------------------------| ------------- |
| Dynamine  | `constants.TOOL_DYNAMINE`   | `"dynamine"`  |
| EfoldMine | `constants.TOOL_EFOLDMINE`  | `"efoldmine"` |
| Disomine  | `constants.TOOL_DISOMINE`   | `"disomine"`  |
| AgMata    | `constants.TOOL_AGMATA`     | `"agmata"`    |
| PSPer     | `constants.TOOL_PSP`        | `"psper"`     |

The next table shows all the available predictor values by predictor:

| Predictor | Output key       | Output values (type) |
| --------- | ---------------- | -------------------- |
| Dynamine  | `"backbone"`     | `[Float]`            |
| Dynamine  | `"sidechain"`    | `[Float]`            |
| Dynamine  | `"helix"`        | `[Float]`            |
| Dynamine  | `"ppII"`         | `[Float]`            |
| Dynamine  | `"coil"`         | `[Float]`            |
| Dynamine  | `"sheet"`        | `[Float]`            |
| EfoldMine | `"earlyFolding"` | `[Float]`            |
| Disomine  | `"disoMine"`     | `[Float]`            |
| AgMata    | `"agmata"`       | `[Float]`            |
| PSPer     | `"viterbi"`      | `[Float]`            |
| PSPer     | `"complexity"`   | `[Float]`            |
| PSPer     | `"tyr"`          | `[Float]`            |
| PSPer     | `"arg"`          | `[Float]`            |
| PSPer     | `"RRM"`          | `[Float]`            |
| PSPer     | `"disorder"`     | `[Float]`            |

For MSA input files, the distribution dictionary and/or JSON will include:

```python
multiple_seq.get_all_predictions_msa_distrib()['results']
```

| Predictor | Output key       | Output values (type) |
| --------- | ---------------- | -------------------- |
| Dynamine  | `"backbone"`     | `['median', 'thirdQuartile', 'firstQuartile', 'topOutlier', 'bottomOutlier']`            |
| Dynamine  | `"sidechain"`    | `['median', 'thirdQuartile', 'firstQuartile', 'topOutlier', 'bottomOutlier']`            |
| Dynamine  | `"helix"`        | `['median', 'thirdQuartile', 'firstQuartile', 'topOutlier', 'bottomOutlier']`            |
| Dynamine  | `"ppII"`         | `['median', 'thirdQuartile', 'firstQuartile', 'topOutlier', 'bottomOutlier']`            |
| Dynamine  | `"coil"`         | `['median', 'thirdQuartile', 'firstQuartile', 'topOutlier', 'bottomOutlier']`            |
| Dynamine  | `"sheet"`        | `['median', 'thirdQuartile', 'firstQuartile', 'topOutlier', 'bottomOutlier']`            |
| EfoldMine | `"earlyFolding"` | `['median', 'thirdQuartile', 'firstQuartile', 'topOutlier', 'bottomOutlier']`            |
| Disomine  | `"disoMine"`     | `['median', 'thirdQuartile', 'firstQuartile', 'topOutlier', 'bottomOutlier']`            |
| AgMata    | `"agmata"`       | `['median', 'thirdQuartile', 'firstQuartile', 'topOutlier', 'bottomOutlier']`            |
| PSPer     | `"viterbi"`      | `['median', 'thirdQuartile', 'firstQuartile', 'topOutlier', 'bottomOutlier']`            |
| PSPer     | `"complexity"`   | `['median', 'thirdQuartile', 'firstQuartile', 'topOutlier', 'bottomOutlier']`            |
| PSPer     | `"tyr"`          | `['median', 'thirdQuartile', 'firstQuartile', 'topOutlier', 'bottomOutlier']`            |
| PSPer     | `"arg"`          | `['median', 'thirdQuartile', 'firstQuartile', 'topOutlier', 'bottomOutlier']`            |
| PSPer     | `"RRM"`          | `['median', 'thirdQuartile', 'firstQuartile', 'topOutlier', 'bottomOutlier']`            |
| PSPer     | `"disorder"`     | `['median', 'thirdQuartile', 'firstQuartile', 'topOutlier', 'bottomOutlier']`            |

The method `get_all_predictions` will return a dictionary with the following structure:

```python
{
  "SEQUENCE_ID_000": {
    "seq": "the input sequence 0",
    "result001": [0.001, 0.002, ..., 0.00],
    "result002": [0.001, 0.002, ..., 0.00],
    "...": [...],
    "resultN": [0.001, 0.002, ..., 0.00]
  },
  "SEQUENCE_ID_001": {
    "seq": "the input sequence 1",
    "result001": [0.001, 0.002, ..., 0.00],
    "result002": [0.001, 0.002, ..., 0.00],
    "...": [...],
    "resultN": [0.001, 0.002, ..., 0.00]
  },
  "...": { ... },
  "SEQUENCE_ID_N": {
    "seq": "the input sequence N",
    "result001": [0.001, 0.002, ..., 0.00],
    "result002": [0.001, 0.002, ..., 0.00],
    "...": [...],
    "resultN": [0.001, 0.002, ..., 0.00]
  },
}
```

You are ready to use the sequence and predictions to work with them. Here is an example of plotting the data.

```python
backbone_pred = predictions['SEQ001']['backbone']
sidechain_pred = predictions['SEQ001']['sidechain']

plt.plot(range(len(backbone_pred)), backbone_pred, label = "Backbone")
plt.plot(range(len(sidechain_pred)), sidechain_pred, label = "Sidechain")

plt.legend()
plt.xlabel('aa_position')
plt.ylabel('pred_values')
plt.show()
```

#### Running as Python module (no Python code involved)

You are able to use this package directly from your console session with no Python code involved. Further details available on [the official Python documentation site](https://docs.python.org/3/tutorial/modules.html#executing-modules-as-scripts)

```console
usage: b2bTools [-h] [-v] -i INPUT_FILE -o OUTPUT_JSON_FILE
                [-t OUTPUT_TABULAR_FILE] [-m METADATA_FILE]
                [-dj DISTRIBUTION_JSON_FILE] [-dt DISTRIBUTION_TABULAR_FILE]
                [-s {comma,tab}] [--short_ids] [--mode {single_seq,msa}]
                [--dynamine] [--disomine] [--efoldmine] [--agmata] [--psper]

Bio2Byte Tool - Command Line Interface

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -i INPUT_FILE, --input_file INPUT_FILE
                        File to process
  -o OUTPUT_JSON_FILE, --output_json_file OUTPUT_JSON_FILE
                        Path to JSON output file
  -t OUTPUT_TABULAR_FILE, --output_tabular_file OUTPUT_TABULAR_FILE
                        Path to tabular output file
  -m METADATA_FILE, --metadata_file METADATA_FILE
                        Path to tabular metadata file
  -dj DISTRIBUTION_JSON_FILE, --distribution_json_file DISTRIBUTION_JSON_FILE
                        Path to distribution output JSON file
  -dt DISTRIBUTION_TABULAR_FILE, --distribution_tabular_file DISTRIBUTION_TABULAR_FILE
                        Path to distribution output JSON file
  -s {comma,tab}, --sep {comma,tab}
                        Tabular separator
  --short_ids           Trim sequence ids (up to 20 chars per seq)
  --mode {single_seq,msa}
                        Execution mode: Single Sequence or MSA Analysis
  --dynamine            Run DynaMine predictor
  --disomine            Run DisoMine predictor
  --efoldmine           Run EFoldMine predictor
  --agmata              Run AgMata predictor
  --psper               Run PSPer predictor
```

##### To display the help section

```console
b2bTools --help
```

##### To visualize the version

```console
b2bTools --version
```

##### Example for Single Sequence

Please run this command to get all the predictions from your input FASTA file:

```console
b2bTools \
  --input_file /path/to/input/example_toy.fasta \
  --output_json_file /path/to/output/example_toy.json \
  --output_tabular_file /path/to/output/example_toy.csv \
  --metadata_file /path/to/output/example_toy.meta.csv
```

Expected output:

```console
2023-07-04 16:04:23,630 [b2bTools v3.0.6 INFO] Arguments parsed with success
2023-07-04 16:04:23,630 [b2bTools v3.0.6 INFO] Reading sequences from: /path/to/input/example_toy.fasta
2023-07-04 16:04:23,630 [b2bTools v3.0.6 INFO] Tools to execute: ['dynamine']
2023-07-04 16:04:23,630 [b2bTools v3.0.6 INFO] Predicting sequence(s)
...
2023-07-04 16:04:23,986 [b2bTools v3.0.6 INFO] Saving results in JSON format in: /path/to/output/example_toy.json
2023-07-04 16:04:24,006 [b2bTools v3.0.6 INFO] Saving results in tabular format in: /path/to/output/example_toy.csv
2023-07-04 16:04:24,040 [b2bTools v3.0.6 INFO] Saving metadata in tabular format in: /path/to/output/example_toy.meta.csv
2023-07-04 16:04:24,279 [b2bTools v3.0.6 INFO] Execution finished with success
```

Otherwise, if you need to extract only one sequence from the input file:

```console
b2bTools \
  --sequence_id Q647G9 \
  --input_file /path/to/input/example_toy.fasta \
  --output_json_file /path/to/output/example_toy.json \
  --output_tabular_file /path/to/output/example_toy.csv \
  --metadata_file /path/to/output/example_toy.meta.csv
```

```console
2023-07-04 16:25:35,486 [b2bTools v3.0.6 INFO] Arguments parsed with success
2023-07-04 16:25:35,486 [b2bTools v3.0.6 INFO] Reading sequences from: /path/to/input/example_toy.fasta
2023-07-04 16:25:35,486 [b2bTools v3.0.6 INFO] Sequence to filter: Q647G9
2023-07-04 16:25:35,486 [b2bTools v3.0.6 INFO] Tools to execute: ['dynamine']
2023-07-04 16:25:35,486 [b2bTools v3.0.6 INFO] Predicting sequence(s)
...
2023-07-04 16:25:35,842 [b2bTools v3.0.6 INFO] Saving results for Q647G9 in JSON format in: /path/to/output/example_toy.json
2023-07-04 16:25:35,845 [b2bTools v3.0.6 INFO] Saving results for Q647G9 in tabular format in: /path/to/output/example_toy.csv
2023-07-04 16:25:35,860 [b2bTools v3.0.6 INFO] Saving metadata for Q647G9 in tabular format in: /path/to/output/example_toy.meta.csv
2023-07-04 16:25:35,893 [b2bTools v3.0.6 INFO] Execution finished with success
```

##### Example for MSA

Please run this command to get all the predictions from your input MSA file:

```console
b2bTools \
  --mode msa \
  --input_file /path/to/input/small_alignment.clustal \
  --output_json_file /path/to/output/small_alignment.clustal.json \
  --output_tabular_file /path/to/output/small_alignment.clustal.csv \
  --metadata_file /path/to/output/small_alignment.clustal.meta.csv \
  --distribution_json_file /path/to/output/small_alignment.clustal.distrib.json \
  --distribution_tabular_file /path/to/output/small_alignment.clustal.distrib.csv
```

Expected output:

```console
2023-07-04 16:06:40,524 [b2bTools v3.0.6 INFO] Arguments parsed with success
2023-07-04 16:06:40,524 [b2bTools v3.0.6 INFO] Reading sequences from: /path/to/input/small_alignment.clustal
2023-07-04 16:06:40,524 [b2bTools v3.0.6 INFO] Tools to execute: ['dynamine']
2023-07-04 16:06:40,524 [b2bTools v3.0.6 INFO] Predicting sequence(s)
...
2023-07-04 16:06:40,749 [b2bTools v3.0.6 INFO] Saving results in JSON format in: /path/to/output/small_alignment.clustal.json
2023-07-04 16:06:40,751 [b2bTools v3.0.6 INFO] Saving distributions in JSON format in: /path/to/output/small_alignment.clustal.distrib.json
2023-07-04 16:06:40,760 [b2bTools v3.0.6 INFO] Saving distributions in tabular format in: /path/to/output/small_alignment.clustal.distrib.csv
2023-07-04 16:06:40,784 [b2bTools v3.0.6 INFO] Saving results in tabular format in: /path/to/output/small_alignment.clustal.csv
2023-07-04 16:06:40,788 [b2bTools v3.0.6 INFO] Saving metadata in tabular format in: /path/to/output/small_alignment.clustal.meta.csv
2023-07-04 16:06:40,807 [b2bTools v3.0.6 INFO] Execution finished with success
```

Otherwise, if you need to extract only one sequence from the input file:

```console
b2bTools \
  --mode msa \
  --sequence_id SEQ_1
  --input_file /path/to/input/small_alignment.clustal \
  --output_json_file /path/to/output/small_alignment.clustal.json \
  --output_tabular_file /path/to/output/small_alignment.clustal.csv \
  --metadata_file /path/to/output/small_alignment.clustal.meta.csv \
  --distribution_json_file /path/to/output/small_alignment.clustal.distrib.json \
  --distribution_tabular_file /path/to/output/small_alignment.clustal.distrib.csv
```

```console
2023-07-04 16:28:34,388 [b2bTools v3.0.6 INFO] Arguments parsed with success
2023-07-04 16:28:34,388 [b2bTools v3.0.6 INFO] Reading sequences from: /path/to/input/small_alignment.clustal
2023-07-04 16:28:34,388 [b2bTools v3.0.6 INFO] Sequence to filter: SEQ_1
2023-07-04 16:28:34,388 [b2bTools v3.0.6 INFO] Tools to execute: ['dynamine']
2023-07-04 16:28:34,388 [b2bTools v3.0.6 INFO] Predicting sequence(s)
...
2023-07-04 16:28:34,602 [b2bTools v3.0.6 INFO] Saving results for SEQ_1 in JSON format in: /path/to/output/small_alignment.clustal.json
2023-07-04 16:28:34,603 [b2bTools v3.0.6 INFO] Saving distributions in JSON format in: /path/to/output/small_alignment.clustal.distrib.json
2023-07-04 16:28:34,612 [b2bTools v3.0.6 INFO] Saving distributions in tabular format in: /path/to/output/small_alignment.clustal.distrib.csv
2023-07-04 16:28:34,632 [b2bTools v3.0.6 INFO] Saving results for SEQ_1 in tabular format in: /path/to/output/small_alignment.clustal.csv
2023-07-04 16:28:34,635 [b2bTools v3.0.6 INFO] Saving metadata for SEQ_1 in tabular format in: /path/to/output/small_alignment.clustal.meta.csv
2023-07-04 16:28:34,651 [b2bTools v3.0.6 INFO] Execution finished with success
```

#### From an aligned file

```python
import matplotlib.pyplot as plt
from b2bTools import MultipleSeq

multiple_seq = MultipleSeq()
multiple_seq.from_aligned_file("/path/to/example.fasta")

predictions = multiple_seq.get_all_predictions_msa("SEQ001")
backbone_pred = predictions['backbone']
sidechain_pred = predictions['sidechain']

plt.legend()
plt.xlabel('aa_position')
plt.ylabel('pred_values')
plt.show()
```

#### From two MSA files

```python
import matplotlib.pyplot as plt
from b2bTools import MultipleSeq

multiple_seq = MultipleSeq()
multiple_seq.from_two_msa("/path/to/example_a.fasta", "/path/to/example_b.fasta")

predictions = multiple_seq.get_all_predictions_msa("SEQ001")
backbone_pred = predictions['backbone']
sidechain_pred = predictions['sidechain']

plt.legend()
plt.xlabel('aa_position')
plt.ylabel('pred_values')
plt.show()
```

#### From a JSON with variations file

In this case, we support a JSON format to introduce variants in a sequence. For instance:

```json
{
  "metadata": { "name": "target_fasta_file" },
  "WT": "MAKSTILALLALVLVAHASAMRRERGRQGDSSSCERQVDRVNLKPCEQHIMQRIMGEQEQYDSYDIRSTRSSDQQQRCCDELNEMENTQRCMCEALQQIMENQCDRLQDRQMVQQFKRELMNLPQQCNFRAPQRCDLDVSGGRC",
  "Variants": {
    "Var1": ["A3S", "A11G"],
    "Var2": ["A2G", "K3_S4insPH", "T5del"]
  }
}
```

Where WT is the wild-type sequence, and the Variants key includes a dictionary of different variations. Each of them are handled by an array of replacements:

- <Target Residue><New Residue> (For example: Replace the A at the position 3 with a S would be `"A3S"`)

Regarding the input fasta file, the `metadata` key contains the name of the input, remember it should stored in the same directory than the json file.

The code snippet is:

```python
import matplotlib.pyplot as plt
from b2bTools import MultipleSeq

multiple_seq = MultipleSeq()
multiple_seq.from_json("/path/to/example.json")

predictions = multiple_seq.get_all_predictions_msa("SEQ001")
backbone_pred = predictions['backbone']
sidechain_pred = predictions['sidechain']

plt.legend()
plt.xlabel('aa_position')
plt.ylabel('pred_values')
plt.show()
```

#### From a sequence performing a BLAST before running the predictions

In case you want to perform a mutation of a residue at one specific position, you have the parameters `mut_position`, `mut_residue` and the value of `mut_option` must be `"y"`.

```python
import matplotlib.pyplot as plt
from b2bTools import MultipleSeq

multiple_seq = MultipleSeq()
multiple_seq.from_blast("path/to/example.fasta", mut_option="y", mut_position=1, mut_residue="A")

predictions = multiple_seq.get_all_predictions_msa("SEQ001")
backbone_pred = predictions['backbone']
sidechain_pred = predictions['sidechain']

plt.legend()
plt.xlabel('aa_position')
plt.ylabel('pred_values')
plt.show()
```

#### From an UniRef ID performing a BLAST before running the predictions

```python
import matplotlib.pyplot as plt
from b2bTools import MultipleSeq

multiple_seq = MultipleSeq()
multiple_seq.from_uniref("A2R2V4")

predictions = multiple_seq.get_all_predictions_msa("SEQ001")
backbone_pred = predictions['backbone']
sidechain_pred = predictions['sidechain']

plt.legend()
plt.xlabel('aa_position')
plt.ylabel('pred_values')
plt.show()
```

**⚠️ Note**: the query using the UniRef ID was limited to 25 results to increase the time performance.

### 🔍 ShiftCrypt predictor (NMR data)

```python
import json
from b2bTools.nmr.shiftCrypt.Predictor import ShiftCrypt
from b2bTools.nmr.shiftCrypt.shiftcrypt_pkg import shiftcrypt_parser as parser

shiftcrypt_instance = ShiftCrypt()
path_to_input = '/path/to/example.nef'

allProteinShifts = parser.parse_official(path_to_input)
result_list = shiftcrypt_instance.predictShifts(
    allProteinShifts,
    modelClass='1'
)

with open(f"{path_to_input}.json", "w") as fp:
    json.dump(result_list, fp, indent=4)
```

Regarding the `modelClass` parameter of method `predictShifts`:

- `modelClass='1'`: the method with the full set of Cs. this may retur a lot of -10 (missing values) because of the scarcity of cs data for some residues
- `modelClass='2'`: the method with just the most common Cs values
- `modelClass='3'`: the method with only N and H CS. Used for dimers


The next table shows all the available predictor values from `shiftcrypt_instance.predictShifts`. Please remind that the returning value is a list of dictionaries with these values:

| Predictor   | Output key       | Output values (type) |
| ---------   | ---------------- | -------------------- |
| ShiftCrypt  | `"ID_file"`      | `String`             |
| ShiftCrypt  | `"sequence"`     | `[Char]`             |
| ShiftCrypt  | `"seqCodes"`     | `[Integer]`          |
| ShiftCrypt  | `"shiftCrypt"`   | `[Float]`            |
| ShiftCrypt  | `"chainCode"`    | `String`             |

## 📚 Documentation: classes & methods

If you are interested in further details, please read the full documentation on [the Bio2Byte website](https://bio2byte.be/b2btools/package-documentation).

To generate locally the documentation you can follow the next steps described in this section.

1. Download the source code of the Bio2Byte Tools in your local environment:

```console
$ git clone git@bitbucket.org:bio2byte/b2btools.git && cd b2btools
```

2. Run the following command:

```console
$ make generate-docs
```

3. And then open folder `./wrapped_documentation`

**💡 Notes:** At any moment, you can read the docs of a method invoking the `__doc__` method (e.g. `print(SingleSeq.predict.__doc__)`).

## 📖 How to cite

If you use this package or data in this package, please cite:

| Predictor | Authors | Cite | Digital Object Identifier (DOI) |
| --------- | --------- | --------- | --------- |
| Dynamine  | Elisa Cilia, Rita Pancsa, Peter Tompa, Tom Lenaerts, and Wim Vranken | _Elisa Cilia, Rita Pancsa, Peter Tompa, Tom Lenaerts, and Wim Vranken._ From protein sequence to dynamics and disorder with DynaMine **Nature Communications 4:2741 (2013)** | https://www.nature.com/articles/ncomms3741 |
| Disomine  | Gabriele Orlando, Daniele Raimondi, Francesco Codice, Francesco Tabaro, Wim Vranken | _Gabriele Orlando, Daniele Raimondi, Francesco Codice, Francesco Tabaro, Wim Vranken._ Prediction of disordered regions in proteins with recurrent Neural Networks and protein dynamics. **bioRxiv 2020.05.25.115253 (2020)** | https://www.biorxiv.org/content/10.1101/2020.05.25.115253v1 |
| EfoldMine | Raimondi, D., Orlando, G., Pancsa, R. et al |  _Raimondi, D., Orlando, G., Pancsa, R. et al._ Exploring the Sequence-based Prediction of Folding Initiation Sites in Proteins. **Sci Rep 7, 8826 (2017)** | https://doi.org/10.1038/s41598-017-08366-3 |
| AgMata    | Gabriele Orlando, Alexandra Silva, Sandra Macedo-Ribeiro, Daniele Raimondi, Wim Vranken | _Gabriele Orlando, Alexandra Silva, Sandra Macedo-Ribeiro, Daniele Raimondi, Wim Vranken._ Accurate prediction of protein beta-aggregation with generalized statistical potentials **Bioinformatics , Volume 36, Issue 7, 1 April 2020, Pages 2076–2081 (2020)** | https://academic.oup.com/bioinformatics/article/36/7/2076/5670527 |
| PSPer    | Gabriele Orlando,  Daniele Raimondi,  Francesco Tabaro,  Francesco Codicè,  Yves Moreau, Wim F Vranken  | _Gabriele Orlando and others_, Computational identification of prion-like RNA-binding proteins that form liquid phase-separated condensates, **Bioinformatics, Volume 35, Issue 22, November 2019, Pages 4617–4623** | https://doi.org/10.1093/bioinformatics/btz274 |
| ShiftCrypt    | Gabriele Orlando,  Daniele Raimondi,  Luciano Porto Kagami,  Wim F Vranken | _Gabriele Orlando and others_. ShiftCrypt: a web server to understand and biophysically align proteins through their NMR chemical shift values, **Nucleic Acids Research, Volume 48, Issue W1, 02 July 2020, Pages W36–W40** | https://doi.org/10.1093/nar/gkaa391 |

<!--
## 📝 License
Bio2Byte Tools is free and open-source software licensed under the Apache 2.0 License.
-->

## 📝 Terms of use

1. The Bio2Byte group aims to promote open science by providing freely available online services, database and software relating to the life sciences, with focus on proteins. Where we present scientific data generated by others we impose no additional restriction on the use of the contributed data than those provided by the data owner.
1. The Bio2Byte group expects attribution (e.g. in publications, services or products) for any of its online services, databases or software in accordance with good scientific practice. The expected attribution will be indicated in 'How to cite' sections (or equivalent).
1. The Bio2Byte group is not liable to you or third parties claiming through you, for any loss or damage.
1. Any questions or comments concerning these Terms of Use can be addressed to [Wim Vranken](mailto:wim.vranken@vub.be).

<hr/>
<p align="center">© Wim Vranken, Bio2Byte group, VUB, Belgium</p>
<p align="center"><a href="https://bio2byte.be/" target="_blank" ref="noreferrer noopener">https://bio2byte.be/</a></p>

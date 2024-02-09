**Original Readme below!**

# Semantic Label Augmentation for Zero-Shot Hierarchical Classification

## Info
* Python version 3.8.8
* Install modules: ```pip install -r requirements.txt```

Please follow these steps in order to reproduce the results obtained in the paper

### Dataset download and preparation

Create the data folder that will hold the repository:

```python
mkdir datasets
```

Experiments are based on the following three datasets:

- to be completed with the name of the dataset and the to where they can be downloaded
-
-

Each dataset needs to be copied into its own subfolder inside the `datasets` folder. At the ned the structure of subfolders needs to be as it follows: 

```bash
datasets
├── AmazonHTC
├── DBPedia_Extract
└── WebOfScience

```

### Create an OpenAI account and get your personal api_key
Register on [**OpenAI website**](https://openai.com/) and create your own personal [KEY](https://platform.openai.com/api-keys)  to use the OpenAI API. 

FIXME: specify what to do with the API key, should it be stored in some file?

### Run the basic USP computation

Use the command (dimmi se è scritto bene)

```bash
python USP_benchmarking.py --dataset='AmazonHTC' --build_tree=True
```

Be sure to write build_tree=True as the script needs to create and save the taxonomy file for the first time. The script will also perform Zero-Shot Hierarchical classification using USP technique and print the final classification results in tabular form.

### Extend the dataset taxonomy using HiLA

Execute HiLA running the command 

```bash
python tax_deepening.py --key --tax_tree
```

where tax_tree is the path to the dataset taxonomy file. The script will overwrite the taxonomy file with the deepened one.

### Run the USP computation again

Use the command (dimmi se è scritto bene)

```bash
python USP_benchmarking.py --dataset='AmazonHTC' 
```

This time the USP computation will show the results from our paper.

### (Optional) Compute the metrics for the chosen dataset

Run the command

```bash
python density_estimation.py --dataset='AmazonHTC' 
```

to compute the metrics defined in our paper for every node with children.

### Original Readme
The original Readme can be found at [this link](https://github.com/bong-yo/TaxonomyZeroShooter)


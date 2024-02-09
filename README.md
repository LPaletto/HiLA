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
Register on [**OpenAI website**](https://openai.com/) and create your own personal [key](https://platform.openai.com/api-keys)  to use the OpenAI API. Take note of the API key, you will need it later on.


### Run the basic USP computation

**FIXME**: when you mention USP computation, link it to the repository of the original paper.

Launch the USP computation of the label taxonomy. For instance, for the AmazonHTC dataset, use the command:

```bash
python3 USP_benchmarking.py --dataset='AmazonHTC' --build_tree=True
```

In addition to creating the taxonomy, which will be saved in the folder `datasets/AmazonHTC/tax_tree.json`, the script will also perform Zero-Shot Hierarchical classification using USP technique and print the final classification results in tabular form. 

### Extend the dataset taxonomy using HiLA

Execute the HiLA algorithm to extend the taxonomy, running the command: 

```bash
python tax_deepening.py --key <YOUR API KEY> --tax_tree <PATH TO THE tax_tree.json FILE CREATED IN PREVIOUS STEP>
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


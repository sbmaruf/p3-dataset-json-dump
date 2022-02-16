# Download and Export P3 dataset to jsonl format

For some reason if you have GPU access, huggingface datasets occupy gpus to load the dataset. So please make sure your torch and tensorflow doesn't use cuda. Also note that, it donwloads the full P3 dataset at first then extract the json lines from the P3 dataset.

1. Clone the dataset repository.

```
git clone https://huggingface.co/datasets/bigscience/P3
```

2. Retrieve the configs of the P3 dataset 

```
cp P3/data_split_sizes.csv  .
rm -rf P3
```

3. Now export from huggingface dataset. Only use higher `--num-proc` if you have enough CPU.

```
export CACHE_DIR=cache
export RAW_OUTPUT_DIR="./raw_output_dir"
mkdir -p $CACHE_DIR
mkdir -p $RAW_OUTPUT_DIR
python export_p3_to_jsonl.py \
--dataset-name-or-path "bigscience/P3" \
--cache-dir $CACHE_DIR \
--raw-output-dir "./raw_output_dir" \
--num-proc 8
```

use `--config` flag to specify specific prompted dataset from P3. All the dataset info can be found in `data_split_sizes.csv` 

```
export CACHE_DIR=cache
export RAW_OUTPUT_DIR="./raw_output_dir"
mkdir -p $CACHE_DIR
mkdir -p $RAW_OUTPUT_DIR
python export_p3_to_jsonl.py \
--dataset-name-or-path "bigscience/P3" \
--cache-dir $CACHE_DIR \
--raw-output-dir "$RAW_OUTPUT_DIR" \
--config 'rotten_tomatoes_Sentiment_with_choices_' \
--num-proc 1
```

This will create a jsonl dump for each of the dataset split of P3 in $RAW_OUTPUT_DIR. 

A tree of the file structure would be,

```
raw_output_dir
├── log.txt
├── rotten_tomatoes_Sentiment_with_choices_
│   ├── test.jsonl
│   ├── train.jsonl
│   └── validation.jsonl
└── super_glue_boolq_based_on_the_following_passage
    ├── test.jsonl
    ├── train.jsonl
    └── validation.jsonl
```

Each of the line from the `*.jsonl` file will contain a sample. Here is an example for a single sample, 

```
{
    "source": "Based on the following passage, is durham university part of the russell group? Russell Group -- In March 2012 it was announced that four universities -- Durham, Exeter, Queen Mary University of London; and York -- would become members of the Russell Group in August of the same year. All of the new members had previously been members of the 1994 Group of British universities.", 
    "target": "Yes", 
    "prompt_name": "super_glue_boolq_based_on_the_following_passage", 
    "split_name": "validation"
}
```
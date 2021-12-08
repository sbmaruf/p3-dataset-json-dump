# Download and Export P3 dataset to jsonl format

1. Clone the dataset repository.

```
git clone https://huggingface.co/datasets/bigscience/P3
```

2. Retrieve the configs of the P3 dataset 

```
cp P3/data_split_sizes.csv  .
rm -rf P3
```

3. Now export from huggingface dataset.

```
export CACHE_DIR=~/.cache
export RAW_OUTPUT_DIR="./raw_output_dir"
mkdir -p $RAW_OUTPUT_DIR
python export_p3_to_jsonl.py \
--dataset-name-or-path "bigscience/P3" \
--cache-dir $CACHE_DIR \
--raw-output-dir "./raw_output_dir" \
--num-proc 8
```

use `--config` flag to specify specific prompted dataset from P3. All the dataset info can be found in `data_split_sizes.csv` 

```
export CACHE_DIR=~/.cache
export RAW_OUTPUT_DIR="./raw_output_dir"
mkdir -p $RAW_OUTPUT_DIR
python export_p3_to_jsonl.py \
--dataset-name-or-path "bigscience/P3" \
--cache-dir $CACHE_DIR \
--raw-output-dir "./raw_output_dir" \
--config 'super_glue_boolq_based_on_the_following_passage' 'rotten_tomatoes_Sentiment_with_choices_' \
--num-proc 8
```

This will create a json dumps for each of the dataset split of of P3 in $RAW_OUTPUT_DIR. 
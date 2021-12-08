import os
import json
import argparse
import datasets
import concurrent.futures


def load_and_index_dataset(dataset_name_or_path, config, cache_dir, raw_output_dir):
    
    def export(file_path, sub_dataset, dataset_name, tot_sample):
        with open(file_path, "w") as file_ptr:
            for dt in sub_dataset:
                json_dt = {
                    "source": dt['inputs_pretokenized'],
                    "target": dt['targets_pretokenized'],
                    "prompt_name": dataset_name
                }
                file_ptr.write("{}\n".format(json.dumps(json_dt)))
        assert sum([1 for line in open(file_path, "r")]) == tot_sample

    print("[x] Processing : {}".format(config))
    sub_dataset = datasets.load_dataset(
        dataset_name_or_path, config[0], cache_dir=cache_dir)
    file_folder = os.path.join(raw_output_dir, config[0])
    os.makedirs(file_folder, exist_ok=True)

    split_info = config[1]
    for split, tot_sample in split_info.items():
        split_file_path = os.path.join(file_folder, "{}.jsonl".format(split))
        split_sub_dataset = sub_dataset[split]
        export(split_file_path, split_sub_dataset, config[0], tot_sample)

    print("[x] Done {}".format(config))
    with open(os.path.join(raw_output_dir, "log.txt"), 'a') as filePtr:
        filePtr.write("{}\n".format(config[0]))
    return 0


def get_dataset_configs(args):
    all_configs, ret_config = {}, []
    for i, line in enumerate(open("data_split_sizes.csv", "r")):
        if i == 0:
            continue
        config_name, data_split = line.split("|")[0], json.loads(line.split("|")[1])
        all_configs[config_name]=data_split
    if args.configs is None:
        ret_config = [(cfg_name,split_info) for cfg_name, split_info in all_configs.items()]
    else:
        for cfg in args.configs:
            if cfg in all_configs:
                ret_config.append( (cfg, all_configs[cfg]) )
            else:
                raise NotImplementedError("Cannot find config in `https://huggingface.co/datasets/bigscience/P3/data_split_sizes.csv`.")
    return ret_config


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('--dataset-name-or-path', type=str, default="P3.py",
                        help="Path to the dataloader file")
    parser.add_argument('--cache-dir', type=str, required=True,
                        help='Path to the cache dir. (The directory may require very large space if it\'s not cached earlier.)')
    parser.add_argument('--raw-output-dir', type=str, required=True,
                        help='Path to the raw-output dir.')
    parser.add_argument('--num-proc', type=int, default=64,
                        help='Number of files to be processed in parallel.')
    parser.add_argument('--configs', nargs='+', default=None,
                        help='Config of the P3 split. If `None` it exports all the split.')
    args = parser.parse_args()
    configs = get_dataset_configs(args)
    total_num_config = len(configs)

    with open(os.path.join(args.raw_output_dir, "log.txt"), 'w') as filePtr:
        pass

    # Run multiprocessor
    with concurrent.futures.ProcessPoolExecutor(max_workers=args.num_proc) as executor:
        results = executor.map(
            load_and_index_dataset,
            [args.dataset_name_or_path for _ in range(total_num_config)],
            configs,
            [args.cache_dir for _ in range(total_num_config)],
            [args.raw_output_dir for _ in range(total_num_config)]
        )

    with open(os.path.join(args.raw_output_dir, "log.txt"), 'r') as filePtr:
        written_dataset = [line.strip() for line in  filePtr]
        for cfg in configs:
            if cfg[0] not in written_dataset:
                print("Failed to extract {} dataset.".format(cfg))



if __name__ == '__main__':
    main()
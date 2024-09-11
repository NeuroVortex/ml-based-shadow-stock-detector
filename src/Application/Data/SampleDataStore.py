import pandas as pd


class SampleDataStore:

    def save(self, data, file_path: str):
        flat_dict = self.__flatten_dict(data)
        with pd.HDFStore(file_path+'.h5', mode='w') as store:
            for key, df in flat_dict.items():
                store.put(key, df)
        print(f"All dataframes saved to {file_path}")

    @classmethod
    def __flatten_dict(cls, d, sep='_'):
        items = []
        for group, subgroups in d.items():
            for subgroup, dfs in subgroups.items():
                for i, df in enumerate(dfs):
                    flat_key = f"{group}{sep}{subgroup}{sep}{i}"
                    items.append((flat_key, df))
        return dict(items)

    @classmethod
    def __transform_dict(cls, dataset_store):
        new_dict = {}
        for key, value in dataset_store.items():
            new_dict[key] = {}

            for lv1_key, lv1_value in value.items():
                if lv1_key == 'similar_candles':
                    new_lv1_key = 'SimilarCandles'
                    new_dict[key][new_lv1_key] = []
                    for i, item in enumerate(lv1_value):
                        new_lv2_dict = {f'SimilarCandle{i}': item[f'Similar_Candle_{i}']}
                        new_dict[key][new_lv1_key].append(new_lv2_dict)

                else:
                    new_lv1_key = 'DissimilarCandles'
                    new_dict[key][new_lv1_key] = []
                    for i, item in enumerate(lv1_value):
                        new_lv2_dict = {f'DissimilarCandle{i}': item[f'Dissimilar_Candle_{i}']}
                        new_dict[key][new_lv1_key].append(new_lv2_dict)

        return new_dict

    @classmethod
    def __unflatten_dict(cls, flat_dict, sep='_'):
        nested_dict = {}
        for k, v in flat_dict.items():
            keys = k.split(sep)
            if len(keys) != 3:
                continue
            group, subgroup, idx = keys[0], keys[1], int(keys[2])

            if group not in nested_dict:
                nested_dict[group] = {}
            if subgroup not in nested_dict[group]:
                nested_dict[group][subgroup] = []

            while len(nested_dict[group][subgroup]) <= idx:
                nested_dict[group][subgroup].append(None)

            nested_dict[group][subgroup][idx] = v

        return nested_dict

    # Function to load dataframes from an HDF5 file and restore the nested dictionary structure
    def load(self, file_path):
        flatten_dict = self.__load_data(file_path)
        unflatten_dict = self.__unflatten_dict(flatten_dict)
        return unflatten_dict

    @classmethod
    def __load_data(cls, file_path):
        flat_dict = {}
        with pd.HDFStore(file_path, mode='r') as store:
            for key in store.keys():
                flat_key = key.strip('/')
                flat_dict[flat_key] = store[flat_key]

        return flat_dict

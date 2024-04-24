import sys
from pathlib import Path
from time import perf_counter

import numpy as np
import polars as pl
from autofaiss import build_index
from datasets import Dataset, concatenate_datasets, load_from_disk
from loguru import logger

sys.path.extend([str(Path.home() / 'PycharmProjects/retrieval')])
from build_index.func import tfidf, pp_text, make_dir


class Data:
    def __init__(self, path: Path):
        self.path = path

    def save_tmp(self, dataset, pp, path_tmp_ds, path_tmp_array, fn_kwargs):
        dataset = dataset.map(pp, batched=True, batch_size=512, fn_kwargs=fn_kwargs)
        dataset.set_format(type='numpy', columns=['embeddings'], output_all_columns=True)
        np.save(path_tmp_array, dataset['embeddings'])
        dataset.save_to_disk(path_tmp_ds)

    def create_dataset(self, data, preprocess, pp, mode: str = ''):
        # input
        path_tmp = {}
        for i in [f'{mode}_array', f'{mode}_ds']:
            path_tmp.update({i: Path(f'{self.path}/{i}')})
            make_dir(path_tmp[i])
        # model
        fn_kwargs = {'col': f'{mode}_item_name_clean', 'preprocess': preprocess}

        # save embeddings into array
        batch = 1_500_000
        if data.shape[0] > batch:
            logger.info(f'Create batch dataset: total data {data.shape}, batch {batch}')
            # batch
            for idx, b in enumerate(range(0, data.shape[0], batch)):
                # load dataset
                dataset = Dataset.from_pandas(data[b:b + batch].to_pandas())
                path_tmp_array = str(path_tmp[f'{mode}_array'] / f'{idx}.npy')
                path_tmp_ds = path_tmp[f'{mode}_ds'] / f'{idx}'
                self.save_tmp(dataset, pp, path_tmp_ds, path_tmp_array, fn_kwargs)
            return path_tmp
        else:
            logger.info(f'Create full dataset: total data {data.shape}')
            dataset = Dataset.from_pandas(data.to_pandas())
            path_tmp_array = str(path_tmp[f'{mode}_array'] / f'0.npy')
            path_tmp_ds = path_tmp[f'{mode}_ds'] / f'0'
            self.save_tmp(dataset, pp, path_tmp_ds, path_tmp_array, fn_kwargs)
            return path_tmp


class BELargeScale:
    def __init__(
            self,
            path: Path,
            text_sparse: int = 512,
            img_dim: int = None,
            text_dense: int = None,
    ):
        self.text_sparse = text_sparse
        self.path = path

    def match(self, df_db: pl.DataFrame, df_q: pl.DataFrame, top_k: int = 10):
        # tf-idf
        all_items = list(set(df_db['db_item_name_clean'].to_list() + df_q['q_item_name_clean'].to_list()))
        vectorizer = tfidf(all_items, dim=self.text_sparse)

        # dataset
        data = Data(self.path)
        path_tmp_db, path_tmp_q = None, None
        if self.text_sparse:
            path_tmp_db = data.create_dataset(df_db, mode='db', preprocess=vectorizer, pp=pp_text)
            path_tmp_q = data.create_dataset(df_q, mode='q', preprocess=vectorizer, pp=pp_text)

        # build index
        start = perf_counter()
        path_index = self.path / 'index'
        build_index(
            str(path_tmp_db['db_array']),
            index_path=str(path_index / f'ip.index'),
            index_infos_path=str(path_index / f'index.json'),
            save_on_disk=True,
            metric_type='ip',
            verbose=30,
        )
        logger.info(f'[Matching] Index: {perf_counter() - start:,.2f}s')

        # load dataset shard
        dataset_db = concatenate_datasets([
            load_from_disk(str(f)) for f in path_tmp_db['db_ds'].glob(f'*')
        ])
        dataset_q = concatenate_datasets([
            load_from_disk(str(f)) for f in path_tmp_q['q_ds'].glob('*')
        ])

        # add index
        dataset_db.load_faiss_index('embeddings', path_index / f'ip.index')

        # query
        start = perf_counter()
        score, result = dataset_db.get_nearest_examples_batch(
            'embeddings',
            dataset_q['embeddings'],
            k=top_k
        )
        for i, v in enumerate(result):
            del v['embeddings']
        logger.info(f'[Matching] Query: {perf_counter() - start:,.2f}s')

        # post process
        dict_ = {'score': [list(i) for i in score]}
        df_score = pl.LazyFrame(dict_).collect()
        df_result = pl.LazyFrame(result).drop(['embeddings']).collect()
        df_match = pl.concat([df_q, df_result, df_score], how='horizontal')
        df_match = df_match.explode([i for i in df_match.columns if 'db' in i] + ['score'])

        return df_match

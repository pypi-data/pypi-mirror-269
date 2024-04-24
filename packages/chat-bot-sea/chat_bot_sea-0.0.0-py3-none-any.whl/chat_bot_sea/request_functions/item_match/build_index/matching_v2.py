import polars as pl
from pathlib import Path
from qdrant_client import AsyncQdrantClient, QdrantClient
from qdrant_client.http import models
from loguru import logger
import asyncio
from time import perf_counter
from tqdm import tqdm
import sys

sys.path.extend([str(Path.home() / 'PycharmProjects/retrieval')])
from build_index.model import Model
from build_index.func import tfidf

logger.remove()
logger.add(sys.stdout, colorize=True, format='<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}:{function}</cyan> | <level>{message}</level>')


class Data:
    def __init__(self):
        self.payload = None

    def create_dataset(
            self,
            df,
            mode: str = None,
            text_sparse: int = None,
            img_dim: int = None,
            vectorizer=None,
    ) -> list[dict]:
        start = perf_counter()

        # dataframe to dataset
        from datasets import Dataset
        dataset = Dataset.from_pandas(df.to_pandas())

        # sparse
        if text_sparse:
            # sparse_model_id = 'naver/splade_v2_distil'
            # sparse_model, sparse_tokenizer = Model().get_sparse(sparse_model_id)
            # fn_kwargs = {'col': f'{mode}item_name_clean', 'sparse_tokenizer': sparse_tokenizer, 'sparse_model': sparse_model}
            # dataset = dataset.map(Model.pp_sparse, batched=True, batch_size=128, fn_kwargs=fn_kwargs)
            # dataset = dataset.map(Model.pp_sparse_norm, batched=True, batch_size=128, fn_kwargs=fn_kwargs)
            fn_kwargs = {'col': f'{mode}item_name_clean', 'vectorizer': vectorizer}
            dataset = dataset.map(Model.pp_sparse_tfidf, batched=True, batch_size=128, fn_kwargs=fn_kwargs)
            # del sparse_model, sparse_tokenizer

        # img
        if img_dim:
            img_model, img_processor = Model().get_img()
            fn_kwargs = {'col': f'{mode}file_path', 'processor': img_processor, 'model': img_model}
            dataset = dataset.map(Model.pp_img, batched=True, batch_size=512, fn_kwargs=fn_kwargs)
            del img_model, img_processor

        # dataset
        self.payload = dataset.to_pandas().reset_index().to_dict('records')
        logger.success(f'Dataset: create payloads {perf_counter() - start:.2f}s')
        return self.payload


async def DB_upsert(
        collection_name: str,
        payloads: list[dict],
        text_sparse: int = None,
        text_dense_dim: int = None,
        img_dim: int = None,

):
    config = {'host': 'localhost', 'grpc_port': 6334, 'prefer_grpc': True}
    client = AsyncQdrantClient(**config)

    # sparse vectors config
    # sparse_vectors_config = {}

        # sparse_vectors_config = {'text-sparse': models.SparseVectorParams(
        #     index=models.SparseIndexParams(on_disk=False),
        # )}

    # dense vectors config
    vectors_config = {}
    if text_sparse:
        vectors_config.update({'text-sparse': models.VectorParams(
            size=text_sparse,
            distance=models.Distance.COSINE,
            on_disk=False
        )})
    if text_dense_dim:
        vectors_config.update({'text-dense': models.VectorParams(
            size=text_dense_dim,
            distance=models.Distance.COSINE,
            on_disk=False
        )})
    if img_dim:
        vectors_config.update({'img-dense': models.VectorParams(
            size=img_dim,
            distance=models.Distance.COSINE,
            on_disk=False
        )})

    collection_params = {
        'collection_name': collection_name,
        # 'sparse_vectors_config': sparse_vectors_config,
        'vectors_config': vectors_config,
        'optimizers_config': models.OptimizersConfigDiff(
            indexing_threshold=0,
            default_segment_number=10
        ),  # disable indexing during upload
        'shard_number': 2,
        'quantization_config': models.ScalarQuantization(
            scalar=models.ScalarQuantizationConfig(type=models.ScalarType.INT8, always_ram=True)
        )
    }

    # create db
    await client.create_collection(**collection_params)

    # DB: records
    col_exclude = [f'index', 'sparse_indices', 'sparse_embed', 'sparse_embed', 'dense_embed', 'img_embed']
    records = []
    for idx, value in tqdm(enumerate(payloads), 'DB: Loading payloads', total=len(payloads)):
        vector = {}
        if text_sparse:
            vector.update({'text-sparse': value['sparse_embed'].tolist()})
            # vector.update({
            #     'text-sparse': models.SparseVector(
            #         indices=value['sparse_indices'].tolist(),
            #         values=value['sparse_embed'].tolist(),
            #     )
            # })
        if text_dense_dim:
            vector.update({'text-dense': value['dense_embed'].tolist()})
        if img_dim:
            vector.update({'img-dense': value['img_embed'].tolist()})

        point = models.PointStruct(
            id=value['index'],
            vector=vector,
            payload={_: value[_] for _ in value if _ not in col_exclude}
        )
        records.append(point)

    # DB: upsert
    start = perf_counter()
    upload_features = [client.upsert(collection_name=collection_name, points=[record]) for record in records]
    await asyncio.gather(*upload_features)
    logger.success(f'DB: upsert {perf_counter() - start:.2f}s')

    # DB: params
    collection_params = {
        'collection_name': collection_name,
        'optimizers_config': models.OptimizersConfigDiff(indexing_threshold=20_000_000),  # default
    }
    await client.update_collection(**collection_params)


def check_collections(collections_name: str = None, remove: bool = True):
    client = QdrantClient('localhost', port=6333)
    list_all_collections = [i.name for i in list(client.get_collections().collections)]
    if collections_name in list_all_collections:
        logger.info(f'Collection: {collections_name} has already existed')
    if remove:
        client.delete_collection(collection_name=collections_name)
        logger.success(f'Collection: {collections_name} has been removed')


async def DB_query(
        collection_name: str,
        payloads: list[dict],
        top_k: int = 5,
        text_sparse: int = None,
        text_dense_dim: int = None,
        img_dim: int = None,
):
    # config
    config = {'host': 'localhost', 'grpc_port': 6334, 'prefer_grpc': True}
    client = AsyncQdrantClient(**config)

    # load records
    start = perf_counter()
    results = []
    for idx, value in enumerate(payloads):
        tmp = None
        if text_sparse:
            tmp = models.NamedVector(name='text-sparse', vector=value['sparse_embed'].tolist())
            # tmp = models.NamedSparseVector(
            #         name='text-sparse',
            #         vector=models.SparseVector(
            #             indices=value['sparse_indices'].tolist(),
            #             values=value['sparse_embed'].tolist())
            # )
        if text_dense_dim:
            tmp = models.NamedVector(name='text-dense', vector=value['dense_embed'].tolist())
        if img_dim:
            tmp = models.NamedVector(name='img-dense', vector=value['img_embed'].tolist())
        results.append(tmp)

    # append all
    search_features = [client.search(
        collection_name=collection_name,
        query_vector=vector,
        limit=top_k,
        # search_params=models.SearchParams(hnsw_ef=128, exact=True)
    ) for vector in results]
    results = await asyncio.gather(*search_features)

    logger.success(f'DB: query {perf_counter() - start:.2f}s')
    return results


class BE:
    def __init__(
            self,
            text_sparse: int = None,
            text_dense: int = None,
            img_dim: int = None,
    ):
        self.text_sparse = text_sparse
        self.text_dense = text_dense
        self.img_dim = img_dim

    def load_data(self, df: pl.DataFrame, mode: str = '', vectorizer=None) -> list[dict]:
        return Data().create_dataset(
            df,
            mode=mode,
            text_sparse=self.text_sparse,
            img_dim=self.img_dim,
            vectorizer=vectorizer
        )

    def match_qdrant(
            self,
            df_db: pl.DataFrame,
            df_q: pl.DataFrame,
            top_k: int = 10,
            collections_name: str = 'streamlit',
    ) -> pl.DataFrame:
        from collections import OrderedDict

        all_items = list(set(df_db['db_item_name_clean'].to_list() + df_q['q_item_name_clean'].to_list()))
        vectorizer = tfidf(all_items, dim=self.text_sparse)

        payloads_db = self.load_data(df_db, 'db_', vectorizer=vectorizer)
        payloads_q = self.load_data(df_q, 'q_', vectorizer=vectorizer)
        self.dim_sparse = payloads_q[0]['sparse_embed'].shape[0]

        # check if a collection exists
        check_collections(collections_name, remove=True)

        # upsert
        asyncio.run(DB_upsert(
            collection_name=collections_name,
            payloads=payloads_db,
            text_sparse=self.dim_sparse,
            img_dim=self.img_dim,
            text_dense_dim=self.text_dense,
        ))

        # db: batch avoid timeout
        batch_size = 10_000
        query_result = []
        for i in tqdm(range(0, len(payloads_q), batch_size)):
            tmp = payloads_q[i:i + batch_size]
            results = asyncio.run(DB_query(
                collection_name=collections_name,
                payloads=tmp,
                top_k=top_k,
                text_sparse=self.dim_sparse,
                img_dim=self.img_dim,
                text_dense_dim=self.text_dense,
            ))
            query_result.extend(results)

        # chunking timeout
        for i, v in enumerate(payloads_q):
            v.update({'score': [_.score for _ in query_result[i]]})
            v.update({'db_match': [OrderedDict(sorted(_.payload.items())) for _ in query_result[i]]})
            if self.text_sparse:
                # del v['sparse_embed'], v['sparse_indices'], v['index'], v['sparse_embed']
                del v['index'], v['sparse_embed']
            if self.img_dim:
                del v['img_embed'], v['index']
            if self.text_dense:
                del v['dense_embed'], v['index']
        df_match = (
            pl.DataFrame(payloads_q)
            .explode(['score', 'db_match'])
            .unnest('db_match')
        )
        return df_match

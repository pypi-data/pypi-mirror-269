import torch
from torch.nn import functional as F
from PIL import Image
from loguru import logger
import sys

logger.remove()
logger.add(sys.stdout, colorize=True, format='<green>{time:HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}:{function}</cyan> | <level>{message}</level>')
device = 'cuda' if torch.cuda.is_available() else 'mps' if torch.backends.mps.is_available() else 'cpu'


class Model:
    def __init__(self):
        self.device = device
        self.dense_model = None
        self.dense_tokenizer = None
        self.sparse_tokenizer = None
        self.sparse_model = None
        self.img_model = None
        self.img_processor = None
        logger.info(f'Run model on device: {self.device}')

    def get_sparse(self, model_id: str):
        from transformers import AutoModelForMaskedLM, AutoTokenizer

        self.sparse_tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.sparse_model = AutoModelForMaskedLM.from_pretrained(model_id).to(self.device)
        logger.info(f'Sparse model: {model_id}')
        return self.sparse_model, self.sparse_tokenizer

    def get_dense(self, model_id: str):
        from sentence_transformers import SentenceTransformer

        self.dense_model = SentenceTransformer(model_id, device=self.device)
        logger.info(f'Dense model: {model_id}')
        return self.dense_model

    def get_img(self, model_id: str = 'openai/clip-vit-base-patch32'):
        from transformers import AutoProcessor, CLIPVisionModel

        self.img_processor = AutoProcessor.from_pretrained(model_id)
        self.img_model = CLIPVisionModel.from_pretrained(model_id).to(self.device)
        logger.info(f'Image model: {model_id}')
        return self.img_model, self.img_processor

    @staticmethod
    def compute_sparse_vector(texts: list[str], sparse_tokenizer, sparse_model, device):
        """
        Computes a vector from logits and attention mask using ReLU, log, and max operations.
        """
        tokens = sparse_tokenizer(texts, truncation=True, padding=True, return_tensors='pt', max_length=40).to(device)
        output = sparse_model(**tokens)
        logits, attention_mask = output.logits, tokens.attention_mask
        del tokens, output

        relu_log = torch.log(1 + torch.relu(logits))
        weighted_log = relu_log * attention_mask.unsqueeze(-1)
        del logits, attention_mask

        tvecs, _ = torch.max(weighted_log, dim=1)
        tvecs = tvecs.cpu().detach().numpy()
        del weighted_log

        indices, vecs = [], []
        for batch in tvecs:
            indices.append(batch.nonzero()[0].tolist())
            vecs.append(batch[indices[-1]].tolist())

        return indices, vecs

    @staticmethod
    def compute_sparse_vector_norm(texts: list[str], sparse_tokenizer, sparse_model, device):
        """
        Computes a vector from logits and attention mask using ReLU, log, and max operations.
        """
        tokens = sparse_tokenizer(texts, truncation=True, padding=True, return_tensors='pt', max_length=40).to(device)
        output = sparse_model(**tokens)
        logits, attention_mask = output.logits, tokens.attention_mask
        del tokens, output

        relu_log = torch.log(1 + torch.relu(logits))
        weighted_log = relu_log * attention_mask.unsqueeze(-1)
        del logits, attention_mask

        tvecs, _ = torch.max(weighted_log, dim=1)
        tvecs = tvecs.cpu().detach().numpy()
        return tvecs

    @staticmethod
    def pp_sparse(batch, col, sparse_tokenizer, sparse_model):
        query_indices, query_values = Model.compute_sparse_vector(batch[col], sparse_tokenizer, sparse_model, device)
        return {'sparse_embed': query_values, 'sparse_indices': query_indices}

    @staticmethod
    def pp_sparse_norm(batch, col, sparse_tokenizer, sparse_model):
        embed = Model.compute_sparse_vector_norm(batch[col], sparse_tokenizer, sparse_model, device)
        return {'dense_embed': embed}

    @staticmethod
    def pp_sparse_tfidf(batch, vectorizer, col: str) -> dict:
        embeddings = vectorizer.transform(batch[col]).toarray()
        return {'sparse_embed': embeddings}

    @staticmethod
    def pp_dense(batch, col, dense_model):
        dense_embed = dense_model.encode(batch[col], device=device)
        return {'dense_embed': dense_embed}

    @staticmethod
    def pp_img(batch, col, processor, model):
        images = [Image.open(i).convert('RGB') for i in batch[col]]
        inputs = processor(images=images, return_tensors='pt').to(device)
        with torch.inference_mode():
            outputs = model(**inputs)
        pooled_output = outputs.pooler_output
        embeddings = F.normalize(pooled_output, p=2, dim=1).cpu().numpy()
        return {'img_embed': embeddings}

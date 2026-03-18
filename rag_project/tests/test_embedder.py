import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
import numpy as np
from embedder import Embedder

@pytest.fixture(scope="module")
def embedder():
    return Embedder()

def test_embed_returns_ndarray(embedder):
    result = embedder.embed(["тестовый текст"])
    assert isinstance(result, np.ndarray)

def test_embed_shape(embedder):
    texts = ["первый текст", "второй текст", "третий текст"]
    result = embedder.embed(texts)
    assert result.shape == (3, 384)

def test_embed_one_shape(embedder):
    result = embedder.embed_one("один текст")
    assert result.shape == (384,)

def test_similar_texts_closer(embedder):
    v1 = embedder.embed_one("кот сидит на диване")
    v2 = embedder.embed_one("кошка лежит на диване")
    v3 = embedder.embed_one("налоговый кодекс статья 42")
    sim_12 = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    sim_13 = np.dot(v1, v3) / (np.linalg.norm(v1) * np.linalg.norm(v3))
    assert sim_12 > sim_13
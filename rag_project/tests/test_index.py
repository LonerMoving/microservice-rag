import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
import numpy as np
from index import FAISSIndex
from embedder import Embedder

@pytest.fixture(scope="module")
def embedder():
    return Embedder()

@pytest.fixture
def index():
    return FAISSIndex()

@pytest.fixture
def filled_index(embedder):
    idx = FAISSIndex()
    chunks = [
        "Василий занимается разработкой на Python",
        "Опыт работы с машинным обучением и FAISS",
        "Кибербезопасность и аудит встроенного ПО",
    ]
    vectors = embedder.embed(chunks)
    idx.add(chunks, vectors)
    return idx, chunks

def test_empty_index(index):
    assert index.index.ntotal == 0

def test_add_increases_count(embedder, index):
    chunks = ["тестовый чанк"]
    vectors = embedder.embed(chunks)
    index.add(chunks, vectors)
    assert index.index.ntotal == 1

def test_search_returns_list(filled_index):
    idx, chunks = filled_index
    result = idx.search(np.random.rand(384).astype(np.float32))
    assert isinstance(result, list)

def test_search_finds_relevant(embedder, filled_index):
    idx, chunks = filled_index
    query = embedder.embed_one("машинное обучение")
    result = idx.search(query, k=1)
    assert len(result) == 1
    assert "машинным обучением" in result[0]

def test_save_and_load(filled_index, tmp_path):
    idx, chunks = filled_index
    path = str(tmp_path / "test_index")
    idx.save(path)
    
    new_idx = FAISSIndex()
    new_idx.load(path)
    assert new_idx.index.ntotal == idx.index.ntotal
    assert new_idx.chunks == idx.chunks
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from chunker import chunk_text

def test_chunk_basic():
    text = "A" * 1000
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    assert len(chunks) == 3

def test_chunk_size():
    text = "A" * 1000
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    assert len(chunks[0]) == 500
    assert len(chunks[1]) == 500

def test_chunk_overlap():
    text = "A" * 1000
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    assert chunks[1] == text[450:950]

def test_chunk_empty():
    chunks = chunk_text("", chunk_size=500, overlap=50)
    assert chunks == []

def test_chunk_shorter_than_size():
    text = "A" * 100
    chunks = chunk_text(text, chunk_size=500, overlap=50)
    assert len(chunks) == 1
    assert chunks[0] == text
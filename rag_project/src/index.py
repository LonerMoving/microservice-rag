import faiss
import numpy as np
import pickle
from pathlib import Path

class FAISSIndex:
    def __init__(self, dim: int = 384):
        self.index = faiss.IndexFlatL2(dim)
        self.chunks: str = []

    def add(self, chunks: list[str], vectors: np.ndarray):
        self.index.add(vectors.astype(np.float32))
        self.chunks.extend(chunks)

    def search(self, query_vector: np.ndarray, k: int = 3) -> list[str]:
        data = query_vector.reshape(1, -1)
        D, I = self.index.search(data, k)
        return [self.chunks[i] for i in I[0] if i < len(self.chunks)]

    def save(self, path: str):
        faiss.write_index(self.index, path + ".index")
        with open(path + ".chunks", 'wb') as file:
            pickle.dump(self.chunks, file)
        
    def load(self, path: str):
        self.index = faiss.read_index(path + ".index")
        with open(path + ".chunks", 'rb') as file:
            self.chunks = pickle.load(file)
import pymupdf
from docx import Document
from pathlib import Path

def load_file(filepath: str) -> str:
    path = Path(filepath)
    
    if not path.exists():
        raise FileNotFoundError(f"Файл не найден: {filepath}")
    
    match path.suffix.lower():
        case ".txt":
            return path.read_text(encoding="utf-8")
        
        case ".pdf":
            doc = pymupdf.open(filepath)
            return "\n".join(page.get_text() for page in doc)
        
        case ".docx":
            doc = Document(filepath)
            return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
        
        case _:
            raise ValueError(f"Неподдерживаемый формат: {path.suffix}")

def load_directory(dir_path: str) -> dict[str, str]:
    path = Path(dir_path)
    result = {}
    
    for file in path.iterdir():
        if file.suffix.lower() in (".txt", ".pdf", ".docx"):
            try:
                result[file.name] = load_file(str(file))
                print(f"✓ Загружен: {file.name} ({len(result[file.name])} символов)")
            except Exception as e:
                print(f"✗ Ошибка {file.name}: {e}")
    
    return result
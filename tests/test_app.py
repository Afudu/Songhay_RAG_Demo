import pandas as pd
from app import is_empty, load_excel_as_documents


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_excel(rows: list[dict], tmp_path) -> str:
    df = pd.DataFrame(rows)
    path = tmp_path / "test_glossary.xlsx"
    df.to_excel(path, index=False, engine="openpyxl")
    return str(path)


# ── is_empty() ────────────────────────────────────────────────────────────────

def test_is_empty_blank_string():
    assert is_empty("") is True


def test_is_empty_nan_string():
    assert is_empty("nan") is True


def test_is_empty_nan_uppercase():
    assert is_empty("NaN") is True


def test_is_empty_valid_value():
    assert is_empty("Database") is False


def test_is_empty_whitespace():
    assert is_empty("   ") is False


# ── load_excel_as_documents() ─────────────────────────────────────────────────

def test_loads_valid_rows(tmp_path):
    path = make_excel([
        {"English": "Database", "French": "Base de données", "Songhay": "Tiira-hugu"},
        {"English": "Password", "French": "Mot de passe", "Songhay": "Sennifufal"},
    ], tmp_path)
    docs = load_excel_as_documents(path)
    assert len(docs) == 2


def test_document_content_format(tmp_path):
    path = make_excel([
        {"English": "Database", "French": "Base de données", "Songhay": "Tiira-hugu"},
    ], tmp_path)
    docs = load_excel_as_documents(path)
    assert "English: Database" in docs[0].page_content
    assert "French: Base de données" in docs[0].page_content
    assert "Songhay: Tiira-hugu" in docs[0].page_content


def test_document_metadata(tmp_path):
    path = make_excel([
        {"English": "Database", "French": "Base de données", "Songhay": "Tiira-hugu"},
    ], tmp_path)
    docs = load_excel_as_documents(path)
    assert docs[0].metadata["english"] == "Database"
    assert docs[0].metadata["french"] == "Base de données"
    assert docs[0].metadata["songhay"] == "Tiira-hugu"


def test_skips_empty_english(tmp_path):
    path = make_excel([
        {"English": "", "French": "Base de données", "Songhay": "Tiira-hugu"},
        {"English": "Password", "French": "Mot de passe", "Songhay": "Sennifufal"},
    ], tmp_path)
    docs = load_excel_as_documents(path)
    assert len(docs) == 1
    assert docs[0].metadata["english"] == "Password"


def test_skips_empty_french(tmp_path):
    path = make_excel([
        {"English": "Database", "French": "", "Songhay": "Tiira-hugu"},
        {"English": "Password", "French": "Mot de passe", "Songhay": "Sennifufal"},
    ], tmp_path)
    docs = load_excel_as_documents(path)
    assert len(docs) == 1


def test_skips_empty_songhay(tmp_path):
    path = make_excel([
        {"English": "Database", "French": "Base de données", "Songhay": ""},
        {"English": "Password", "French": "Mot de passe", "Songhay": "Sennifufal"},
    ], tmp_path)
    docs = load_excel_as_documents(path)
    assert len(docs) == 1


def test_skips_header_row(tmp_path):
    path = make_excel([
        {"English": "English", "French": "French", "Songhay": "Songhay"},
        {"English": "Database", "French": "Base de données", "Songhay": "Tiira-hugu"},
    ], tmp_path)
    docs = load_excel_as_documents(path)
    assert len(docs) == 1


def test_skips_nan_rows(tmp_path):
    df = pd.DataFrame([
        {"English": "Database", "French": "Base de données", "Songhay": "Tiira-hugu"},
        {"English": None, "French": None, "Songhay": None},
    ])
    path = tmp_path / "test_nan.xlsx"
    df.to_excel(path, index=False, engine="openpyxl")
    docs = load_excel_as_documents(str(path))
    assert len(docs) == 1


def test_empty_file_returns_empty_list(tmp_path):
    path = make_excel([], tmp_path)
    docs = load_excel_as_documents(path)
    assert docs == []

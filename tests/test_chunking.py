# 测试 chunking 的边界情况
from app.services.chunking import chunk_text


def test_short_text_is_single_chunk() -> None:
    assert chunk_text("hello world") == ["hello world"]


def test_empty_text_gives_no_chunks() -> None:
    assert chunk_text("   \n\n  ") == []


def test_paragraphs_are_merged_up_to_limit() -> None:
    text = "aaaa\n\nbbbb\n\ncccc"
    chunks = chunk_text(text, max_chars=10)
    assert chunks == ["aaaa\n\nbbbb", "cccc"]


def test_long_paragraph_is_split() -> None:
    chunks = chunk_text("x" * 25, max_chars=10)
    assert all(len(c) <= 10 for c in chunks)
    assert "".join(chunks) == "x" * 25
# Chunking:把长文档切成小段,每段不超过 max_chars 个字符
def chunk_text(text: str, max_chars: int = 800) -> list[str]:
    # 先按空行切成 paragraphs,过长的 paragraph 再硬切
    pieces: list[str] = []
    for paragraph in text.split("\n\n"):
        paragraph = paragraph.strip()
        while len(paragraph) > max_chars:
            pieces.append(paragraph[:max_chars])
            paragraph = paragraph[max_chars:]
        if paragraph:
            pieces.append(paragraph)

    # 再把相邻的短 paragraphs 合并,直到快超过 max_chars
    chunks: list[str] = []
    current = ""
    for piece in pieces:
        if current and len(current) + len(piece) + 2 > max_chars:
            chunks.append(current)
            current = piece
        else:
            current = f"{current}\n\n{piece}" if current else piece
    if current:
        chunks.append(current)
    return chunks
def markdown_to_blocks(text):
    blocks = text.split("\n\n")
    filtered_blocks = []
    for char in blocks:
        cleaned = char.strip()
        if cleaned == "":
            continue
        filtered_blocks.append(cleaned)
    return filtered_blocks    
        
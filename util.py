def save_text(text_to_save, path):
    with open(path) as f:
        f.write(text_to_save)

import os


def read_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"El archivo {file_path} no existe.")
    
    with open(file_path, mode="r", encoding="UTF-8") as f:
        return f.readlines()
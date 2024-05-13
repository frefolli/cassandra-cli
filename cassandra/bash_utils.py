def read_bash_file(bash_file_path: str) -> str:
  with open(bash_file_path, mode="r", encoding="utf-8") as file:
    return file.read()

def write_bash_file(bash_file_path: str, obj):
  with open(bash_file_path, mode="w", encoding="utf-8") as file:
      file.write(obj)

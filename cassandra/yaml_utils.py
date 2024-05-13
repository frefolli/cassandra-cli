import yaml

def read_yaml_file(yaml_file_path: str) -> dict:
  with open(yaml_file_path, mode="r", encoding="utf-8") as file:
    return yaml.load(file, yaml.SafeLoader)

def write_yaml_file(yaml_file_path: str, obj):
  with open(yaml_file_path, mode="w", encoding="utf-8") as file:
    yaml.dump(obj, file)

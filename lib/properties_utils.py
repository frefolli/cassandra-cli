def write_properties_file(properties_file_path: str, obj):
  with open(properties_file_path, mode="w", encoding="utf-8") as file:
    for key in obj:
      file.write("%s=%s" % (key, obj[key]))

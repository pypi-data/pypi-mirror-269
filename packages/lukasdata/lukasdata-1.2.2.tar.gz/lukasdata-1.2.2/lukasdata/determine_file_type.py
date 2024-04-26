import regex as re

file_type_regex=re.compile("\..*")
datatype_regex=re.compile("pdf|json|txt|xlsx")

def determine_file_type(file_name): #vielleicht in einem anderen module?
      #datatype=re.search(datatype_regex,file_name).group()
      file_type=file_type_regex.findall(file_name)[0].lstrip(".")
      return file_type

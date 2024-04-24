import os
def string_to_txt(string,file_name,path):
    os.chdir(path)
    with open(file_name+".txt","w",encoding="utf-8") as f:
        f.write(string,)

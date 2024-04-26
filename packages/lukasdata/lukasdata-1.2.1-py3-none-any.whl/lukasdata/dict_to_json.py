import os
import json
def dict_to_json(dict,title,directory="C:/Users/lukas/Desktop/bachelor/data"):
      os.chdir(directory)
      with open(title+".json", "w", encoding="utf-8") as outfile:
            json_file=json.dumps(dict,ensure_ascii=False)
            outfile.write(json_file)
            print(f"{title} changed")

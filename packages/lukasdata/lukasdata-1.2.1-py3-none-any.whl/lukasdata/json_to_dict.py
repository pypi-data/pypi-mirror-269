import os
import json
def json_to_dict(filename,dir="C:/Users/lukas/Desktop/bachelor/data"):
      os.chdir(dir)
      with open(filename,"r",encoding="utf-8") as f:
            data=f.readlines()[0]

      dict=json.loads(data) 
      return dict
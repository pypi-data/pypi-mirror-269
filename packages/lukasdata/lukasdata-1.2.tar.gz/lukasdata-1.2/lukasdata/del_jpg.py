import os
def del_jpg(path="C:/Users/lukas/Desktop/bachelor/pdf"):
      for file in os.listdir(path):
            if file.endswith(".jpg"):
                  os.remove(file)
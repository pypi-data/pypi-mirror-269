import os
def chdir_bachelor():
      os.chdir("C:/Users/lukas/Desktop/bachelor")

def chdir_data():
      os.chdir("C:/Users/lukas/Desktop/bachelor/data")

def chdir_pdf():
      os.chdir("C:/Users/lukas/Desktop/bachelor/pdf") 

def chdir_auth():
      os.chdir("C:/Users/lukas/Desktop/bachelor/auth")    

def chdir_txt():
      os.chdir("C:/Users/lukas/Desktop/bachelor/txt")    

def chdir_fig():
      os.chdir("C:/Users/lukas/Desktop/bachelor/data/figures")          

def switch_dir(type):
      if type =="pdf":
            chdir_pdf()
      if type == "json":
            chdir_data()
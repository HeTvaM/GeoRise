# import system libs
import json
import os

from tkinter.messagebox import showerror

# import user's libs
from logger import log_with_return, log
from decor import check

#>------------SUMMARY----------------<
# This module for decorator, save and load file. The file is uploaded in Json format in the transmitted file name
# Each function first checks for file coexistence, which is implemented through the decorator
# functions:
# -save
# -upload
#>------------SUMMARY----------------<

def er4():
    showerror("Ошибка!", "Данный файл существует!")

ERROR = er4

@check(ERROR)
def save(file, dict):
    with open(f"{file}.txt", "w+") as fileToWrite:
        json.dump(dict, fileToWrite)
    os.remove(file)
    return

@check(ERROR)
def upload(file):
    with open(f"{file}", "r+") as fileToRead:
            dict = json.load(fileToRead)
    return dict

if __name__=="__main__":
    # Тест на работоспособность функций
    file = "Text"
    dict = {"Figure":[(0,0),(1,-2),(4,5),(-4,5)],
            "Dot": [(1,1)]}
    save("Text", dict)
    print(upload(file))

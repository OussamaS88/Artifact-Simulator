import pandas as pd
from pytesseract import pytesseract
from PIL import Image
import os

path_to_tesseract = "C://Program Files/Tesseract-OCR/tesseract.exe"
parent_dir = os.getcwd()
dataPath = "{}/static/data/".format(parent_dir)
setData = pd.read_json("{}set_names.json".format(dataPath))
def readFromImage(path_to_image):
    try:
        img = Image.open(path_to_image)
        width, height = img.size
        setImg = img.crop((1,1, width, 50))
        subs = img.crop((73, 270, 368, 480))
        mainInfo = img.crop((1,110,240, 200))
        aTypeIMG = img.crop((7, 50, 195, 100))
        pytesseract.tesseract_cmd = path_to_tesseract
        
        setTess = pytesseract.image_to_string(setImg)
        subTess= pytesseract.image_to_string(subs)
        maintess = pytesseract.image_to_string(mainInfo)
        aTypeTess = pytesseract.image_to_string(aTypeIMG)
        found = False
        for x in setData.values.flatten():
            if found == True: break
            for j in setTess.split(" "):
                if j in x:
                    found = True
                    setTess = setData[setData == x].dropna(axis = 1, how="all").columns[0]
                    break

        subStatStrings = set(subTess.split("\n")).difference(("", " ", "  "))
        mainStrings = [x for x in maintess.split("\n") if x not in ["", " ", "  "]]
        subs = [x.split(" +") for x in subStatStrings]
        aType = aTypeTess.split(" ")[0]
        if len(mainStrings) != 2:
            mainStrings = ["NULL","0"]
        if "%" in mainStrings[1]:
            mainStrings[1] = mainStrings[1][:-1]
        try:
            mainStat = [mainStrings[0], float(mainStrings[1])]
        except:
            mainStat = [mainStrings[0], 0]
        subS = []
        subV = []
        for k in subs:
            if '%' in k[1]:
                k[1] = k[1][:-1]
            k[1] = float(k[1])
            subS.append(k[0])
            subV.append(k[1])
        return [setTess, aType, mainStat, subS, subV]
    except:
        return "Failed"
import pandas as pd
from pytesseract import pytesseract
from PIL import Image

path_to_tesseract = "C://Program Files/Tesseract-OCR/tesseract.exe"


def readFromImage(path_to_image):
    try:
        img = Image.open(path_to_image)
        width, height = img.size
        subs = img.crop((73, 270, 368, 480))
        mainInfo = img.crop((1,110,210, 200))
        aTypeIMG = img.crop((7, 50, 195, 100))
        pytesseract.tesseract_cmd = path_to_tesseract
        
        subTess= pytesseract.image_to_string(subs)
        maintess = pytesseract.image_to_string(mainInfo)
        aTypeTess = pytesseract.image_to_string(aTypeIMG)
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
        return [aType, mainStat, subS, subV]
    except:
        return "Failed"
# print(readFromImage("savedArtifacts/new/3.jpg"))
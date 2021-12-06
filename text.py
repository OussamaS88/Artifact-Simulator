import pandas as pd
from pytesseract import pytesseract
from PIL import Image, ImageOps, ImageDraw
import os

path_to_tesseract = "C://Program Files/Tesseract-OCR/tesseract.exe"
parent_dir = os.getcwd()
dataPath = "{}/static/data/".format(parent_dir)
setData = pd.read_json("{}set_names.json".format(dataPath))
mainStats = pd.read_json("{}main.json".format(dataPath)).index.tolist()
def readFromImage(path_to_image):
    try:
        img = Image.open(path_to_image)
        width, height = img.size
        setImg = img.crop((1,1, width, 50))
        subs = img.crop((73, 270, 368, 480))
        mainInfo = img.crop((1,110,280, 200))
        aTypeIMG = img.crop((7, 50, 195, 100))
        levelImg = img.crop((2,240, 300, 295))
        mS = img.crop((1, 110, 280, 155))
        mV = img.crop((1, 155, 280, 200))
        pytesseract.tesseract_cmd = path_to_tesseract
        levelTess = pytesseract.image_to_string(levelImg)
        setTess = pytesseract.image_to_string(setImg)
        subTess= pytesseract.image_to_string(subs)
        maintess = pytesseract.image_to_string(mainInfo)
        aTypeTess = pytesseract.image_to_string(aTypeIMG)
        try:
            level = int(levelTess[1:])
        except:
            level = 0

        found = False
        if setTess in setData.values.flatten():
            found = True
        else :
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
            mStess =  list(set(pytesseract.image_to_string(mS).split("\n")).difference(("", " ", "  ")))
            
            l = 0
            m = ''
            if len(mStess) > 0:
                for k in mStess:
                    if len(k) > l:
                        m = k
                        l = len(k)
                mStess = m
            mVtess =  set(pytesseract.image_to_string(mV).split("\n")).difference(("", " ", "  "))
            if len(mVtess) < 1:
                if len(mStess) > 0:
                     mainStrings= [mStess,"FILL"]
            else:
                found = False
                biggestLen = 0
                incorrectStat = ''
                for k in mainStrings:
                    if len(k)> biggestLen:
                        incorrectStat = k
                        biggestLen = len(k)
                if len(incorrectStat.split(" ")) > 1:
                    for s in mainStats:
                        if incorrectStat.split(" ")[0] in s:
                            incorrectStat = s
                            found = True
                            mainStrings = [incorrectStat,"FILL"]
                            break
                if found == False:
                    mainStrings = ["NULL","0"]
        if mainStrings[0] not in mainStats:
            biggestLen = 0
            for k in mainStrings:
                if len(k)> biggestLen:
                    mainStrings[0] = k
                    biggestLen = len(k)
            found = False
            if len(mainStrings[0].split(" ")) > 1:
                    for s in mainStats:
                        if mainStrings[0].split(" ")[0] in s:
                            mainStrings[0] = s
                            found = True
                            mainStrings = [mainStrings[0],"FILL"]
                            break
            if found == False:
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
        return [setTess, level, aType, mainStat, subS, subV]
    except:
        return "Failed"
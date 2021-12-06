from PIL import Image, ImageFont, ImageDraw
from numpy.random import default_rng
import os

parent_dir = os.getcwd()
fontPath = "{}/static/fonts/".format(parent_dir)

rng = default_rng()

regFont = ImageFont.truetype("{}Lato-Regular.ttf".format(fontPath), 24)
boldFont = ImageFont.truetype("{}Lato-Bold.ttf".format(fontPath), 40)
smallBoldFont = ImageFont.truetype("{}Lato-Bold.ttf".format(fontPath), 24)

def render(artifact, save= False, name="default", show = True, path="savedArtifacts/"):
    set = artifact.loc["set", "Value"]
    type = artifact.loc["type", "Stat"]
    if "Goblet" in type:
        type = "Goblet"
    elif "Circlet" in type:
        type = "Circlet"
    background = Image.open("static/{}/{}.jpg".format(set, type))
    bgEdit = ImageDraw.Draw(background)
    mStat = artifact.loc["mainStat", "Stat"]
    mStatV = str(artifact.loc["mainStat", "Value"])
    level = int(artifact.loc["type", "Value"])
    levelStr = "+" + str(level)
    if "%" in mStat:
        mStatV = mStatV + "%"
    bgEdit.text((20,125), mStat, (196, 169, 162), font=regFont)
    bgEdit.text((20,150), mStatV, (245, 245, 245), font=boldFont)
    # bgEdit.rounded_rectangle((24,252, 70, 285),radius= 5, fill=(150,154,157))
    if level > 10:
        bgEdit.text((25, 253), levelStr, (27,27,27), font = smallBoldFont)
    else:
        bgEdit.text((30, 253), levelStr, (27,27,27), font = smallBoldFont)
    pos = 300
    for i in range(len(artifact) - 3):
        s = artifact.iloc[i+3, 0]
        v = str(artifact.iloc[i+3, 1])
        if "%"in s:
            v = v + "%"
        t = "•  " + s + " +" + v
        bgEdit.text((55, pos), t, (80, 84, 87), font=smallBoldFont)
        pos+=37
    if save == True:
        background.save("{}/{}.jpg".format(path , str(name)))
    return background.show() if show else artifact
from PIL import Image, ImageFont, ImageDraw

regFont = ImageFont.truetype("Lato-Regular.ttf", 24)
boldFont = ImageFont.truetype("Lato-Bold.ttf", 40)
smallBoldFont = ImageFont.truetype("Lato-Bold.ttf", 24)

def render(artifact, save= False, name="default", show = True, path="savedArtifacts/"):
    type = artifact.loc["type", "Stat"]
    if "Goblet" in type:
        type = "Goblet"
    elif "Circlet" in type:
        type = "Circlet"
    background = Image.open("static/{}.jpg".format(type))
    bgEdit = ImageDraw.Draw(background)
    mStat = artifact.loc["mainStat", "Stat"]
    mStatV = str(artifact.loc["mainStat", "Value"])
    if "%" not in mStat:
        mStatV = mStatV[:-2]
    else:
        mStatV = mStatV + "%"
    bgEdit.text((20,125), mStat, (196, 169, 162), font=regFont)
    bgEdit.text((20,150), mStatV, (245, 245, 245), font=boldFont)
    pos = 300
    for i in range(len(artifact) - 2):
        s = artifact.iloc[i+2, 0]
        v = str(artifact.iloc[i+2, 1])
        if "%" not in s:
            v = v[:-2]
        else:
            v = v + "%"
        t = "•  " + s + " +" + v
        bgEdit.text((55, pos), t, (80, 84, 87), font=smallBoldFont)
        pos+=37
    if save == True:
        background.save("{}/{}.jpg".format(path , str(name)))
    return background.show() if show else artifact
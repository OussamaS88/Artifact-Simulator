import numpy as np
import pandas as pd
from numpy.random import default_rng
import json
import im as renderer
import os
import text as imageProcessor

rng = default_rng()
parent_dir = os.getcwd()

dataPath = "{}/static/data/".format(parent_dir)
savePath = "{}/savedArtifacts/".format(parent_dir)
subStatChances = pd.read_json("{}sub.json".format(dataPath)).fillna(0)
mainStatChances = pd.read_json("{}main.json".format(dataPath)).fillna(0)
values = pd.read_json("{}values.json".format(dataPath)).fillna(0)
sets = pd.read_json("{}sets.json".format(dataPath))
exceptions = values[mainStatChances][9:-1].index.tolist()

def gen(specifiedType = None, lines=None, domain="random", set= None):
    if domain == "random":
        domain = rng.choice(sets.columns)
    else:
        if domain not in sets.columns: return "Domain not available"
    if set == None:
        set = rng.choice(sets[domain])
    else:
        if set not in sets.values:
            return "Set not available"
        else:
            domain = sets[sets == set].dropna(axis = 1, how="all").columns[0]
    artifact = {"Stat":{}, "Value":{}}
    artifact["Stat"]["set"] = domain
    artifact["Value"]["set"] = set
    a = rng.choice(mainStatChances.columns) if specifiedType == None else specifiedType
    myType = mainStatChances[a][mainStatChances[a] > 0] * 100
    stat = getStat(myType)
    artifact["Stat"]["mainStat"] = stat

    tempName = reFormatSpecialType(myType.name, stat)

    artifact["Stat"]["type"] = tempName
    artifact["Value"]["type"] = 0

    artifact["Value"]["mainStat"]= values.loc[stat, "mainStat"][0]
    value = ""
    try :
        value = subStatChances[tempName].drop(stat)
    except:
        value = subStatChances[tempName]
        if tempName == "GobletEl" or tempName == "CircletHB":
            for x in exceptions:
                if x in value: value = value.drop(x)
    lineDecider = rng.choice([3,3,3,4]) if lines == None else lines
    for r in range(lineDecider):
        s = getStat(value)
        value = value.drop(s)
        artifact["Stat"]["sub" + str(r+1)] = s
        artifact["Value"]["sub" + str(r+1)] = rng.choice(values.loc[s, "subStat"])
    return pd.DataFrame(artifact)

def getStat(myType):
    z = np.empty(np.sum(myType.values, dtype= np.int32), dtype= object)
    j = 0
    for (x,y) in zip(myType.index, myType.values):
        temp = 0
        for p in np.arange(int(y)):
            z[j+p] = x
            temp +=1
        j += temp
    stat = rng.choice(z)
    return stat

def upgrade(artifact):
    if artifact.loc["type", "Value"] >= 20: return artifact
    artifact.loc["type", "Value"] += 4
    artifact.loc["mainStat", "Value"] = values.loc[artifact.loc["mainStat", "Stat"], "mainStat"][int(artifact.loc["type", "Value"] / 4)]
    if "sub4" not in artifact.index:
        aName = artifact.loc["type", "Stat"]
        v = ""
        try :
            v = subStatChances[aName].drop(artifact.loc["mainStat", "Stat"]) 
        except:
            v = subStatChances[aName]
            if aName == "GobletEl" or aName == "CircletHB":
                for x in exceptions:
                    if x in v: v = v.drop(x)
        for k in [artifact.loc["sub1":, "Stat"]]:
            v = v.drop(k)

        s = getStat(v)
        k = artifact.to_dict()
        k['Stat']["sub4"] = s
        k['Value']["sub4"] = rng.choice(values.loc[s, "subStat"])
        return pd.DataFrame(k)
    else:
        r = "sub" + str(rng.choice([1,2,3,4]))
        artifact.loc[r, "Value"] = np.round(artifact.loc[r, "Value"] + rng.choice(values.loc[artifact.loc[r, "Stat"], "subStat"]), 1) 
        return artifact

def save_artifact(artifact: pd.DataFrame, position = -1):
    s = json.dumps(artifact.to_dict())
    if position < 0:
        with open("{}artifacts.json".format(savePath),'r+') as file:
            file_data = json.load(file)
            k = 0
            if len(file_data) > 0:
                k = int(list(file_data.keys())[-1]) + 1
                file_data[k] = s
            else:
                file_data[len(file_data)] = s
            file.seek(0)
            json.dump(file_data, file, indent = 4)
    else:
        removeArtifact(str(position))
        with open("{}artifacts.json".format(savePath),'r+') as file:
            file_data = json.load(file)
            file_data[position] = s
            file.seek(0)
            json.dump(file_data, file, indent = 4)
    return s

def retrieveArtifact(pos = -1):
    data = {}
    arr = []
    with open("{}artifacts.json".format(savePath), "r") as file:
        data = json.load(file)
    if pos < 0:
        for x in data:
            arr.append(pd.read_json(data[x]))
        return arr
    else:
        return pd.read_json(data[str(pos)])

def removeArtifact(position = -1):
    data = {}
    k = None
    with open("{}artifacts.json".format(savePath), 'r') as data_file:
        data = json.load(data_file)
    if position < 0:
        i = data.copy()
        count = 0
        for count,j in enumerate(i):
            data.pop(j)
        k = "Artifacts removed :" + str(count)
    else:
        try:
            k= data[str(position)]
            data.pop(str(position))
        except:
            return "No artifact at this position"
    with open("{}artifacts.json".format(savePath), 'w') as data_file:
        data = json.dump(data, data_file)
    return k

def returnSpecific(mySet, countOnly= False, aType=None, main= None):
    arr = []
    for x in retrieveArtifact():
        if set(mySet).issubset(set(x.loc["sub1":, "Stat"].values)):
            if aType == None:
                if main == None:
                    arr.append(x)
                else:
                    if main in x.loc["mainStat", "Stat"]: arr.append(x)
            else:
                if aType in x.loc["type", "Stat"]:
                    if main == None:
                        arr.append(x)
                    else:
                        if main in x.loc["mainStat", "Stat"]: arr.append(x)
    return arr if countOnly == False else len(arr)

def upgradeCount(artifact, count = 0):
    for i in range(count):
        artifact = upgrade(artifact)
    return artifact

def upgradeMax(artifact):
    return upgradeCount(artifact, 5)

def createCustom(type,level, mainStat, substats, svalues, setName):
    if len(substats) > 4 or len(svalues) > 4 or (len(substats) != len(svalues)):
        return "Invalid"
    domain = sets[sets == setName].dropna(axis = 1, how="all").columns[0]
    main = [mainStat[0],mainStat[1]]
    aType = [type, level]
    subs = []
    for i in range(len(substats)):
        subs.append([substats[i], svalues[i]])
    subsIndex = []
    for k in range(len(substats)):
        subsIndex.append("sub" + str(k+1))
    data = [[domain, setName], main, aType]
    data.extend(subs)
    indices = ["set", "mainStat", "type"]
    indices.extend(subsIndex)
    artifact = pd.DataFrame(data, index=indices, columns=["Stat", "Value"])
    return artifact

def reRoll(artifact, subs, numbers, tries = 0):
    temp = artifact.copy()
    max = upgradeMax(artifact)
    if not (set(subs).issubset(set(max.loc["sub1":, "Stat"].values))):
        tries +=1
        reRoll(temp, subs, numbers, tries)
    else:
        for (stat, num) in zip(subs, numbers):
            if max[max.Stat == stat].Value[0] >= num:
                continue
            else:
                tries +=1
                return reRoll(temp, subs, numbers, tries)
    return [max, tries+1]

def reset(count = 0):
    removeArtifact()
    if count > 0:
        for i in range(count):
            save_artifact(gen())
    else : removeArtifact()

def saveCopies(artifact = "random", count = 1, name = 0, directory = "default", set = "default"):
    if count < 1 : return
    domain = None
    path = None
    try:
        path = os.path.join(parent_dir, "savedArtifacts/" + directory)
        os.mkdir(path)
    except:
        for k in rng.integers(0, 30, size=10):
            directory += str(k)
        path = os.path.join(parent_dir,"savedArtifacts/" + directory)
        os.mkdir(path)
    if (not isinstance(artifact, pd.DataFrame)) and artifact == "random":
        if count > 25: count = 25
        for a in range(count):
            artifact = gen()
            if set == "random":
                domain = rng.choice(sets.columns)
                set = rng.choice(sets[domain])
            elif set == "default":
                set = artifact.loc["set", "Value"]
                domain = artifact.loc["set", "Stat"]
            else:
                try:
                    domain = sets[sets == set].dropna(axis = 1, how="all").columns[0]
                except:
                    return "Set unavailable"
            artifact.loc["type", "Value"] == set
            artifact.loc["type", "Stat"] == domain
            renderer.render(artifact, save= True, name=str(a+1), path = path, show=False)
    elif isinstance(artifact, pd.DataFrame):
        stop = 0
        if set == "random":
            domain = rng.choice(sets.columns)
            set = rng.choice(sets[domain])
        elif set == "default":
            set = artifact.loc["set", "Value"]
            domain = artifact.loc["set", "Stat"]
        else:
            try:
                domain = sets[sets == set].dropna(axis = 1, how="all").columns[0]
            except:
                return "Set unavailable"
        artifact.loc["type", "Value"] == set
        artifact.loc["type", "Stat"] == domain
        for a in range(count):
            renderer.render(artifact, save= True, name=str(a), path = path, show=False)
            artifact = upgrade(artifact)
            stop += 1
            if stop == 6: return
    return "Must be higher than 0"

def imageToArtifact(path):
    i = imageProcessor.readFromImage(path)
    if not isinstance(i, list): return i
    setName, level, aType, mainStat, subS, subV = i
    if mainStat[0] == "NULL" or mainStat[0] not in mainStatChances[aType].index.tolist():
        # print(mainStat[0])
        choices = mainStatChances[aType][mainStatChances[aType] > 0].index.tolist()
        mainStat[0] = rng.choice(choices)
    
    aType = reFormatSpecialType(aType, mainStat[0])

    if mainStat[1] == 0 or "FILL":
        try:
            mainStat[1] = values.loc[mainStat[0], "mainStat"][0]
        except:
            mainStat[1] = values.loc[mainStat[0], "mainStat"]
    return createCustom(aType, level, mainStat, subS, subV, setName)

def reFormatSpecialType(aType, mainStat):
    if aType == "Circlet":
        if mainStat in ['Crit Rate%', 'Crit DMG%']:
            aType +="Crit"
        elif mainStat in 'Healing Bonus%':
            aType += 'HB'
        else :
            aType += "Normal"
    elif aType == "Goblet":
        if mainStat in ['ATK%', 'HP%', 'DEF%', 'Elemental Mastery', 'Energy Recharge%']:
            aType +="NonEl"
        else :
            aType += "El"
    return aType
# k = gen(specifiedType="Circlet")
# saveCopies(gen(specifiedType="Circlet"), directory="b")
print(imageToArtifact("savedArtifacts/b/0.jpg"))
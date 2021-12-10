import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

global_stats = pd.read_json("static/data/values.json")["subStat"].dropna().index.tolist()

def as_bar_chart(artifacts, subs = None):
    if "sub4" in artifacts.index:
        all_stats = np.array(artifacts.loc[["sub1", "sub2", "sub3", "sub4"], "Stat"])
    else:
        all_stats = np.array(artifacts.loc[["sub1", "sub2", "sub3"], "Stat"])
    plt.hist(all_stats)
    plt.show()
    return
def as_pie_chart(artifacts, subs = None, highlighted_stat = None):
    if "sub4" in artifacts.index:
        all_stats = np.array(artifacts.loc[["sub1", "sub2", "sub3", "sub4"], "Stat"])
    else:
        all_stats = np.array(artifacts.loc[["sub1", "sub2", "sub3"], "Stat"])
    stat, count = np.unique(all_stats, return_counts=True)
    if highlighted_stat != None:
        ex = [0.2 if x == highlighted_stat else 0 for x in stat]
    else:
        ex = highlighted_stat
    plt.pie(count, labels=stat, explode=ex)
    plt.show()
    return
def barDem(artifacts = None):
    all_stats = {}
    for art in artifacts:
        for x in art.loc["sub1":, "Stat"].tolist():
            all_stats.setdefault(x, []).append(art.loc["type", "Stat"])

    all_types = {}
    for art in artifacts:
        t = art.loc["type", "Stat"]
        if "Circlet" in t:
            t = "Circlet"
        elif "Goblet" in t:
            t = "Goblet"
        all_types.setdefault(t, []).extend(art.loc["sub1":, "Stat"].tolist())

    fig, ax = plt.subplots()
    s = get_counts(all_types)
    heights = s.copy()
    for i,h in enumerate(heights):
        if i == 0:
            heights[h] = [0,0,0,0,0,0,0,0,0,0]
        else:
            heights[h] = list(np.array(list(heights.values())[i-1]) + list(s.values())[i-1])
    bars = []
    for k in list(s.keys()):
        bars.append(ax.bar(range(len(global_stats)), s[k], bottom=heights[k], label=k))
    for p in bars:
        ax.bar_label(p, label_type='center')
    ax.axhline(0, color='grey', linewidth=0.8)
    display_labels = global_stats.copy()
    for x in range(len(display_labels)):
        k = display_labels[x].split(" ")
        if len(k) > 1:
            display_labels[x] = k[0][0] + k[1][0]
    ax.set_xticks(range(len(global_stats)), labels=display_labels)
    ax.legend()
    plt.show()

def get_counts(arr, t = None):
    types = {"Flower" : [], "Plume": [], "Sands": [], "Goblet": [], "Circlet" : []}
    for x in types:
        for y in global_stats:
            if x in arr:
                types[x].append(occ(y, arr[x]))
            else :
                types[x].append(0)
    return types

def occ(s, arr):
    o = 0
    for i in arr:
        if i == s:
            o +=1
    return o
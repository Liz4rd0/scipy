from os import stat
import pandas as pd
import io
import codecs
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import seaborn as sns
import ipywidgets as widgets
import warnings
warnings.filterwarnings('ignore')


def life_expectancy(sterberate):
    sterberate = sterberate[:202]
    sterberate = sterberate.rename(columns = {"Unnamed: 0" : "Geschlecht", "Unnamed: 1" : "Alter"})

    # converts date columns and calculates difference
    sterberate["Unterschied 2018/20 nach 2019/21"] = sterberate["2019/21"].str.replace(",", ".").astype(float) - sterberate["2018/20"].str.replace(",", ".").astype(float)
    sterberate["Unterschied 2017/19 nach 2018/20"] = sterberate["2018/20"].str.replace(",", ".").astype(float) - sterberate["2017/19"].str.replace(",", ".").astype(float)
    sterberate["Unterschied 2016/18 nach 2017/19"] = sterberate["2017/19"].str.replace(",", ".").astype(float) - sterberate["2016/18"].str.replace(",", ".").astype(float)

    age = sterberate["Alter"].str.split(" ", expand = True)
    sterberate["Alter"] = age[0]

    sterberate = pd.melt(
        sterberate,
        id_vars = ["Geschlecht", "Alter"], 
        value_vars = ["Unterschied 2018/20 nach 2019/21", "Unterschied 2017/19 nach 2018/20", "Unterschied 2016/18 nach 2017/19"])


    sterberate = sterberate.rename(columns = {"variable" : "von nach", "value" : "Unterschied"})

    f, axes = plt.subplots(2,1,  figsize=(25, 20))
    sns.set_theme(style = "ticks", palette = "pastel")

    g1 = sns.lineplot( 
        data = sterberate[sterberate["Geschlecht"] == 'männlich'], 
        x = "Alter", 
        y = "Unterschied", 
        hue = "von nach",  
        ax = axes[0])

    g2 = sns.lineplot( 
        data = sterberate[sterberate["Geschlecht"] == 'weiblich'], 
        x = "Alter", 
        y = "Unterschied", 
        hue = "von nach",  
        ax = axes[1])

    g1.set_ylabel("Unterschied der Lebenserwartung in Jahren")
    g2.set_ylabel("Unterschied der Lebenserwartung in Jahren")

    plt.show()

if __name__ == "__main__" :
    sterberate = pd.read_csv("data/periodensterberate.csv", encoding = 'cp1252', sep = ";", header = 6)
    life_expectancy(sterberate)
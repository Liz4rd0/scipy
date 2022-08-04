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

def clean_data(stat) : 
    """Cleans the ds.csv dataset"""
    
    # The Dataset ends after 330 lines 
    stat = stat[:330]
    stat = stat.rename(columns = {"Unnamed: 0" : "Jahre", "Unnamed: 1" : "Todesursachen"})
    # unavailable values are replaced by 0
    stat = stat.replace("-", 0)
    stat = stat.replace(".", 0)
    
    # columns with unknown age are removed
    stat = stat.drop('weiblich.17', axis = 1)
    stat = stat.drop("männlich.17", axis = 1)
    
    # merges rows concerning the agegroup
    for i in range(0,36):
        stat.iloc[0,i] = stat.iloc[0,i]  + stat.iloc[1,i]
    #deletes row with now redundant information on agegroup
    stat = stat.drop(1, axis = 0)
    #unpivots columns regarding agegroup and gender
    stat = stat.melt(id_vars = ['Jahre', 'Todesursachen'], value_vars = stat.drop(['Jahre', 'Todesursachen'], axis = 1))
    # splits unpivoted value column to seperate the values from the agegroup information
    value_split = stat[stat.columns[3]].str.split("Altersgruppen",expand = True)
    stat[["value", "Altersgruppe"]] = value_split
    
    stat[["Altersgruppe"]] = stat[["Altersgruppe"]].ffill()
    stat[["value"]] = stat[["value"]].fillna(0)
    
    stat = stat.rename(columns = {"variable" : "Geschlecht"})
    
    # removes the number from the "Geschlecht" column
    stat_Geschlecht = stat[stat.columns[2]].str.split(".",expand = True) 
    stat[["Geschlecht"]] = stat_Geschlecht[[0]]
    # drops first row
    stat = stat.drop(0, axis = 0)
    stat = stat.dropna()

    
    stat[["value"]] = stat[["value"]].astype(int)
    
    # Since some values are counted in the superordinate category and the subordinate category, 
    # we specified the superordinate categories to filter and reduce duplication.
    # Since the Subcagetories do not always add up to the supercategories, we selected the supercategories 
    causes = ["Bestimmte infektiöse und parasitäre Krankheiten", 
              "Neubildungen", 
              "Krankheiten des Blutes u. der blutbildenden Organe", 
              "\"Endokrine, Ernährungs- u. Stoffwechselkrankheiten\"",
              "Psychische und Verhaltensstörungen", 
              "Krankheiten d. Nervensystems u. d. Sinnesorgane", 
              "Meningitis", 
              "Krankheiten des Kreislaufsystems",
              "Zerebrovaskuläre Krankheiten",
              "Krankheiten des Atmungssystems",
              "COVID-19, Virus nachgewiesen", 
              "COVID-19, Virus nicht nachgewiesen", 
              "Krankheiten des Verdauungssystems", 
              "Krankheiten der Leber", 
              "Krankheiten der Haut und der Unterhaut",
              "Krankh. des Muskel-Skelett-Systems u. Bindegewebes",
              "Krankheiten des Urogenitalsystems", 
              "\"Schwangerschaft, Geburt und Wochenbett\"", 
              "Best.Zustände mit Ursprung in der Perinatalperiode", 
              "\"Angeb. Fehlbildungen,DeformitÃ¤ten,Chromosomenanom.\"",
              "Symptome und abnorme klinische und Laborbefunde", 
              "Plötzlicher Kindstod", 
              "Sonst. ungenau bezeichnete u. unbek. Todesursachen", 
              "Äußere Ursachen von Morbidität und Mortalität", 
              "Vorsätzliche Selbstbeschädigung", 
              "Tätlicher Angriff", 
              "Ereignis, dessen nähere Umstände unbestimmt sind" ]
    stat = stat[stat["Todesursachen"].isin(causes) ]
    stat[stat["Todesursachen"] == "Krankeiten des Atmungssystems"] = stat[stat["Todesursachen"] == "Krankeiten des Atmungssystems"] - stat[(stat["Todesursachen"].str.contains("COVID")) == True]
    return stat


def overviewPlot(stat_cleaned):
    """Plots the top causes of death 2017-2020"""
    # extracts the top causes of death
    top_ursachen = stat_cleaned.groupby(["Jahre", "Todesursachen"])["value"].sum().reset_index().sort_values(by ="value",ascending = False)
    top_urs = top_ursachen.head(20)
    # extracts covid from the dataset
    cov = top_ursachen[top_ursachen["Todesursachen"].str.contains("COVID")].groupby("Jahre")["value"].sum().reset_index()
    cov["Todesursachen"]= ["COVID", "COVID", "COVID", "COVID"]
    # All other causes are counted towards "Sonstige"
    sonst = top_ursachen[4:]
    sonst = sonst[(sonst["Todesursachen"].str.contains("COVID")) == False]
    sonst = sonst.groupby("Jahre")["value"].sum().reset_index()
    sonst["Todesursachen"]= ["Sonstige", "Sonstige", "Sonstige", "Sonstige"]
 
    # concatinates the top causes, covid and sonstige
    top_urs = pd.concat([cov,top_urs, sonst]).reset_index()
   
    # creates the plot
    f = plt.figure()
    f.set_figwidth(20)
    f.set_figheight(10)
    sns.set_theme(palette = "pastel")
    sns.histplot(data = top_urs, x = "Jahre",weights = "value", hue = "Todesursachen",multiple = "stack")
    plt.title("Gesamtzahl der Todesfälle pro Jahr")
    plt.ylabel("Anzahl der Todesfälle")
    plt.show()


def compareTotalNumberOfDeath(stat_cleaned):
    """prints the factor by which the number of deaths has increased in 2020 compared to the mean of the 3 preceeding years"""

    stat_total =stat_cleaned.groupby(["Jahre"])["value"].sum().reset_index()
    mean_before_covid =np.mean(stat_total[:3]["value"])
    after_vs_before = stat_total.iloc[[3]]["value"]/mean_before_covid
    print("The factor by which the number of deaths has increased in 2020 compared to the mean of the 3 preceeding years: ")
    print(after_vs_before[3])


def compareNmberOfDeathsPerAgegroup(stat_cleaned):
    """Plots the mean of deaths per age group before and after covid started"""
    
    # exclueds 2020 and determines the mean
    stat_total_age =stat_cleaned[(stat_cleaned["Jahre"]== '2020') == False].groupby([ "Altersgruppe"])["value"].sum().reset_index()
    stat_total_age["value"] = (stat_total_age["value"]/3)
    stat_total_age = stat_total_age.rename(columns ={"value": "2017 - 2019"})
    
    # determines the number in 2020
    stat_total_age["2020"] = stat_cleaned[(stat_cleaned["Jahre"]== '2020') ].groupby([ "Altersgruppe"])["value"].sum().reset_index()["value"]
    stat_total_age = stat_total_age.melt(id_vars = ['Altersgruppe'], value_vars = ['2017 - 2019', "2020"])
    #stat_total_age = stat_total_age.sort_values(by = ["value"])
    
    f = plt.figure()
    f.set_figwidth(20)
    f.set_figheight(10)
    sns.set_theme(style = "ticks", palette = "pastel")
    chart = sns.barplot(data = stat_total_age, x = "Altersgruppe",y = "value", hue = "variable")
    chart.set_xticklabels(chart.get_xticklabels(), rotation = 45,horizontalalignment = 'right')
    plt.title("Gesamtzahl an Todesfällen pro Altersgruppe")
    plt.ylabel("Anzahl an Todesfällen")
    plt.show()

def compareNumberOfDeathsPerDisease(todesursache):
    """Plots the mean of deaths per cause before and after covid started"""
    stat = pd.read_csv("ds.csv", encoding = 'cp1252', sep = ";", header = 7)
    stat_cleaned = clean_data(stat)
    
    stat_cleaned = stat_cleaned[stat_cleaned['Todesursachen'] == todesursache]
    
    # exclueds 2020 and determines the mean
    
    stat_total_cause =stat_cleaned[(stat_cleaned["Jahre"]== '2020') == False].groupby([ "Todesursachen"])["value"].sum().reset_index()
    stat_total_cause["value"] = (stat_total_cause["value"]/3)
    stat_total_cause = stat_total_cause.rename(columns ={"value": "2017 - 2019"})
    
    
    # determines the number in 2020
    stat_total_cause["2020"] = stat_cleaned[(stat_cleaned["Jahre"]== '2020')].groupby([ "Todesursachen"])["value"].sum().reset_index()["value"]
    stat_total_cause = stat_total_cause.melt(id_vars = ["Todesursachen"], value_vars = ['2017 - 2019', "2020"])
    stat_total_cause = stat_total_cause.sort_values(by = ["value"])
    
    
    f = plt.figure()
    f.set_figwidth(20)
    f.set_figheight(10)
    sns.set_theme(style = "ticks", palette = "pastel")
    chart = sns.barplot(data = stat_total_cause, x = "Todesursachen",y = "value", hue = "variable")
    plt.title("Gesamtzahl an Todesfällen pro Todesursache")
    plt.ylabel("Anzahl an Todesfällen")
    plt.show()

def InteractiveAgePlot(altersgruppe):
    """Interactive Plot to display the difference before covid and after covid onset in the diferent age groups"""
    global data_for_later
    
    stat =pd.read_csv("ds.csv", encoding = 'cp1252', sep = ";", header = 7)
    stat_cleaned = clean_data(stat)
    
    # exclude Covid
    stat_cleaned = stat_cleaned[(stat_cleaned["Todesursachen"].str.contains("COVID")) == False]
    stat_cleaned = stat_cleaned[stat_cleaned["Altersgruppe"] == altersgruppe]

    # get the 2017 - 2019 (2017-2019) and create new column
    stat_total_cause =stat_cleaned[(stat_cleaned["Jahre"]== '2020') == False].groupby(["Altersgruppe", "Todesursachen"])["value"].sum().reset_index()
    stat_total_cause["value"] = (stat_total_cause["value"]/3)
    stat_total_cause = stat_total_cause.rename(columns ={"value": "2017 - 2019"})
    stat_total_cause["2020"] = stat_cleaned[(stat_cleaned["Jahre"]== '2020') ].groupby(["Altersgruppe", "Todesursachen"])["value"].sum().reset_index()["value"]

    # create column with the difference before and after covid
    stat_total_cause["difference"] = abs(stat_total_cause["2020"] - stat_total_cause["2017 - 2019"])
    data_for_later = stat_total_cause # safe data for later
    max_diffs = stat_total_cause.groupby(["Altersgruppe"])["difference"].max().reset_index()


    stat_max_diffs = pd.DataFrame()
    # merges max difference with the dataset
    for m in max_diffs.itertuples():  
        stat_max_diffs = pd.concat([stat_max_diffs,stat_total_cause.loc[(stat_total_cause["Altersgruppe"] == m[1]) & (stat_total_cause["difference"] == m[2])]], ignore_index = True)
    stat_max_diffs = stat_max_diffs.melt(id_vars = ["Altersgruppe","Todesursachen"], value_vars = ['2017 - 2019', "2020"])
    
    sns.set_theme(style = "ticks", palette = "pastel")
    sns.catplot( data = stat_max_diffs, x = "Altersgruppe", y = "value", hue = "variable", kind = "bar").set(title=stat_max_diffs["Todesursachen"][0])
    plt.ylabel("Anahl an Todesfällen")
    plt.show()

if __name__ == "__main__":
    
    stat =pd.read_csv("data/ds.csv", encoding = 'cp1252', sep = ";", header = 7)
    stat_cleaned = clean_data(stat)
    overviewPlot(stat_cleaned)
    compareTotalNumberOfDeath(stat_cleaned)
    compareNmberOfDeathsPerAgegroup(stat_cleaned)

    a = stat_cleaned.groupby("Todesursachen")["value"].sum().reset_index()["Todesursachen"]
    drop = widgets.Dropdown(options = a)
    widgets.interact(compareNumberOfDeathsPerDisease, todesursache = drop)

    a = stat_cleaned.groupby("Altersgruppe")["value"].sum().reset_index()["Altersgruppe"]
    drop = widgets.Dropdown(options = a)
    widgets.interact(InteractiveAgePlot, altersgruppe = drop)

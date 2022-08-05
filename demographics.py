from os import stat
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import warnings
import death_statistic
warnings.filterwarnings('ignore')

def clean_data2(population):
    """Function for cleaning the population dataset"""
    # calculate difference between 2020 and 2019 and the mean between 2019 and 2017
    population["difference2020-2019"] = population["31.12.2020"] - population["31.12.2019"]
    population["difference2019-2017"] = (population["31.12.2019"] - population["31.12.2018"] + population["31.12.2018"] - population["31.12.2017"])/2 

    population = population.drop(["31.12.2017", "31.12.2018", "31.12.2021", "31.12.2020", "31.12.2019"], axis = 1)

    # conversion of age column to an integer Series
    population = population.dropna()
    population = population[population["Unnamed: 0"] != "Insgesamt"]
    population["Unnamed: 0"] = population["Unnamed: 0"].str.replace("unter 1 Jahr", "0")
    population["Unnamed: 0"] = population["Unnamed: 0"].str.replace(" Jahre und mehr", "")
    population["Unnamed: 0"] = population["Unnamed: 0"].str.replace("-Jährige", "").astype(int)

    # pivot longer: columns '31.12.2019' and '31.12.2020' to one column 'year'
    population = pd.melt(population, id_vars=['Unnamed: 0'], value_vars=['difference2020-2019', 'difference2019-2017'])
    population = population.rename(columns = {"Unnamed: 0" : "age"})#, "variable" : "year", "value": "population"})

    # drop row with total number
    population = population[population["age"] != "Insgesamt"]
    # sort rows by age
    population = population.sort_values(by = ["age"]).reset_index()
    #drop old index
    population = population.drop('index', axis = 1)

    # create column with age group and 
    i = 0
    population['Altersgruppe'] = population['age']
    # age groups are defined by their maximum age (should create same age groups like in the death data set)
    age_groups = [1,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,99]
    for a in population['age']:
        for g in age_groups:
            if a < g:
                population['Altersgruppe'][i] = g
                break
        i += 1
    return population


def plot(population):
    """shows a plot of the demographic change"""
    f = plt.figure()
    f.set_figwidth(20)
    f.set_figheight(10)
    sns.barplot(data=population, y = 'value',x = 'age', hue = 'variable', palette = 'pastel')
    plt.title("Veränderungen der Demographie")
    plt.xlabel("Alter")
    plt.ylabel("Unterschied der Menschenanzahl")
    plt.show()

def plot_difference(population, stat_cleaned):
    """shows a plot of the demographic change between 2019 and 2020"""
    group_pop = population.groupby(['Altersgruppe', 'variable'])['value'].sum().reset_index()
    stat_cleaned = stat_cleaned[(stat_cleaned["Todesursachen"].str.contains("COVID")) == False]

    # get the 2017 - 2019 (2017-2019) and create new column
    stat_total_cause =stat_cleaned[(stat_cleaned["Jahre"]== '2020') == False].groupby(["Altersgruppe", "Todesursachen"])["value"].sum().reset_index()
    stat_total_cause["value"] = (stat_total_cause["value"]/3)
    stat_total_cause = stat_total_cause.rename(columns ={"value": "2017 - 2019"})
    stat_total_cause["2020"] = stat_cleaned[(stat_cleaned["Jahre"]== '2020') ].groupby(["Altersgruppe", "Todesursachen"])["value"].sum().reset_index()["value"]

    # create column with the difference before and after covid
    stat_total_cause["difference"] = stat_total_cause["2020"] - stat_total_cause["2017 - 2019"]


    cd = stat_total_cause
    stat =pd.read_csv("data/ds.csv", encoding = 'cp1252', sep = ";", header = 7)
    stat_cleaned = death_statistic.clean_data(stat)
    stat_cleaned = stat_cleaned[(stat_cleaned["Jahre"]== '2020') ]
    stat_total_cov = stat_cleaned[stat_cleaned["Todesursachen" ].str.contains("COVID")].groupby([ "Altersgruppe"])["value"].sum().reset_index()
    cd = stat_total_cov
    #cd = cd[cd["difference"] != 0.0].reset_index()

    # convert Altersgruppe to integer series
    cd['Altersgruppe'] = cd['Altersgruppe'].str.replace(" Jahre", "")
    cd['Altersgruppe'] = cd['Altersgruppe'].str.replace(" Jahr", "")
    cd['Altersgruppe'] = cd['Altersgruppe'].str.replace("85 und mehr", "99")
    cd['Altersgruppe'] = cd['Altersgruppe'].str.slice(start=-2).astype(int)

    cd = cd.groupby('Altersgruppe')['value'].sum()

    fig, ax = plt.subplots(1,2, figsize = (20,10))
    fig.subplots_adjust(hspace=0.7)
    # Plot how the demographics change from 2019 to 2020
    sns.barplot(data = group_pop[group_pop['variable'] == 'difference2020-2019'], y = 'Altersgruppe', x = 'value', ax = ax[0], orient = 'h')
    ax[0].set_title("Wie sich die Demographie von 2019 - 2020 verändert hat")
    ax[0].set_xlabel("Unterschied der Menschenanzahl")
    # Plot the total number of deaths per age group for COVID
    sns.set_theme(style = "ticks", palette = "pastel")
    chart = sns.barplot(data = stat_total_cov, y = "Altersgruppe",x = "value", ax = ax[1], orient = 'h')
    ax[1].set_title("Anzahl an Todesfällen pro Altersgruppe für COVID")
    ax[1].set_xlabel("Anzahl an Todesfällen")
    plt.show()

if __name__ == "__main__" :
    population = pd.read_csv("data/age.csv", encoding = 'cp1252', sep = ";", header = 6)
    stat =pd.read_csv("data/ds.csv", encoding = 'cp1252', sep = ";", header = 7)
    stat_cleaned = death_statistic.clean_data(stat)
    population = clean_data2(population)
    
    plot(population)
    plot_difference(population, stat_cleaned)

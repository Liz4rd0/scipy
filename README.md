# Death Statistics in Germany
## Project by Nicole Rogalla and Lisa Artmann

> The detailed functionality and interpretation of the project is explained in the Jupyter notebook

## Goal
The goal of our project is to analyze the death statistics in Germany with respect to Covid-19, specifically the effect on the total number of deaths, other causes of death, life expectancy and demographics. 

## Process: 
- get dataset before Covid19 and after Covid19 (2017-2019, 2020) 
- clean dataset
- analyze if covid lead to more deaths in 2020 and what covid death patients would have otherwise died of (and what their age would have been)
  - compare total number of deaths from different years overall and in the different age groups
- analyze if some other causes of death declined due to Covid19 (if percentage is less than average of 2017-2019)
  - how did measures against Covid19 influence the likelihood of dying of other causes (e.g. car accidents)
  - plot difference for most prominent causes of death
- investigate if life expectancy declined due to Covid19 by comparing the life expectancy before and during Covid19
- how did covid change the demographics in germany (dataset with demographics of germany from 2017-2019, 2020) (was change bigger from 2019-2020 in comparison to average of 2017-2018 and 2018-2019)
  - plot demographics

## Libraries
numpy, pandas, matplotlib, SciPy, seaborn, ipywidgets

## Prerequisits and Instructions
- All the above mentioned libraries must be installed
- click on run cell in the death_statistic.py file in visual code
- execute the life_expectancy.py and demographics.py
- OR run the jupyter notebook


## Resources
Statistisches Bundesamt. (2021). Gestorbene: Deutschland, Jahre, Todesursachen, Geschlecht, Altersgruppen. (23211-0004). [Data set]. https://www-genesis.destatis.de/genesis/online?operation=find&suchanweisung_language=de&query=lebenserwartung#abreadcrumb

Statistisches Bundesamt. (2022). Durchschnittliche Lebenserwartung (Periodensterbetafel): Deutschland, Jahre, Geschlecht, Vollendetes Alter. (12621-0002). [Data set]. https://www-genesis.destatis.de/genesis//online?operation=table&code=12621-0002&bypass=true&levelindex=0&levelid=1659649201416#abreadcrumb

Statistisches Bundesamt. (2022). Bevölkerung: Deutschland, Stichtag, Altersjahre. (12411-0005). [Data set]. https://www-genesis.destatis.de/genesis//online?operation=table&code=12411-0005&bypass=true&levelindex=0&levelid=1659705608317#abreadcrumb

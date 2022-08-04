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
numpy, panda, matplotlib, SciPy, seaborn

## Resources
- https://www-genesis.destatis.de/genesis/online?operation=abruftabelleBearbeiten&levelindex=1&levelid=1659649214846&auswahloperation=abruftabelleAuspraegungAuswaehlen&auswahlverzeichnis=ordnungsstruktur&auswahlziel=werteabruf&code=12621-0002&auswahltext=&werteabruf=Werteabruf#abreadcrumb
- https://www-genesis.destatis.de/genesis//online?operation=table&code=23211-0004&bypass=true&levelindex=0&levelid=1659649356469#abreadcrumb
- https://www-genesis.destatis.de/genesis/online?sequenz=tabelleErgebnis&selectionname=12411-0005#abreadcrumb

# COVID-19 daily death prediction 
[![Open in Code Ocean](https://codeocean.com/codeocean-assets/badge/open-in-code-ocean.svg)](https://codeocean.com/capsule/3aa3e186-03f3-43b4-85d1-fe86f43bedd9/tree)

DOI: https://doi.org/10.24433/CO.1663204.v1

The paper was published:
Takefuji, Y. Deathdaily: A Python Package Index for predicting the number of daily COVID-19 deaths. Netw Model Anal Health Inform Bioinforma 11, 14 (2022). https://doi.org/10.1007/s13721-022-00359-1

Verification for computational reproducibility & quality is doned by codeocean:
https://codeocean.com/capsule/3aa3e186-03f3-43b4-85d1-fe86f43bedd9/tree

deathdaily is a Python program using new_deaths.csv for predicting daily deaths due to COVID-19 in the next seven days. The prediction is based on the Xthe degree polynomial curve-fitting.

According to PyPI Stats at https://pepy.tech/, deathdaily has been downloaded by 30105 times worldwide as of Feb.22, 2023, one of the most popular COVID-19 tools of its kind.

deathdaily takes three parameters: country, days, the xth degree of a polynomial.
Days shows the number of days used for calculating the curve-fiting function with xth
degree of a polynomial for curve-fitting function.

The maximum days range is available from Jan.22 2020 to the day you have downloaded in new_deaths.csv file. 

Y-axis depicts the number of daily deaths in the country.

# new_deaths.csv

deathdaily needs a new_deaths.csv file for predicting the daily deaths of the next seven days.

The new_deaths.csv file is automatically downloaded by deathdaily from the following site:

https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/jhu/new_deaths.csv


# How to install deathdaily

$ pip install deathdaily

or

$ pip install deathdaily --force-reinstall --no-cache-dir --no-binary :all:

# How to run deathdaily 

"country" shows which country you would like to predict the daily deaths of the next seven days.

"days" indicates how many days are used for Xth degree polynomial curve-fitting.

"degree" determines the degree of polynomial curve-fitting.

$ deathdaily Japan days degree

$ deathdaily Japan 200 11

country="Japan", days=200, degree=11

<img src="https://github.com/y-takefuji/covid-19_daily_death_prediction/raw/main/Japan.png" width=320 height=240 >


$ deathdaily 'United States' 200 11

<img src="https://github.com/y-takefuji/covid-19_daily_death_prediction/raw/main/United States.png" width=320 height=240 >

$ deathdaily Israel 200 9

<img src="https://github.com/y-takefuji/covid-19_daily_death_prediction/raw/main/Israel.png" width=320 height=240 >

$ deathdaily 'United Kingdom' 100 11

<img src="https://github.com/y-takefuji/covid-19_daily_death_prediction/raw/main/United Kingdom.png" width=320 height=240 >

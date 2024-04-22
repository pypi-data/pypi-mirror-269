# vud4
[![Open in Code Ocean](https://codeocean.com/codeocean-assets/badge/open-in-code-ocean.svg)](https://codeocean.com/capsule/1960114/tree)


Takefuji Y. Vaccine effects on COVID-19 infection with bivalent boosting by age group. Drug Resist Updat. 2023 Dec 27;73:101039. doi: 10.1016/j.drup.2023.101039. Epub ahead of print. PMID: 38169273.

vud4.py is to calculate the time-series effect of vaccination on mortality in six age groups (18-29 years, 30-49 years, 50-64 years, 65-79 years, 80+ years, and all ages) for three vaccination types: bivalent booster, fully vaccinated, and unvaccinated. The CDC dataset for the period October 1, 2021 through January 23, 2023 was used for this study:
https://data.cdc.gov/api/views/54ys-qyzm/rows.csv

vud4 is a PyPI application. PyPI allows vud4 to run on Windows, MacOS and Linux Operating Systems as long as Python is installed on the system.

# How to install vud4
$ pip install vud4

# How to run vud4
$ vud4

enter one of age groups: vud4 80+

18-29,30-49,50-64,65-79,80+,all_ages

$ vud4 80+

<img src='https://github.com/y-takefuji/vud4/raw/main/bivalent_80%2B.png' height=240 width=280>

# hiscovid
[![Open in Code Ocean](https://codeocean.com/codeocean-assets/badge/open-in-code-ocean.svg)](https://codeocean.com/capsule/5655627/tree)

Taiwan' data from the dataset was removed by the provider.

Takefuji Y. (2022) hiscovid for calculating time transition scores of policies against COVID-19 [Source Code]. https://doi.org/10.24433/CO.7364293.v1

Publications:

Takefuji Y. (2022). Sustainable policy: Don't get infected and don't infect others. Journal of Hazardous Materials Advances, 8, 100165. https://doi.org/10.1016/j.hazadv.2022.100165

Takefuji Y. (2022). COVID-19 policy analysis for 10 European countries. Zeitschrift fur Gesundheitswissenschaften = Journal of public health, 1–8. Advance online publication. https://doi.org/10.1007/s10389-022-01786-0

Takefuji Y. (2023). Policy analysis and data mining tools for controlling COVID-19 policies. Network modeling and analysis in health informatics and bioinformatics, 12(1), 4. https://doi.org/10.1007/s13721-022-00400-3

Takefuji Y. (2023). How to build disaster-resilient cities and societies for making people happy. Building and environment, 228, 109845. https://doi.org/10.1016/j.buildenv.2022.109845



hiscovid is a PyPI tool that calculates time transition scores for individual policies against COVID-19.

The goal of hiscovid is for policymakers to identify when they made mistakes.
Policymakers must learn their mistakes for possible corrections in the future.

The time transition score is calculated by dividing the number of deaths in the time series 
due to COVID-19 by the population in millions.

Scores monotonically increase so that policymakers can only suppress them, but cannot improve them.
Mistakes by policymakers cannot be corrected and are fatal forever.

The lower the score, the better the policy.

In other words, the score is equivalent to the accumulation of mistakes made by policymakers.

The perfect policy outcome means there are no covid-19 deaths. There is no perfect policy in the world, but
mistakes by policymakers can be corrected for future better decisions.


hiscovid scrapes the latest data from the following site over the Internet:

https://covid.ourworldindata.org/data/owid-covid-data.csv

Data of Taiwan was removed from March 2023!

Mistakes can be observed in the calculated graph.

# How to install hiscovid
$ pip install hiscovid

# How to run hiscovid
$ hiscovid <country name(s)>

$ hiscovid Japan 'South Korea'

<img src='https://github.com/y-takefuji/hiscovid/raw/main/jsk.png' height=480 width=640>

$ hiscovid Japan Taiwan

<img src='https://github.com/y-takefuji/hiscovid/raw/main/twjp.png' height=480 width=640>


The vertical axis shows the overall result scores for policy, individual behavior, vaccination, 
and new COVID-19 variants. 
Score is the number of deaths due to COVID-19 per population in millions.

In the graph of South Korea, there are two points where the slope of the scoreline changed abruptly,
including mid-November 2021 and mid-February 2022.

In the graph of Japan, there is a single abruptly changed point around mid-January 2022.


$ hiscovid Taiwan 'New Zealand'

<img src='https://github.com/y-takefuji/hiscovid/raw/main/twnz.png' height=480 width=640>

There is one point in the Taiwan graph that changes abruptly around mid-May 2021.

There is one point in the New Zealand graph that changes abruptly around the mid-February 2022.

$ hiscovid Taiwan 'United States' 'United Kingdom'

<img src='https://github.com/y-takefuji/hiscovid/raw/main/twusuk.png' height=480 width=640>

In the US graph, the scoreline is constantly bad, but a single point that changes abruptly around the mid-August 2021.

In the UK graph, there are two points where the slope of the scoreline changed abruptly,
including the mid-March 2020 and the mid-October 2020.


# Students exercises
question: Can you convert hiscovid into a program that produces black and white lines?

<img src='https://github.com/y-takefuji/hiscovid/raw/main/bw.png' height=480 width=640>


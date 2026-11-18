import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

from urllib.request import urlopen
from bs4 import BeautifulSoup

url_recipes = "https://zeldacentral.com/games/tears-of-the-kingdom/recipes/?"
html_recipes = urlopen(url_recipes)

recipes = BeautifulSoup(html, 'lxml')

soup.find_all('table')

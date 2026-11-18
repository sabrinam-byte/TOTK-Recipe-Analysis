import pandas as pd

url = "https://zeldacentral.com/games/tears-of-the-kingdom/recipes/"

tables = pd.read_html(url)

print(len(tables))

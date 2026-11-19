import pandas as pd
import matplotlib.pyplot as plt

totk_materials_table = pd.read_csv("Data Spreadsheet for Tears of the Kingdom (1.4.0) - Materials.csv")

totk_recipes_table = pd.read_csv("Data Spreadsheet for Tears of the Kingdom (1.4.0) - Food.csv")

botw_materials_table = pd.read_csv("Breath of the Wild - Items Checklist - Materials.csv")

filtered_totk_materials_table = totk_materials_table.loc[totk_materials_table["Cooking Effect Level"].isnull() & totk_materials_table["Hearts Recovered"].isnull()]

botw = pd.read_csv("BOTW Recipes Expanded.csv", header=None,
                   names=["Dish Type", "Name", "Ing1", "Ing2", "Ing3", "Ing4", "Ing5"])
botw = botw.dropna(subset=["Dish Type"])                              
botw = botw[botw["Dish Type"] != "BREATH OF THE WILD RECIPES"]       
botw = botw[botw["Dish Type"] != "MONSTER FOODS"]                     
botw["Dish Type"] = botw["Dish Type"].str.title()
botw_cols = ["Ing1", "Ing2", "Ing3", "Ing4", "Ing5"]

totk = totk_recipes_table[totk_recipes_table["Cooking Method"] == "Cooking Pot"]
totk_cols = ["Required Ingredient 1", "Required Ingredient 2", "Required Ingredient 3",
             "Required Ingredient 4", "Required Ingredient 5"]

# how many different ingredients each recipe uses
botw["Num Ingredients"] = botw[botw_cols].nunique(axis=1)
totk["Num Ingredients"] = totk[totk_cols].replace("-", pd.NA).nunique(axis=1)

# one row per (recipe, ingredient), so we can count how many recipes use each ingredient
botw_long = botw.melt(id_vars="Name", value_vars=botw_cols, value_name="Ingredient")
botw_long = botw_long.dropna(subset=["Ingredient"]).drop_duplicates(subset=["Name", "Ingredient"])
botw_long["Ingredient"] = botw_long["Ingredient"].str.strip()

totk_long = totk.melt(id_vars="Name", value_vars=totk_cols, value_name="Ingredient")
totk_long = totk_long[totk_long["Ingredient"] != "-"].dropna(subset=["Ingredient"])
totk_long = totk_long.drop_duplicates(subset=["Name", "Ingredient"])

botw["Dish Type"].value_counts().head(12).plot(kind="bar", color="#0072B2", figsize=(8, 5))
plt.title("BOTW: Recipes per Dish Type")
plt.xlabel("Dish type")
plt.ylabel("Number of recipes")
plt.tight_layout()
plt.show()

botw_long["Ingredient"].value_counts().head(10).plot(kind="bar", color="#0072B2", figsize=(8, 5))
plt.title("BOTW: 10 Most Common Ingredients")
plt.xlabel("Ingredient")
plt.ylabel("Number of recipes that use it")
plt.tight_layout()
plt.show()

totk_long["Ingredient"].value_counts().head(10).plot(kind="bar", color="#E69F00", figsize=(8, 5))
plt.title("TOTK: 10 Most Common Ingredients")
plt.xlabel("Ingredient")
plt.ylabel("Number of recipes that use it")
plt.tight_layout()
plt.show()

totk["Num Ingredients"].value_counts().sort_index().plot(kind="bar", color="#E69F00")
plt.title("TOTK: Number of Different Ingredients per Recipe")
plt.xlabel("Number of different ingredients")
plt.ylabel("Number of recipes")
plt.show()

botw["Game"] = "BOTW"
totk["Game"] = "TOTK"
both = pd.concat([botw[["Game", "Name", "Num Ingredients"]],
                  totk[["Game", "Name", "Num Ingredients"]]], ignore_index=True)

# percent of each game's recipes (BOTW and TOTK have different numbers of recipes)
share = pd.crosstab(both["Num Ingredients"], both["Game"], normalize="columns") * 100
share.plot(kind="bar", color=["#0072B2", "#E69F00"])
plt.title("BOTW vs TOTK: Number of Different Ingredients per Recipe")
plt.xlabel("Number of different ingredients")
plt.ylabel("Percent of that game's recipes")
plt.legend(title="Game")
plt.show()

shared = ["Goat Butter", "Hylian Rice", "Rock Salt", "Tabantha Wheat",
          "Fresh Milk", "Goron Spice", "Cane Sugar"]
compare = pd.DataFrame({
    "BOTW": botw_long["Ingredient"].value_counts() / len(botw) * 100,
    "TOTK": totk_long["Ingredient"].value_counts() / len(totk) * 100
}).loc[shared]

compare.plot(kind="bar", color=["#0072B2", "#E69F00"], figsize=(8, 5))
plt.title("BOTW vs TOTK: Shared Ingredients")
plt.xlabel("Ingredient")
plt.ylabel("Percent of recipes that use it")
plt.legend(title="Game")
plt.tight_layout()
plt.show()
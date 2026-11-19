"""
Sabrina Mickley
CSE163 TOTK Project
This file reads CSV files containing recipe data for Breath of the Wild (BOTW)
and Tears of the Kingdom (TOTK), cleans the data as necessary, and creates visualizations to 
compare statistics regarding the two games recipe and ingredient usage, including common 
ingredients, number of ingredients per recipe, and number of recipes per dish type.
"""

import pandas as pd
import matplotlib.pyplot as plt


"""
Converts TOTK recipes into a long format, preserving the recipe's
name and effect alongside each ingredient.
"""
def make_totk_long(totk: pd.DataFrame, totk_cols: list) -> pd.DataFrame:
    totk = totk.copy()
    totk["_RecipeID"] = range(len(totk))

    totk_long = totk.melt(
        id_vars=["_RecipeID", "Name", "Effect"],
        value_vars=totk_cols,
        value_name="Ingredient"
    )

    totk_long["Ingredient"] = totk_long["Ingredient"].str.strip()
    totk_long["Effect"] = totk_long["Effect"].str.strip()

    totk_long = totk_long.replace("", pd.NA)
    totk_long = totk_long[
        totk_long["Ingredient"] != "-"
    ].dropna(subset=["Ingredient", "Effect"])

    totk_long = totk_long.drop_duplicates(
        subset=["_RecipeID", "Ingredient"]
    )

    return totk_long


"""
Creates a bar chart showing the number of recipes per dish type in BOTW.
"""
def number_of_recipes_botw(botw: pd.DataFrame) -> None:
    botw["Dish Type"].value_counts().head(12).plot(kind="bar", color="#0072B2", figsize=(8, 5))
    plt.title("BOTW: Recipes per Dish Type")
    plt.xlabel("Dish type")
    plt.ylabel("Number of recipes")
    plt.tight_layout()
    plt.show()


"""
Creates a bar chart showing the 10 most common ingredients in BOTW.
"""
def common_ingredients_botw(botw_long: pd.DataFrame) -> None:
    botw_long["Ingredient"].value_counts().head(10).plot(kind="bar", color="#0072B2", figsize=(8, 5))
    plt.title("BOTW: 10 Most Common Ingredients")
    plt.xlabel("Ingredient")
    plt.ylabel("Number of recipes that use it")
    plt.tight_layout()
    plt.show()


"""
Creates a bar chart showing the 10 most common ingredients in TOTK.
"""
def common_ingredients_totk(totk_long: pd.DataFrame) -> None:
    totk_long["Ingredient"].value_counts().head(10).plot(kind="bar", color="#E69F00", figsize=(8, 5))
    plt.title("TOTK: 10 Most Common Ingredients")
    plt.xlabel("Ingredient")
    plt.ylabel("Number of recipes that use it")
    plt.tight_layout()
    plt.show()


"""
Creates a bar chart showing the 10 ingredients associated with the greatest 
number of unique recipe effects in TOTK."""
def versatile_ingredients_totk(totk_long: pd.DataFrame) -> None:
    effect_counts = (
        totk_long.groupby("Ingredient")["Effect"]
        .nunique()
        .sort_values(ascending=False)
        .head(10)
    )

    effect_counts.sort_values().plot(
        kind="barh",
        color="#E69F00",
        figsize=(9, 6)
    )

    plt.title("TOTK: 15 Most Versatile Ingredients")
    plt.xlabel("Number of Different Effects")
    plt.ylabel("Ingredient")
    plt.tight_layout()
    plt.show()



"""
Sets up the data frames and calls all the visualization functions.
"""
if __name__ == "__main__":

    totk_recipes_table = pd.read_csv("Data Spreadsheet for Tears of the Kingdom (1.4.0) - Food.csv")


    botw = pd.read_csv("BOTW Recipes Expanded.csv", header=None,
                        names=["Dish Type", "Name", "Ing1", "Ing2", "Ing3", "Ing4", "Ing5"])
    botw = botw.dropna(subset=["Dish Type"])                              
    botw = botw[botw["Dish Type"] != "BREATH OF THE WILD RECIPES"]       
    botw = botw[botw["Dish Type"] != "MONSTER FOODS"]
    botw["Name"] = botw["Name"].fillna(botw["Dish Type"])                     
    botw["Dish Type"] = botw["Dish Type"].str.title()
    botw_cols = ["Ing1", "Ing2", "Ing3", "Ing4", "Ing5"]

    totk = totk_recipes_table[totk_recipes_table["Cooking Method"] == "Cooking Pot"]
    totk_cols = ["Required Ingredient 1", "Required Ingredient 2", "Required Ingredient 3",
                "Required Ingredient 4", "Required Ingredient 5"]

 
    botw["Num Ingredients"] = botw[botw_cols].nunique(axis=1)
    totk["Num Ingredients"] = totk[totk_cols].replace("-", pd.NA).nunique(axis=1)

    botw_long = botw.melt(id_vars="Name", value_vars=botw_cols, value_name="Ingredient")
    botw_long = botw_long.dropna(subset=["Ingredient"]).drop_duplicates(subset=["Name", "Ingredient"])
    botw_long["Ingredient"] = botw_long["Ingredient"].str.strip()

    totk_long = make_totk_long(totk, totk_cols)

    print(botw_long["Ingredient"].value_counts())
    print(totk_long["Ingredient"].value_counts())


    number_of_recipes_botw(botw)

    common_ingredients_botw(botw_long)

    common_ingredients_totk(totk_long)

    versatile_ingredients_totk(totk_long)

    


 


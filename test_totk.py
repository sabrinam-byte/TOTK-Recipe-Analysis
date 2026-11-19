"""
Sabrina Mickley
CSE163 TOTK Project
This file contains tests to check that the steps used in visualization.py to
clean and process data are working as expected, using smaller datasets and
and direct counting (rather than panda methods) to verify the results.
"""

import pandas as pd
import matplotlib.pyplot as plt


"""
Converts TOTK into a long format, preserving the recipe's name and effect along 
with each ingredient, making it easier to count how many recipes use each ingredient.
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
Tests that the make_totk_long function correctly transforms the data and preserves
relevant information, using a smaller data set.
"""
def test_totk_long(totk: pd.DataFrame, totk_cols: list) -> None:
    sample = totk.head(20).copy()
    sample_long = make_totk_long(sample, totk_cols)

    assert "Ingredient" in sample_long.columns
    assert "Effect" in sample_long.columns
    assert "_RecipeID" in sample_long.columns

    assert sample_long["Ingredient"].notna().all()
    assert sample_long["Effect"].notna().all()

    assert not (sample_long["Ingredient"] == "-").any()

    assert not sample_long.duplicated(
        subset=["_RecipeID", "Ingredient"]
    ).any()

    for _, row in sample_long.iterrows():
        original_recipe = sample.iloc[row["_RecipeID"]]

        assert row["Effect"] == original_recipe["Effect"]
        assert row["Ingredient"] in original_recipe[totk_cols].values

    print("All TOTK long-format tests passed!")


"""
Returns the number of distinct effects associated with each ingredient, to use as
a measure of versatility for the ingredient. 
"""
def get_versatility(totk_long: pd.DataFrame) -> pd.Series:
    return (
        totk_long.groupby("Ingredient")["Effect"]
        .nunique()
        .sort_values(ascending=False)
    )


"""
Tests that the get_versatility function correctly counts the number of distinct effects
associated with each ingredient using a small subset.
"""
def test_versatility(totk: pd.DataFrame, totk_cols: list) -> None:

    sample = totk.head(20).copy()
    sample_long = make_totk_long(sample, totk_cols)

    versatility = get_versatility(sample_long)

    assert len(versatility) > 0

    assert (versatility >= 1).all()

    for ingredient in versatility.index:
        expected = len(
            set(sample_long.loc[
                sample_long["Ingredient"] == ingredient, "Effect"
            ])
        )

        assert versatility[ingredient] == expected

    print("All versatility tests passed!")


"""
Tests whether BOTW ingredient frequencies are calculated correctly.
"""
def test_botw_frequencies(botw_long: pd.DataFrame) -> None:
    
    frequencies = botw_long["Ingredient"].value_counts()

    assert len(frequencies) > 0
    assert (frequencies > 0).all()

    for ingredient, count in frequencies.items():
        expected = (botw_long["Ingredient"] == ingredient).sum()
        assert count == expected

    print("All BOTW frequency tests passed!")


"""
Sets up the data frames and runs all the tests.
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

    test_totk_long(totk, totk_cols)
    test_versatility(totk, totk_cols)

    test_botw_frequencies(botw_long)


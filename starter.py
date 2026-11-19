import pandas as pd

totk_materials_table = pd.read_csv("Data Spreadsheet for Tears of the Kingdom (1.4.0) - Materials.csv")

totk_recipes_table = pd.read_csv("Data Spreadsheet for Tears of the Kingdom (1.4.0) - Food.csv")

botw_recipes_table = pd.read_csv("BOTW Recipes Expanded.csv")

botw_materials_table = pd.read_csv("Breath of the Wild - Items Checklist - Materials.csv")

filtered_totk_materials_table = totk_materials_table.loc[totk_materials_table["Cooking Effect Level"].isnull() & totk_materials_table["Hearts Recovered"].isnull()]

fruit_botw = botw_materials_table.iloc[0:9][["Materials"]]

fruit_totk = filtered_totk_materials_table.loc[filtered_totk_materials_table["ActorName"].str.contains("Fruit"), ["Name"]]

mushroom_botw = botw_materials_table.iloc[10:22][["Materials"]]

mushroom_totk = filtered_totk_materials_table.loc[filtered_totk_materials_table["ActorName"].str.contains("Mushroom"), ["Name"]]

meat_botw = botw_materials_table.iloc[38:44][["Materials"]]

meat_totk = filtered_totk_materials_table.loc[filtered_totk_materials_table["ActorName"].str.contains("Meat"), ["Name"]]

seafood_botw = botw_materials_table.iloc[72:90][["Materials"]]

seafood_totk = filtered_totk_materials_table.loc[(filtered_totk_materials_table["ActorName"].str.contains("Fish") | filtered_totk_materials_table["Name"].str.contains("Crab")), ["Name"]]

insect_botw = botw_materials_table.iloc[91:109][["Materials"]]

insect_totk = filtered_totk_materials_table.loc[(filtered_totk_materials_table["ActorName"].str.contains("Insect") & ~filtered_totk_materials_table["Name"].str.contains("Crab")), ["Name"]]

monster_part_botw = botw_materials_table.iloc[119:151][["Materials"]]

monster_part_totk = filtered_totk_materials_table.loc[filtered_totk_materials_table["ActorName"].str.contains("Monster"), ["Name"]]


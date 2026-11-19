import openpyxl
import pandas as pd

file_path = "BOTW Recipe List.xlsx"

wb = openpyxl.load_workbook(file_path)
ws = wb[wb.sheetnames[0]]

# Save the merged ranges before unmerging
merged_ranges = list(ws.merged_cells.ranges)

for merged_range in merged_ranges:

    # Get the value from the top-left cell
    value = ws.cell(
        row=merged_range.min_row,
        column=merged_range.min_col
    ).value

    # Unmerge the cells
    ws.unmerge_cells(str(merged_range))

    # Fill EVERY cell in the original merged range
    for row in range(merged_range.min_row,
                     merged_range.max_row + 1):

        for col in range(merged_range.min_col,
                         merged_range.max_col + 1):

            ws.cell(row=row, column=col).value = value

# Save the expanded spreadsheet
wb.save("BOTW Recipe List Expanded.xlsx")

df = pd.read_excel("BOTW Recipe List Expanded.xlsx", header=None)

# Export to CSV
df.to_csv("BOTW Recipes Expanded.csv", index=False, header=False)


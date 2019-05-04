import sys
import pandas as pd

# 2.     Write a computer program (Python/C++/Java) to preprocess the data

filename = "ALL_vs_AML_train_set_38_sorted.res"
output_filename = "testoutput.csv"

dt = []

with open(filename, "r") as file:
	for row in file:
		cell = row.split("\t")
		dt.append(cell)

# pandas housekeeping

df = pd.DataFrame(dt)
df.columns = dt[0]

columns = list(df)

# ·       Eliminate the “endogenous control” genes (housekeeping genes);

df = df[df.Description.str.contains("endogenous control") == False]

# ·       Eliminate the genes with all As across the experiments;

df = df[(df.iloc[:, 1:] != "A").all(axis=1)]

# ·       Replace all the expression values below some threshold cut-off value to that threshold value (pick 20 to be the threshold cut-off value);

for x in range(len(dt)):
	for y in range(len(dt[x])):
		if(dt[x][y].isdigit() and int(dt[x][y]) < 20):
			dt[x][y] = "20"

# ·       Eliminate the genes with less than two fold change across the experiments (max/min <2);

# ???????????????

# ·       Save the Affymetrics ID of the genes and its expression values into a file. The file should look like the following:

# remove description column and empty columns, as well as other cluttery rows
del df['Description']
del df['']
df = df.drop([0,1,2])

df.to_csv(output_filename, encoding='utf-8', index=False) # export csv of data

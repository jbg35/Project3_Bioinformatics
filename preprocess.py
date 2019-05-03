import re
import sys

# 1) Eliminate the “endogenous control” genes (housekeeping genes);
#
# 2) Eliminate the genes with all As across the experiments;
#
# 3) Replace all the expression values below some
# threshold cut-off value to that threshold value
# (pick 20 to be the threshold cut-off value);
#
# 4) Eliminate the genes with less than two fold
# change across the experiments (max/min <2);
#
# 5) Save the Affymetrics ID of the genes and its expression 
# values into a file. The file should look like the following:


def preprocess(filepath):
    newfilepath = filepath[:9] + "new_" + filepath[9:]

    file = open(filepath, "r+")
    newfile = open(newfilepath, "w+")

    for line in file:
        if "endogenous control" not in line:
            newfile.write(line)

    file.close()
    newfile.close()


trainData = "Datasets\ALL_vs_AML_train_set_38_sorted.res"
testData = "Datasets\Leuk_ALL_AML.test.res"

preprocess(trainData)
#preprocess(testData)

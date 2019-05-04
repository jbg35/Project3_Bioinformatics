import re
import sys
from scipy import stats
# Feature selection using the training data set
# a.      Sort genes in your preprocessed training dataset based on their p-values
# 			You may use excel spread sheet to do it.
# ·       Syntax: TTEST(array1,array2,tails,type)
# ·       Use 2 for tails (two tailed distribution) and 3 for type (assuming unequal variances)
# ·       Enter t-test to get help from Excel if you need
# b.     Select 50 top genes (with smallest p-values) and save the expression data of the 50 genes (clearly the number of top genes is a parameter and can be varied. If you prefer, you can plot the p-values and then decide the # of features to choose.)

# ttest info for python 
# https://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.stats.ttest_ind.html

def write_file(genes_to_write, FILE_):
    data = open("ALL_vs_AML_train_set_38_sorted.res")
    extra_ = [data.readline(), data.readline()]
    
    preprocessed_data = open(FILE_, "+w")
    preprocessed_data.writelines(extra_)
    preprocessed_data.write(str(len(genes_to_write)) + "\n")
    for gene_ in genes_to_write:
        row_data = gene_["description"] + "\t" + gene_["name"]
        # PAM is just the column with p, a or m
        for j_ in gene_["column_values"]:
            for k_ in gene_["column_values"][j_]:
                intensity_and_PAM = gene_["column_values"][j_][k_]
                row_data = row_data + "\t" + intensity_and_PAM["intensity"]
                row_data = row_data + "\t" + intensity_and_PAM["PAM"]
        row_data = row_data + "\n"
        preprocessed_data.write(row_data)

    data.close()
    preprocessed_data.close()

def read_file(vector, train):  
    gene_array = []

    vector_info = open(vector)
    # Removes info at top of vector file
    vector_filler = vector_info.readline().split(" ")
    column_labels = vector_info.readline().split(" ")
    column_labels.remove("\n")
    
    gene_data = open(train)
    
    # Labels for the columns
    column_name_filler = gene_data.readline().split("\t")
    column_name_filler.remove("\n")
    
    columns = gene_data.readline().split("\t")
    columns.remove("\n")

    # Removes empty cells
    for i in columns:
        if i == "":
            columns.remove(i)

    gene_count = gene_data.readline()

    row_ = gene_data.readlines()
    for j_ in row_:
        j_ = j_.split("\t") 
        if "\n" in j_:
            j_.remove("\n")

        add_gene = {"name":j_[1], "description":j_[0], "column_values":{"AML":{}, "ALL":{}}}
        index = 2
        while index < len(j_):
            intensity_and_PAM = {"intensity":j_[index], "PAM":j_[index + 1]}
            
            INDEXER = int((index - 2) / 2)
            scale_factor = columns[INDEXER]

            if column_labels[INDEXER] == '0': 
                add_gene["column_values"]["ALL"][scale_factor] = intensity_and_PAM
            else:
                add_gene["column_values"]["AML"][scale_factor] = intensity_and_PAM
            index += 2
        
        gene_array.append(add_gene)

    gene_data.close()

    return gene_array

def selection(gene_array):
	for i_ in gene_array:
	    aml_arr = []
	    all_arr = []
	    for j_ in i_["column_values"]["AML"]:
	        aml_arr.append(int(i_["column_values"]["AML"][j_]["intensity"]))
	    for j_ in i_["column_values"]["ALL"]:
	        all_arr.append(int(i_["column_values"]["ALL"][j_]["intensity"]))
	    i_["P_VALUE"] = stats.ttest_ind(aml_arr, all_arr, equal_var=False).pvalue
	    #equal_var : bool, optional
		#If True (default), perform a standard independent 2 sample test that assumes 
		#equal population variances [R315]. If False, perform Welch’s t-test, which 
		#does not assume equal population variance [R316].

	gene_array.sort(key=lambda SORT:SORT["P_VALUE"])
	top_50 = gene_array[0:50]
	print(top_50[0])
	write_file(top_50, "ALL_vs_AML_train_set_38_selection.res")

if __name__ == "__main__":
	gene_array = read_file("ALL_vs_AML_train_set_38_sorted.cls", "ALL_vs_AML_train_set_38_cleaned.res" )
	selection(gene_array)
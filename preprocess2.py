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
# 5) Save the Affymetrics name of the genes and its expression 
# values into a file. The file should look like the following:


def write_file(genes_to_write):
    data = open("ALL_vs_AML_train_set_38_sorted.res")
    extra_ = [data.readline(), data.readline()]
    
    preprocessed_data = open("ALL_vs_AML_train_set_38_cleaned.res", "+w")
    preprocessed_data.writelines(extra_)
    preprocessed_data.write(str(len(genes_to_write)) + "\n")
    for gene_ in genes_to_write:
        row_data = gene_["description"] + "\t" + gene_["name"]

        for j_ in gene_["column_values"]:
            for k_ in gene_["column_values"][j_]:
                intensity_and_PAM = gene_["column_values"][j_][k_]
                row_data = row_data + "\t" + intensity_and_PAM["intensity"]
                row_data = row_data + "\t" + intensity_and_PAM["PAM"]
        row_data = row_data + "\n"
        preprocessed_data.write(row_data)

    data.close()
    preprocessed_data.close()

def read_file():  
    gene_array = []

    vector_info = open("ALL_vs_AML_train_set_38_sorted.cls")
    # Removes info at top of vector file
    vector_filler = vector_info.readline().split(" ")
    column_labels = vector_info.readline().split(" ")
    column_labels.remove("\n")
    
    gene_data = open("ALL_vs_AML_train_set_38_sorted.res")
    
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

def preprocess(genes_from_file):
    remove_ = []
    for gene in genes_from_file:
        if "endogenous control" in gene["description"]:
            remove_.append(gene)
        else:
            bool_flag = True
            threshold = 20
            
            for j_ in gene["column_values"]:
                for k_ in gene["column_values"][j_]:
                    intensity = gene["column_values"][j_][k_]["intensity"]

                    if int(intensity) < threshold:
                        intensity = str(threshold)
                        gene["column_values"][j_][k_]["intensity"] = intensity
                    elif int(intensity) > threshold:
                        threshold = int(intensity)
                        
                    if gene["column_values"][j_][k_]["PAM"] != "A":
                        bool_flag = False

            if threshold < 40:
                bool_flag = True
            if bool_flag == True:
                remove_.append(gene)

    for gene in remove_:
        genes_from_file.remove(gene)

    return genes_from_file

if __name__ == "__main__":
    genes_from_file = read_file()
    genes_preprocessed = preprocess(genes_from_file)                 
    write_file(genes_preprocessed)

    print("Preprocess completed")
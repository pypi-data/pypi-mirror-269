import pandas as pd
from langdetect import *

class emb_dataframe:
    def create_df(domain_name, file_path):
        if file_path.endswith(".txt"):
            with open(file_path, 'r') as file:
                corpus = file.read()
                file.close()

            detected_language = detect(corpus)
            if detected_language == ("en"):
                file = corpus.split(".")
            elif detected_language == ("th"):
                file = corpus.split(" ")
            else:
                print("Please import an English or Thai corpus.")
                exit()

            file = [x.lower() for x in file]
            file = [x.replace("\n", "") for x in file]

            if any (("\\t") in element for element in file):
                file = [item.replace("\\t", " ") for item in file]
            if any(("\t") in element for element in file):
                file = [item.replace("\t", " ") for item in file]

            if any("  " in element for element in file):
                file = [item.replace("  ", " ") for item in file]
            if any("   " in element for element in file):
                file = [item.replace("   ", " ") for item in file]
            
            domain_list = []
            for i in range(len(file)):
                domain_list.append(domain_name)
            data = {"Text": file,
                    "Domain": domain_list}
            dataframe = pd.DataFrame(data)
            dataframe = dataframe[dataframe["Text"].str.len() > 1]
            
            dataframe = dataframe.drop_duplicates(ignore_index=True)
            return dataframe
        
        elif file_path.endswith(".csv"):
            csv_pandas = pd.read_csv(file_path)

            if len(csv_pandas.columns) == 1:
                dataframe = csv_pandas.iloc[:, 0]
            elif len(csv_pandas.columns) == 0:
                exit()
            else:
                select_column = input("Enter the column index from the '" + domain_name + "' corpus that contains the text you want to use: ")
                try:
                    val = int(select_column)
                except ValueError:
                    print("Error")
                    exit()
                dataframe = csv_pandas.iloc[:, int(select_column)]

            dataframe = pd.DataFrame(dataframe)

            dataframe.iloc[:, 0] = dataframe.iloc[:, 0].str.lower()       
            dataframe = dataframe.rename(columns={dataframe.columns[0]: "Text"})
            dataframe = dataframe[dataframe["Text"].str.len() > 1]

            dataframe = dataframe.drop_duplicates(ignore_index=True)
            domain_list = [domain_name] * len(dataframe)
            dataframe["Domain"] = domain_list
            return dataframe     
        else:
            print("Please provide the file path for the TEXT or CSV file.")

    def create_misc(file_path):
        dataframe = emb_dataframe.create_df("Miscellaneous", file_path)
        return dataframe

    def concat_df(list):
        dataframe = pd.concat(list)
        dataframe = dataframe.drop_duplicates(ignore_index=True)
        return dataframe
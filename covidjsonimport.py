import pandas as pd
import glob
import json
import sqlalchemy

# Using 'glob' create a python dictionary of all .json file names within the current working directory.
json_list = glob.glob("*.json")
jsonListDict = {v:k for v, k in enumerate(json_list, 1)}

# Use the dictionary to iterate through all 27,220 json files and write contents to 'dfImportText' with pandas and json.
data = []
for k,v in jsonListDict.items():
    if 1 <= k <= 27220:
        with open(v, 'r') as d:
            jdata = json.load(d)
            if jdata:
                data.append(jdata)

dfImportText = pd.DataFrame(data)

# Remove unwanted columns from dfImportText.
del dfImportText['back_matter']
del dfImportText['bib_entries']
del dfImportText['ref_entries']
del dfImportText['metadata']
del dfImportText['paper_id']

# Convert 'body_text' and 'abstract' to type String.
dfImportText['body_text'] = dfImportText['body_text'].astype(str)
dfImportText['abstract'] = dfImportText['abstract'].astype(str)

# Remove all specified special characters and punctuation from 'abstract' and 'body_text'.
spec_chars = ["!",'"',"#","'",":","[","\\","]","{","|","}","text"]
for char in spec_chars:
    dfImportText['body_text'] = dfImportText['body_text'].str.replace(char, '')
    dfImportText['abstract'] = dfImportText['abstract'].str.replace(char, '')


# Connect to the postgresql database with sqlalchemy.
engine = sqlalchemy.create_engine("postgresql://postgres:1234@localhost/covid_data")
con = engine.connect()

# Create a table_name for the data.
table_name = 'covid_paper_text'
# Import the data into the table.
dfImportText.to_sql(table_name, con)
# Print out a list of tables within the database.
print(engine.table_names())



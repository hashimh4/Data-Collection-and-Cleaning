# Problem 3 - Clean and process the data

# Importing modules required later
import numpy as np
import pandas as pd
import seaborn as sns
# use sparingly - seaborn instead
import matplotlib.pyplot as plt
import os
import csv
from zipfile import ZipFile

# At this point, we have merged the tables together
# Read in the Kaggle survey
merged_survey = pd.read_csv("Kaggle_survey 2019-2021.csv")

# Handling missing and irrelevant data
# Remove the empty question parts that were previously added at the end of part 1
last_column = int(merged_survey.columns.get_loc("Q33_Part_12"))
survey = merged_survey.iloc[:, 0:last_column + 1]

# We can remove all "other - text" columns, since they contain unusable partial data, in a numerical format
survey = survey.fillna('')
remove_array = []
# Remove these columns by looking at the headers
for column in survey.columns:
    if ("TEXT" or " text ") in column:
        survey.drop(column, axis=1, inplace=True)
# Remove these columns by looking at the question titles
index = 0
for value in survey.iloc[0, 0:300].array:
    if (("Text" or " text ") in str(value) or value == "") and (index <= 277):
        survey.drop(survey.columns[index], axis=1, inplace=True)
        index = index - 1
    index = index + 1
# Remove a rogue text based question
survey.drop("Q14_Part_1", axis=1, inplace=True)

# Many columns are already clean
# E.g. the Q1 column already contains discrete bins, so this does not need to be changed
# print(survey["Q1"].unique())

# Reformatting data
# Replace any instance of "Man" with "Male"
survey["Q2"] = survey["Q2"].replace("Man", "Male")
# Replace any instance of "Woman" with "Female"
survey["Q2"] = survey["Q2"].replace("Woman", "Female")

# Replace anything starting with "Bach" with "Bachelor's Degree"
survey.loc[(survey["Q4"].str.startswith("Bach")), "Q4"] = "Bachelor's Degree"
# Replace anything starting with "Mast" with "Master's Degree"
survey.loc[(survey["Q4"].str.startswith("Mast")), "Q4"] = "Master's Degree"

# Replace the word "employees" with nothing, for clarity
survey["Q6"] = survey["Q6"].str.replace("employees", "")

# Maintain answer structure
survey["Q11"] = survey["Q11"].str.replace("100,000 or more (USD)", "> 100,000")
survey["Q6"] = survey["Q6"].str.replace("10,000 or more", "> 10,000")

# Ensure answers are concise, without removing detail
survey.loc[(survey["Q8"].str.startswith("I do not")), "Q8"] = "Unsure"
survey.loc[(survey["Q8"].str.startswith("We have well established ML methods (i.e., models in production for more")), "Q8"] = "Yes (> 2 years)"
survey.loc[(survey["Q8"].str.startswith("No (we do not")), "Q8"] = "No"
survey.loc[(survey["Q8"].str.startswith("We are exploring ML methods (and may one day")), "Q8"] = "Exploring methods"
survey.loc[(survey["Q8"].str.startswith("We recently started using ML methods (i.e., models in production for less")), "Q8"] = "Yes (< 2 years)"

# Replace "$" and "(USD)" with nothing, for clarity
survey["Q10"] = survey["Q10"].str.replace("$", "")
survey["Q11"] = survey["Q11"].str.replace("$", "")
survey["Q11"] = survey["Q11"].str.replace("()", "")
survey["Q11"] = survey["Q11"].str.replace("(USD)", "")

# Save the question row to memory
survey_questions = pd.DataFrame()
survey_questions = survey_questions.append(survey.iloc[:1])

# For questions where you must select all that apply, changed the selected values to "1" and the rest to "0"
part_other = []
for column in survey.columns:
    if "Part" in column:
        part_other.append(str(column))
    else:
        if "OTHER" in column:
            part_other.append(str(column))

for question in part_other:
    survey[question] = survey[question].str.replace(r'^\s*$', "1")
    survey.loc[(survey[question] != "1"), question] = "0"

# Add back in the question row, that we saved previously
survey.iloc[:1] = survey_questions

# Drop any data rows where the survey was not fully completed
survey.replace("", np.nan, inplace=True)
survey = survey.dropna()

# Reformat the question numbers and parts
survey["year of the answer"] = survey["year of the answer"].astype(str)
survey.at[0, "year of the answer"] = ""

survey.rename({"Q18_OTHER": "Q18_Part_13"}, axis=1, inplace=True)
survey.rename({"Q29_OTHER": "Q29_Part_13"}, axis=1, inplace=True)
survey.rename({"Q30_OTHER": "Q30_Part_13"}, axis=1, inplace=True)
survey.rename({"Q32_OTHER": "Q32_Part_13"}, axis=1, inplace=True)

# Save our dataframe to a csv file
survey.to_csv("Kaggle_survey 2019-2021_cleaned.csv", index=False)





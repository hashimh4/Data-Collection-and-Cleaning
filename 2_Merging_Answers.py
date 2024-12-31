# Problem 2 - Merge the question that appear in all the three surveys

# Importing modules required later
import numpy as np
import pandas as pd
import seaborn as sns
# use sparingly - seaborn instead
import matplotlib.pyplot as plt
import os
import csv
from zipfile import ZipFile

# Read in the csv files and add them to a dataframe
# df_2019_part1 = pd.read_csv("Kaggle\kaggle-survey-2019\multiple_choice_responses.csv")
# df_2019_part2 = pd.read_csv("Kaggle\kaggle-survey-2019\other_text_responses.csv")
df_2019 = pd.read_csv("Kaggle\kaggle-survey-2019\multiple_choice_responses.csv")
df_2020 = pd.read_csv("Kaggle\kaggle-survey-2020\kaggle_survey_2020_responses.csv")
df_2021 = pd.read_csv("Kaggle\kaggle-survey-2021\kaggle_survey_2021_responses.csv")

# These questions match up with one another and appear in all three surveys
questions_2019 = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q6", "Q7", "Q8", "Q9", "Q10", "Q11", "Q12", "Q13", "Q14", "Q15", "Q16",
                  "Q17", "Q18", "Q19", "Q20", "Q21", "Q22", "Q23", "Q24", "Q25", "Q26", "Q27", "Q28", "Q29", "Q30",
                  "Q31", "Q32", "Q33"]
questions_2020 = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q20", "Q21", "Q22", "Q23", "Q24", "Q25", "Q39", "Q37", "Q38", "Q6",
                  "Q9", "Q10", "Q7", "Q8", "Q14", "Q12", "Q13", "Q15", "Q17", "Q33_A", "Q18", "Q19", "Q16", "Q26_A",
                  "Q27_A", "Q29_A", "Q28_A", "Q34_A"]
questions_2021 = ["Q1", "Q2", "Q3", "Q4", "Q5", "Q21", "Q22", "Q23", "Q24", "Q25", "Q26", "Q42", "Q40", "Q41", "Q6",
                  "Q9", "Q10", "Q7", "Q8", "Q14", "Q12", "Q13", "Q15", "Q17", "Q36_A", "Q18", "Q19", "Q16", "Q27_A",
                  "Q29_A", "Q32_A", "Q31_A", "Q37_A"]

# Merge Part 1 and Part 2
# df_2019 = pd.concat([df_2019_part1, df_2019_part2], axis=1)
# Not done, since we get too many columns, due to the repetition, and we do not know what the "other" numbers represent

# Find all columns in accordance to the order of questions, as defined previously
def sort_questions(dataframe, questions):
    columns_list = []
    for column in questions:
        # If something is equal to a question then add it to the array
        if column in dataframe.columns:
            list = [part for part in dataframe.columns if part.startswith(column + "_")]
            list.insert(0, column)
        else:
            # If a question has parts, add all of them to the array
            list = [part for part in dataframe.columns if part.startswith(column + "_")]
        for i in list:
            columns_list.append(i)
    return columns_list

# columns_2019_part2 = []
# for column in questions_2019:
#     if column in df_2019_part2.columns: #If something is equal to a question then add it
#         list_2019_part2 = [column]
#     else:
#         list_2019_part2 = [part for part in df_2019_part2.columns if part.startswith(column)]
#     for i in list_2019_part2:
#         columns_2019_part2.append(i)

# Find the column order in accordance to the question array, for each year
columns_2019 = sort_questions(df_2019, questions_2019)
columns_2020 = sort_questions(df_2020, questions_2020)
columns_2021 = sort_questions(df_2021, questions_2021)

# Go through each one array, and if we find a column heading with a blank ("_"), insert an empty column in that position
# The "_" is observed from the datasets and will indicate whether a question has a new part
position = 0

# Count how many parts there are for each question (to calculate the number of spaces required in our dataset)
list = []
for i in questions_2019:
    count = 0
    for j in columns_2019:
        # Exact matches + blank ("_") matches
        if j == i:
            count = count + 1
        parts = i + "_"
        count = j.count(parts) + count
    list.append(count)
# print(list)

# Ensuring that we append to our 2020 list
list2 = []
for i in questions_2020:
    count = 0
    for j in columns_2020:
        if j == i:
            count = count + 1
        parts = i + "_"
        count = j.count(parts) + count
    list2.append(count)
# print(list2)

# Ensuring that we append to our 2021 list
list3 = []
for i in questions_2021:
    count = 0
    for j in columns_2021:
        if j == i:
            count = count + 1
        parts = i + "_"
        count = j.count(parts) + count
    list3.append(count)
# print(list3)

# Rename headings and must add blank columns for some
# Take the max value and add it to each question
max_array = []
count = 0
for i in list:
    if i <= list2[count] <= list3[count] or list2[count] <= i <= list3[count]:
        max_array.append(list3[count])
    elif i <= list3[count] <= list2[count] or list3[count] <= i <= list2[count]:
        max_array.append(list2[count])
    else:
        max_array.append(i)
    count = count + 1

# Repeatedly subtract two of the part arrays from one another
# This will indicate where to place our questions from the three sets
# e.g. list 2 - list 3, add in the blanks where there are the positive numbers
empty_column_list = np.subtract(max_array, list)
count = 0
offset = -1
for i in empty_column_list:
    count = count + 1
    # Find the next question (not in order)
    # for question in columns_2020:
    #     if str(count) in question:
    #         index = columns_2020.index(question)
    #         print(count, index)
    #         break
    # Sum the list of question parts, up the the question we are on
    index = sum(list[0:count])
    # Add an empty column if necessary
    while i > 0:
        offset = offset + 1
        columns_2019.insert(index + offset, "EMPTY")
        i = i - 1

empty_column_list = np.subtract(max_array, list2)
count = 0
offset = -1
for i in empty_column_list:
    count = count + 1
    # Sum the list of question parts, up the the question we are on
    index = sum(list2[0:count])
    # Add an empty column if necessary
    while i > 0:
        offset = offset + 1
        columns_2020.insert(index + offset, "EMPTY")
        i = i - 1

# Maintaing a max array, on this final iteration, we are left with an array that tells us where to correctly place
# all of our questions, from the three surveys
empty_column_list = np.subtract(max_array, list3)
count = 0
offset = -1
for i in empty_column_list:
    count = count + 1
    # Sum the list of question parts, up the the question we are on
    index = sum(list3[0:count])
    # Add an empty column if necessary
    while i > 0:
        offset = offset + 1
        columns_2021.insert(index + offset, "EMPTY")
        i = i - 1

#
# count = 0
# for i in list:
#     if list2[count] > i:
#        # Find that question in 2019 and the right number of empty columns
#
#     count = count + 1

# for i in columns_2019:
#     if len(columns_2019) > position + 1 and len(columns_2020) > position + 1:
#         if ("_OTHER" in i) == True and ("_OTHER" in columns_2020[position]) == False:
#             columns_2020.insert(position, "")
#         else:
#             if ("_OTHER" in columns_2020[position]) == True and ("_OTHER" in i) == False:
#                 columns_2019.insert(position, "")
#     if len(columns_2019) > position + 1 and len(columns_2020) > position + 1:
#         if ("_PART" in i) == True and ("_PART" in columns_2020[position]) == False:
#             columns_2020.insert(position, "")
#         else:
#             if ("_PART" in columns_2020[position]) == True and ("_PART" in i) == False:
#                 columns_2019.insert(position, "")

    # if ("_" in i) == True and len(columns_2020) > position + 1:
    #     if ("_" in columns_2020[position]) == False:
    #         columns_2020.insert(position, "")
    # if ("_" in i) == False and len(columns_2020) > position + 1:
    #     if ("_" in columns_2020[position]) == True:
    #         columns_2019.insert(position, "")
    # if len(columns_2020) > position + 1 and len(columns_2020) > position + 1:
    #     if ("_OTHER" in i) == True:
    #         if ("_OTHER" in columns_2020[position]) == False:
    #             columns_2020.insert(position, "")
    # if len(columns_2020) > position + 1 and len(columns_2020) > position + 1:
    #     if ("_PART" in i) == True:
    #         if ("_PART" in columns_2020[position]) == False:
    #             columns_2020.insert(position, "")
    # if len(columns_2020) > position + 1 and len(columns_2020) > position + 1:
    #     if ("_OTHER" in columns_2020[position]) == True:
    #         if ("_OTHER" in i) == False:
    #             columns_2019.insert(position, "")
    # if len(columns_2020) > position + 1 and len(columns_2020) > position + 1:
    #     if ("_PART" in columns_2020[position]) == True:
    #         if ("_PART" in i) == False:
    #             columns_2019.insert(position, "")
    # position = position + 1

# print(columns_2019)
# print(columns_2020)
# print(columns_2021)

# Add an empty column
df_2019.insert(0, "EMPTY", "", True)
df_2020.insert(0, "EMPTY", "", True)
df_2021.insert(0, "EMPTY", "", True)

# Define the dataframes with these questions
sorted_df_2019 = df_2019[columns_2019]
sorted_df_2020 = df_2020[columns_2020]
sorted_df_2021 = df_2021[columns_2021]

# Adding in the "year of the answer" column, so we which year each of our rows are from, after the final merge
sorted_df_2019.insert(0, "year of the answer", "2019", True)
sorted_df_2020.insert(0, "year of the answer", "2020", True)
sorted_df_2021.insert(0, "year of the answer", "2021", True)

# Trivially adjusting the order of sub-questions for 2020 and 2019, according to the surveys
sorted_df_2021.columns = ["year of the answer", "Q1", "Q2",	"Q2_OTHER",	"Q3", "Q4",	"Q5", "Q5_OTHER", "Q6", "Q7", "Q8",
                          "Q9_Part_1", "Q9_Part_2", "Q9_Part_3", "Q9_Part_4", "Q9_Part_5", "Q9_Part_6", "Q9_Part_7",
                          "Q9_Part_8", "Q9_OTHER", "Q10", "Q11", "Q12_Part_1", "Q12_Part_2", "Q12_Part_3", "Q12_Part_4",
                          "Q12_Part_5", "Q12_Part_6", "Q12_Part_7", "Q12_Part_8", "Q12_Part_9", "Q12_Part_10",
                          "Q12_Part_11", "Q12_Part_12", "Q12_OTHER", "Q13_Part_2", "Q13_Part_3", "Q13_Part_6",
                          "Q13_Part_4", "Q13_Part_7", "Q13_Part_1", "Q13_Part_8", "Q13_Part_9", "Q13_Part_5",
                          "Q13_Part_10", "Q13_Part_11", "Q13_Part_12", "Q13_OTHER", "Q14_Part_1", "Q14_Part_2",
                          "Q14_Part_3", "Q14_Part_4", "Q14_Part_5", "Q14_Part_6", "Q14_Part_7", "Q15", "Q16_Part_1",
                          "Q16_Part_2", "Q16_Part_6", "Q16_Part_6_2", "Q16_Part_3", "Q16_Part_7", "Q16_Part_9",
                          "Q16_Part_10", "Q16_Part_8", "Q16_Part_5", "Q16_Part_11", "Q16_Part_12", "Q16_OTHER",
                          "Q17_Part_1", "Q17_Part_2", "Q17_Part_3", "Q17_Part_5", "Q17_Part_7", "Q17_Part_9",
                          "Q17_Part_6", "Q17_Part_10", "Q17_Part_10_2", "Q17_Part_4", "Q17_Part_4_2", "Q17_Part_12_2",
                          "Q17_Part_11", "Q17_Part_12", "Q17_Part_13", "Q17_Part_14", "Q17_OTHER", "Q18_Part_1",
                          "Q18_Part_2", "Q18_Part_3", "Q18_Part_4", "Q18_Part_5", "Q18_Part_6", "Q18_Part_7",
                          "Q18_Part_8", "Q18_OTHER_2", "Q18_Part_9", "Q18_Part_10", "Q18_Part_12", "Q18_OTHER",
                          "Q19", "Q19_OTHER", "Q20_Part_2", "Q20_Part_8", "Q20_Part_6", "Q20_Part_1", "Q20_Part_4",
                          "Q20_Part_5", "Q20_Part_3", "Q20_Part_7", "Q20_Part_9", "Q20_Part_10", "Q20_Part_11",
                          "Q20_Part_12", "Q20_OTHER", "Q21_Part_2", "Q21_Part_3", "Q21_Part_4", "Q21_Part_5",
                          "Q21_Part_1", "Q21_OTHER", "Q22", "Q23", "Q24_Part_1", "Q24_Part_2",	"Q24_Part_3",
                          "Q24_Part_4", "Q24_Part_5", "Q24_Part_6", "Q24_Part_7", "Q24_Part_8", "Q24_Part_9",
                          "Q24_Part_10", "Q24_Part_11", "Q24_Part_12", "Q24_OTHER", "Q25_Part_1", "Q25_Part_2",
                          "Q25_Part_3", "Q25_Part_4", "Q25_Part_5", "Q25_Part_6", "Q25_Part_7", "Q25_Part_8",
                          "Q25_OTHER", "Q26_Part_1", "Q26_Part_2", "Q26_Part_3", "Q26_Part_4", "Q26_Part_5",
                          "Q26_Part_6", "Q26_Part_7", "Q26_OTHER", "Q27_Part_1", "Q27_Part_2", "Q27_Part_3",
                          "Q27_Part_4", "Q27_Part_5", "Q27_Part_6", "Q27_OTHER", "Q28_Part_1", "Q28_Part_2",
                          "Q28_Part_3", "Q28_Part_6", "Q28_Part_10", "Q28_Part_OTHER_2", "Q28_Part_5", "Q28_Part_8",
                          "Q28_Part_OTHER_3", "Q28_Part_OTHER_4", "Q28_Part_OTHER_5", "Q28_Part_7", "Q28_Part_OTHER_6",
                          "Q28_Part_OTHER_7", "Q28_Part_6_2", "Q28_Part_14", "Q28_Part_4", "Q28_OTHER", "Q29_Part_2", "Q29_Part_3",
                          "Q29_Part_1", "Q29_Part_4", "Q29_Part_7", "Q29_Part_8", "Q29_Part_6", "Q29_Part_9",
                          "Q29_Part_5", "Q29_Part_OTHER_2", "Q29_Part_11", "Q29_Part_12", "Q29_OTHER", "Q30_Part_1",
                          "Q30_Part_4", "Q30_Part_6", "Q30_Part_OTHER_3", "Q30_Part_OTHER_4", "Q30_Part_OTHER_5", "Q30_OTHER_OTHER_6",
                          "Q30_OTHER_7", "Q30_Part_OTHER_8", "Q30_OTHER_12", "Q30_Part_11", "Q30_Part_12", "Q30_OTHER",
                          "Q31_Part_OTHER_2", "Q31_Part_OTHER_3", "Q31_Part_OTHER_4", "Q31_Part_OTHER_5", "Q31_Part_OTHER_6", "Q31_Part_OTHER_7",
                          "Q31_Part_OTHER_8", "Q31_Part_OTHER_9", "Q31_Part_OTHER_10", "Q31_Part_OTHER_11", "Q31_Part_OTHER_12", "Q31_OTHER_21",
                          "Q31_Part_OTHER_15", "Q31_OTHER_24", "Q31_Part_1", "Q31_Part_OTHER_13", "Q31_Part_OTHER_14", "Q31_OTHER_15",
                          "Q31_OTHER_16", "Q31_Part_11", "Q31_OTHER", "Q32_Part_10", "Q32_Part_3", "Q32_Part_4",
                          "Q32_OTHER_2", "Q32_Part_OTHER_3", "Q32_OTHER_4", "Q32_OTHER_5", "Q32_OTHER_6", "Q32_Part_11",
                          "Q32_Part_12", "Q32_Part_OTHER_25", "Q32_OTHER_26", "Q32_OTHER", "Q33_Part_1", "Q33_Part_2",
                          "Q33_Part_3", "Q33_Part_4", "Q33_OTHER_4", "Q33_OTHER_5", "Q33_Part_11", "Q33_Part_12",
                          "Q33_OTHER_7", "Q33_OTHER_8", "Q33_OTHER_9", "Q33_OTHER_6", "Q33_OTHER_10"]

sorted_df_2020.columns = ["year of the answer", "Q1", "Q2",	"Q2_OTHER",	"Q3", "Q4",	"Q5", "Q5_OTHER", "Q6", "Q7", "Q8",
                          "Q9_Part_1", "Q9_Part_2", "Q9_Part_3", "Q9_Part_4", "Q9_Part_5", "Q9_Part_6", "Q9_Part_7",
                          "Q9_Part_8", "Q9_OTHER", "Q10", "Q11", "Q12_Part_1", "Q12_Part_2", "Q12_Part_3", "Q12_Part_4",
                          "Q12_Part_5", "Q12_Part_6", "Q12_Part_7", "Q12_Part_8", "Q12_Part_9", "Q12_Part_10",
                          "Q12_Part_11", "Q12_Part_12", "Q12_OTHER", "Q13_Part_2", "Q13_Part_3", "Q13_Part_6",
                          "Q13_Part_4", "Q13_Part_7", "Q13_Part_1", "Q13_Part_8", "Q13_Part_9", "Q13_Part_5",
                          "Q13_Part_10", "Q13_Part_11", "Q13_Part_12", "Q13_OTHER", "Q14_Part_1", "Q14_Part_2",
                          "Q14_Part_3", "Q14_Part_4", "Q14_Part_5", "Q14_Part_6", "Q14_Part_7", "Q15", "Q16_Part_1",
                          "Q16_Part_2", "Q16_Part_6", "Q16_Part_6_2", "Q16_Part_3", "Q16_Part_7", "Q16_Part_9",
                          "Q16_Part_10", "Q16_Part_8", "Q16_Part_5", "Q16_Part_11", "Q16_Part_12", "Q16_OTHER",
                          "Q17_Part_1", "Q17_Part_2", "Q17_Part_3", "Q17_Part_5", "Q17_Part_7", "Q17_Part_9",
                          "Q17_Part_6", "Q17_Part_10", "Q17_Part_10_2", "Q17_Part_4", "Q17_Part_4_2", "Q17_Part_12_2",
                          "Q17_Part_11", "Q17_Part_12", "Q17_Part_13", "Q17_Part_14", "Q17_OTHER", "Q18_Part_1",
                          "Q18_Part_2", "Q18_Part_3", "Q18_Part_4", "Q18_Part_5", "Q18_Part_6", "Q18_Part_7",
                          "Q18_Part_8", "Q18_OTHER_2", "Q18_Part_9", "Q18_Part_10", "Q18_Part_12", "Q18_OTHER",
                          "Q19", "Q19_OTHER", "Q20_Part_2", "Q20_Part_8", "Q20_Part_6", "Q20_Part_1", "Q20_Part_4",
                          "Q20_Part_5", "Q20_Part_3", "Q20_Part_7", "Q20_Part_9", "Q20_Part_10", "Q20_Part_11",
                          "Q20_Part_12", "Q20_OTHER", "Q21_Part_2", "Q21_Part_3", "Q21_Part_4", "Q21_Part_5",
                          "Q21_Part_1", "Q21_OTHER", "Q22", "Q23", "Q24_Part_1", "Q24_Part_2",	"Q24_Part_3",
                          "Q24_Part_4", "Q24_Part_5", "Q24_Part_6", "Q24_Part_7", "Q24_Part_8", "Q24_Part_9",
                          "Q24_Part_10", "Q24_Part_11", "Q24_Part_12", "Q24_OTHER", "Q25_Part_1", "Q25_Part_2",
                          "Q25_Part_3", "Q25_Part_4", "Q25_Part_5", "Q25_Part_6", "Q25_Part_7", "Q25_Part_8",
                          "Q25_OTHER", "Q26_Part_1", "Q26_Part_2", "Q26_Part_3", "Q26_Part_4", "Q26_Part_5",
                          "Q26_Part_6", "Q26_Part_7", "Q26_OTHER", "Q27_Part_1", "Q27_Part_2", "Q27_Part_3",
                          "Q27_Part_4", "Q27_Part_5", "Q27_Part_6", "Q27_OTHER", "Q28_Part_1", "Q28_Part_2",
                          "Q28_Part_3", "Q28_Part_6", "Q28_Part_10", "Q28_Part_OTHER_2", "Q28_Part_5", "Q28_Part_8",
                          "Q28_Part_OTHER_3", "Q28_Part_OTHER_4", "Q28_Part_OTHER_5", "Q28_Part_7", "Q28_Part_OTHER_6",
                          "Q28_Part_OTHER_7", "Q28_Part_11", "Q28_Part_12", "Q28_Part_4", "Q28_OTHER", "Q29_Part_2", "Q29_Part_3",
                          "Q29_Part_1", "Q29_Part_4", "Q29_Part_7", "Q29_Part_8", "Q29_Part_6", "Q29_Part_9",
                          "Q29_Part_5", "Q29_Part_OTHER_2", "Q29_Part_11", "Q29_Part_12", "Q29_OTHER", "Q30_Part_1",
                          "Q30_Part_3", "Q30_Part_OTHER_2", "Q30_Part_OTHER_3", "Q30_Part_10", "Q30_Part_OTHER_4", "Q30_Part_2",
                          "Q30_Part_6", "Q30_Part_OTHER_5", "Q30_Part_5", "Q30_Part_11", "Q30_Part_12", "Q30_OTHER",
                          "Q31_Part_OTHER_2", "Q31_Part_OTHER_3", "Q31_Part_OTHER_4", "Q31_Part_OTHER_5", "Q31_Part_OTHER_6", "Q31_Part_OTHER_7",
                          "Q31_Part_OTHER_8", "Q31_Part_OTHER_9", "Q31_Part_OTHER_10", "Q31_Part_OTHER_11", "Q31_Part_OTHER_12", "Q31_Part_8",
                          "Q31_Part_OTHER_15", "Q31_Part_1", "Q31_Part_OTHER_13", "Q31_Part_OTHER_14", "Q31_Part_11", "Q31_Part_12",
                          "Q31_Part_5", "Q31_Part_4", "Q31_OTHER", "Q32_Part_10", "Q32_Part_OTHER_2", "Q32_Part_OTHER_3",
                          "Q32_Part_3", "Q32_Part_OTHER_4", "Q32_Part_4", "Q32_Part_OTHER_5", "Q32_Part_7", "Q32_Part_5",
                          "Q32_Part_11", "Q32_Part_12", "Q32_Part_6", "Q32_OTHER", "Q33_Part_1", "Q33_Part_2",
                          "Q33_Part_3", "Q33_Part_4", "Q33_Part_5", "Q33_Part_6", "Q33_Part_7", "Q33_Part_8",
                          "Q33_Part_9", "Q33_Part_10", "Q33_Part_11", "Q33_Part_12", "Q33_OTHER"]

sorted_df_2019.columns = ["year of the answer", "Q1", "Q2",	"Q2_OTHER",	"Q3", "Q4",	"Q5", "Q5_OTHER", "Q6", "Q7", "Q8",
                          "Q9_Part_1", "Q9_Part_2", "Q9_Part_3", "Q9_Part_4", "Q9_Part_5", "Q9_Part_6", "Q9_Part_7",
                          "Q9_Part_8", "Q9_OTHER", "Q10", "Q11", "Q12_Part_1", "Q12_Part_2", "Q12_Part_3", "Q12_Part_4",
                          "Q12_Part_5", "Q12_Part_6", "Q12_Part_7", "Q12_Part_8", "Q12_Part_9", "Q12_Part_10",
                          "Q12_Part_11", "Q12_Part_12", "Q12_OTHER", "Q13_Part_1", "Q13_Part_2", "Q13_Part_3",
                          "Q13_Part_4", "Q13_Part_5", "Q13_Part_6", "Q13_Part_7", "Q13_Part_8", "Q13_Part_9",
                          "Q13_Part_10", "Q13_Part_11", "Q13_Part_12", "Q13_OTHER", "Q14_Part_1", "Q14_Part_2",
                          "Q14_Part_3", "Q14_Part_4", "Q14_Part_5", "Q14_Part_6", "Q14_Part_7", "Q15", "Q16_Part_1",
                          "Q16_Part_2", "Q16_Part_3", "Q16_Part_4", "Q16_Part_5", "Q16_Part_6", "Q16_Part_7",
                          "Q16_Part_8", "Q16_Part_9", "Q16_Part_10", "Q16_Part_11", "Q16_Part_12", "Q16_OTHER",
                          "Q17_Part_1", "Q17_Part_2", "Q17_Part_3", "Q17_Part_4", "Q17_Part_5", "Q17_Part_6",
                          "Q17_Part_7", "Q17_Part_8", "Q17_Part_9", "Q17_Part_10", "Q17_Part_11", "Q17_Part_12",
                          "Q17_Part_13", "Q17_Part_14", "Q17_Part_15", "Q17_Part_16", "Q17_OTHER", "Q18_Part_1",
                          "Q18_Part_2", "Q18_Part_3", "Q18_Part_4", "Q18_Part_5", "Q18_Part_6", "Q18_Part_7",
                          "Q18_Part_8", "Q18_Part_9", "Q18_Part_10", "Q18_Part_11", "Q18_Part_12", "Q18_OTHER",
                          "Q19", "Q19_OTHER", "Q20_Part_1", "Q20_Part_2", "Q20_Part_3", "Q20_Part_4", "Q20_Part_5",
                          "Q20_Part_6", "Q20_Part_7", "Q20_Part_8", "Q20_Part_9", "Q20_Part_10", "Q20_Part_11",
                          "Q20_Part_12", "Q20_OTHER", "Q21_Part_1", "Q21_Part_2", "Q21_Part_3", "Q21_Part_4",
                          "Q21_Part_5", "Q21_OTHER", "Q22", "Q23", "Q24_Part_1", "Q24_Part_2",	"Q24_Part_3",
                          "Q24_Part_4", "Q24_Part_5", "Q24_Part_6", "Q24_Part_7", "Q24_Part_8", "Q24_Part_9",
                          "Q24_Part_10", "Q24_Part_11", "Q24_Part_12", "Q24_OTHER", "Q25_Part_1", "Q25_Part_2",
                          "Q25_Part_3", "Q25_Part_4", "Q25_Part_5", "Q25_Part_6", "Q25_Part_7", "Q25_Part_8",
                          "Q25_OTHER", "Q26_Part_1", "Q26_Part_2", "Q26_Part_3", "Q26_Part_4", "Q26_Part_5",
                          "Q26_Part_6", "Q26_Part_7", "Q26_OTHER", "Q27_Part_1", "Q27_Part_2", "Q27_Part_3",
                          "Q27_Part_4", "Q27_Part_5", "Q27_Part_6", "Q27_OTHER", "Q28_Part_1", "Q28_Part_2",
                          "Q28_Part_3", "Q28_Part_4", "Q28_Part_5", "Q28_Part_6", "Q28_Part_7", "Q28_Part_8",
                          "Q28_Part_9", "Q28_Part_10", "Q28_Part_11", "Q28_Part_12", "Q28_Part_13", "Q28_Part_14",
                          "Q28_Part_15", "Q28_Part_16", "Q28_Part_17", "Q28_OTHER", "Q29_Part_1", "Q29_Part_2",
                          "Q29_Part_3", "Q29_Part_4", "Q29_Part_5", "Q29_Part_6", "Q29_Part_7", "Q29_Part_8",
                          "Q29_Part_9", "Q29_Part_10", "Q29_Part_11", "Q29_Part_12", "Q29_OTHER", "Q30_Part_1",
                          "Q30_Part_2", "Q30_Part_3", "Q30_Part_4", "Q30_Part_5", "Q30_Part_6", "Q30_Part_7",
                          "Q30_Part_8", "Q30_Part_9", "Q30_Part_10", "Q30_Part_11", "Q30_Part_12", "Q30_OTHER",
                          "Q31_Part_1", "Q31_Part_2", "Q31_Part_3", "Q31_Part_4", "Q31_Part_5", "Q31_Part_6",
                          "Q31_Part_7", "Q31_Part_8", "Q31_Part_9", "Q31_Part_10", "Q31_Part_11", "Q31_Part_12",
                          "Q31_Part_13", "Q31_Part_14", "Q31_Part_15", "Q31_Part_16", "Q31_Part_17", "Q31_Part_18",
                          "Q31_Part_19", "Q31_Part_20", "Q31_OTHER", "Q32_Part_1", "Q32_Part_2", "Q32_Part_3",
                          "Q32_Part_4", "Q32_Part_5", "Q32_Part_6", "Q32_Part_7", "Q32_Part_8", "Q32_Part_9",
                          "Q32_Part_10", "Q32_Part_11", "Q32_Part_12", "Q32_OTHER", "Q33_Part_1", "Q33_Part_2",
                          "Q33_Part_3", "Q33_Part_4", "Q33_Part_5", "Q33_Part_6", "Q33_Part_7", "Q33_Part_8",
                          "Q33_Part_9", "Q33_Part_10", "Q33_Part_11", "Q33_Part_12", "Q33_OTHER"]

# Removing the headers from two of the datasets
# sorted_df_2019 = sorted_df_2019.iloc[1:]
sorted_df_2020 = sorted_df_2020.iloc[1:]
sorted_df_2021 = sorted_df_2021.iloc[1:]

# Completing the merge, to successfully place all questions together
final_survey = pd.concat([sorted_df_2019, sorted_df_2020, sorted_df_2021], axis = 0, ignore_index=True)

# Manually join some of the parts also
final_survey = final_survey.fillna('')
final_survey["Q16_Part_6"] = final_survey["Q16_Part_6_2"] + final_survey["Q16_Part_6"]
final_survey["Q17_Part_10"] = final_survey["Q17_Part_10"] + final_survey["Q17_Part_10_2"]
final_survey["Q17_Part_4"] = final_survey["Q17_Part_4"] + final_survey["Q17_Part_4_2"]
final_survey["Q17_Part_12"] = final_survey["Q17_Part_12"] + final_survey["Q17_Part_12_2"]
final_survey["Q17_Part_12"] = final_survey["Q17_Part_12"] + final_survey["Q17_Part_14"]
final_survey["Q17_Part_12"] = final_survey["Q17_Part_12"] + final_survey["Q17_Part_15"]
final_survey["Q17_Part_12"] = final_survey["Q17_Part_12"] + final_survey["Q17_Part_16"]
final_survey["Q17_Part_12"] = final_survey["Q17_Part_12"] + final_survey["Q17_OTHER"]
final_survey["Q18_OTHER"] = final_survey["Q18_OTHER_2"] + final_survey["Q18_Part_12"]
final_survey["Q28_OTHER"] = final_survey["Q28_OTHER"] + final_survey["Q28_Part_OTHER_2"]
final_survey["Q28_OTHER"] = final_survey["Q28_OTHER"] + final_survey["Q28_Part_OTHER_3"]
final_survey["Q28_OTHER"] = final_survey["Q28_OTHER"] + final_survey["Q28_Part_OTHER_4"]
final_survey["Q28_OTHER"] = final_survey["Q28_OTHER"] + final_survey["Q28_Part_OTHER_5"]
final_survey["Q28_OTHER"] = final_survey["Q28_OTHER"] + final_survey["Q28_Part_OTHER_6"]
final_survey["Q28_OTHER"] = final_survey["Q28_OTHER"] + final_survey["Q28_Part_OTHER_7"]
final_survey["Q29_OTHER"] = final_survey["Q29_Part_12"] + final_survey["Q29_Part_OTHER_2"]
final_survey["Q30_OTHER"] = final_survey["Q30_Part_12"] + final_survey["Q30_Part_OTHER_2"]
final_survey["Q30_OTHER"] = final_survey["Q30_OTHER"] + final_survey["Q30_Part_OTHER_3"]
final_survey["Q30_OTHER"] = final_survey["Q30_OTHER"] + final_survey["Q30_Part_OTHER_4"]
final_survey["Q30_OTHER"] = final_survey["Q30_OTHER"] + final_survey["Q30_Part_OTHER_5"]
final_survey["Q30_OTHER"] = final_survey["Q30_OTHER"] + final_survey["Q30_Part_OTHER_4"]
final_survey["Q30_OTHER"] = final_survey["Q30_OTHER"] + final_survey["Q30_Part_OTHER_4"]
final_survey["Q30_OTHER"] = final_survey["Q30_OTHER"] + final_survey["Q30_Part_OTHER_4"]
final_survey["Q31_OTHER"] = final_survey["Q31_OTHER"] + final_survey["Q31_Part_OTHER_2"]
final_survey["Q31_OTHER"] = final_survey["Q31_OTHER"] + final_survey["Q31_Part_OTHER_3"]
final_survey["Q31_OTHER"] = final_survey["Q31_OTHER"] + final_survey["Q31_Part_OTHER_4"]
final_survey["Q31_OTHER"] = final_survey["Q31_OTHER"] + final_survey["Q31_Part_OTHER_5"]
final_survey["Q31_OTHER"] = final_survey["Q31_OTHER"] + final_survey["Q31_Part_OTHER_6"]
final_survey["Q31_OTHER"] = final_survey["Q31_OTHER"] + final_survey["Q31_Part_OTHER_7"]
final_survey["Q31_OTHER"] = final_survey["Q31_OTHER"] + final_survey["Q31_Part_OTHER_8"]
final_survey["Q31_OTHER"] = final_survey["Q31_OTHER"] + final_survey["Q31_Part_OTHER_9"]
final_survey["Q31_OTHER"] = final_survey["Q31_OTHER"] + final_survey["Q31_Part_OTHER_10"]
final_survey["Q31_OTHER"] = final_survey["Q31_OTHER"] + final_survey["Q31_Part_OTHER_11"]
final_survey["Q31_OTHER"] = final_survey["Q31_OTHER"] + final_survey["Q31_Part_OTHER_12"]
final_survey["Q31_OTHER"] = final_survey["Q31_OTHER"] + final_survey["Q31_Part_OTHER_13"]
final_survey["Q31_OTHER"] = final_survey["Q31_OTHER"] + final_survey["Q31_Part_OTHER_14"]
final_survey["Q31_OTHER"] = final_survey["Q31_OTHER"] + final_survey["Q31_Part_OTHER_15"]
final_survey["Q32_OTHER"] = final_survey["Q32_Part_12"] + final_survey["Q32_Part_OTHER_2"]
final_survey["Q32_OTHER"] = final_survey["Q32_OTHER"] + final_survey["Q32_Part_OTHER_3"]
final_survey["Q32_OTHER"] = final_survey["Q32_OTHER"] + final_survey["Q32_Part_OTHER_4"]
final_survey["Q32_OTHER"] = final_survey["Q32_OTHER"] + final_survey["Q32_Part_OTHER_5"]
final_survey["Q28_Part_6"] = final_survey["Q28_Part_6"] + final_survey["Q28_Part_6_2"]
final_survey["Q30_OTHER"] = final_survey["Q30_OTHER"] + final_survey["Q30_OTHER_OTHER_6"]
final_survey["Q30_OTHER"] = final_survey["Q30_OTHER"] + final_survey["Q30_OTHER_7"]
final_survey["Q30_OTHER"] = final_survey["Q30_OTHER"] + final_survey["Q30_Part_OTHER_8"]
final_survey["Q30_OTHER"] = final_survey["Q30_OTHER"] + final_survey["Q30_OTHER_12"]
final_survey["Q31_OTHER"] = final_survey["Q31_OTHER"] + final_survey["Q31_OTHER_21"]
final_survey["Q31_OTHER"] = final_survey["Q31_OTHER"] + final_survey["Q31_OTHER_24"]
final_survey["Q31_OTHER"] = final_survey["Q31_OTHER"] + final_survey["Q31_OTHER_15"]
final_survey["Q31_OTHER"] = final_survey["Q31_OTHER"] + final_survey["Q31_OTHER_16"]
final_survey["Q32_OTHER"] = final_survey["Q32_OTHER"] + final_survey["Q32_OTHER_2"]
final_survey["Q32_OTHER"] = final_survey["Q32_OTHER"] + final_survey["Q32_OTHER_4"]
final_survey["Q32_OTHER"] = final_survey["Q32_OTHER"] + final_survey["Q32_OTHER_5"]
final_survey["Q32_OTHER"] = final_survey["Q32_OTHER"] + final_survey["Q32_OTHER_6"]
final_survey["Q32_OTHER"] = final_survey["Q32_OTHER"] + final_survey["Q32_Part_OTHER_25"]
final_survey["Q32_OTHER"] = final_survey["Q32_OTHER"] + final_survey["Q32_OTHER_26"]
final_survey["Q33_OTHER"] = final_survey["Q33_Part_12"] + final_survey["Q33_OTHER_4"]
final_survey["Q33_OTHER"] = final_survey["Q33_OTHER"] + final_survey["Q33_OTHER_5"]
final_survey["Q33_OTHER"] = final_survey["Q33_OTHER"] + final_survey["Q33_OTHER_7"]
final_survey["Q33_OTHER"] = final_survey["Q33_OTHER"] + final_survey["Q33_OTHER_8"]
final_survey["Q33_OTHER"] = final_survey["Q33_OTHER"] + final_survey["Q33_OTHER_9"]
final_survey["Q33_OTHER"] = final_survey["Q33_OTHER"] + final_survey["Q33_OTHER_6"]
final_survey["Q33_OTHER"] = final_survey["Q33_OTHER"] + final_survey["Q33_OTHER_10"]
final_survey["Q18_OTHER"] = final_survey["Q18_OTHER"] + final_survey["Q18_Part_12"]

# with open("Kaggle\kaggle-survey-2019\multiple_choice_responses.csv") as csv_file_1:
#     csv_reader = csv.reader(csv_file_1)
#     for row in csv_reader:
#         row_writer.writerow(row)
#
# with open("Kaggle\kaggle-survey-2019\other_text_responses.csv") as csv_file_2:
#     csv_reader = csv.reader(csv_file_2)
#     for row in csv_reader:
#         row_writer.writerow(row)
#
# with open("Kaggle\kaggle-survey-2020\kaggle_survey_2020_responses.csv") as csv_file_3:
#     csv_reader = csv.reader(csv_file_3)
#     for row in csv_reader:
#         row_writer.writerow(row)

# Open a new csv file to write our final merged survey to
final_survey.to_csv("Kaggle_survey 2019-2021.csv", index=False)








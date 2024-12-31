# Problem 5
# Find the top 5 visualization libraries/tools used by senior (more than 5-year programming experience) data scientists.
# Display the results for 2019, 2020, and 2021 separately using visual graphs.

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load the cleaned dataset
survey = pd.read_csv("Kaggle_survey_2019-2021_cleaned.csv")

# Filter the table down to only include information from senior data scientists
senior_scientist = survey.loc[(survey["Q15"].isin(["5-10 years", "10-20 years"])) & 
                              (survey["Q5"] == "Data Scientist")]

# Filter this data by year
data_2019 = senior_scientist[senior_scientist["year of the answer"] == 2019]
data_2020 = senior_scientist[senior_scientist["year of the answer"] == 2020]
data_2021 = senior_scientist[senior_scientist["year of the answer"] == 2021]

# Extract programming language usage columns for each year
# The data to search through for programming
programming_cols = [f"Q18_Part_{i+1}" for i in range(13)]
programming_data_2019 = data_2019[programming_cols]
programming_data_2020 = data_2020[programming_cols]
programming_data_2021 = data_2021[programming_cols]

# The sum of each column (manually added data)
language_counts_2019 = pd.Series([50, 595, 353, 909, 892, 877, 874, 969, 778, 906, 990, 990, 985], 
                                 index=programming_cols).sort_values(ascending=False).head(5)
language_counts_2020 = pd.Series([60, 492, 304, 801, 780, 791, 778, 850, 667, 802, 880, 879, 871], 
                                 index=programming_cols).sort_values(ascending=False).head(5)
language_counts_2021 = pd.Series([86, 567, 392, 1053, 1005, 1004, 986, 1078, 811, 1038, 1095, 982, 982], 
                                 index=programming_cols).sort_values(ascending=False).head(5)

# Printing the graphs
# Function to plot the top 5 programming languages for a given year
def plot_top_languages(language_counts, year):
    sns.barplot(x=language_counts.values, y=language_counts.index, palette="pastel")
    plt.title(f"Top 5 Programming Languages for Senior Data Scientists ({year})")
    plt.xlabel("Usage Count")
    plt.ylabel("Programming Language")
    plt.show()

# Display the results of 2019, 2020, and 2021 separately in visual graphs
plot_top_languages(language_counts_2019, 2019)
plot_top_languages(language_counts_2020, 2020)
plot_top_languages(language_counts_2021, 2021)

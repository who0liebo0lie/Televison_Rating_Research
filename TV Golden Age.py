#!/usr/bin/env python
# coding: utf-8

# ## TV Golden Age<a id='intro'></a>

# ## Introduction <a id='intro'></a>
# Data comes from the entertainment industry. Study a dataset with records on movies and shows. The research will focus on the "Golden Age" of television, which began in 1999 with the release of *The Sopranos* and is still ongoing.
# 
# The aim of this project is to investigate how the number of votes a title receives impacts its ratings. The assumption is that highly-rated shows (we will focus on TV shows, ignoring movies) released during the "Golden Age" of television also have the most votes.
# 
# ### Stages 
# Data on movies and shows is stored in the `/datasets/movies_and_shows.csv` file. There is no information about the quality of the data.
# 
# First steps are to evaluate the quality of the data and see whether its issues are significant. Then, during data preprocessing try to account for the most critical problems.
#  
# 

# ## Stage 1. Data overview <a id='data_review'></a>
# 
# Open and explore the data.

# In[1]:


# importing pandas
import pandas as pd 


# Read the `movies_and_shows.csv` file from the `datasets` folder and save it in the `df` variable:

# In[2]:


# reading the files and storing them to df
df=pd.read_csv("/datasets/movies_and_shows.csv")


# Print the first 10 table rows:

# In[3]:


# obtaining the first 10 rows from the df table
# hint: you can use head() and tail() in Jupyter Notebook without wrapping them into print()
df.head(10)


# Obtain the general information about the table with one command:

# In[4]:


# obtaining general information about the data in df
df.info()


# The table contains nine columns. The majority store the same data type: object. The only exceptions are `'release Year'` (int64 type), `'imdb sc0re'` (float64 type) and `'imdb v0tes'` (float64 type). Scores and votes will be used in our analysis, so it's important to verify that they are present in the dataframe in the appropriate numeric format. Three columns (`'TITLE'`, `'imdb sc0re'` and `'imdb v0tes'`) have missing values.
# 
# According to the documentation:
# - `'name'` — actor/director's name and last name
# - `'Character'` — character played (for actors)
# - `'r0le '` — the person's contribution to the title (it can be in the capacity of either actor or director)
# - `'TITLE '` — title of the movie (show)
# - `'  Type'` — show or movie
# - `'release Year'` — year when movie (show) was released
# - `'genres'` — list of genres under which the movie (show) falls
# - `'imdb sc0re'` — score on IMDb
# - `'imdb v0tes'` — votes on IMDb
# 
# We can see three issues with the column names:
# 1. Some names are uppercase, while others are lowercase.
# 2. There are names containing whitespace.
# 3. A few column names have digit '0' instead of letter 'o'. 
# 

# ### Conclusions <a id='data_review_conclusions'></a> 
# 
# Each row in the table stores data about a movie or show. The columns can be divided into two categories: the first is about the roles held by different people who worked on the movie or show (role, name of the actor or director, and character if the row is about an actor); the second category is information about the movie or show itself (title, release year, genre, imdb figures).
# 
# It's clear that there is sufficient data to do the analysis and evaluate our assumption. However, to move forward, we need to preprocess the data.

# ## Stage 2. Data preprocessing <a id='data_preprocessing'></a>
# Correct the formatting in the column headers and deal with the missing values. Then, check whether there are duplicates in the data.

# In[5]:


# the list of column names in the df table
df.loc[0:9]


# Change the column names according to the rules of good style:
# * If the name has several words, use snake_case
# * All characters must be lowercase
# * Remove whitespace
# * Replace zero with letter 'o'

# In[6]:


# renaming columns
print(df.columns)
def clean_headers(test):
    clean_headers=[]
    for run in test:
        run = run.lower()
        run = run.replace('0','o')
        run = run.strip()
        run = run.replace(' ','_')
        clean_headers.append(run)
    return clean_headers
df.columns=clean_headers(df)
print(df.columns)


# Check the result. Print the names of the columns once more:

# In[7]:


# checking result: the list of column names
clean_headers(df.loc[0:9])


# ### Missing values <a id='missing_values'></a>
# First, find the number of missing values in the table. To do so, combine two `pandas` methods:

# In[8]:


# calculating missing values
df.isna().sum()


# Not all missing values affect the research: the single missing value in `'title'` is not critical. The missing values in columns `'imdb_score'` and `'imdb_votes'` represent around 6% of all records (4,609 and 4,726, respectively, of the total 85,579). To avoid this issue, drop rows with missing values in the `'imdb_score'` and `'imdb_votes'` columns.

# In[9]:


# dropping rows where columns with title, scores and votes have missing values
df=df.dropna(axis=0)


# Count the missing values again.

# In[10]:


# counting missing values
df.isna().sum()


# ### Duplicates <a id='duplicates'></a>
# Find the number of duplicate rows in the table using one command:

# In[11]:


# counting duplicate rows
df.duplicated().sum()


# Review the duplicate rows to determine if removing them would distort our dataset.

# In[12]:


# Produce table with duplicates (with original rows included) and review last 5 rows
dfs=df.duplicated()
dfs.tail()


# There are two clear duplicates in the printed rows. Remove them.
# Call the `pandas` method for getting rid of duplicate rows:

# In[13]:


# removing duplicate rows
df=df.drop_duplicates().reset_index()


# Check for duplicate rows once more to make sure you have removed all of them:

# In[14]:


# checking for duplicates
df.duplicated().sum()


# Now get rid of implicit duplicates in the `'type'` column. 

# Print a list of unique `'type'` names, sorted in alphabetical order. To do so:
# * Retrieve the intended dataframe column 
# * Apply a sorting method to it
# * For the sorted column, call the method that will return all unique column values

# In[15]:


# viewing unique type names
df['type'].sort_values().unique()



# Look through the list to find implicit duplicates of `'show'`. These could be names written incorrectly or alternative names of the same genre.
# 
# Following implicit duplicates:
# * `'shows'`
# * `'SHOW'`
# * `'tv show'`
# * `'tv shows'`
# * `'tv series'`
# * `'tv'`
# 
# Declare the function `replace_wrong_show()` with two parameters: 
# * `wrong_shows_list=` — the list of duplicates
# * `correct_show=` — the string with the correct value
# 
# The function should correct the names in the `'type'` column from the `df` table (i.e., replace each value from the `wrong_shows_list` list with the value in `correct_show`).

# In[16]:


# function for replacing implicit duplicates
def replace_wrong_show(wrong_shows_list, correct_show):
    df['type'] = df['type'].replace(wrong_shows_list, correct_show)
wrong_shows_list=['SHOW','shows', 'tv', 'tv series',
       'tv show', 'tv shows']
correct_show='SHOW'


  


# Call `replace_wrong_show()` and pass it arguments so that it clears implicit duplicates and replaces them with `SHOW`:

# In[17]:


# removing implicit duplicate
replace_wrong_show(wrong_shows_list, correct_show)


# Make sure the duplicate names are removed. Print the list of unique values from the `'type'` column:

# In[18]:


# viewing unique genre names
df['type'].sort_values().unique()


# ### Conclusions <a id='data_preprocessing_conclusions'></a>
# We detected three issues with the data:
# 
# - Incorrect header styles
# - Missing values
# - Duplicate rows and implicit duplicates
# 
# The headers have been cleaned up to make processing the table simpler.
# 
# All rows with missing values have been removed. 
# 
# The absence of duplicates will make the results more precise and easier to understand.
# 
# Now we can move on to our analysis of the prepared data.

# ## Stage 3. Data analysis <a id='hypotheses'></a>

# Define how the assumption will be checked. Calculate the average amount of votes for each score (this data is available in the `imdb_score` and `imdb_votes` columns), and then check how these averages relate to each other. If the averages for shows with the highest scores are bigger than those for shows with lower scores, the assumption appears to be true.
# 
# Based on this, complete the following steps:
# 
# - Filter the dataframe to only include shows released in 1999 or later.
# - Group scores into buckets by rounding the values of the appropriate column (a set of 1-10 integers will help us make the outcome of our calculations more evident without damaging the quality of our research).
# - Identify outliers among scores based on their number of votes, and exclude scores with few votes.
# - Calculate the average votes for each score and check whether the assumption matches the results.

# In[19]:


# using conditional indexing modify df so it has only titles released after 1999 (with 1999 included)
# give the slice of dataframe new name

df_later1999=df[df['release_year'] >= 1999]
df_later1999




# In[20]:


# repeat conditional indexing so df has only shows (movies are removed as result)
df_only_show=df_later1999[df_later1999['type'] == 'SHOW']

df_only_show.head()


# In[21]:


df.head()


# The scores that are to be grouped should be rounded. For instance, titles with scores like 7.8, 8.1, and 8.3 will all be placed in the same bucket with a score of 8.

# In[22]:


# rounding column with scores
df_only_show=df_only_show.round({'imdb_score': 0 })
#checking the outcome with tail()
df_only_show.tail()


# It is now time to identify outliers based on the number of votes.

# In[23]:


# Use groupby() for scores and count all unique values in each group, print the result
df_only_show.groupby(["imdb_score"]).size()


# Based on the aggregation performed, it is evident that scores 2 (24 voted shows), 3 (27 voted shows), and 10 (only 8 voted shows) are outliers. There isn't enough data for these scores for the average number of votes to be meaningful.

# To obtain the mean numbers of votes for the selected scores (we identified a range of 4-9 as acceptable), use conditional filtering and grouping.

# In[24]:


# filter dataframe using two conditions (scores to be in the range 4-9)
df_score_range_filter=df_only_show[df_only_show['imdb_score'] >= 4]
df_score_range_filter = df_score_range_filter[df_score_range_filter['imdb_score'] <= 9]
# group scores and corresponding average number of votes, reset index and print the result
df_score_range_filter=df_score_range_filter.groupby(["imdb_score"])["imdb_votes"].mean().reset_index()
df_score_range_filter
#df_score_range_filter['imdb_votes'].unique()


# Now for the final step! Round the column with the averages, rename both columns, and print the dataframe in descending order.

# In[25]:


# round column with averages
df_score_range_filter['imdb_votes']=df_score_range_filter['imdb_votes'].round(0)
                        
# rename columns
df_score_range_filter = df_score_range_filter.rename(columns={"imdb_score": "average_imdb_score", "imdb_votes": "average_imdb_votes"})
# print dataframe in descending order
df_score_range_filter.sort_values(by='average_imdb_score',ascending=False)


# The assumption macthes the analysis: the shows with the top 3 scores have the most amounts of votes.

# ## Conclusion <a id='hypotheses'></a>

# The research done confirms that highly-rated shows released during the "Golden Age" of television also have the most votes. While shows with score 4 have more votes than ones with scores 5 and 6, the top three (scores 7-9) have the largest number. The data studied represents around 94% of the original set, so we can be confident in our findings.

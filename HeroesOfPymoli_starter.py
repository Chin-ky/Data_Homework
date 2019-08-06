#!/usr/bin/env python
# coding: utf-8

# ### Heroes Of Pymoli Data Analysis
# * Of the 1163 active players, the vast majority are male (84%). There also exists, a smaller, but notable proportion of female players (14%).
# 
# * Our peak age demographic falls between 20-24 (44.8%) with secondary groups falling between 15-19 (18.60%) and 25-29 (13.4%).  
# -----

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[2]:


# Dependencies and Setup
import pandas as pd
import numpy as np

# File to Load (Remember to Change These)
file_to_load = "Resources/purchase_data.csv"

# Read Purchasing File and store into Pandas data frame
purchase_data = pd.read_csv(file_to_load)
purchase_data.head()


# ## Player Count

# * Display the total number of players
# 

# In[33]:


# Use the column for screen names "SN", to calculate the total players
total_players = len(purchase_data["SN"].value_counts())

# Create a dataframe "player_count"
player_count = ({"Total Players":[total_players]})
player_count


# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[34]:


# Calculations for the Purchasing Analysis variables
unique_items = len(purchase_data["Item ID"].unique())
average_price = purchase_data["Price"].mean()
total_purchases = purchase_data["Purchase ID"].count()
total_revenue = purchase_data["Price"].sum()

# Create a dataframe to hold the valuesobtained from the calculations
purchasing_analysis_df = pd.DataFrame({"Number of Unique Items":[unique_items],
                           "Average Price":[average_price], 
                           "Number of Purchases": [total_purchases], 
                           "Total Revenue": [total_revenue]})

# Format the summary "purchasing_analysis" to reflect currency
purchasing_analysis_df.style.format({'Average Price':"${:,.2f}",
                         'Total Revenue': '${:,.2f}'})


# ## Gender Demographics

# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 

# In[36]:


# Organize purchase_data into gender groupings
gender_info = purchase_data.groupby("Gender")

# Count the total number of unique screen names "SN" by gender
gender_count = gender_info.nunique()["SN"]

# Divide the gender count by the total players 
gender_percentage = gender_count / total_players * 100

# Create a data frame with the values from the calculations above
gender_demographics_df = pd.DataFrame({"Percentage of Players": gender_percentage, "Total Count": gender_count})

# Format the values by sorting the total count in descending order, and the percentage by two decimal places
gender_demographics_df.sort_values(["Total Count"], ascending = False).style.format({"Percentage of Players":"{:.2f}"})


# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[13]:


# Count the total purchases by gender 
purchase_count = gender_info["Purchase ID"].count()

# Calculate the average purchase prices by gender
avg_purchase_price = gender_info["Price"].mean()

# Calculate the average purchase total by gender 
total_purchase_value = gender_info["Price"].sum()

# Divide the average purchase total by gender by the purchase count by unique shoppers
avg_purchase_per_person = total_purchase_value/gender_count

# Create a data frame for the values obtained 
gender_demographics_df = pd.DataFrame({"Purchase Count": purchase_count, 
                                    "Average Purchase Price": avg_purchase_price,
                                    "Average Purchase Value": total_purchase_value,
                                    "Avg Purchase Total per Person": avg_purchase_per_person})

# Format the data frame with "Gender" as the index name in the top left corner
gender_demographics_df.index.name = "Gender"

# Format the dataframe to reflect currency
gender_demographics_df.style.format({"Average Purchase Value":"${:,.2f}",
                                  "Average Purchase Price":"${:,.2f}",
                                  "Avg Purchase Total per Person":"${:,.2f}"})


# ## Age Demographics

# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# In[19]:


# Create bins for the ages
age_bins = [0, 9.90, 14.90, 19.90, 24.90, 29.90, 34.90, 39.90, 99999]
group_names = ["<10", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40+"]

# Sort the age values into bins created above
purchase_data["Age Group"] = pd.cut(purchase_data["Age"],age_bins, labels=group_names)
purchase_data

# Create and group the new data frame "Age Group"
age_group = purchase_data.groupby("Age Group")

# Count the total players by age
total_count_age = age_group["SN"].nunique()

# Calculate the percentages using the age category 
percentage_by_age = (total_count_age/total_players) * 100

# Create a data frame with the results
age_demographics_df = pd.DataFrame({"Percentage of Players": percentage_by_age, "Total Count": total_count_age})

# Format the data frame to have no index name
age_demographics_df.index.name = None

# Format percentage with two decimal places 
age_demographics_df.style.format({"Percentage of Players":"{:,.2f}"})


# ## Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[18]:


# Count the purchases by age group
purchase_count_age = age_group["Purchase ID"].count()

# Calculate the  average purchase price by age group 
avg_purchase_price_age = age_group["Price"].mean()

# Calculate the total purchase value by age group 
total_purchase_value_age = age_group["Price"].sum()

# Calculate the average purchase per person in the age group (total purchase value by age divided by the total count by age)
avg_purchase_per_person_age = total_purchase_value_age/total_count_age

# Create data frame with results
age_demographics_df = pd.DataFrame({"Purchase Count": purchase_count_age,
                                 "Average Purchase Price": avg_purchase_price_age,
                                 "Total Purchase Value":total_purchase_value_age,
                                 "Average Purchase Total per Person": avg_purchase_per_person_age})

# Format the data frame to have no index name
age_demographics_df.index.name = None

# Format data frame for currency style
age_demographics_df.style.format({"Average Purchase Price":"${:,.2f}",
                               "Total Purchase Value":"${:,.2f}",
                               "Average Purchase Total per Person":"${:,.2f}"})


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[20]:


# Group purchase data by screen names "SN"
spender_info = purchase_data.groupby("SN")

# Count the total purchases by name
purchase_count_spender = spender_info["Purchase ID"].count()

# Calculate the average purchase by name 
avg_purchase_price_spender = spender_info["Price"].mean()

# Calculate the purchase total 
total_purchase_value_spender = spender_info["Price"].sum()

# Create a data frame with the results obtained
top_spenders_df = pd.DataFrame({"Purchase Count": purchase_count_spender,
                             "Average Purchase Price": avg_purchase_price_spender,
                             "Total Purchase Value":total_purchase_value_spender})

# Sort the data frame in descending order to obtain the top 5 spender by names 
top_5_spenders = top_spenders_df.sort_values(["Total Purchase Value"], ascending=False).head()

# Format the data frame to reflect currency
top_5_spenders.style.format({"Average Purchase Total":"${:,.2f}",
                                 "Average Purchase Price":"${:,.2f}", 
                                 "Total Purchase Value":"${:,.2f}"})


# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[23]:


# Create a new data frame with items related information 
items = purchase_data[["Item ID", "Item Name", "Price"]]

# Sort the item data by Item ID and Item Name 
item_info = items.groupby(["Item ID","Item Name"])

# Count the number of times an item has been purchased 
purchase_count_item = item_info["Price"].count()

# Calculate the purchase value per item 
purchase_value_item = (item_info["Price"].sum()) 

# Find the price of individual items
item_price = purchase_value_item/purchase_count_item

# Create a data frame with the values obtained
most_popular_items_df = pd.DataFrame({"Purchase Count": purchase_count_item, 
                                   "Item Price": item_price,
                                   "Total Purchase Value":purchase_value_item})

# Sort in descending order to obtain the top spender names and provide the top 5 item names
five_most_popular_items_df = most_popular_items_df.sort_values(["Purchase Count"], ascending=False).head()

# Format the data frame to reflect currency
five_most_popular_items_df.style.format({"Item Price":"${:,.2f}",
                                "Total Purchase Value":"${:,.2f}"})


# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[25]:


# Use the most_popular items data frame and change the sorting to find the highest total purchase value
five_most_popular_items_df = most_popular_items_df.sort_values(["Total Purchase Value"], ascending=False).head()  

# Format to reflect currency styling
five_most_popular_items_df.style.format({"Item Price":"${:,.2f}",
                                "Total Purchase Value":"${:,.2f}"})


# In[ ]:





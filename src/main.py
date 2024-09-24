#!/usr/bin/env python
# coding: utf-8

# # 1. Preparation

# In[1]:


import os
import re
import pandas as pd
import numpy as np


# In[2]:


OUTPUT_DIR = "../output_data"


# ## 1.A. Common Functions

# In[3]:


def merge_id(prev_table, keys_table, name):
    merged_df = prev_table.merge(
        keys_table, left_on=name, right_on=name, how="left"
    )
    merged_df = merged_df.rename(columns={"id": f"{name}_id"})
    merged_df = merged_df.drop(columns=[name])
    merged_df[f"{name}_id"] = (
        merged_df[f"{name}_id"]
        .where(merged_df[f"{name}_id"].notna(), 0)
        .astype(int)
    )
    return merged_df


# In[4]:


def cleanup_semicolon(source):
    with open(source, "r") as file:
        content = file.read()
    updated_content = content.replace(";", "")
    with open(source, "w") as file:
        file.write(updated_content)


# ## 1.B. Key Table Generator

# In[5]:


def create_table_key(dataframe, column):
    file_path = f"{OUTPUT_DIR}/key_{column}.csv"
    new_table = (
        pd.DataFrame(dataframe[column].unique(), columns=[column])
        .dropna()
        .sort_values(column)
        .reset_index(drop=True)
    )

    # If the file already exists, load it
    if os.path.exists(file_path):
        existing_table = pd.read_csv(file_path)
        # Find the new values that are not in the existing table
        new_values = new_table[~new_table[column].isin(existing_table[column])]
        if not new_values.empty:
            # Assign IDs to the new values, starting after the max existing ID
            max_id = existing_table["id"].max()
            new_values["id"] = range(max_id + 1, max_id + 1 + len(new_values))
            # Append the new values to the existing table
            updated_table = pd.concat(
                [existing_table, new_values], ignore_index=True
            )
        else:
            updated_table = existing_table  # No new values to add, keep existing table as is
    else:
        # If the file doesn't exist, create new IDs starting from 1
        new_table["id"] = range(1, len(new_table) + 1)
        updated_table = new_table
    updated_table[["id", column]].to_csv(file_path, index=False)
    return updated_table


# # 2. JMP Dataset

# In[6]:


JMP_INPUT_FILE = "../input_data/JMP/jmp.csv"
JMP_OUTPUT_FILE = f"{OUTPUT_DIR}/table_jmp.csv"


# In[7]:


data = pd.read_csv(JMP_INPUT_FILE, encoding="latin-1")
data.head()


# ## 2.A. JMP Data Processing

# ### 2.A.1 Rename the columns

# In[8]:


data.columns = [
    "country",
    "year",
    "jmp_name",
    "total_ALB",
    "annual_rate_change_ALB",
    "total_SM",
    "annual_rate_change_SM",
    "manual_rate_change_SM",
    "manual_rate_change_ALB",
]
data.head()


# ### 2.A.2. Categorize the Values

# In[9]:


data_melted = pd.melt(
    data,
    id_vars=["country", "year", "jmp_name"],  # columns to keep
    var_name="variable",  # melted
    value_name="value",  # values
)
data_melted["value_type"] = data_melted["variable"].apply(
    lambda x: "total" if "total" in x else "annual_rate_change"
)
data_melted["jmp_category"] = data_melted["variable"].apply(
    lambda x: "ALB" if "ALB" in x else "SM"
)
data_melted = data_melted.drop(columns=["variable"])
data_melted.head()


# ## 2.B. JMP Table Keys

# ### 2.B.1. Countries

# In[10]:


countries_table = create_table_key(data_melted, "country")
countries_table


# ### 2.B.1. JMP Names

# In[11]:


jmp_names_table = create_table_key(data_melted, "jmp_name")
jmp_names_table


# ### 2.B.2. JMP Categories

# In[12]:


jmp_categories_table = create_table_key(data_melted, "jmp_category")
jmp_categories_table


# ### 2.B.3. JMP Value Types

# In[13]:


value_types_table = create_table_key(data_melted, "value_type")
value_types_table


# ## 2.C. JMP Table Results

# ### 2.C.1. JMP Key Table Mapping

# In[14]:


table_with_id = merge_id(data_melted, value_types_table, "value_type")
table_with_id = merge_id(table_with_id, countries_table, "country")
table_with_id = merge_id(table_with_id, jmp_names_table, "jmp_name")
table_with_id = merge_id(table_with_id, jmp_categories_table, "jmp_category")


# ### 2.C.2. JMP Final Result

# In[15]:


table_with_id.head()


# ### 2.C.3. Save JMP Table

# In[16]:


table_with_id.to_csv(JMP_OUTPUT_FILE, index=False)


# # 3. IFS Dataset

# In[17]:


IFS_INPUT_DIR = "../input_data/IFs"
IFS_OUTPUT_FILE = f"{OUTPUT_DIR}/table_ifs.csv"
final_columns = [
    "indicator",
    "year",
    "country",
    "unit",
    "value_name",
    "jmp_category",
    "commitment",
    "value",
]


# In[18]:


files_to_keep = [
    "01. Deaths by Category of Cause - Millions (2nd Dimensions = Diarrhea).csv",
    "11. Governance Effectiveness - WB index.csv",
    "12. Value Added by Sector, Currency - Billion dollars.csv",
    "13. Sanitation Services, Access, percent of population (2nd Dimensions = Basic + Safely Managed).csv",
    "14. Sanitation Services, Access, Number of people, million (2nd Dimensions = Basic + Safely Managed).csv",
    "15. Sanitation Services, Expenditure, Capital, Billion $ (2nd Dimensions = Basic + Safely Managed).csv",
    "16. Sanitation Services, Expenditure, Maintenance, Billion $ (2nd Dimensions = Basic + Safely Managed).csv",
    "17. Water Services, Access, percent of population (2nd Dimension = Basic + Safely Managed).csv",
    "18. Water Services, Access, Number of people, million (2nd Dimensions = Basic + Safely Managed).csv",
    "19. Water Services, Expenditure, Capital, Billion $ (2nd Dimensions = Basic + Safely Managed).csv",
    "20. Water Services, Expenditure, Maintenance, Billion $ (2nd Dimensions = Basic + Safely Managed).csv",
    "21. Population - Millions.csv",
    "23. GDP (PPP) - Billion dollars.csv",
    "24. Stunted children, History and Forecast - Million.csv",
    "25. Population under 5 Years, Headcount - Millions.csv",
    "26. Malnourished Children, Headcount - Millions.csv",
]
files = [
    f"{IFS_INPUT_DIR}/{f}"
    for f in os.listdir(IFS_INPUT_DIR)
    if os.path.isfile(os.path.join(IFS_INPUT_DIR, f))
]
files = [f"{IFS_INPUT_DIR}/{file}" for file in files_to_keep]


# ## 3.A. IFS Functions

# In[19]:


def get_ifs_name(source):
    return re.sub(
        r"^\d+\. ", "", source.replace(f"{IFS_INPUT_DIR}/", "")
    ).replace(".csv", "")


# In[20]:


def get_value_types(lst):
    lst = lst.split(".")[0]
    lst = lst.replace("_0_", "_0.").split("_")
    return lst


# In[21]:


def cleanup_data(dataframe):
    dataframe["unit"] = dataframe["unit"].apply(
        lambda x: x.replace("2017", "") if x else None
    )
    dataframe["value"] = dataframe["value"].apply(
        lambda x: x.replace(" ", "") if " " in str(x) else x
    )
    dataframe["value"] = dataframe["value"].apply(
        lambda x: x if len(str(x)) > 0 else np.nan
    )


# ## 3.B. IFS Data Processing

# In[22]:


combined_df = pd.DataFrame(columns=final_columns)
for file in files:
    print(f"Processing {file}")
    cleanup_semicolon(file)
    data = pd.read_csv(file, header=[1, 4, 5], sep=",")
    new_columns = list(data.columns)
    for i, col in enumerate(new_columns):
        if col == (
            "Unnamed: 0_level_0",
            "Unnamed: 0_level_1",
            "Unnamed: 0_level_2",
        ):
            new_columns[i] = "Year"
    data.columns = new_columns
    df = pd.DataFrame(data.to_dict("records"))
    df_melted = df.melt(
        id_vars=["Year"], var_name="variable", value_name="value"
    )
    new_data = []
    for value_list in df_melted.to_dict("records"):
        value_type = get_value_types(value_list["variable"][2])
        new_data.append(
            {
                "year": value_list["Year"],
                "country": value_list["variable"][0],
                "unit": value_list["variable"][1],
                "value_type": list(filter(lambda v: v, value_type)),
                "value": value_list["value"],
            }
        )
    df = pd.DataFrame(new_data)
    df_split = pd.DataFrame(df["value_type"].tolist(), index=df.index)
    df_split.columns = ["value_name", "jmp_category", "commitment"]
    df_final = pd.concat([df, df_split], axis=1)
    df_final["indicator"] = get_ifs_name(file)
    df_final = df_final[final_columns]
    combined_df = pd.concat(
        [combined_df.dropna(axis=1, how="all"), df_final], ignore_index=True
    )


# In[23]:


cleanup_data(combined_df)
combined_df.head()


# **To check the results before merging with the ID, please run the following command:**

# In[24]:


# combined_df.to_csv("./testing.csv",index=False)


# ## 3.C. IFS Table of Keys

# ### 3.C.1. Indicators

# In[25]:


indicator_table = create_table_key(combined_df, "indicator")
indicator_table


# ### 3.C.2. Units

# In[26]:


units_table = create_table_key(combined_df, "unit")
units_table


# ### 3.C.3. Value Names

# In[27]:


value_names_table = create_table_key(combined_df, "value_name")
value_names_table


# ### 3.C.4. JMP Categories (Retry)

# In[28]:


jmp_categories_table = create_table_key(combined_df, "jmp_category")
jmp_categories_table


# ### 3.C.5. Commitments

# In[29]:


commitments_table = create_table_key(combined_df, "commitment")
commitments_table


# ## 3.D. IFS Table Results

# ### 3.D.1. Custom Table Mapping (JMP)
#
# - FS = Full Sanitation Access
# - FW = Full Water Access
# - FWS = Full Water and Sanitation Access
# - SI = Sanitation Increased
# - WI = Water Increased
# - WSI = Water and Sanitation Increased

# In[30]:


jmp_dict = dict(zip(jmp_names_table["jmp_name"], jmp_names_table["id"]))


# In[31]:


def map_jmp_ids(jmp_type):
    ids = []
    if "W" in jmp_type:  # Water is indicated by 'W' in the type
        ids.append(jmp_dict["Water"])
    if "S" in jmp_type:  # Sanitation is indicated by 'S' in the type
        ids.append(jmp_dict["Sanitation"])
    return ids


# In[32]:


combined_df["jmp_name_ids"] = combined_df["value_name"].apply(map_jmp_ids)
combined_df.tail(2)


# ### 3.D.2. IFS Key Table Mapping

# In[33]:


table_with_id = merge_id(combined_df, indicator_table, "indicator")
table_with_id = merge_id(table_with_id, units_table, "unit")
table_with_id = merge_id(table_with_id, value_names_table, "value_name")
table_with_id = merge_id(table_with_id, jmp_categories_table, "jmp_category")
table_with_id = merge_id(table_with_id, commitments_table, "commitment")
table_with_id = merge_id(table_with_id, countries_table, "country")


# ### 3.D.3. IFS Final Result

# In[34]:


table_with_id = table_with_id[table_with_id["value"].notna()]
table_with_id = table_with_id.sort_values("year")
table_with_id.reset_index(drop=True).tail()


# ### 3.D.2. Save IFS Table

# In[35]:


table_with_id.to_csv(IFS_OUTPUT_FILE, index=False)

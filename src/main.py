#!/usr/bin/env python
# coding: utf-8

# 1. Preparation

import os
import glob
import re
import pandas as pd
import numpy as np
import difflib
import itertools


OUTPUT_DIR = "../output_data"


csv_files = glob.glob(os.path.join(OUTPUT_DIR, "*.csv"))
for file in csv_files:
    try:
        os.remove(file)
        print(f"Removed: {file}")
    except Exception as e:
        print(f"Error removing {file}: {e}")


## 1.A. Data Input and Output

JMP_INPUT_FILE = "../input_data/JMP/jmp.csv"
JMP_OUTPUT_FILE = f"{OUTPUT_DIR}/table_jmp.csv"
IFS_INPUT_DIR = "../input_data/IFs"
IFS_OUTPUT_FILE = f"{OUTPUT_DIR}/table_ifs.csv"
IFS_GRAPH_OUTPUT_FILE = f"{OUTPUT_DIR}/table_graph_ifs.csv"
IFS_PR_OUTPUT_FILE = f"{OUTPUT_DIR}/table_ifs_progress_rates.csv"


## 1.B. Common Functions
#
# Common functions are a collection of functions used by both data sources (IFS and JMP).
#
# - **merge_id**: This function merges two data tables based on a common column replaces missing values with 0, and renames the column for easier identification.
# - **cleanup_semicolon**: Replaces all occurrences of semicolons (;) with an empty string, cleaning up the extra characters that have been included in the Excel format from IFS.


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


def cleanup_semicolon(source):
    with open(source, "r") as file:
        content = file.read()
    updated_content = content.replace(";", "")
    with open(source, "w") as file:
        file.write(updated_content)


## 1.C. Key Table Generator
#
# This function generates a unique key table for a specified column from both IFS and JMP table, saving the keys to a CSV file.
# If the CSV file already exists, it appends new values to the existing file while ensuring unique IDs for each entry.


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


## 1.D. Country Mapping
#
# This section compares two lists of country names—jmp_country_list from the JMP dataset and ifs_country_list from the IFS dataset—and finds the closest matches using string similarity. It also includes a mapping for countries with naming differences between the two lists.

data_jmp = pd.read_csv(JMP_INPUT_FILE, encoding="latin-1")


jmp_country_list = list(data_jmp["COUNTRY, AREA OR TERRITORY"].unique())
ifs_country_list = [
    "All countries WHHS Tool1",
    "Congo Dem. Republic of the",
    "Ethiopia",
    "Ghana",
    "Guatemala",
    "Haiti",
    "India",
    "Indonesia",
    "Kenya",
    "Liberia",
    "Madagascar",
    "Malawi",
    "Mali",
    "Mozambique",
    "Nepal",
    "Nigeria",
    "Philippines",
    "Rwanda",
    "Senegal",
    "Sudan South",
    "Tanzania",
    "Uganda",
    "Zambia",
]


# Find the closest match
for country in ifs_country_list:
    probability = difflib.get_close_matches(
        country, jmp_country_list, n=3, cutoff=0.4
    )
    if probability:
        if country not in probability:
            print(f"{country} -> {list(probability)}")
    else:
        print(f"NOT FOUND: {country}")


country_mapping = {
    "All countries WHHS Tool1": "All High Priority Countries",
    "United Republic of Tanzania": "Tanzania",
    "Congo Dem. Republic of the": "Democratic Republic of the Congo",
    "Sudan South": "South Sudan",
}


def map_country_name(country):
    return country_mapping.get(country, country)


# 3. IFS Dataset

final_columns = [
    "indicator",
    "year",
    "country",
    "unit",
    "value_name",
    "jmp_category",
    "commitment",
    "value",
    "base_value",
    "initial_value",
    "2030",
    "2050",
]


files_to_keep = [
    "01. Deaths by Category of Cause - Millions (2nd Dimensions = Diarrhea).csv",
    "06. Poverty Headcount less than $2.15 per Day, Log Normal - Millions.csv",
    "08. State Failure Instability Event - IFs Index.csv",
    "11. Governance Effectiveness - WB index.csv",
    "13. Sanitation Services, Access, percent of population (2nd Dimensions = Basic + Safely Managed).csv",
    "14. Sanitation Services, Access, Number of people, million (2nd Dimensions = Basic + Safely Managed).csv",
    "15. Sanitation Services, Expenditure, Capital, Billion $ (2nd Dimensions = Basic + Safely Managed).csv",
    "16. Sanitation Services, Expenditure, Maintenance, Billion $ (2nd Dimensions = Basic + Safely Managed).csv",
    "17. Water Services, Access, percent of population (2nd Dimensions = Basic + Safely Managed).csv",
    "18. Water Services, Access, Number of people, million (2nd Dimensions = Basic + Safely Managed).csv",
    "19. Water Services, Expenditure, Capital, Billion $ (2nd Dimensions = Basic + Safely Managed).csv",
    "20. Water Services, Expenditure, Maintenance, Billion $ (2nd Dimensions = Basic + Safely Managed).csv",
    "23. GDP (PPP) - Billion dollars.csv",
    "24. Stunted children, History and Forecast - Million.csv",
    "26. Malnourished Children, Headcount - Millions.csv",
]
year_filter_config = {
    "year_range": {
        "years": list(range(2018, 2051)),
        "files": [
            "13. Sanitation Services, Access, percent of population (2nd Dimensions = Basic + Safely Managed).csv",
            "17. Water Services, Access, percent of population (2nd Dimensions = Basic + Safely Managed).csv",
        ],
    },
    "milestone_years": [
        2019,
        2030,
        2050,
    ],  # 2019 for initial only but we remove them after get it
}


files = [
    f"{IFS_INPUT_DIR}/{f}"
    for f in os.listdir(IFS_INPUT_DIR)
    if os.path.isfile(os.path.join(IFS_INPUT_DIR, f))
]
files = [f"{IFS_INPUT_DIR}/{file}" for file in files_to_keep]


## 3.A. IFS Functions
#
# IFS functions are a collection of functions used only by IFS data source
#
# - **base_jmp_category**: This function assigns or updates the JMP category based on specific conditions in the input data, particularly for records where the value is base; It converts certain base categories to simplified abbreviations ("BS" or "SM"), otherwise; retains the existing category
# - **get_ifs_name**: This function extracts and cleans the name of an IFS data file by removing unwanted text and formatting, such as numbering, directory paths, and file extensions.
# - **get_value_types**: This function processes a string by manipulating its structure to generate a list of values based on certain patterns. But it also replaces occurrences of '_0_' with '_0.' in the string, since '_0_5' is '0.5'.
# - **cleanup_data**: This function cleans a DataFrame by removing unnecessary parts of the text in the "unit" column and ensuring consistency in the "value" column. Specifically, it unifies the unit formatting by removing "2017" from units like "Billion 2017" and handles space and empty value issues in the "value" column.
# - **filter_dataframe_by_year**: This function filters a DataFrame based on a year configuration, depending on the config in previous section. It checks the configuration to determine whether to filter by a specific year range or milestone years.
# - **remove_unmatches_jmp_category**: This function identifies rows in a dataset where the JMP category ("jmp_category") does not match the base category ("2nd_dimension"), according to specific rules. It returns True for rows where the mismatch occurs, indicating that the row should be removed.
# - **remove_unmatch_commitment**: This function identifies rows in a dataset where the "commitment" year does not match the actual "year" of the data. It returns True for rows where the mismatch occurs, indicating that the row should be removed.


def base_jmp_category(x):
    if "Base" in str(x["value_name"]):
        if "Basic" in x["2nd_dimension"]:
            return "BS"
        if "Safely" in x["2nd_dimension"]:
            return "SM"
        return np.nan
    return x["jmp_category"]


def get_ifs_name(source):
    source = re.sub(r"\s*\(2nd Dimension.*?\)", "", source)
    return re.sub(
        r"^\d+\. ", "", source.replace(f"{IFS_INPUT_DIR}/", "")
    ).replace(".csv", "")


def get_value_types(lst):
    lst = lst.split(".")[0]
    lst = lst.replace("_0_", "_0.").split("_")
    return lst


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


def filter_dataframe_by_year(dataframe, filename):
    filename = filename.split("/")[3]
    if (
        filename in year_filter_config["year_range"]["files"]
    ):  # Filter using the year_range
        filtered_df = dataframe[
            dataframe["year"].isin(year_filter_config["year_range"]["years"])
        ]
    else:  # Filter using milestone_years
        filtered_df = dataframe[
            dataframe["year"].isin(year_filter_config["milestone_years"])
        ]
    return filtered_df.reset_index(drop=True)


def remove_unmatches_jmp_category(x):
    if x["value_name"] != "Base":
        if x["2nd_dimension"] == "Basic" and x["jmp_category"] == "SM":
            return True
        if x["2nd_dimension"] == "SafelyManaged" and x["jmp_category"] == "ALB":
            return True
        if x["2nd_dimension"] == "SafelyManaged" and x["jmp_category"] == "BS":
            return True
    return False


def remove_unmatch_commitment(x):
    # 07 October 2024 https://akvo.slack.com/archives/C070F7D7VFS/p1728289594284939?thread_ts=1728268592.335199&cid=C070F7D7VFS
    if "2030" in x["commitment"]:
        if x["year"] == 2050:
            return True
        if x["year"] > 2030:
            return True
        # if str(x["year"]).strip() != "2030":
        #    return True
    if "2050" in x["commitment"]:
        if x["year"] == 2030:
            return True
        # if str(x["year"]).strip() != "2050":
        #    return True
    return False


def add_initial_value_for_wash(x, dataframe):
    if x["year"] == 2030 or x["year"] == 2050 or x["year"] == 2022:
        value_of_min_year = list(
            dataframe[
                (dataframe["indicator"] == x["indicator"])
                & (dataframe["country"] == x["country"])
                & (dataframe["jmp_category"] == x["jmp_category"])
                & (dataframe["year"] == dataframe["year"].min())
            ]["value"]
        )
        if len(value_of_min_year):
            return value_of_min_year[0]
    return np.nan


def add_base_value(x, dataframe, is_wash_data=True):
    if x["value_name"] != "Base":
        if is_wash_data:
            value_of_base = list(
                dataframe[
                    (dataframe["indicator"] == x["indicator"])
                    & (dataframe["country"] == x["country"])
                    & (dataframe["jmp_category"] == x["jmp_category"])
                    & (dataframe["year"] == x["year"])
                    & (dataframe["value_name"] == "Base")
                    & (dataframe["2nd_dimension"] == x["2nd_dimension"])
                ]["value"]
            )
            if len(value_of_base):
                return value_of_base[0]
        else:
            value_of_base = list(
                dataframe[
                    (dataframe["indicator"] == x["indicator"])
                    & (dataframe["country"] == x["country"])
                    & (dataframe["year"] == x["year"])
                    & (dataframe["value_name"] == "Base")
                ]["value"]
            )
            if len(value_of_base):
                return value_of_base[0]
    return np.nan


def modify_commitment_name(x):
    commitment_name = str(x["commitment"]).strip()
    if x["value_name"] == "Base":
        return "Base"
    if "2030" in commitment_name or "2050" in commitment_name:
        value_name = x["value_name"]
        if "W" in value_name and "S" in value_name:
            value_name = "Water and Sanitation"
        if "W" in value_name:
            value_name = "Water"
        if "S" in value_name:
            value_name = "Sanitation"
        return f"Full {value_name} Access in {commitment_name}"
    return x["commitment"]


def get_alb_value(x, df):
    if x["2nd_dimension"] == "Basic":
        additional_value = df[
            (df["indicator"] == x["indicator"])
            & (df["year"] == x["year"])
            & (df["country"] == x["country"])
            & (df["commitment"] == x["commitment"])
            & (df["value_name"] == x["value_name"])
            & (df["2nd_dimension"] == "SafelyManaged")
        ]
        if not additional_value.empty:
            return x["value"] + additional_value["value"].iloc[0]
    return x["value"]


## 3.B. IFS Data Processing

### 3.B.1. Combine, Filter and Remap IFS Values
#
# This section describes the process of transforming and processing IFS data files into a unified DataFrame (combined_df). The transformation involves cleaning, reshaping, and filtering the data to prepare it for analysis.

# In[28]:


combined_df = pd.DataFrame(columns=final_columns)
for file in files:
    # test only 1 file
    # if file != "../input_data/IFs/17. Water Services, Access, percent of population (2nd Dimensions = Basic + Safely Managed).csv":
    # continue
    cleanup_semicolon(file)
    data = pd.read_csv(file, header=[1, 2, 4, 5], sep=",")
    new_columns = list(data.columns)
    for i, col in enumerate(new_columns):
        if col == (
            "Unnamed: 0_level_0",
            "Unnamed: 0_level_1",
            "Unnamed: 0_level_2",
            "Unnamed: 0_level_3",
        ):
            new_columns[i] = "Year"
    data.columns = new_columns
    df = pd.DataFrame(data.to_dict("records"))
    df_melted = df.melt(
        id_vars=["Year"], var_name="variable", value_name="value"
    )
    new_data = []
    for value_list in df_melted.to_dict("records"):
        value_type = get_value_types(value_list["variable"][3])
        new_data.append(
            {
                "year": int(value_list["Year"]),
                "country": map_country_name(value_list["variable"][0]),
                "2nd_dimension": value_list["variable"][1],
                "unit": value_list["variable"][2],
                "value_type": list(filter(lambda v: v, value_type)),
                "value": value_list["value"],
            }
        )
    df = pd.DataFrame(new_data)
    df = filter_dataframe_by_year(df, file)
    df_split = pd.DataFrame(df["value_type"].tolist(), index=df.index)
    df_split.columns = ["value_name", "jmp_category", "commitment"]
    df_final = pd.concat([df, df_split], axis=1)

    df_final["indicator"] = get_ifs_name(file)
    df_final["jmp_category"] = df_final.apply(base_jmp_category, axis=1)
    df_final["jmp_category"] = df_final["jmp_category"].replace({"BS": "ALB"})
    df_final["commitment"] = df_final.apply(modify_commitment_name, axis=1)
    # df_final.to_csv("testing-1.csv",index=False)
    # Add Value for ALB
    if "Water Service" in file or "Sanitation Service" in file:
        # for n in df_final.to_dict("records"):
        #  if n["country"] == "Democratic Republic of the Congo":
        #      print(n)
        df_final["value"] = df_final.apply(
            lambda x: get_alb_value(x, df_final), axis=1
        )

    df_final["remove"] = df_final.apply(remove_unmatches_jmp_category, axis=1)
    df_final = df_final[df_final["remove"] == False].reset_index(drop=True)

    # Add initial value column
    df_final["initial_value"] = np.nan
    df_final["base_value"] = np.nan
    df_final["2030"] = np.nan
    df_final["2050"] = np.nan
    if (
        "Water Service" in file or "Sanitation Service" in file
    ):  # Filter using the filename
        df_final["initial_value"] = df_final.apply(
            lambda x: add_initial_value_for_wash(x, df_final), axis=1
        )
        df_final["base_value"] = df_final.apply(
            lambda x: add_base_value(x, df_final), axis=1
        )
        print(f"[WASH] : {file}")
    else:
        df_final["base_value"] = df_final.apply(
            lambda x: add_base_value(x, df_final, is_wash_data=False), axis=1
        )
        print(f"[OTHER]: {file}")
    if (
        file.split("/")[3] not in year_filter_config["year_range"]["files"]
    ):  # remove after get initial value (for non wash)
        df_final = df_final[df_final["year"] != 2019].reset_index(drop=True)
    else:
        df_final["2030"] = df_final.apply(
            lambda x: float(x["value"])
            if "2030" in x["commitment"]
            else np.nan,
            axis=1,
        )
        df_final["2050"] = df_final.apply(
            lambda x: float(x["value"])
            if "2050" in x["commitment"]
            else np.nan,
            axis=1,
        )
    df_final = df_final[final_columns]
    combined_df = pd.concat(
        [combined_df.dropna(axis=1, how="all"), df_final], ignore_index=True
    )


# df_final[
# (df_final["country"] == "Liberia")
# & (df_final["year"] == 2030)
# ].to_csv("check.csv")


# Test for Congo
# combined_df[
# (combined_df["indicator"] == "Sanitation Services, Access, percent of population") &
# (combined_df["country"] == "Liberia") &
# (combined_df["value_name"] == "Base")
# ]


# Remove rows when commitment doesn't match with the year

# 07 October 2024 https://akvo.slack.com/archives/C070F7D7VFS/p1728289594284939?thread_ts=1728268592.335199&cid=C070F7D7VFS
combined_df["remove"] = combined_df.apply(
    lambda x: remove_unmatch_commitment(x), axis=1
)
# I moved this removal execution to before saving because we need the commitment per year for the IFS graphic table.
# combined_df = combined_df[combined_df['remove'] == False].reset_index(drop=True)
# combined_df = combined_df.drop(columns=['remove'])


### 3.B.2. IFS Data Cleanup

cleanup_data(combined_df)
combined_df.head()


# **To check the results before merging with the ID:**

testing = (
    combined_df[combined_df["remove"] == False].reset_index(drop=True).copy()
)
testing = testing.drop(columns=["remove"])
testing.to_csv("../tests/ifs-testing.csv", index=False)


## 3.C. IFS Table of Keys

### 3.C.1. Indicators

indicator_table = create_table_key(combined_df, "indicator")
indicator_table


### 3.C.2. Units

units_table = create_table_key(combined_df, "unit")
units_table


### 3.C.3. Value Names

value_names_table = create_table_key(combined_df, "value_name")
value_names_table


### 3.C.4. JMP Categories

jmp_categories_table = create_table_key(combined_df, "jmp_category")
jmp_categories_table


### 3.C.5. JMP Names Table (Custom)

jmp_names_table = pd.DataFrame(
    [
        {"id": 1, "jmp_name": "Water"},
        {"id": 2, "jmp_name": "Sanitation"},
        {"id": 3, "jmp_name": "Water and Sanitation"},
    ]
)
jmp_names_table.to_csv(f"{OUTPUT_DIR}/key_jmp_name.csv", index=False)


### 3.C.6. Commitments

commitments_table = create_table_key(combined_df, "commitment")
commitments_table


### 3.C.7. Country

countries_table = create_table_key(combined_df, "country")
countries_table


## 3.D. IFS Table Results

### 3.D.1. Custom Table Mapping (JMP Name)
#
# - FS = Full Sanitation Access
# - FW = Full Water Access
# - FWS = Full Water and Sanitation Access
# - SI = Sanitation Increased
# - WI = Water Increased
# - WSI = Water and Sanitation Increased

jmp_dict = dict(zip(jmp_names_table["jmp_name"], jmp_names_table["id"]))


def map_jmp_id(x):
    value_name = x["value_name"]
    # For the Base data
    if value_name == "Base":
        if x["indicator"].startswith("Water"):
            return jmp_dict["Water"]
        if x["indicator"].startswith("Sanitation"):
            return jmp_dict["Sanitation"]
    if (
        "W" in value_name and "S" in value_name
    ):  # Water and Sanitation is indicated by 'WS' combined
        return jmp_dict["Water and Sanitation"]
    if "W" in value_name:  # Water is indicated by 'W'
        return jmp_dict["Water"]
    if "S" in value_name:  # Sanitation is indicated by 'S'
        return jmp_dict["Sanitation"]
    return 0


combined_df["jmp_name_id"] = combined_df.apply(map_jmp_id, axis=1)
combined_df.tail(2)


### 3.D.2. IFS Key Table Mapping

ifs_table_with_id = merge_id(combined_df, indicator_table, "indicator")
ifs_table_with_id = merge_id(ifs_table_with_id, units_table, "unit")
ifs_table_with_id = merge_id(ifs_table_with_id, value_names_table, "value_name")
ifs_table_with_id = merge_id(
    ifs_table_with_id, jmp_categories_table, "jmp_category"
)
ifs_table_with_id = merge_id(ifs_table_with_id, commitments_table, "commitment")
ifs_table_with_id = merge_id(ifs_table_with_id, countries_table, "country")


### 3.D.3. IFS Final Result

ifs_table_with_id = ifs_table_with_id[
    ifs_table_with_id["value"].notna()
].reset_index(drop=True)
ifs_table_with_id = ifs_table_with_id.sort_values(by="year").reset_index(
    drop=True
)
ifs_table_with_id.reset_index(drop=True).tail()


### 3.D.2. Save IFS Table

final_ifs = ifs_table_with_id[ifs_table_with_id["remove"] == False].reset_index(
    drop=True
)
final_ifs = final_ifs.drop(columns=["remove"])
final_ifs.drop(columns=["2030", "2050"]).to_csv(IFS_OUTPUT_FILE, index=False)


### 3.D.3. Save IFS Graph Table

# First Graph

graph_with_id = ifs_table_with_id[
    ifs_table_with_id["indicator_id"].isin([7, 13])
].drop(columns=["remove"])
graph_with_id = graph_with_id.copy()
graph_with_id.loc[:, "actual_year"] = graph_with_id["year"]
graph_with_id.loc[:, "year"] = graph_with_id["year"].apply(
    lambda x: 2030 if x <= 2030 else 2050
)
graph_with_id.loc[:, "value"] = graph_with_id.apply(
    lambda x: x["value"]
    if (
        x["2030"] is not np.nan
        or x["2050"] is not np.nan
        or base_value is np.nan
    )
    else np.nan,
    axis=1,
)
graph_with_id = graph_with_id[
    [
        "actual_year",
        "year",
        "country_id",
        "indicator_id",
        "value_name_id",
        "jmp_name_id",
        "jmp_category_id",
        "commitment_id",
        "value",
    ]
]

# Duplicate Year 2030 so it can be shown in 2050

replicate_for_2050 = graph_with_id[graph_with_id["year"] == 2030].copy()
replicate_for_2050.loc[:, "year"] = 2050
combined_graph = pd.concat(
    [graph_with_id, replicate_for_2050], ignore_index=True
)
combined_graph = combined_graph.dropna(subset=["value"])

combined_graph["full_wash_coverage"] = 1
combined_graph["actual_commitment_id"] = combined_graph["commitment_id"]

base_commitment = combined_graph[combined_graph["commitment_id"] == 5].copy()
base_commitment.loc[:, "full_wash_coverage"] = 0
for a in range(1, 5):
    base_commitment.loc[:, "commitment_id"] = a
    combined_graph = pd.concat(
        [combined_graph, base_commitment], ignore_index=True
    )


combined_graph.to_csv(IFS_GRAPH_OUTPUT_FILE, index=False)

# Duplicate Commitment Key for Legend

actual_commitment = pd.read_csv(f"{OUTPUT_DIR}/key_commitment.csv")
actual_commitment = actual_commitment.rename(
    columns={"commitment": "actual_commitment"}
)
actual_commitment.to_csv(f"{OUTPUT_DIR}/key_actual_commitment.csv", index=False)


## 3.E. Progress Rates

### 3.E.1 Progress Rates Functions


def get_alb_value_for_progress_rates(x, dataframe):
    if x["jmp_category"] == "ALB":
        sm_value = list(
            dataframe[
                (dataframe["jmp_category"] == "SM")
                & (dataframe["indicator"] == x["indicator"])
                & (dataframe["country"] == x["country"])
                & (dataframe["year"] == x["year"])
            ]["value"]
        )[0]
        return x["value"] + sm_value
    return x["value"]


### 3.E.2 Progress Rates Collections

progress_rates_columns = [
    "indicator",
    "year",
    "country",
    "jmp_category",
    "value_name",
    "value",
]
progress_rates_df = pd.DataFrame(columns=progress_rates_columns)
for file in files:
    # test only 1 file
    if file.split("/")[3] not in year_filter_config["year_range"]["files"]:
        continue
    print(file)
    data = pd.read_csv(file, header=[1, 2, 4, 5], sep=",")
    new_columns = list(data.columns)
    for i, col in enumerate(new_columns):
        if col == (
            "Unnamed: 0_level_0",
            "Unnamed: 0_level_1",
            "Unnamed: 0_level_2",
            "Unnamed: 0_level_3",
        ):
            new_columns[i] = "Year"
    data.columns = new_columns
    df = pd.DataFrame(data.to_dict("records"))
    df_melted = df.melt(
        id_vars=["Year"], var_name="variable", value_name="value"
    )
    new_data = []
    for value_list in df_melted.to_dict("records"):
        value_type = get_value_types(value_list["variable"][3])
        new_data.append(
            {
                "year": int(value_list["Year"]),
                "country": map_country_name(value_list["variable"][0]),
                "2nd_dimension": value_list["variable"][1],
                "unit": value_list["variable"][2],
                "value_type": list(filter(lambda v: v, value_type)),
                "value": value_list["value"],
            }
        )
    df = pd.DataFrame(new_data)
    df_split = pd.DataFrame(df["value_type"].tolist(), index=df.index)
    df_split.columns = ["value_name", "jmp_category", "commitment"]
    df_final = pd.concat([df, df_split], axis=1)
    df_final["indicator"] = get_ifs_name(file)
    df_final["jmp_category"] = df_final.apply(base_jmp_category, axis=1)
    df_final["jmp_category"] = df_final["jmp_category"].replace({"BS": "ALB"})
    df_final["commitment"] = df_final.apply(modify_commitment_name, axis=1)
    df_final = df_final[df_final["commitment"] == "Base"]
    df_final = df_final[progress_rates_columns]
    df_final["value"] = df_final.apply(
        lambda x: get_alb_value_for_progress_rates(x, df_final), axis=1
    )
    progress_rates_df = pd.concat(
        [progress_rates_df.dropna(axis=1, how="all"), df_final],
        ignore_index=True,
    )


progress_rates_df = progress_rates_df.sort_values(
    by=["indicator", "country", "jmp_category", "value_name", "year"]
)
progress_rates_df["yearly_increase"] = progress_rates_df.groupby(
    ["indicator", "country", "jmp_category"]
)["value"].diff()


### 3.E.3 Progress Rates Year Filters

progress_rates_df["full_services"] = progress_rates_df["value"].apply(
    lambda x: x > 99
)


filtered_dfs = []

# Iterate over each group
for name, group in progress_rates_df.groupby(
    ["indicator", "country", "jmp_category", "value_name"]
):
    group = group.sort_values(by="value")
    group["yearly_increase"] = group["value"].diff()
    avg_yearly_increase = group["yearly_increase"].mean()

    reached_100 = group[group["value"] >= 99]
    if not reached_100.empty:
        filtered_group = reached_100.iloc[[0]].copy()
        # Add the avg_yearly_increase as a new column
        filtered_group.loc[:, "avg_yearly_increase"] = avg_yearly_increase
        filtered_group.loc[:, "full_services"] = True
    else:
        filtered_group = pd.DataFrame(
            {
                "indicator": [name[0]],
                "country": [name[1]],
                "jmp_category": [name[2]],
                "value_name": [name[3]],
                "year": [2100],
                "value": [
                    group["value"].iloc[-1]
                ],  # current value (latest in time)
                "avg_yearly_increase": [avg_yearly_increase],
                "full_services": False,
            }
        )
    filtered_dfs.append(filtered_group)
progress_rates_df = pd.concat(filtered_dfs, ignore_index=True)


progress_rates_df = progress_rates_df[
    progress_rates_columns + ["avg_yearly_increase", "full_services"]
]


### 3.E.4. Progress Rates Key Table Mapping

progress_rates_df["jmp_name_id"] = progress_rates_df.apply(map_jmp_id, axis=1)
progress_rates_df = merge_id(
    progress_rates_df, jmp_categories_table, "jmp_category"
)
progress_rates_df = merge_id(progress_rates_df, countries_table, "country")
progress_rates_df = merge_id(progress_rates_df, indicator_table, "indicator")


progress_rates_df = progress_rates_df.drop(columns=["value_name"])


### 3.D.2. Save Progress Rates Table

progress_rates_df.to_csv(IFS_PR_OUTPUT_FILE, index=False)


# 2. JMP Dataset

data = pd.read_csv(JMP_INPUT_FILE, encoding="latin-1")
data.head()


## 2.A. JMP Data Processing

### 2.A.1. Rename the columns

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
data = data.drop(columns=["manual_rate_change_SM", "manual_rate_change_ALB"])
data.head()


### 2.A.2. Categorize the Values

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
data_melted["jmp_category"] = data_melted["jmp_category"].replace({"BS": "ALB"})
data_melted["country"] = data_melted["country"].apply(map_country_name)
data_melted = data_melted.drop(columns=["variable"])
data_melted["value"] = data_melted["value"].apply(
    lambda x: np.nan if x == -99 else x
)
data_melted.head()


## 2.B. JMP Table Keys

### 2.B.1. JMP Categories (Retry)

jmp_categories_table = create_table_key(data_melted, "jmp_category")
jmp_categories_table


### 2.B.2. JMP Value Types

value_types_table = create_table_key(data_melted, "value_type")
value_types_table


## 2.C. JMP Table Results

### 2.C.1. JMP Key Table Mapping

jmp_table_with_id = merge_id(data_melted, value_types_table, "value_type")
jmp_table_with_id = merge_id(jmp_table_with_id, countries_table, "country")
jmp_table_with_id = merge_id(jmp_table_with_id, jmp_names_table, "jmp_name")
jmp_table_with_id = merge_id(
    jmp_table_with_id, jmp_categories_table, "jmp_category"
)


### 2.C.2. JMP Data Cleanup
# - Remove Nullable Country

jmp_table_with_id = jmp_table_with_id[
    jmp_table_with_id["country_id"] != 0
].reset_index(drop=True)


### 2.C.3. JMP Final Result

jmp_table_with_id.head()


### 2.C.3. Save JMP Table

jmp_table_with_id.to_csv(JMP_OUTPUT_FILE, index=False)


# 4. Post Data Transform

## 4.A. Post Data Functions


def replace_key_table_values(table_name, new_values):
    key_table_file_path = f"{OUTPUT_DIR}/key_{table_name}.csv"
    df = pd.read_csv(key_table_file_path)
    df = df.replace(new_values)
    df.to_csv(key_table_file_path, index=False)
    return df


## 4.B. Replace Key Tables with Predefined Strings

### 4.B.1 Replace Commitment Values

replace_key_table_values(
    "commitment",
    {
        "0.5x": "Halving",
        "2x": "Doubling",
        "4x": "Quadrupling",
        "6x": "Six-Fold",
        "Base": "Business-as-usual",
    },
)


replace_key_table_values(
    "actual_commitment",
    {
        "0.5x": "Halving",
        "2x": "Doubling",
        "4x": "Quadrupling",
        "6x": "Six-Fold",
        "Base": "Business-as-usual",
    },
)


### 4.B.2 Replace JMP Category

replace_key_table_values(
    "jmp_category",
    {
        "ALB": "At Least Basic",
        "SM": "Safely Managed",
    },
)


### 4.B.3 Replace Value Name

replace_key_table_values(
    "value_name", {"FS": "Full Sanitation Access", "FW": "Full Water Access"}
)

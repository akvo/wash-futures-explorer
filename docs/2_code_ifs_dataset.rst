==============
2. IFs Dataset
==============

This section describes the steps to process the IFs dataset, applying filters, cleaning data, and transforming it to align with WASH indicators and milestones. It includes specific functions for handling and manipulating IFs data, preparing it for further analysis and visualization.

**Final Columns for Output**

The following columns are retained in the final dataset for consistency and usability in downstream processing:

.. code-block:: python

    final_columns = ['indicator','year','country','unit','value_name','jmp_category',
                     'commitment','value','base_value','initial_value','2030','2050']

**Files to Keep**

The IFs dataset includes a selected list of files, each representing various indicators or metrics relevant to WASH. These files are stored in `IFS_INPUT_DIR` and include the following:

.. code-block:: python

    files_to_keep = [
        '01. Deaths by Category of Cause - Millions (2nd Dimensions = Diarrhea).csv',
        '06. Poverty Headcount less than $2.15 per Day, Log Normal - Millions.csv',
        '08. State Failure Instability Event - IFs Index.csv',
        '11. Governance Effectiveness - WB index.csv',
        # Additional files listed in the dataset...
    ]

**Year Filtering Configuration**

The year filtering configuration determines which years are kept in the final dataset, allowing for analysis by key milestone years (2019, 2030, and 2050).

.. code-block:: python

    year_filter_config = {
        "year_range": {
            "years": list(range(2018, 2051)),
            "files": [
                '13. Sanitation Services, Access, percent of population (2nd Dimensions = Basic + Safely Managed).csv',
                '17. Water Services, Access, percent of population (2nd Dimensions = Basic + Safely Managed).csv',
            ]
        },
        "milestone_years": [2019, 2030, 2050]
    }

---

2.A. IFS Functions
------------------

The following functions perform specific transformations, cleanups, and mappings on the IFs dataset to ensure consistency with the WASH indicators.

1. **base_jmp_category**

   Determines the JMP category based on the "2nd_dimension" field and assigns either "BS" (Basic) or "SM" (Safely Managed) accordingly.

   .. code-block:: python

       def base_jmp_category(x):
           if "Base" in str(x["value_name"]):
               if "Basic" in x["2nd_dimension"]:
                   return "BS"
               if "Safely" in x["2nd_dimension"]:
                   return "SM"
               return np.nan
           return x["jmp_category"]

2. **get_ifs_name**

   Cleans up the source file name by removing unnecessary components, such as "2nd Dimension" information, and provides a simplified file name.

   .. code-block:: python

       def get_ifs_name(source):
           source = re.sub(r"\s*\(2nd Dimension.*?\)", "", source)
           return re.sub(r'^\d+\. ', '', source.replace(f"{IFS_INPUT_DIR}/", "")).replace(".csv", "")

3. **get_value_types**

   Splits a string to extract value types, handling numeric formatting issues that may be present in file names.

   .. code-block:: python

       def get_value_types(lst):
           lst = lst.split('.')[0]
           lst = lst.replace('_0_','_0.').split("_")
           return lst

4. **cleanup_data**

   Cleans up the data by removing unnecessary characters in the "unit" and "value" columns, replacing empty values with NaN for consistency.

   .. code-block:: python

       def cleanup_data(dataframe):
           dataframe['unit'] = dataframe['unit'].apply(lambda x: x.replace("2017","") if x else None)
           dataframe['value'] = dataframe['value'].apply(lambda x: x.replace(' ','') if ' ' in str(x) else x)
           dataframe['value'] = dataframe['value'].apply(lambda x: x if len(str(x)) > 0 else np.nan)

5. **filter_dataframe_by_year**

   Filters the dataset by year based on the file name, using either a predefined range or milestone years.

   .. code-block:: python

       def filter_dataframe_by_year(dataframe, filename):
           filename = filename.split("/")[3]
           if filename in year_filter_config["year_range"]["files"]:
               filtered_df = dataframe[dataframe['year'].isin(year_filter_config["year_range"]["years"])]
           else:
               filtered_df = dataframe[dataframe['year'].isin(year_filter_config["milestone_years"])]
           return filtered_df.reset_index(drop=True)

6. **remove_unmatches_jmp_category**

   Removes entries where the JMP category does not match the expected "Base" value or is inconsistent with the "2nd_dimension" field.

   .. code-block:: python

       def remove_unmatches_jmp_category(x):
           if x["value_name"] != "Base":
               if x["2nd_dimension"] == "Basic" and x["jmp_category"] == "SM":
                   return True
               if x["2nd_dimension"] == "SafelyManaged" and x["jmp_category"] == "ALB":
                   return True
               if x["2nd_dimension"] == "SafelyManaged" and x["jmp_category"] == "BS":
                   return True
           return False

7. **remove_unmatch_commitment**

   Removes entries where the year does not align with the defined "commitment" target (e.g., 2030 or 2050).

   .. code-block:: python

       def remove_unmatch_commitment(x):
           if "2030" in x['commitment']:
               if x["year"] == 2050 or x["year"] > 2030:
                   return True
           if "2050" in x['commitment'] and x["year"] == 2030:
               return True
           return False

8. **add_initial_value_for_wash**

   Adds initial values for WASH indicators based on the earliest year available in the dataset.

   .. code-block:: python

       def add_initial_value_for_wash(x, dataframe):
           if x["year"] in [2030, 2050, 2022]:
               value_of_min_year = list(dataframe[
                   (dataframe["indicator"] == x["indicator"]) &
                   (dataframe["country"] == x["country"]) &
                   (dataframe["jmp_category"] == x["jmp_category"]) &
                   (dataframe["year"] == dataframe["year"].min())
               ]['value'])
               if len(value_of_min_year):
                   return value_of_min_year[0]
           return np.nan

9. **add_base_value**

   Adds the base value for an indicator, using "Base" entries in the dataset if available.

   .. code-block:: python

       def add_base_value(x, dataframe, is_wash_data=True):
           if x["value_name"] != "Base":
               if is_wash_data:
                   value_of_base = list(dataframe[
                       (dataframe["indicator"] == x["indicator"]) &
                       (dataframe["country"] == x["country"]) &
                       (dataframe["jmp_category"] == x["jmp_category"]) &
                       (dataframe["year"] == x["year"]) &
                       (dataframe["value_name"] == "Base") &
                       (dataframe["2nd_dimension"] == x["2nd_dimension"])
                   ]['value'])
                   if len(value_of_base):
                       return value_of_base[0]
               else:
                   value_of_base = list(dataframe[
                       (dataframe["indicator"] == x["indicator"]) &
                       (dataframe["country"] == x["country"]) &
                       (dataframe["year"] == x["year"]) &
                       (dataframe["value_name"] == "Base")
                   ]['value'])
                   if len(value_of_base):
                       return value_of_base[0]
           return np.nan

10. **modify_commitment_name**

    Modifies the commitment name for clarity, appending relevant indicators such as "Water" or "Sanitation" as needed.

    .. code-block:: python

        def modify_commitment_name(x):
            commitment_name = str(x['commitment']).strip()
            if x["value_name"] == "Base":
                return "Base"
            if "2030" in commitment_name or "2050" in commitment_name:
                value_name = x['value_name']
                if 'W' in value_name and 'S' in value_name:
                    value_name = "Water and Sanitation"
                if 'W' in value_name:
                    value_name = "Water"
                if 'S' in value_name:
                    value_name = "Sanitation"
                return f"Full {value_name} Access in {commitment_name}"
            return x['commitment']

11. **get_alb_value**

    Adjusts values based on "Basic" and "SafelyManaged" categories in the dataset.

    .. code-block:: python

        def get_alb_value(x, df):
            if x["2nd_dimension"] == "Basic":
                additional_value = df[
                    (df["indicator"] == x["indicator"]) &
                    (df["year"] == x["year"]) &
                    (df["country"] == x["country"]) &
                    (df["commitment"] == x["commitment"]) &
                    (df["value_name"] == x["value_name"]) &
                    (df["2nd_dimension"] == "SafelyManaged")
                ]
                if not additional_value.empty:
                    return x["value"] + additional_value["value"].iloc[0]
            return x["value"]

---

These functions collectively handle filtering, cleaning, and transforming the IFs dataset, ensuring consistency with WASH categories and preparing it for subsequent analysis.

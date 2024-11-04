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
==================

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

2.B. IFS Data Processing
========================

2.B.1. Combine, Filter, and Remap IFs Values
--------------------------------------------

This section describes the process of transforming and processing IFs data files into a unified DataFrame, `combined_df`. The transformation involves cleaning, reshaping, and filtering the data to prepare it for analysis.

### Combining and Transforming Data

The following code iterates over each file in the IFs dataset, applies necessary transformations, and combines them into a single DataFrame (`combined_df`) for analysis.

.. code-block:: python

    combined_df = pd.DataFrame(columns=final_columns)
    for file in files:
        cleanup_semicolon(file)
        data = pd.read_csv(file, header=[1,2,4,5], sep=',')

        # Update column names
        new_columns = list(data.columns)
        for i, col in enumerate(new_columns):
            if col == ('Unnamed: 0_level_0', 'Unnamed: 0_level_1', 'Unnamed: 0_level_2', 'Unnamed: 0_level_3'):
                new_columns[i] = 'Year'
        data.columns = new_columns
        df = pd.DataFrame(data.to_dict('records'))

        # Reshape data
        df_melted = df.melt(id_vars=['Year'], var_name='variable', value_name='value')
        new_data = []
        for value_list in df_melted.to_dict('records'):
            value_type = get_value_types(value_list["variable"][3])
            new_data.append({
                "year": int(value_list["Year"]),
                "country": map_country_name(value_list["variable"][0]),
                "2nd_dimension": value_list["variable"][1],
                "unit": value_list["variable"][2],
                "value_type": list(filter(lambda v: v, value_type)),
                "value": value_list["value"]
            })
        df = pd.DataFrame(new_data)

        # Apply filters and transformations
        df = filter_dataframe_by_year(df, file)
        df_split = pd.DataFrame(df['value_type'].tolist(), index=df.index)
        df_split.columns = ['value_name', 'jmp_category', 'commitment']
        df_final = pd.concat([df, df_split], axis=1)

        # Assign indicator and clean up categories
        df_final['indicator'] = get_ifs_name(file)
        df_final['jmp_category'] = df_final.apply(base_jmp_category, axis=1)
        df_final['jmp_category'] = df_final['jmp_category'].replace({"BS": "ALB"})
        df_final['commitment'] = df_final.apply(modify_commitment_name, axis=1)

        # Adjust values based on category
        if "Water Service" in file or "Sanitation Service" in file:
            df_final['value'] = df_final.apply(lambda x: get_alb_value(x, df_final), axis=1)

        df_final['remove'] = df_final.apply(remove_unmatches_jmp_category, axis=1)
        df_final = df_final[df_final['remove'] == False].reset_index(drop=True)

        # Add initial and base values
        df_final['initial_value'] = np.nan
        df_final['base_value'] = np.nan
        df_final['2030'] = np.nan
        df_final['2050'] = np.nan

        if "Water Service" in file or "Sanitation Service" in file:
            df_final['initial_value'] = df_final.apply(lambda x: add_initial_value_for_wash(x, df_final), axis=1)
            df_final['base_value'] = df_final.apply(lambda x: add_base_value(x, df_final), axis=1)
        else:
            df_final['base_value'] = df_final.apply(lambda x: add_base_value(x, df_final, is_wash_data=False), axis=1)

        if file.split("/")[3] not in year_filter_config["year_range"]["files"]:
            df_final = df_final[df_final['year'] != 2019].reset_index(drop=True)
        else:
            df_final['2030'] = df_final.apply(lambda x: float(x["value"]) if "2030" in x["commitment"] else np.nan, axis=1)
            df_final['2050'] = df_final.apply(lambda x: float(x["value"]) if "2050" in x["commitment"] else np.nan, axis=1)

        df_final = df_final[final_columns]
        combined_df = pd.concat([combined_df.dropna(axis=1, how='all'), df_final], ignore_index=True)

### Filtering Commitments

After combining the data, a final filter is applied to remove any rows that do not align with the target commitment year (2030 or 2050).

.. code-block:: python

    combined_df['remove'] = combined_df.apply(lambda x: remove_unmatch_commitment(x), axis=1)

---

2.B.2. IFS Data Cleanup
-----------------------

The `cleanup_data` function is applied to the `combined_df` DataFrame to finalize data cleaning by removing extraneous characters in columns such as "unit" and handling missing values. For details on `cleanup_data`, refer to ***IFS Functions** in Section 2.A.

---

2.C. IFs Table of Keys
======================

In this section, we generate unique key tables for various columns in the IFs dataset, which are used to standardize identifiers across the data. Each key table is saved as a separate CSV file.

2.C.1. Indicators
-----------------

Generates a unique identifier for each indicator in the dataset.

.. code-block:: python

    indicator_table = create_table_key(combined_df, 'indicator')

2.C.2. Units
------------

Creates a key table for the "unit" column to ensure consistent units across all data files.

.. code-block:: python

    units_table = create_table_key(combined_df, 'unit')

2.C.3. Value Names
------------------

Assigns unique identifiers to each "value_name" in the dataset for standardized referencing.

.. code-block:: python

    value_names_table = create_table_key(combined_df, 'value_name')

2.C.4. JMP Categories
---------------------

Generates a key table for the "jmp_category" column, ensuring consistent JMP categorization.

.. code-block:: python

    jmp_categories_table = create_table_key(combined_df, 'jmp_category')

2.C.5. JMP Names Table (Custom)
-------------------------------

Defines a custom key table for the JMP names used in the dataset, with a manual assignment of IDs for "Water," "Sanitation," and "Water and Sanitation."

.. code-block:: python

    jmp_names_table = pd.DataFrame([
        {"id": 1,"jmp_name": "Water"},
        {"id": 2,"jmp_name": "Sanitation"},
        {"id": 3,"jmp_name": "Water and Sanitation"}
    ])
    jmp_names_table.to_csv(f'{OUTPUT_DIR}/key_jmp_name.csv',index=False)

2.C.6. Commitments
------------------

Creates a unique identifier table for the "commitment" column, which is crucial for tracking progress toward specified targets (e.g., 2030 and 2050 goals).

.. code-block:: python

    commitments_table = create_table_key(combined_df, 'commitment')

2.C.7. Country
--------------

Generates a key table for the "country" column, standardizing country names across all datasets.

.. code-block:: python

    countries_table = create_table_key(combined_df, 'country')

---

These key tables ensure that each essential column in the dataset has a unique identifier, facilitating consistency and accuracy in data processing and subsequent analyses.

2.D. IFS Table Results
======================

This section documents the final steps of processing the IFs dataset by applying custom mappings, creating key table mappings, and preparing the final tables for output. These steps ensure that all data is structured and standardized, ready for visualization and analysis.

---

2.D.1. Custom Table Mapping (JMP Name)
--------------------------------------

To standardize WASH indicators in the IFs dataset, we map specific JMP names (such as Water, Sanitation) to unique identifiers using the `jmp_dict` dictionary. The `map_jmp_id` function assigns JMP name IDs to each row based on the `value_name` and `indicator` columns.

**JMP Name Codes**

- **FS**: Full Sanitation Access
- **FW**: Full Water Access
- **FWS**: Full Water and Sanitation Access
- **SI**: Sanitation Increased
- **WI**: Water Increased
- **WSI**: Water and Sanitation Increased

**Code**

.. code-block:: python

    jmp_dict = dict(zip(jmp_names_table['jmp_name'], jmp_names_table['id']))

    def map_jmp_id(x):
        value_name = x["value_name"]
        # For the Base data
        if value_name == "Base":
            if x["indicator"].startswith("Water"):
                return jmp_dict['Water']
            if x["indicator"].startswith("Sanitation"):
                return jmp_dict['Sanitation']
        if 'W' in value_name and 'S' in value_name:
            return jmp_dict['Water and Sanitation']
        if 'W' in value_name:
            return jmp_dict['Water']
        if 'S' in value_name:
            return jmp_dict['Sanitation']
        return 0

    combined_df['jmp_name_id'] = combined_df.apply(map_jmp_id, axis=1)

The `map_jmp_id` function applies specific conditions to assign the correct JMP name ID for each row in the dataset, enhancing consistency in JMP categories across records.

---

2.D.2. IFS Key Table Mapping
----------------------------

The following code maps unique IDs from various key tables (such as `indicator`, `unit`, `value_name`, etc.) into the `combined_df` DataFrame. This ensures each attribute is represented with a standardized identifier for consistent reference.

**Code**

.. code-block:: python

    ifs_table_with_id = merge_id(combined_df, indicator_table, 'indicator')
    ifs_table_with_id = merge_id(ifs_table_with_id, units_table, 'unit')
    ifs_table_with_id = merge_id(ifs_table_with_id, value_names_table, 'value_name')
    ifs_table_with_id = merge_id(ifs_table_with_id, jmp_categories_table, 'jmp_category')
    ifs_table_with_id = merge_id(ifs_table_with_id, commitments_table, 'commitment')
    ifs_table_with_id = merge_id(ifs_table_with_id, countries_table, 'country')

The above mappings ensure that each key table is referenced consistently, with unique IDs assigned to indicators, units, values, categories, commitments, and countries.

---

2.D.3. IFS Final Result
-----------------------

After applying key table mappings and ensuring all values are correctly assigned, we prepare the final table by removing rows without valid values and sorting by year.

.. code-block:: python

    ifs_table_with_id = ifs_table_with_id[ifs_table_with_id['value'].notna()].reset_index(drop=True)
    ifs_table_with_id = ifs_table_with_id.sort_values(by='year').reset_index(drop=True)

This final sorting and filtering step ensures the data is clean and organized, ready for export.

---

2.D.4. Save IFS Table
---------------------

We save the final cleaned and filtered data (excluding milestone columns) to a CSV file for analysis and visualization.

.. code-block:: python

    final_ifs = ifs_table_with_id[ifs_table_with_id['remove'] == False].reset_index(drop=True)
    final_ifs = final_ifs.drop(columns=['remove'])
    final_ifs.drop(columns=['2030', '2050']).to_csv(IFS_OUTPUT_FILE, index=False)

This `final_ifs` file contains the core dataset, cleaned and prepared for analysis.

---

2.D.5. Save IFS Graph Table
---------------------------

The final graph table is prepared for specific visualizations, duplicating certain entries for compatibility with 2050 projections.

1. **Initial Graph Preparation**

   This table retains only specific indicators and adds an `actual_year` column to track the year of each entry. We then map each year to the nearest milestone year (2030 or 2050).

   .. code-block:: python

       graph_with_id = ifs_table_with_id[ifs_table_with_id['indicator_id'].isin([7, 13])].drop(columns=['remove'])
       graph_with_id.loc[:, 'actual_year'] = graph_with_id['year']
       graph_with_id.loc[:, 'year'] = graph_with_id['year'].apply(lambda x: 2030 if x <= 2030 else 2050)
       graph_with_id.loc[:, 'value'] = graph_with_id.apply(lambda x: x['value'] if (x['2030'] is not np.nan or x['2050'] is not np.nan or base_value is np.nan) else np.nan, axis=1)
       graph_with_id = graph_with_id[['actual_year','year','country_id','indicator_id','value_name_id','jmp_name_id','jmp_category_id','commitment_id','value']]

2. **Replicating 2030 for 2050**

   We duplicate rows with year 2030 to show the same data in 2050 for certain projections.

   .. code-block:: python

       replicate_for_2050 = graph_with_id[graph_with_id['year'] == 2030].copy()
       replicate_for_2050.loc[:, 'year'] = 2050
       combined_graph = pd.concat([graph_with_id, replicate_for_2050], ignore_index=True)
       combined_graph = combined_graph.dropna(subset=['value'])

3. **Additional Fields and Base Commitment**

   The `combined_graph` DataFrame is expanded to include a `full_wash_coverage` field and duplicated commitments for visual legend consistency.

   .. code-block:: python

       combined_graph['full_wash_coverage'] = 1
       combined_graph['actual_commitment_id'] = combined_graph['commitment_id']

       base_commitment = combined_graph[combined_graph['commitment_id'] == 5].copy()
       base_commitment.loc[:, 'full_wash_coverage'] = 0
       for a in range(1, 5):
           base_commitment.loc[:, 'commitment_id'] = a
           combined_graph = pd.concat([combined_graph, base_commitment], ignore_index=True)

   The `combined_graph` DataFrame is saved as the final graph table, ready for visualization.

   .. code-block:: python

       combined_graph.to_csv(IFS_GRAPH_OUTPUT_FILE, index=False)

4. **Duplicate Commitment Key for Legend**

   Finally, we create an additional commitment key table to support graph legends in visualizations.

   .. code-block:: python

       actual_commitment = pd.read_csv(f"{OUTPUT_DIR}/key_commitment.csv")
       actual_commitment = actual_commitment.rename(columns={"commitment": "actual_commitment"})
       actual_commitment.to_csv(f"{OUTPUT_DIR}/key_actual_commitment.csv", index=False)

This additional commitment key table ensures consistency in legends and provides clarity for commitment types in visual outputs.

---

This section completes the processing of the IFs dataset, producing final tables for analysis and visualization and establishing consistent mappings and keys for attributes across the data.

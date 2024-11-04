1. Preparation
==============

In this initial step, we prepare the environment for data transformation by defining the necessary directories, importing libraries, setting up file paths for input and output data, and defining common utility functions used throughout the process.

**Libraries Used**

- `os`: For handling file operations and paths.
- `glob`: For finding all CSV files in the output directory.
- `re`: For handling regular expressions.
- `pandas`: For data manipulation and transformation.
- `numpy`: For numerical operations.
- `difflib`: For string matching.
- `itertools`: For creating iterators, used in later steps.

1.A. Import Required Libraries
------------------------------

The following code imports the required libraries, sets up the output directory, and removes any existing CSV files in the output folder to ensure a clean start for data processing.

.. code-block:: python

    import os
    import glob
    import re
    import pandas as pd
    import numpy as np
    import difflib
    import itertools

    OUTPUT_DIR = '../output_data'

    # Remove any existing CSV files in the output directory
    csv_files = glob.glob(os.path.join(OUTPUT_DIR, '*.csv'))
    for file in csv_files:
        try:
            os.remove(file)
            print(f"Removed: {file}")
        except Exception as e:
            print(f"Error removing {file}: {e}")

---

1.B. Data Input and Output
--------------------------

Define the file paths for both input and output data. These paths will be used throughout the transformation process to read input files and save the transformed data.

.. code-block:: python

    # Define file paths for input and output data
    JMP_INPUT_FILE = '../input_data/JMP/jmp.csv'
    JMP_OUTPUT_FILE = f'{OUTPUT_DIR}/table_jmp.csv'
    IFS_INPUT_DIR = '../input_data/IFs'
    IFS_OUTPUT_FILE = f'{OUTPUT_DIR}/table_ifs.csv'
    IFS_GRAPH_OUTPUT_FILE = f'{OUTPUT_DIR}/table_graph_ifs.csv'
    IFS_PR_OUTPUT_FILE = f'{OUTPUT_DIR}/table_ifs_progress_rates.csv'

In this setup, we specify:

- **JMP_INPUT_FILE**: The path to the JMP data file.
- **JMP_OUTPUT_FILE**: The output file for the processed JMP data.
- **IFS_INPUT_DIR**: The directory containing IFs input files.
- **IFS_OUTPUT_FILE**: The output file for the processed IFs data.
- **IFS_GRAPH_OUTPUT_FILE**: The output file for graph-specific data.
- **IFS_PR_OUTPUT_FILE**: The output file for IFs progress rates data.

These file paths ensure that input and output data are organized for efficient access and storage.

---

1.C. Common Functions
---------------------

The following common functions are utility functions that assist in data merging and cleanup. These functions are used across multiple stages of data transformation to streamline operations.

**Function Definitions**

1. **merge_id**

   This function merges two data tables based on a specified common column (`name`), replaces any missing values with `0`, renames the column for easier identification, and converts the IDs to integers. It is particularly useful for aligning tables with a shared key field.

   .. code-block:: python

       def merge_id(prev_table, keys_table, name):
           """
           Merge two tables based on a common column and rename the column for easier identification.

           Parameters:
           prev_table (pd.DataFrame): The primary DataFrame.
           keys_table (pd.DataFrame): The secondary DataFrame with matching key columns.
           name (str): The column name on which to merge.

           Returns:
           pd.DataFrame: Merged DataFrame with renamed and cleaned ID column.
           """
           merged_df = prev_table.merge(keys_table, left_on=name, right_on=name, how='left')
           merged_df = merged_df.rename(columns={'id': f'{name}_id'})
           merged_df = merged_df.drop(columns=[name])
           merged_df[f'{name}_id'] = merged_df[f'{name}_id'].where(merged_df[f'{name}_id'].notna(), 0).astype(int)
           return merged_df

   **Explanation**: This function takes in two data tables and merges them based on a common column (specified by `name`). After merging, the function:
   - Renames the ID column for clarity.
   - Replaces any missing values with `0`.
   - Ensures the ID column is of integer type.

2. **cleanup_semicolon**

   This function reads a file and replaces all occurrences of semicolons (`;`) with an empty string. It is useful for cleaning up extra characters that may appear in data files exported from Excel or other tools.

   .. code-block:: python

       def cleanup_semicolon(source):
           """
           Remove all semicolons from a text file.

           Parameters:
           source (str): The path to the file to be cleaned.

           Returns:
           None: The file is modified in place.
           """
           with open(source, 'r') as file:
               content = file.read()
           updated_content = content.replace(';', '')
           with open(source, 'w') as file:
               file.write(updated_content)

   **Explanation**: `cleanup_semicolon` is designed to clean up any extraneous semicolons in a file, which may result from certain export formats or delimiters in the data. It operates directly on the file specified by `source` and removes all instances of `;`.

---

These preparation steps ensure a clean working directory, establish structured file paths, and provide essential data preparation functions, including:

- **Data Merging**: `merge_id` facilitates merging and ID handling across tables.
- **Text Cleanup**: `cleanup_semicolon` ensures data files are free from extraneous characters, improving compatibility for later processing.

---

1.D. Key Table Generator
------------------------

The `create_table_key` function generates key tables for specific columns in a DataFrame. Key tables assign unique IDs to values in specified columns, ensuring consistency across datasets when merging or mapping data. This function checks if a key table already exists for a given column; if it does, it appends any new values not yet recorded.

**Function Definition**

.. code-block:: python

    def create_table_key(dataframe, column):
        file_path = f'{OUTPUT_DIR}/key_{column}.csv'
        new_table = pd.DataFrame(
            dataframe[column].unique(),
            columns=[column]
        ).dropna().sort_values(column).reset_index(drop=True)

        # If the file already exists, load it
        if os.path.exists(file_path):
            existing_table = pd.read_csv(file_path)
            # Find the new values that are not in the existing table
            new_values = new_table[~new_table[column].isin(existing_table[column])]
            if not new_values.empty:
                # Assign IDs to the new values, starting after the max existing ID
                max_id = existing_table['id'].max()
                new_values['id'] = range(max_id + 1, max_id + 1 + len(new_values))
                # Append the new values to the existing table
                updated_table = pd.concat([existing_table, new_values], ignore_index=True)
            else:
                updated_table = existing_table  # No new values to add, keep existing table as is
        else:
            # If the file doesn't exist, create new IDs starting from 1
            new_table['id'] = range(1, len(new_table) + 1)
            updated_table = new_table
        updated_table[['id', column]].to_csv(file_path, index=False)
        return updated_table

**Explanation**: The `create_table_key` function performs the following tasks:
- Extracts unique values from a specified column in a DataFrame.
- Assigns unique IDs to each value.
- Saves the table as `key_<column>.csv` in the output directory.
- Checks for any new values not already in the existing key table and appends them if necessary.

This function ensures that all values in a given column have a unique ID, which supports consistent referencing in other datasets and transformations.

---

1.E. Country Mapping
--------------------

The **Country Mapping** section addresses naming inconsistencies between the JMP and IFs datasets. Using string similarity matching, we find the closest matches between country names in both lists and apply a mapping to standardize names for easier merging.

**Steps**

1. **Country Lists**: We create lists of unique country names from both the JMP and IFs datasets.

   .. code-block:: python

       data_jmp = pd.read_csv(JMP_INPUT_FILE, encoding='latin-1')
       jmp_country_list = list(data_jmp["COUNTRY, AREA OR TERRITORY"].unique())
       ifs_country_list = ['All countries WHHS Tool1','Congo Dem. Republic of the','Ethiopia','Ghana','Guatemala','Haiti','India',
                           'Indonesia','Kenya','Liberia','Madagascar','Malawi','Mali','Mozambique','Nepal','Nigeria','Philippines',
                           'Rwanda','Senegal','Sudan South','Tanzania','Uganda','Zambia']

2. **Closest Match**: For each country in the IFs list, we use `difflib` to find the closest match in the JMP list. If there’s no match, we mark it as "NOT FOUND" for manual review.

   .. code-block:: python

       # Find the closest match
       for country in ifs_country_list:
           probability = difflib.get_close_matches(country, jmp_country_list, n=3, cutoff=0.4)
           if probability:
               if country not in probability:
                   print(f"{country} -> {list(probability)}")
           else:
               print(f"NOT FOUND: {country}")

3. **Manual Country Mapping**: A dictionary called `country_mapping` manually maps countries with known naming differences between the JMP and IFs datasets.

   .. code-block:: python

       country_mapping = {
           "All countries WHHS Tool1": "All High Priority Countries",
           "United Republic of Tanzania": "Tanzania",
           "Congo Dem. Republic of the": "Democratic Republic of the Congo",
           "Sudan South": "South Sudan",
       }

4. **Mapping Function**: The `map_country_name` function applies the `country_mapping` dictionary to map inconsistent country names from the IFs dataset to the standardized names used in the JMP dataset.

   .. code-block:: python

       def map_country_name(country):
           return country_mapping.get(country, country)

**Explanation**: The **Country Mapping** step ensures consistent country names across datasets by:
- Identifying close matches based on string similarity.
- Standardizing names via a manual dictionary for known discrepancies.
- Providing a function (`map_country_name`) to apply these mappings as needed.

This approach allows us to address country name inconsistencies effectively, ensuring seamless integration of data from both the JMP and IFs sources.

---

These preparation steps complete the setup necessary for further data transformation. The **Key Table Generator** creates unique identifiers for essential columns, and the **Country Mapping** standardizes country names, providing consistency across datasets.

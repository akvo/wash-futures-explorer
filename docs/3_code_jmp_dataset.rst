==============
3. JMP Dataset
==============

The **JMP Dataset** section documents the steps for processing and transforming the JMP data, including renaming columns, categorizing values, and mapping key tables to standardize data attributes.

---

3.A. JMP Data Processing
========================

In this step, the JMP data is loaded, columns are renamed for clarity, and values are categorized to prepare the dataset for further analysis.

**Loading Data**

The JMP dataset is read into a DataFrame.

.. code-block:: python

    data = pd.read_csv(JMP_INPUT_FILE, encoding='latin-1')
    data.head()

3.A.1 Rename the Columns
------------------------

Column names are renamed for better clarity and understanding of each variable.

.. code-block:: python

    data.columns = [
        'country',
        'year',
        'jmp_name',
        'total_ALB',
        'annual_rate_change_ALB',
        'total_SM',
        'annual_rate_change_SM',
        'manual_rate_change_SM',
        'manual_rate_change_ALB'
    ]

    data = data.drop(columns=[
        'manual_rate_change_SM',
        'manual_rate_change_ALB'
    ])

3.A.2 Categorize the Values
---------------------------

The data is reshaped using `pd.melt`, categorizing the `value_type` and `jmp_category` columns. Values of `-99` are replaced with `NaN`.

.. code-block:: python

    data_melted = pd.melt(
        data,
        id_vars=['country', 'year', 'jmp_name'],  # columns to keep
        var_name='variable',  # melted column
        value_name='value'  # values column
    )

    data_melted['value_type'] = data_melted['variable'].apply(lambda x: 'total' if 'total' in x else 'annual_rate_change')
    data_melted['jmp_category'] = data_melted['variable'].apply(lambda x: 'ALB' if 'ALB' in x else 'SM')
    data_melted['jmp_category'] = data_melted['jmp_category'].replace({"BS": "ALB"})
    data_melted['country'] = data_melted['country'].apply(map_country_name)
    data_melted = data_melted.drop(columns=['variable'])
    data_melted['value'] = data_melted['value'].apply(lambda x: np.nan if x == -99 else x)

This transformation ensures that values are properly categorized and ready for key mappings.

---

3.B. JMP Table Keys
===================

To standardize and reference columns consistently, key tables are created for `jmp_category` and `value_type`.

3.B.1 JMP Categories
--------------------

The JMP categories table is extended with additional categories, using the `create_table_key` function to maintain consistency with the existing IFS table keys.

.. code-block:: python

    jmp_categories_table = create_table_key(data_melted, 'jmp_category')

### 3.B.2 JMP Value Types

A key table for `value_type` is created, which assigns unique identifiers to each value type in the dataset.

.. code-block:: python

    value_types_table = create_table_key(data_melted, 'value_type')

---

3.C. JMP Table Results
======================

This section details the process of merging identifiers from the key tables, performing data cleanup, and saving the final JMP table.

3.C.1 JMP Key Table Mapping
---------------------------

Using the `merge_id` function, we map key tables to the main JMP DataFrame (`data_melted`), ensuring each field has a unique identifier.

.. code-block:: python

    jmp_table_with_id = merge_id(data_melted, value_types_table, 'value_type')
    jmp_table_with_id = merge_id(jmp_table_with_id, countries_table, 'country')
    jmp_table_with_id = merge_id(jmp_table_with_id, jmp_names_table, 'jmp_name')
    jmp_table_with_id = merge_id(jmp_table_with_id, jmp_categories_table, 'jmp_category')

3.C.2 JMP Data Cleanup (Remove Nullable Country)
------------------------------------------------

After mapping, rows with undefined `country_id` values are removed.

.. code-block:: python

    jmp_table_with_id = jmp_table_with_id[jmp_table_with_id['country_id'] != 0].reset_index(drop=True)

This step ensures that all rows in the final dataset have a valid `country_id`.

3.C.3 JMP Final Result
----------------------

We review the final table to confirm that all mappings and transformations were successful.

.. code-block:: python

    jmp_table_with_id.head()

3.C.4 Save JMP Table
--------------------

The processed JMP data is saved to a CSV file for further analysis or visualization.

.. code-block:: python

    jmp_table_with_id.to_csv(JMP_OUTPUT_FILE, index=False)

The saved file provides a complete view of the JMP dataset, including standardized identifiers and organized values.

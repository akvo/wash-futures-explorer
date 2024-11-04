=========================
4. Post Data Transform
=========================

The **Post Data Transform** section finalizes the data preparation by renaming key tables to make them more readable and standardized for visualization. This includes functions to replace specific values in key tables with predefined strings.

---

4.A. Post Data Functions
========================

The `replace_key_table_values` function updates values in a specified key table based on a dictionary of replacements. This function is used to rename specific values, improving readability and interpretation in visualizations.

**Function Definition**

.. code-block:: python

    def replace_key_table_values(table_name, new_values):
        key_table_file_path = f"{OUTPUT_DIR}/key_{table_name}.csv"
        df = pd.read_csv(key_table_file_path)
        df = df.replace(new_values)
        df.to_csv(key_table_file_path, index=False)
        return df

**Parameters**

- `table_name`: The name of the key table to be updated.
- `new_values`: A dictionary where keys represent existing values and values represent the new, replacement values.

This function reads the specified key table, replaces values based on the provided dictionary, and saves the updated table back to the output directory.

---

4.B. Replace Key Tables with Predefined Strings
===============================================

This step applies the `replace_key_table_values` function to multiple key tables, updating specific values to enhance readability.

4.B.1 Replace Commitment Values
-------------------------------

The commitment values in the `commitment` and `actual_commitment` tables are replaced with descriptive terms to make them more intuitive.

**Code**

.. code-block:: python

    replace_key_table_values("commitment", {
        "0.5x": "Halving",
        "2x": "Doubling",
        "4x": "Quadrupling",
        "6x": "Six-Fold",
        "Base": "Business-as-usual"
    })

    replace_key_table_values("actual_commitment", {
        "0.5x": "Halving",
        "2x": "Doubling",
        "4x": "Quadrupling",
        "6x": "Six-Fold",
        "Base": "Business-as-usual"
    })

4.B.2 Replace JMP Category
--------------------------

The `jmp_category` key table values are updated to more descriptive terms for WASH levels of service access.

**Code**

.. code-block:: python

    replace_key_table_values("jmp_category", {
        "ALB": "At Least Basic",
        "SM": "Safely Managed"
    })

4.B.3 Replace Value Name
------------------------

Values in the `value_name` table are updated to more descriptive terms for full access types.

**Code**

.. code-block:: python

    replace_key_table_values("value_name", {
        "FS": "Full Sanitation Access",
        "FW": "Full Water Access"
    })

These replacements ensure that the key tables use clear and descriptive terms, making the data more understandable and ready for visualization.

---

This completes the **Post Data Transform** phase, where key tables are refined for better readability and usability in visual outputs.

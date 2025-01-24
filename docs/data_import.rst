Data Import in PowerBI
=======================

Relational Data Structure
-------------------------
The datasets are structured with two main categories:

1. **Relational Data (`key_` Prefix):**
   Files with the `key_` prefix contain relational data used to define entities and their attributes. These files form the foundation of the relational database model, ensuring consistency and reusability of key information across the dataset.

2. **Value Data (`table` Prefix):**
   Files with the `table` prefix contain the actual data values for analysis. These tables often reference the relational data (keys) to avoid redundancy and reduce file size.

Dataset Location
----------------
Below are the dataset files available in the repository, with links to their respective locations in Git LFS. These links can be used directly for importing data into PowerBI.

Relational Data Files:
1. `key_actual_commitment.csv`_: Relational data for actual commitments.
2. `key_commitment.csv`_: Relational data for commitments.
3. `key_country.csv`_: Relational data for countries.
4. `key_indicator.csv`_: Relational data for indicators.
5. `key_jmp_category.csv`_: Relational data for JMP categories.
6. `key_jmp_name.csv`_: Relational data for JMP names.
7. `key_unit.csv`_: Relational data for units.
8. `key_value_name.csv`_: Relational data for value names.
9. `key_value_type.csv`_: Relational data for value types.

Value Data Files:
1. `table_graph_ifs.csv`_: Value data for IFS graphs.
2. `table_ifs.csv`_: Value data for IFS.
3. `table_ifs_progress_rates.csv`_: Value data for IFS progress rates.
4. `table_jmp.csv`_: Value data for JMP.

.. _key_actual_commitment.csv: https://media.githubusercontent.com/media/akvo/wash-futures-explorer/refs/heads/main/output_data/key_actual_commitment.csv
.. _key_commitment.csv: https://media.githubusercontent.com/media/akvo/wash-futures-explorer/refs/heads/main/output_data/key_commitment.csv
.. _key_country.csv: https://media.githubusercontent.com/media/akvo/wash-futures-explorer/refs/heads/main/output_data/key_country.csv
.. _key_indicator.csv: https://media.githubusercontent.com/media/akvo/wash-futures-explorer/refs/heads/main/output_data/key_indicator.csv
.. _key_jmp_category.csv: https://media.githubusercontent.com/media/akvo/wash-futures-explorer/refs/heads/main/output_data/key_jmp_category.csv
.. _key_jmp_name.csv: https://media.githubusercontent.com/media/akvo/wash-futures-explorer/refs/heads/main/output_data/key_jmp_name.csv
.. _key_unit.csv: https://media.githubusercontent.com/media/akvo/wash-futures-explorer/refs/heads/main/output_data/key_unit.csv
.. _key_value_name.csv: https://media.githubusercontent.com/media/akvo/wash-futures-explorer/refs/heads/main/output_data/key_value_name.csv
.. _key_value_type.csv: https://media.githubusercontent.com/media/akvo/wash-futures-explorer/refs/heads/main/output_data/key_value_type.csv
.. _table_graph_ifs.csv: https://media.githubusercontent.com/media/akvo/wash-futures-explorer/refs/heads/main/output_data/table_graph_ifs.csv
.. _table_ifs.csv: https://media.githubusercontent.com/media/akvo/wash-futures-explorer/refs/heads/main/output_data/table_ifs.csv
.. _table_ifs_progress_rates.csv: https://media.githubusercontent.com/media/akvo/wash-futures-explorer/refs/heads/main/output_data/table_ifs_progress_rates.csv
.. _table_jmp.csv: https://media.githubusercontent.com/media/akvo/wash-futures-explorer/refs/heads/main/output_data/table_jmp.csv

How to Import Datasets
----------------------
Follow these steps to import the datasets into PowerBI and create relational data:

1. **Open PowerBI Desktop:**
   Launch PowerBI Desktop and create a new report.

2. **Import Data from Web Sources:**
   For each dataset:
   - Go to the "Home" tab and click on "Get Data."
   - Select "Web" as the data source.
   - Copy the relevant link from the dataset list above and paste it into the URL field.
   - Click "OK" to load the data into PowerBI.

3. **Load All Required Datasets:**
   Repeat Step 2 for each file you need to import, including both `key_` and `table_` datasets.

4. **Create Relationships:**
   - Once all datasets are loaded, go to the "Model" view in PowerBI.
   - Refer to the relational data structure described in the [Relationships Documentation](https://dbdocs.io/dedenbangkit/usaid-wssh?view=relationships).
   - Create relationships between the datasets by linking their shared keys. For example:
     - Link `key_country.csv` to `table_ifs.csv` using the `country_id` field.
     - Link `key_indicator.csv` to `table_ifs.csv` using the `indicator_id` field.
   - Ensure all relationships are consistent with the documentation to maintain data integrity.

5. **Set Cardinality and Cross-Filtering:**
   - For each relationship, set the appropriate cardinality (e.g., one-to-many or many-to-one).
   - Enable cross-filtering where needed to ensure data flows correctly in your visualizations.

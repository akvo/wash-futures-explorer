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

1. Relational data for actual commitments: `key_actual_commitment.csv`_
2. Relational data for commitments: `key_commitment.csv`_
3. Relational data for countries: `key_country.csv`_
4. Relational data for indicators: `key_indicator.csv`_
5. Relational data for JMP categories: `key_jmp_category.csv`_
6. Relational data for JMP names: `key_jmp_name.csv`_
7. Relational data for units: `key_unit.csv`_
8. Relational data for value names: `key_value_name.csv`_
9. Relational data for value types: `key_value_type.csv`_

Value Data Files:

1. Value data for IFS graphs: `table_graph_ifs.csv`_
2. Value data for IFS: `table_ifs.csv`_
3. Value data for IFS progress rates: `table_ifs_progress_rates.csv`_
4. Value data for JMP: `table_jmp.csv`_

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

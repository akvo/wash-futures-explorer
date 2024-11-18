============
Output Files
============

The **Output Files** section describes the final output files generated from the data transformation process. These files are stored in the `output_data` directory and will be used in the next phase for data visualisation.

**Note**: Given the large size of these files, we are using **Git LFS** (Large File Storage) to store and manage them in version control. Git LFS is a version control solution for files that exceed Git’s standard storage limits, ensuring that data files can be stored efficiently and accessed as needed.

---

Directory Structure
===================

The output files are organised as follows:

.. code-block:: text

    wash-futures-explorer/output_data
    ├── key_actual_commitment.csv
    ├── key_commitment.csv
    ├── key_country.csv
    ├── key_indicator.csv
    ├── key_jmp_category.csv
    ├── key_jmp_name.csv
    ├── key_unit.csv
    ├── key_value_name.csv
    ├── key_value_type.csv
    ├── table_graph_ifs.csv
    ├── table_ifs.csv
    ├── table_ifs_progress_rates.csv
    └── table_jmp.csv

---

File Descriptions
=================

Each output file serves a specific purpose in supporting WASH data visualisation and analysis.

1. **Key Tables**

    - `key_actual_commitment.csv`: Contains standardised commitment names used in visualisations, e.g., "Halving," "Doubling."
    - `key_commitment.csv`: Stores unique identifiers for commitment types, ensuring consistency in referencing.
    - `key_country.csv`: Maps country names to unique identifiers for easy lookup and filtering.
    - `key_indicator.csv`: Contains indicator names with unique identifiers, used to reference indicators consistently.
    - `key_jmp_category.csv`: Stores JMP categories with standardised names such as "At Least Basic" and "Safely Managed."
    - `key_jmp_name.csv`: Maps JMP names to identifiers, with values like "Water," "Sanitation," and "Water and Sanitation."
    - `key_unit.csv`: Stores units of measurement with unique identifiers for each unit used in the dataset.
    - `key_value_name.csv`: Standardises the names of values, including descriptive terms like "Full Sanitation Access" and "Full Water Access."
    - `key_value_type.csv`: Contains types of values (e.g., "total," "annual_rate_change") to distinguish between different measurements.

2. **Data Tables**

    - `table_graph_ifs.csv`: A table specifically formatted for graph visualisations, with key data fields for WASH indicators and milestone years.
    - `table_ifs.csv`: The main IFs data table, containing processed WASH indicators by country and year for further analysis.
    - `table_ifs_progress_rates.csv`: Contains calculated progress rates, including average yearly increases and full-service indicators, to evaluate WASH progress.
    - `table_jmp.csv`: The final JMP dataset, standardised and processed, ready for integration with other datasets and visualisation.

---

These output files form the foundation for the **Data Visualisation** phase, where key insights and trends in WASH data will be displayed for stakeholders. Each file is stored with standardised keys and values to ensure consistent and reliable data handling.

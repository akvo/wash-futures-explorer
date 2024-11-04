=============================
Data Transformation
=============================

Overview
========

The data transformation for **USAID-Tool-1** is performed within a Jupyter Notebook, located in the `src` folder as `data_transform.ipynb`. This notebook prepares the raw data for visualization by performing multiple transformation steps on the IFs and JMP datasets, which are essential for calculating progress rates and organizing WASH indicators.

Required libraries are listed in the `requirements.txt` file in the `src` folder.

---

Transformation Steps
====================

1. Preparation
--------------

### 1.A. Data Input and Output
- **Input Data**: The notebook reads IFs and JMP datasets from the `input_data` directory.
- **Output Data**: The transformed data tables and graphs are saved to the `output` directory for PowerBI visualization.

### 1.B. Common Functions
- **Utility Functions**: Functions for data cleaning, filtering, and mapping values across datasets.
- **Key Operations**: Functions to merge, remap, and categorize indicators and units.

### 1.C. Key Table Generator
- **Key Tables**: Generates tables to map indicators, units, value names, and other key data for consistent referencing across datasets.

### 1.D. Country Mapping
- **Mapping Function**: Creates a standardized mapping of country names and codes between IFs and JMP datasets.

2. IFs Dataset
--------------

### 2.A. IFs Functions
- **Helper Functions**: Functions specific to IFs data transformations, such as combining indicators, remapping values, and cleaning data.

### 2.B. IFs Data Processing

#### 2.B.1 Combine, Filter, and Remap IFs Values
- **Combine Data**: Aggregates values based on key indicators.
- **Filter Data**: Applies filters to retain relevant data.
- **Remap Values**: Remaps values to align with JMP categories.

#### 2.B.2 IFs Data Cleanup
- **Data Cleaning**: Removes duplicates, handles missing values, and standardizes formats.

### 2.C. IFs Table of Keys

#### 2.C.1 Indicators
- **Indicators Table**: Maps IFs indicators to WASH-specific categories.

#### 2.C.2 Units
- **Units Table**: Standardizes units of measurement across indicators.

#### 2.C.3 Value Names
- **Value Names Table**: Maps raw IFs values to interpretable names.

#### 2.C.4 JMP Categories
- **JMP Category Mapping**: Aligns IFs indicators with JMP categories for consistency.

#### 2.C.5 JMP Names Table (Custom)
- **Custom Mapping**: Creates a unique name table to facilitate lookup between IFs and JMP names.

#### 2.C.6 Commitments
- **Commitment Table**: Defines target values and timelines for progress tracking.

#### 2.C.7 Country
- **Country Mapping Table**: Final mapping between country codes and names in IFs and JMP datasets.

### 2.D. IFs Table Results

#### 2.D.1 Custom Table Mapping (JMP Name)
- **Custom Mapping**: Uses JMP names for easier integration into JMP datasets.

#### 2.D.2 IFs Key Table Mapping
- **Key Table Mapping**: Maps keys generated for indicators, units, and values back to IFs data.

#### 2.D.3 IFs Final Result
- **Final Table**: Produces the cleaned, mapped IFs dataset ready for analysis.

#### 2.D.4 Save IFs Table
- **Save Data**: Exports the final IFs table to the output folder.

#### 2.D.5 Save IFs Graph Table
- **Graph Table Export**: Saves a version of the IFs table specifically formatted for graphing in PowerBI.

### 2.E. Progress Rates

#### 2.E.1 Progress Rates Functions
- **Calculation Functions**: Functions for computing yearly and aggregate progress rates.

#### 2.E.2 Progress Rates Collections
- **Collection Tables**: Stores progress rates for different indicators and categories.

#### 2.E.3 Progress Rates Year Filters
- **Yearly Filters**: Filters progress rates by year for trend analysis.

#### 2.E.4 Progress Rates Key Table Mapping
- **Mapping**: Maps calculated progress rates to predefined keys.

#### 2.E.5 Save Progress Rates Table
- **Save Table**: Exports the progress rates table to the output folder.

3. JMP Dataset
--------------

### 3.A. JMP Data Processing

#### 3.A.1 Rename Columns
- **Column Renaming**: Standardizes column names in JMP data for compatibility.

#### 3.A.2 Categorize Values
- **Value Categorization**: Assigns each value to a relevant category for analysis.

### 3.B. JMP Table Keys

#### 3.B.1 JMP Categories (Retry)
- **Category Mapping**: Retries the category mapping to ensure consistency with IFs data.

#### 3.B.2 JMP Value Types
- **Value Types**: Defines and maps value types for JMP indicators.

### 3.C. JMP Table Results

#### 3.C.1 JMP Key Table Mapping
- **Mapping**: Maps JMP keys for easy integration with IFs data.

#### 3.C.2 JMP Data Cleanup
- **Cleanup Process**: Cleans and formats the JMP dataset for analysis.

#### 3.C.3 JMP Final Result
- **Final Table**: Creates the final JMP dataset, ready for analysis and comparison.

#### 3.C.4 Save JMP Table
- **Save Data**: Exports the JMP final table to the output folder.

4. Post Data Transformation
---------------------------

### 4.A. Post Data Functions
- **Additional Processing**: Functions to further clean and standardize the transformed data.

### 4.B. Replace Key Tables with Predefined Strings

#### 4.B.1 Replace Commitment Values
- **Commitment Replacement**: Replaces commitment values with predefined strings for clarity.

#### 4.B.2 Replace JMP Category
- **Category Replacement**: Maps JMP categories to predefined strings.

#### 4.B.3 Replace Value Name
- **Value Name Replacement**: Standardizes value names across the datasets.

---

Refer to `data_visualization.rst` for details on importing the transformed data into PowerBI and generating visualizations.

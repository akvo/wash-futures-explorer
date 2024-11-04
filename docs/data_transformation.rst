=============================
Data Transformation
=============================

Overview
========

The data transformation for **USAID-Tool-1** is performed within a Jupyter Notebook, located in the `src` folder as `data_transform.ipynb`. This notebook prepares the raw data for visualization by performing multiple transformation steps on the IFs and JMP datasets, which are essential for calculating progress rates and organizing WASH indicators.

Required libraries are listed in the `requirements.txt` file in the `src` folder.

Transformation Steps
====================

.. toctree::
   :maxdepth: 2
   :caption: Transformation Steps

   1_code_preparation
   2_code_ifs_dataset
   3_code_jmp_dataset
   3_code_post_data_transformation

---

Refer to `data_visualization.rst` for details on importing the transformed data into PowerBI and generating visualizations.

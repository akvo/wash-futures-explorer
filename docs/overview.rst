========
Overview
========

Purpose
=======

**USAID-Tool-1** is designed to monitor and illustrate the acceleration needed to achieve universal access to clean water and sanitation, based on USAID’s system strengthening efforts. Using data from the **International Futures (IF) model**, the tool combines Python-based data transformations with PowerBI visualizations to support data-driven insights and planning.

Objectives
==========

1. **Monitor WASH Progress**: Track the amount and rate of WASH (Water, Sanitation, and Hygiene) progress as a result of USAID’s system strengthening efforts.
2. **Evaluate Broader Impact**: Understand and improve the impact of WASH programming beyond USAID’s direct interventions throughout the Global Water Strategy period.
3. **Pilot for Replication**: Provide recommendations on the best ‘lean’ monitoring approach that can be effectively replicated in 22 countries.

Components
==========

USAID-Tool-1 consists of three main components:

1. **Data Input**: Raw data derived from the IF model, household surveys, and secondary sources, containing historical and projected indicators related to water and sanitation.
2. **Data Transformation**: A Jupyter Notebook processes and structures the data, preparing it for visualization. The notebook includes steps for data cleaning, calculation of progress rates, and structuring data for PowerBI.
3. **Data Visualization**: PowerBI dashboards display trends, comparisons, and projections in an interactive format, providing stakeholders with actionable insights.

Usage Scenarios
===============

USAID-Tool-1 is suitable for use by:
- **Policy Makers**: To evaluate WASH progress and identify priority areas for intervention.
- **Development Organizations**: To support strategy development, intervention adjustments, and investment planning.
- **Data Analysts**: To explore and analyze data on clean water and sanitation access under various scenarios.

System Requirements
===================

- **Python**: Version 3.7 or higher, with packages listed in `requirements.txt`.
- **Jupyter Notebook**: For running data transformation scripts in an interactive environment.
- **PowerBI**: PowerBI Desktop or a compatible version for data visualization.

Git Repository and Git LFS Configuration
========================================

The USAID-Tool-1 project is managed using Git, with Git Large File Storage (Git LFS) to handle large data files efficiently. Git LFS is particularly useful for tracking and storing files that exceed Git's regular size limits, ensuring that large files (such as CSV, XLSX, and PBIX) are accessible without slowing down the repository.

Git LFS Configuration
---------------------

The following `.gitattributes` configuration is used to track large files in the repository. This configuration ensures that specific file types are managed by Git LFS instead of being stored directly in the Git repository:

.. code-block:: text

    *.csv filter=lfs diff=lfs merge=lfs -text
    *.xlsx filter=lfs diff=lfs merge=lfs -text
    *.pbix filter=lfs diff=lfs merge=lfs -text

Benefits of Git LFS for USAID-Tool-1
------------------------------------

Using Git LFS allows us to:
- Track large data files (such as CSV, Excel, and PowerBI files) efficiently.
- Improve repository performance by keeping large files out of the main Git history.
- Facilitate data updates and sharing within the project, as large files are versioned and stored externally.

To clone the repository with Git LFS, ensure Git LFS is installed on your system. Once installed, run:

.. code-block:: bash

    git lfs install
    git clone <repository-url>

After cloning, the large files will be downloaded as needed when you check out specific branches or commits.

---

For more detailed information, refer to the individual sections on data input, transformation, and visualization. This overview provides a foundation for understanding the purpose, objectives, and methodology of USAID-Tool-1.

==========
Data Input
==========

Overview
========

The data for **WASH Futures Explorer** is sourced from the **International Futures (IFs)** model, a free and open-source quantitative tool designed to help users think systematically about long-term global futures. Developed by the Frederick S. Pardee Center for International Futures, IFs is used by policymakers, researchers, and students worldwide to explore potential global trends, development goals, and targets. The IFs model offers insights into various indicators, including those relevant to water, sanitation, and hygiene (WASH) initiatives.

.. image:: https://korbel.du.edu/sites/default/files/IFsOverviewChart.jpg
   :alt: International Futures (IFs) Overview Chart
   :align: center

In the IFs model, WASH intervention scenarios refers to different policy interventions or changes in key drivers that users can input. These might include investments in infrastructure, policy reforms, or public health campaigns aimed at improving WASH services. Next, the model uses complex algorithms to simulate how these interventions would impact various indicators. This includes changes in access to water and sanitation, health outcomes (e.g., reduction in waterborne diseases), and overall quality of life. The model allows for the comparison of multiple scenarios side-by-side. Users can see how different levels of investment or policy changes might lead to different outcomes, helping policymakers understand the potential benefits and trade-offs.

.. note::
   For more information about the IFs model, visit the `Pardee Wiki page <https://korbel.du.edu/pardee/content/download-ifs>`_.

.. image:: ./_static/images/flow-chart-of-water-and-sanitation-model.png
   :alt: Flow Chart of Water and Sanitation Model
   :align: center


Data Download
=============

To download the IFs model data, follow these steps:

1. Visit `this link <https://korbel.du.edu/pardee/content/download-ifs>`_ and download the data installer package for Windows: `IFs with Pardee 8.28 (July 2022) <https://ifs02.du.edu/IFs%20with%20Pardee%208_28%20July%2022%202024.zip>`_.
2. Extract the package and install the IFs model on a Windows machine.
3. Navigate to the data export options within the IFs tool to export relevant datasets.

Data Files
==========

The following files are included in **WASH Futures Explorer** as primary data sources. Each file represents a different WASH or socio-economic indicator that will be used to analyze progress toward clean water and sanitation access:

- **Deaths by Category of Cause - Millions (Diarrhea)**: `01. Deaths by Category of Cause - Millions (2nd Dimensions = Diarrhea).csv`
- **Poverty Headcount (< $2.15 per Day)**: `06. Poverty Headcount less than $2.15 per Day, Log Normal - Millions.csv`
- **State Failure Instability Event**: `08. State Failure Instability Event - IFs Index.csv`
- **Governance Effectiveness (WB Index)**: `11. Governance Effectiveness - WB index.csv`
- **Sanitation Access (% of Population)**: `13. Sanitation Services, Access, percent of population (2nd Dimensions = Basic + Safely Managed).csv`
- **Sanitation Access (Millions of People)**: `14. Sanitation Services, Access, Number of people, million (2nd Dimensions = Basic + Safely Managed).csv`
- **Sanitation Expenditure (Capital, Billion $)**: `15. Sanitation Services, Expenditure, Capital, Billion $ (2nd Dimensions = Basic + Safely Managed).csv`
- **Sanitation Expenditure (Maintenance, Billion $)**: `16. Sanitation Services, Expenditure, Maintenance, Billion $ (2nd Dimensions = Basic + Safely Managed).csv`
- **Water Access (% of Population)**: `17. Water Services, Access, percent of population (2nd Dimensions = Basic + Safely Managed).csv`
- **Water Access (Millions of People)**: `18. Water Services, Access, Number of people, million (2nd Dimensions = Basic + Safely Managed).csv`
- **Water Expenditure (Capital, Billion $)**: `19. Water Services, Expenditure, Capital, Billion $ (2nd Dimensions = Basic + Safely Managed).csv`
- **Water Expenditure (Maintenance, Billion $)**: `20. Water Services, Expenditure, Maintenance, Billion $ (2nd Dimensions = Basic + Safely Managed).csv`
- **Gross Domestic Product (GDP, PPP, Billion $)**: `23. GDP (PPP) - Billion dollars.csv`
- **Stunted Children (Million)**: `24. Stunted children, History and Forecast - Million.csv`
- **Malnourished Children (Million)**: `26. Malnourished Children, Headcount - Millions.csv`

Data Organisation
=================

All data files are organised under the `input_data` directory as follows:

- **input_data/IFs**: Contains the IFs model data files listed above.
- **input_data/JMP**: Contains additional data from the Joint Monitoring Programme (JMP), specifically the file `JMP-2023-world.xlsx`, which provides complementary information on WASH indicators.

---


.. note::
   Refer to the `data_transformation.rst` section for details on how these data files are processed and prepared for visualisation within **WASH Futures Explorer**.

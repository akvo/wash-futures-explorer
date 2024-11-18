========
Overview
========

Purpose
=======

**WASH Futures Explorer** is designed to monitor and illustrate the acceleration needed to achieve universal access to clean water and sanitation, based on USAID’s system strengthening efforts. USAID suggested using **the International Futures (IFs)** model from the University of Denver’s Pardee Institute for International Development or a similar model. The IFs Model was chosen due to its widespread use by USAID and other development organizations, as well as its ability to adjust parameters related to WASH inputs. Using data from the International Futures (IFs) model, the tool combines Python-based data transformations with PowerBI visualisations to support data-driven insights and planning.

The WASH Futures Explorer enables users to compare different WASH intervention scenarios and assess their impact on various development indicators such as water and sanitation accessibility, health outcomes, prosperity and governance. Based on the data from IFs model, the purpose of WASH Futures Explorer is to give some simple and clear talking points to WASH planners on why their government should invest more in WASH and what potential benefit it has for other sectors.

Objectives
==========

The WASH Futures Explorer Tool will guide you through a step-by-step process to explore various WASH intervention scenarios. With the three steps, it helps you to reach three objectives :

1. Business as Usual
   The Business as Usual page serves as the baseline. It assumes that current trends in WASH access, investments, and policies continue without significant changes. This baseline scenario projects future conditions based on historical data and existing trends, providing a reference point against which other scenarios can be compared. This provides a snapshot of the current trajectory (including WASH access levels and average progress rates) and the year in which universal access is predicted to be reached.

2. Explore the Full WASH Access Scenario
   Full WASH Access Scenarios envision a future where universal access to water and sanitation is achieved by specific target years. These scenarios set ambitious goals for full access and simulate the outcomes if these goals are met by 2030 or 2050. These scenarios demonstrate the potential benefits of achieving full WASH access within specified timeframes, highlighting the long-term improvements in health, prosperity and governance that could result from such ambitious efforts. The analysis can be disaggregated based on sector (sanitation, water, or both), access level (at least basic or safely managed), year (2030 or 2050), and country. The impact table shows how each unique scenario impacts health, prosperity, and governance indicators, compared to the Business as Usual scenario.

3. Investigate the Scenario Explorer
   Once the user has seen what it takes (in terms of acceleration) to have full access by 2030 or 2050, it might not be realistic with the available funding. So the scenario Explorer explores the impact of varying the progress rate of WASH access levels. Users can model different levels of intervention effectiveness by adjusting the national WASH budget commitment to water or sanitation services or both. These scenarios should help users understand the potential outcomes in other sectors, illustrating how even small changes in progress rates can lead to significant differences in other sectors over time. The commitment can be halved, doubled, quadrupled, or increased by six-fold. Each adjustment dynamically recalculates projected impacts on key indicators, such as health outcomes, GDP growth, and governance stability, providing a clear view of how varying investment levels can drive progress in WASH access and broader development goals. For each scenario, the results are compared with the Business as Usual snapshot.




Components
==========

WASH Futures Explorer tool consists of three main components regarding data processing:


1. **Data Input**: Raw data downloaded from the IFs model, containing historical and projected indicators related to water and sanitation, health, prosperity and governance.
2. **Data Transformation**: A Jupyter Notebook processes and structures the data, preparing it for visualisation. The notebook includes steps for data cleaning, calculation of progress rates, and structuring data for PowerBI.
3. **Data Visualisation**: PowerBI dashboards display trends, comparisons, and projections in an interactive format, providing stakeholders with actionable insights.

Usage Scenarios
===============

WASH Futures Explorer is suitable for policy makers, WASH planners and implementers to:

- Illustrate the broader impact of WASH initiatives on national development.
- Demonstrate the benefits of investing in WASH on development outcomes.
- Understand the impact of different WASH commitments on access rates and broader development results.
- Set realistic and achievable goals for WASH progress.
- Make data-driven decisions for future WASH initiatives.

System Requirements
===================

- **Python**: Version 3.7 or higher, with packages listed in `requirements.txt`.
- **Jupyter Notebook**: For running data transformation scripts in an interactive environment.
- **PowerBI**: PowerBI Desktop or a compatible version for data visualisation.

Git Repository and Git LFS Configuration
========================================

The WASH Futures Explorer project is managed using Git, with Git Large File Storage (Git LFS) to handle large data files efficiently. Git LFS is particularly useful for tracking and storing files that exceed Git's regular size limits, ensuring that large files (such as CSV, XLSX, and PBIX) are accessible without slowing down the repository.

Git LFS Configuration
---------------------

The following `.gitattributes` configuration is used to track large files in the repository. This configuration ensures that specific file types are managed by Git LFS instead of being stored directly in the Git repository:

.. code-block:: text

    *.csv filter=lfs diff=lfs merge=lfs -text
    *.xlsx filter=lfs diff=lfs merge=lfs -text
    *.pbix filter=lfs diff=lfs merge=lfs -text

Benefits of Git LFS for WASH Futures Explorer
---------------------------------------------

Using Git LFS allows us to:
- Track large data files (such as CSV, Excel, and PowerBI files) efficiently.
- Improve repository performance by keeping large files out of the main Git history.
- Facilitate data updates and sharing within the project, as large files are versioned and stored externally.

To clone the repository with Git LFS, ensure Git LFS is installed on your system. Once installed, run:

.. code-block:: bash

    git lfs install
    git clone <repository-url>

After cloning, the large files will be downloaded as needed when you check out specific branches or commits.

.. note::
   For more detailed information, refer to the individual sections on data input, transformation, and visualisation. This overview provides a foundation for understanding the purpose, objectives, and methodology of WASH Futures Explorer.


Sustainability Plan
===================

The main sustainability plan for this tool is its reproducibility, so if it is not actively maintained after the end of WSSH D&A, people can still create their own version, adapted to their own processes.

Embedding the Tool Into USAID Systems
-------------------------------------
In order to publish PowerBI dashboards on the PowerBI online service, a PowerBI subscription is required. We believe that a PowerBI Pro subscription is sufficient. It is hosted on WSSH D&A prime’s account and shared on the WSSH D&A webpage on the USAID Global Waters website through an iframe, together with the user documentation and tutorial video. It will be maintained during the length of the program and for one year after the program ends.

Talking Points, Capacity Building and Other Uses From The Mission
-----------------------------------------------------------------
We anticipate that USAID Missions or USAID HQ might want some adaptation to the tool based on some specific programs or planning requirements. There are various different ways to present the same data, or introduce different timelines. These custom options could be addressed through buy-ins.

Continuous improvement
----------------------
A feedback form has been added to the tool and it is expected that we will gather feedback on a continuous basis.  We plan to run 1 to 2 updates a year once we agree on the priority in the feedback received. We anticipate that some re-running of the data will be needed in year 3 to update with latest model data and JMP data.

Licensing
---------

`GNU General Public License <https://github.com/akvo/usaid-wssh/blob/main/LICENSE>`_.

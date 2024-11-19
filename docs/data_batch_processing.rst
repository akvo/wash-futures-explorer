=====================
Data Batch Processing
=====================

**Batch processing in the International Futures model - WASH Futures Explorer This document describes how to perform batch processing in the International Futures model.**

The International Futures model
===============================

The International Futures (IFs) model is a comprehensive forecasting tool used for scenario analysis, enabling users to explore and shape global futures by examining interactions between human, social, and environmental systems over time. It models long-term change across economies, societies, and the environment, facilitating strategic planning and understanding of possible future outcomes. With a database spanning from 1960 and projections up to 2100, IFs covers 186 countries and forecasts numerous variables, making it an invaluable asset for analysing global policy scenarios and addressing grand challenges. For more details, visit here.

Use of the International Futures (IFs) model within USAID WSSH Data & Analytics program Akvo’s role within the USAID WSSH project, which is led by Segura, includes creating a tool (the WASH Futures Explorer) that helps USAID WASH practitioners to better understand:

- The current WASH situation in USAID’s high-priority  key countries (HPCs).
- The effect of changingWASH investments or policies on the  access  to Water and Sanitation services.
- The effect of changing WASH investments or policies on key health, prosperity, and governance indicators.

For more info regarding the International Futures Model, please check:

.. raw:: html

         <div style="position: relative; padding-bottom: 56.25%; height: 0; overflow: hidden; max-width: 100%; height: auto;">
         <iframe src="https://www.youtube.com/embed/elHWDJIizvQ?si=AII7YuY12a9zYsA7" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe>
         </div>

Current WASH Futures Explorer: `PowerBI Link <https://app.powerbi.com/view?r=eyJrIjoiMjg3ZDc2ZDMtNGRlOC00MjMzLWFhODAtMjVhZTkyZjBjZjNmIiwidCI6ImIxNzBlMTE1LWRjM2QtNGU5Mi04NWJlLWU0YjMwMDljNWRjMiIsImMiOjl9>`_

Why Batch Processing?
=====================
Batch processing refers to the bulk download of data - in this case scenario runs of the IFs model. The desktop version of the IFs model has the ability to do batch processing, which is not possible in the online version. In other words, downloading a large amount of data  using the online version is a lengthy process (due to repetitive clicking, and in part because the online version is more error prone). With batch processing, many scenarios can be run simultaneously, thus speeding up the process.

.. note::
   The IFs desktop model runs only on Windows machines and is not compatible with Mac or Linux Operating System.

How to Install the International Futures Model for Batch Processing
===================================================================

Go to `IFs Download Page <https://korbel.du.edu/pardee/content/download-ifs>`_ and click on the latest IFs model to download it locally , for example "IFs V8.06 (September 2023)".

Step 1: Create Scenario Files
*****************************

A scenario file is a text file (with extension .sce) that describes the scenario to be run in the IFs model. We use 36 scenarios:

.. note::
   High-priority countries include: Dem. Republic of the Congo, Ethiopia, Ghana, Guatemala, Haiti, India, Indonesia, Kenya, Liberia, Madagascar, Malawi, Mali, Mozambique, Nepal, Nigeria, Philippines, Rwanda, Senegal, Sudan South, Tanzania, Uganda, Zambia.


Step 2: Batch Run All Scenario Files
************************************

#. Hover over "Scenario Analysis" and click on "Batch Run".
#. In the page that appears, follow the steps in the screenshot below:
   #. Unfold the folder **a User Defined Scenario** by clicking in the triangular icon on the left.
   #. Select the scenario of interest.
   #. Change **Run Year** (the maximum is 2100).
   #. Click on **Select**
#. Wait until you see the text **International Futures has finished running one or more scenarios/cases.** On the screen, click **Continue** to come back to the software’s main menu.


Step 3: Download the Output Files
*********************************

For all scenarios, some .csv files have to be generated for all focus indicators. For the WASH Futures Explorer, this is the complete list of indicators we used.

=====================
Data Batch Processing
=====================

.. note::
   This page describes how to perform batch processing in **the International Futures model**.

The International Futures model
===============================

The International Futures (IFs) model is a comprehensive forecasting tool used for scenario analysis, enabling users to explore and shape global futures by examining interactions between human, social, and environmental systems over time. It models long-term change across economies, societies, and the environment, facilitating strategic planning and understanding of possible future outcomes. With a database spanning from 1960 and projections up to 2100, IFs covers 186 countries and forecasts numerous variables, making it an invaluable asset for analysing global policy scenarios and addressing grand challenges. For more details, visit here.

Use of the International Futures (IFs) model within USAID WSSH Data & Analytics program Akvo’s role within the USAID WSSH project, which is led by Segura, includes creating a tool (the WASH Futures Explorer) that helps USAID WASH practitioners to better understand:

- The current WASH situation in USAID’s high-priority  key countries (HPCs).
- The effect of changingWASH investments or policies on the  access  to Water and Sanitation services.
- The effect of changing WASH investments or policies on key health, prosperity, and governance indicators.

.. note::
   For more info regarding the International Futures Model, please check: `African Futures Project: Water & Sanitation <https://www.youtube.com/watch?v=elHWDJIizvQ>`_

.. note::
   Current WASH Futures Explorer: `PowerBI Link <https://app.powerbi.com/view?r=eyJrIjoiMjg3ZDc2ZDMtNGRlOC00MjMzLWFhODAtMjVhZTkyZjBjZjNmIiwidCI6ImIxNzBlMTE1LWRjM2QtNGU5Mi04NWJlLWU0YjMwMDljNWRjMiIsImMiOjl9>`_

Why Batch Processing?
=====================
Batch processing refers to the bulk download of data - in this case scenario runs of the IFs model. The desktop version of the IFs model has the ability to do batch processing, which is not possible in the online version. In other words, downloading a large amount of data  using the online version is a lengthy process (due to repetitive clicking, and in part because the online version is more error prone). With batch processing, many scenarios can be run simultaneously, thus speeding up the process.

.. note::
   The IFs desktop model runs only on Windows machines and is not compatible with Mac or Linux Operating System.

How to Install the International Futures Model for Batch Processing
===================================================================

Go to `IFs Download Page <https://korbel.du.edu/pardee/content/download-ifs>`_ and click on the latest IFs model to download it locally , for example `IFs V8.06 (September 2023) <https://ifsfiles.du.edu/IFs%20with%20Pardee%208_06%20September%2022%202023.zip>`_.

Step 1: Create Scenario Files
******************************

A scenario file is a text file (with extension .sce) that describes the scenario to be run in the IFs model. We use 36 scenarios:

.. note::
   High-priority countries include: Dem. Republic of the Congo, Ethiopia, Ghana, Guatemala, Haiti, India, Indonesia, Kenya, Liberia, Madagascar, Malawi, Mali, Mozambique, Nepal, Nigeria, Philippines, Rwanda, Senegal, Sudan South, Tanzania, Uganda, Zambia.

.. csv-table:: Scenario of reaching water and sanitation in 2030 and 2050
   :header: "N°", "Scenario (parameter)", "Code", "Description"
   :widths: 2, 28, 15, 55

    1,"sanithhbasictrgtyr = 12, shift years = 6",FS_ALB_2030,Full access to at least basic sanitation services in 2030
    2,"sanithhbasictrgtyr = 32, shift years = 6",FS_ALB_2050,Full access to at least basic sanitation services in 2050
    3,"sanithhsafetrgtyr = 12, shift years = 6",FS_SM_2030,Full access to safely managed sanitation services in 2030
    4,"sanithhsafetrgtyr = 32, shift years = 6",FS_SM_2050,Full access to safely managed sanitation services in 2050
    5,"waterhhbasictrgtyr = 12, shift years = 6",FW_ALB_2030,Full access to at least basic water services in 2030
    6,"waterhhbasictrgtyr = 32, shift years = 6",FW_ALB_2050,Full access to at least basic water services in 2050
    7,"waterhhsafetrgtyr = 12, shift years = 6",FW_SM_2030,Full access to safely managed water services in 2030
    8,"waterhhsafetrgtyr = 32, shift years = 6",FW_SM_2050,Full access to safely managed water services in 2050
    9,"(waterhhbasictrgtyr = 12, shift years = 6) & (sanithhbasictrgtyr = 12, shift years = 6)",FWS_ALB_2030,Full access to at least basic water & sanitation services in 2030
    10,"(waterhhbasictrgtyr = 32, shift years = 6) & (sanithhbasictrgtyr = 32, shift years = 6)",FWS_ALB_2050,Full access to at least basic water & sanitation services in 2050
    11,"(waterhhsafetrgtyr = 12, shift years = 6) & (sanithhsafetrgtyr = 12, shift years = 6)",FWS_SM_2030,Full access to safely managed water & sanitation services in 2030
    12,"(waterhhsafetrgtyr = 32, shift years = 6) & (sanithhsafetrgtyr = 32, shift years = 6)",FWS_SM_2050,Full access to safely managed water & sanitation services in 2050

.. csv-table:: Scenarios for decreasing/increasing water and sanitation in 2030 and 2050
   :header: "N°", "Scenario (parameter)", "Code", "Description"
   :widths: 2, 28, 15, 55

    13,"sanithhm = 0.5, basic, total, shift years = 6",SI_BS_0_5x,Increase basic sanitation services by factor 0.5
    14,"sanithhm = 2, basic, total, shift years = 6",SI_BS_2x,Increase basic sanitation services by factor 2
    15,"sanithhm = 4, basic, total, shift years = 6",SI_BS_4x,Increase basic sanitation services by factor 4
    16,"sanithhm = 6, basic, total, shift years = 6",SI_BS_6x,Increase basic sanitation services by factor 6
    17,"sanithhm = 0.5, safely managed, total, shift years = 6",SI_SM_0_5x,Increase safely managed sanitation services by factor 0.5
    18,"sanithhm = 2, safely managed, total, shift years = 6",SI_SM_2x,Increase safely managed sanitation services by factor 2
    19,"sanithhm = 4, safely managed, total, shift years = 6",SI_SM_4x,Increase safely managed sanitation services by factor 4
    20,"sanithhm = 6, safely managed, total, shift years = 6",SI_SM_6x,Increase safely managed sanitation services by factor 6
    21,"waterhhm = 0.5, basic, total, shift years = 6",WI_BS_0_5x,Increase basic water services by factor 0.5
    22,"waterhhm = 2, basic, total, shift years = 6",WI_BS_2x,Increase basic water services by factor 2
    23,"waterhhm = 4, basic, total, shift years = 6",WI_BS_4x,Increase basic sanitation services by factor 4
    24,"waterhhm = 6, basic, total, shift years = 6",WI_BS_6x,Increase basic water services by factor 6
    25,"waterhhm = 0.5, safely managed, total, shift years = 6",WI_SM_0_5x,Increase safely managed water services by factor 0.5
    26,"waterhhm = 2, safely managed, total, shift years = 6",WI_SM_2x,Increase safely managed water services by factor 2
    27,"waterhhm = 4, safely managed, total, shift years = 6",WI_SM_4x,Increase safely managed water services by factor 4
    28,"waterhhm = 6, safely managed, total, shift years = 6",WI_SM_6x,Increase safely managed water services by factor 6
    29,"(waterhhm = 0.5, basic, total, shift years = 6) & (sanithhm = 0.5, basic, total, shift years = 6)",WSI_BS_0_5x,Increase basic water & sanitation services by factor 0.5
    30,"(waterhhm = 2, basic, total, shift years = 6) & (sanithhm = 2, basic, total, shift years = 6)",WSI_BS_2x,Increase basic water & sanitation services by factor 2
    31,"(waterhhm = 4, basic, total, shift years = 6) & (sanithhm = 4, basic, total, shift years = 6)",WSI_BS_4x,Increase basic water & sanitation services by factor 4
    32,"(waterhhm = 6, basic, total, shift years = 6) & (sanithhm = 6, basic, total, shift years = 6)",WSI_BS_6x,Increase basic water water & services by factor 6
    33,"(waterhhm = 0.5, safely managed, total, shift years = 6) & (sanithhm = 0.5, safely managed, total, shift years = 6)",WSI_SM_0_5x,Increase safely managed water & sanitation services by factor 0.5
    34,"(waterhhm = 2, safely managed, total, shift years = 6) & (sanithhm = 2, safely managed, total, shift years = 6)",WSI_SM_2x,Increase safely managed water & sanitation services by factor 2
    35,"(waterhhm = 4, safely managed, total, shift years = 6) & (sanithhm = 4, safely managed, total, shift years = 6)",WSI_SM_4x,Increase safely managed water & sanitation services by factor 4
    36,"(waterhhm = 6, safely managed, total, shift years = 6) & (sanithhm = 6, safely managed, total, shift years = 6)",WSI_SM_6x,Increase safely managed water & sanitation services by factor 6


Step 2: Batch Run All Scenario Files
************************************

#. Hover over **Scenario Analysis** and click on **Batch Run**.

#. In the page that appears, follow the steps in the screenshot below:

   #. Unfold the folder **a User Defined Scenario** by clicking in the triangular icon on the left.

   #. Select the scenario of interest.

   #. Change **Run Year** (the maximum is 2100).

   #. Click on **Select**

#. Wait until you see the text **International Futures has finished running one or more scenarios/cases.** On the screen, click **Continue** to come back to the software’s main menu.


Step 3: Download the Output Files
*********************************

For all scenarios, some .csv files have to be generated for all focus indicators. For the WASH Futures Explorer, this is the complete list of indicators we used.

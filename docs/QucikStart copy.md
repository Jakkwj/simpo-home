---
sidebar_position: 2
---

# Qucik Start

## Getting Started
The 3 essential elements of **SIMPO** are:
- **BioModel** (model).
- **DataSet** (data).
- **Project** (solution).

The steps of a completed calcualtion process are:

- [Step 1](#step_1): install the calcualtion client on your computer.
- [Step 2](#step_2): create a **BioModel**.
- [Step 3](#step_3): create a **DataSet**.
- [Step 4](#step_4): create a **Project** to combine **BioModel** and **DataSet**.
- [Step 5](#step_5): select a calculation engine (Simulaiton/Sensitivity/Uncertainty/Estimation) to solve them.

<!--  "attention", "caution", "danger", "error", "hint", "important", "note", "tip", "warning" -->

:::tip The Easiest Way

After installing the client, clone a Project from the public Project repository is the easiest way to do the whole thing. Since this action will also clone the correspoding BioModel and Dataset, you can just start the calculaiton and wait for the results after this cloning.

:::

-------

<!-- :::danger Take care

This action is dangerous
::: -->


## <a id="step_1"></a>Step 1: Install



Download the calcualtion client and install it:

- <a href="/client/sludge_client_setup_0.2.0.exe" target="_blank" download>Windows</a>
- <a href="/client/sludge_client_setup_0.2.0.sh" target="_blank" download>Ubuntu</a>: download and run: <code>sudo chmod +x sludge_client_setup.sh && ./sludge_client_setup.sh</code>

<!-- [Markdown](/client/sludge_client_setup_0.2.0.exe) -->




-------


## <a id="step_2a"></a>Step 2a: Sign Up and Sign In

Sign Up and Sign In...


-------



## <a id="step_2"></a>Step 2: Create a BioModel

There are a few ways to create a BioModel (choose 1 from 4 in below):

1. Create an empty BioModel, edit and parsed save the detial later to make it work.
    - Add new components.
    - Add new paramters.
    - Add new processes (in Matrix tab).

  <br />
  <div align="center" style={{marginTop: "0vh"}}>
    <img src="/img/quick_start/step2/1.gif" width="80%"/>
  </div>

1. Or create a BioModel from a: <a href="/template_file/BioModel.xlsx" target="_blank" download>template xlsx file</a>

  <div align="center" style={{marginTop: "0vh"}}>
    <img src="/img/quick_start/step2/2.gif" width="80%"/>
  </div>

1. Or clone a BioModel from the public BioModel repository.

  <div align="center" style={{marginTop: "0vh"}}>
    <img src="/img/quick_start/step2/3.gif" width="80%"/>
  </div>

1. Or clone a Project from the public Project repository would also clone the correspoding BioModel.

  <div align="center" style={{marginTop: "0vh"}}>
    <img src="/img/quick_start/step2/4.gif" width="80%"/>
  </div>


<!-- ..    - Before finished the input, temparary save it to avoid lost the input.
..    - After finished the input, parsed save it to make sure all the input formats are correct.
..    - Optional: release different version to reference it.
   .. 2. Or create a BioModel from a `template xlsx file <http://111.230.245.215/api/download/template/biomodel>`_ while creating.
.. Detial
.. --------------

.. If you create an empty BioModel, you have to make the detial to make it work. -->


-------

## <a id="step_3"></a>Step 3: Create a DataSet

There are a few ways to create a DataSet (choose 1 from 5 in below):

1. Create an empty DataSet, edit and parsed save the detial later to make it work.

    - Add new targets.
    - Add new tanks.
    - Optional: add new links (inflows, flows and connections). This is unnecessary if you only get independent tanks.

  <br />
  <div align="center" style={{marginTop: "0vh"}}>
    <img src="/img/quick_start/step3/1.gif" width="80%"/>
  </div>

1. Or create a DataSet from a preset layout and/or target (from a BioModel).

  <div align="center" style={{marginTop: "0vh"}}>
    <img src="/img/quick_start/step3/2.gif" width="80%"/>
  </div>

1. Or create a DataSet from a: <a href="/template_file/DataSet.xlsx" target="_blank" download>template xlsx file</a>

  <div align="center" style={{marginTop: "0vh"}}>
    <img src="/img/quick_start/step3/3.gif" width="80%"/>
  </div>

1. Or clone a DataSet from the public DataSet repository.

  <div align="center" style={{marginTop: "0vh"}}>
    <img src="/img/quick_start/step3/4.gif" width="80%"/>
  </div>

1. Or clone a Project from the public Project repository would also clone the correspoding Dataset.

  <div align="center" style={{marginTop: "0vh"}}>
    <img src="/img/quick_start/step3/5.gif" width="80%"/>
  </div>

:::tip Layout Flow Chart

Layout flow chart will be generated automatically after adding links (inflows, flows and connections). You can click and edit the tanks, inflows and flows in the chart.

:::

-------


## <a id="step_4"></a>Step 4: Create a Project

You must specify a BioModel and a Dataset to combine them while creating a Project.
There are a few ways to create a Project (choose 1 from 3 in below):

1. Create an empty Project, edit and parsed save the detial later to make it work.

   - If the BioModel's components are all the same as the DataSet's targets, the Project's detial will be created automatically.
   - Otherwise, you must specify the conversion between the BioModel's components and the DataSet's targets.

  <br />
  <div align="center" style={{marginTop: "0vh"}}>
    <img src="/img/quick_start/step4/1.gif" width="80%"/>
  </div>

1. Or create a Project from a: <a href="/template_file/Solution.xlsx" target="_blank" download>template xlsx file</a>

  <div align="center" style={{marginTop: "0vh"}}>
    <img src="/img/quick_start/step4/2.gif" width="80%"/>
  </div>

1. Or clone a Project from the public Project repository.

  <div align="center" style={{marginTop: "0vh"}}>
    <img src="/img/quick_start/step4/3.gif" width="80%"/>
  </div>


-------

## <a id="step_5"></a>Step 5: Solve

The simulation and evaluation can be initiated with just a few clicks:
- Select a calcualtion engine: Simulaiton, Sensitivity, Uncertainty or Estimation.
- Hit the START button and wait for the results, **SIMPO** will plot everything after the calcualtion process is done.

  <div align="center" style={{marginTop: "0vh"}}>
    <img src="/img/quick_start/step5/1.gif" width="80%"/>
  </div>

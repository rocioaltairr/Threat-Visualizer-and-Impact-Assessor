# Threat Visualizer and Impact Assessor

## Overview

The **Threat Visualizer and Impact Assessor** is a Python application designed to visualize and evaluate attack trees. It allows users to:

- Import attack tree specifications
- Interactively add new risks
- Assign probabilities to risks
- Calculates the overall threat assessment rating based on the user-inputted probabilities and assigned risk weights
- Compare the original (pre-digitalisation) and updated (post-digitalisation) threat models by analyzing the system's threat ratings before and after applying user-inputted risk probabilities and weights.

The application supports industry-standard file formats including JSON, YAML, and XML.

## Features
- **Load Attack Trees:** Import attack tree specifications from JSON, YAML, or XML files.
- **Visualize Trees:** Generate graphical representations of the attack trees.
- **Interactive Node Addition:** Add new risks interactively.
- **Risk Value Assignment:** Enter probabilities for risk.
- **Threat Assessment Calculation:** Aggregate probabilities to assess the overall threat rating.

## Requirements

- Required Python libraries:
  - `networkx`
  - `matplotlib`
  - `pyyaml`
  - `xml.etree.ElementTree` (Standard library)

## Installation
- Install Dependencies:
```bash
pip install networkx matplotlib pyyaml
```

## Usage
- Run the Application:
```bash
python attack_tree_app.py
```

- Enter the Attack Tree Specification:
- Enter the attack tree specification (in an industry-standard format such as XML, YAML, or JSON):attack_tree.json
```bash
attack_tree.json
```

- Add Risks:
  - Enter the parent risk type to which you want to add a new risk.
  - Input the name of the new risk to add new risk.
  - Type exit when you are finished adding risks.

- Enter probability of Risk and aggregate value of the overall thread rating probability:
  - Value for Sabotage (suffix '%' for probability): 8%

- After all commands are finished, the application will visualize the attack tree graph as below:
<img width="958" alt="Screenshot 2024-07-20 at 2 11 09 PM" src="https://github.com/user-attachments/assets/0015f5d5-f5b7-4e7a-a35a-a210019fdd62">


- Command example:

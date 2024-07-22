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
- When prompted with 'Do you want to use the default 'pre-digitalisation' model or provide a custom file? (default/custom):', type 'default' to use the pre-digitalisation.json model or type 'custom' to choose your own model in an industry-standard format (XML, YAML, or JSON).
- If type "custom"
- Enter the path to your custom file. For example "attack_tree.json"

- Add Risks:
  - Enter the parent risk type to which you want to add a new risk. For example "Network Attack"
  - Input the name of the new risk to add new risk. For example "IP Spoofing"
  - Type "exit" when you are finished adding risks.

- Enter probability of Risk and aggregate value of the overall thread rating probability:
  - Value for Sabotage (suffix '%' for probability): 8%

- After all commands are finished, the application will visualize the attack tree graph as below:
<img width="1267" alt="Screenshot 2024-07-22 at 1 50 48 AM" src="https://github.com/user-attachments/assets/6531c4ef-860e-4ef9-ba56-c7411a452546">

The pre-digitalisation.json
```bash
{
    "Attack Tree Root": {
        "Physical Attack": {
            "Steal Equipment": 0.12,
            "Theft of Confidential Information": 0
        },
        "Insider Threat": {
            "Data Theft": 0,
            "Sabotage": 0
        },
        "Network Attack": {
            "Packet Sniffing": 0.04
        },
        "Cyber Attack": {
            "Phishing": 0.20,
            "Malware": 0.05,
            "DDoS": 0,
            "SQL Injection": 0
        }
    }
}
```

The post-digitalisation.json file will also be generated.
```bash
{
    "Attack Tree Root": {
        "Physical Attack": {
            "Steal Equipment": 0.15,
            "Theft of Confidential Information": 0.05
        },
        "Insider Threat": {
            "Data Theft": 0.01,
            "Sabotage": 0.05
        },
        "Network Attack": {
            "Packet Sniffing": 0.08,
            "IP Spoofing": 0.07
        },
        "Cyber Attack": {
            "Phishing": 0.07,
            "Malware": 0.25,
            "DDoS": 0.25,
            "SQL Injection": 0.05
        }
    }
}
```
- Command example screenshot:

<img width="800" alt="Screenshot 2024-07-22 at 1 49 30 AM" src="https://github.com/user-attachments/assets/65c7599c-71b9-46d4-9984-502593f1cd5a">


If use attack_tree.json as below:
```bash
{
    "Attack Tree Root": {
        "Physical Attack": {
            "Equipment Theft": 0.02,
            "Unauthorized Access": 0.07
        },
        "Network Attack": {
            "IP Spoofing": 0.02,
            "Packet Sniffing": 0.04
        },      
        "Cyber Attack": {
            "Phishing": 0.04,
            "DDoS": 0.03,
            "SQL Injection": 0.04
        }
    }
}
```
<img width="1306" alt="Screenshot 2024-07-22 at 1 52 53 AM" src="https://github.com/user-attachments/assets/0148a03f-837e-4f23-bc7a-cb963fd781ac">

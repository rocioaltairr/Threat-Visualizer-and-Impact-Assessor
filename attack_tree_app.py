import json
import yaml
import xml.etree.ElementTree as ET
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import os

class AttackTreeApp:
    def __init__(self):
        self.attack_tree = nx.DiGraph()
        self.node_values = {}
        self.current_model = 'pre-digitalisation'  # Default model
        self.weights = { # Define weights for different attack types
            "Physical Attack": 2,
            "Insider Threat": 4,
            "Network Attack": 3,
            "Cyber Attack": 5
        }

    def load_model(self, filename): 
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"File not found: {filename}. Please make sure the file exists in the directory.")
        self.load_tree(filename)

    def load_tree(self, filename): # load an industry-standard format such as XML, YAML, or JSON file
        if filename.endswith('.json'):
            self.load_data(filename, json.load)
        elif filename.endswith('.yaml') or filename.endswith('.yml'):
            self.load_data(filename, yaml.safe_load)
        elif filename.endswith('.xml'):
            self.load_xml(filename)
        else:
            raise ValueError("Unsupported file format")

    def load_data(self, filename, parser): # read json YAML or JOSN file
        try:
            with open(filename, 'r') as file:
                data = parser(file)
            self.parse_attack_tree(data)
        except Exception as e:
            print(f"Failed to load data from {filename}. Error: {e}")

    def load_xml(self, filename): # read json XML file
        try:
            tree = ET.parse(filename)
            root = tree.getroot()
            data = self.xml_to_dict(root)
            self.parse_attack_tree(data)
        except ET.ParseError as e:
            print(f"Failed to parse XML from {filename}. Error: {e}")

    def xml_to_dict(self, elem): # convert xml to dic data model
        d = {elem.tag: {} if elem.attrib else None}
        children = list(elem)
        if children:
            dd = defaultdict(list)
            for dc in map(self.xml_to_dict, children):
                for k, v in dc.items():
                    dd[k].append(v)
            d = {elem.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
        if elem.attrib:
            d[elem.tag].update((k, v) for k, v in elem.attrib.items())
        if elem.text:
            text = elem.text.strip()
            if children or elem.attrib:
                if text:
                    d[elem.tag]['text'] = text
            else:
                d[elem.tag] = text
        return d

    def parse_attack_tree(self, data, parent=None): # parse dic data model to attack tree model
        for key, value in data.items():
            if isinstance(value, dict):
                self.attack_tree.add_node(key)
                if parent:
                    self.attack_tree.add_edge(parent, key)
                self.parse_attack_tree(value, key)
            elif isinstance(value, list):
                for item in value:
                    self.parse_attack_tree({key: item}, parent)
            else:
                if not self.attack_tree.has_node(key):
                    self.attack_tree.add_node(key)
                if parent and not self.attack_tree.has_edge(parent, key):
                    self.attack_tree.add_edge(parent, key)
                self.node_values[key] = value

    def visualize_attack_tree(self):
        plt.figure(figsize=(10, 8))

        # Position nodes using spring layout
        pos = nx.spring_layout(self.attack_tree, seed=42)

        # Draw the nodes and edges
        nx.draw(self.attack_tree, pos, with_labels=True, node_size=3000, node_color='lightblue', edge_color='gray', font_size=10, font_weight='bold')

        # Calculate the total threat assessment rating value
        total_value = self.aggregate_values()

        risk_level = self.get_risk_level(total_value)
        risk_color = self.get_risk_color(total_value)

        # Add the total threat assessment value and risk level
        plt.text(0.05, 0.95, f"Overall threat assessment rating: {total_value*100:.2f}\nRisk Level: {risk_level}", 
                ha='left', va='top', fontsize=12, color=risk_color, transform=plt.gca().transAxes)

        plt.show()
        plt.close()

    def get_risk_level(self, total_value): # Get the risk level
        if total_value > 1:
            return 'High'
        elif total_value > 0.5:
            return 'Medium'
        else:
            return 'Low'

    def get_risk_color(self, total_value):
        if total_value > 1:
            return 'red'   # High risk
        elif total_value > 0.5:
            return 'blue'  # Medium risk
        else:
            return 'green' # Low risk

    def add_risk_interactively(self): # Add risk accoding two user's requirement
        while True:
            parent_risk_type = input("Enter the risk type to which you want to add a new risk (or 'exit' to quit): ")
            if parent_risk_type.lower() == 'exit':
                break
            if not self.attack_tree.has_node(parent_risk_type):
                print(f"Risk type '{parent_risk_type}' does not exist.")
                continue

            new_risk = input(f"Enter the new risk to add under risk type '{parent_risk_type}': ")
            self.attack_tree.add_node(new_risk)
            self.attack_tree.add_edge(parent_risk_type, new_risk)
            print(f"Added risk: {new_risk} under risk type: {parent_risk_type}")

    def add_probability_values(self):
        print("Enter values for the leaf nodes probability:")
        for node in self.attack_tree.nodes():
            if self.attack_tree.out_degree(node) == 0:  # Check if the node is a leaf node
                print(f"Risk found: {node}")
                while True:
                    value = input(f"Value for {node} (suffix '%' for probability): ")
                    try:
                        if value.endswith('%'):
                            self.node_values[node] = float(value[:-1]) / 100
                            break
                        else:
                            print("Invalid format. Please suffix with '%' for probability.")
                    except ValueError:
                        print("Invalid value. Please enter a valid number.")

    def aggregate_values(self):
        total_value = 1
        for value in self.node_values.values():
            total_value *= (1 - value)  # Assuming probabilities are complementary
        return 1 - total_value
    
    def save_attack_tree(self, filename): # Convert the tree structure and node values to a dictionary
        try:
            data = self.tree_to_dict()
            with open(filename, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"Tree saved to {filename}")
        except Exception as e:
            print(f"Failed to save data to {filename}. Error: {e}")

    def aggregate_values(self):
        total_value = 0
        for node in self.attack_tree.nodes(): # If the risk type has a weight defined, apply the weight
            for attack_type, weight in self.weights.items():
                if attack_type in node:
                    node_value = self.node_values.get(node, 0)
                    weighted_value = node_value * weight
                    total_value += weighted_value
                    break
            else: # If no weight is defined for the risk, use its value
                node_value = self.node_values.get(node, 0)
                total_value += node_value
        return total_value


    def tree_to_dict(self, node=None):
        if node is None:
            node = list(self.attack_tree.nodes())[0]  

        attack_tree_dict = {}
        children = list(self.attack_tree.successors(node))
        
        if children:
            for child in children:
                attack_tree_dict.update(self.tree_to_dict(child))  # Update to ensure direct value assignment
        else:
            attack_tree_dict = self.node_values.get(node, 0)
        
        return {node: attack_tree_dict}

if __name__ == "__main__":
    app = AttackTreeApp()

    # Prompt the user for initial data source
    choice = input("Do you want to use the default 'pre-digitalisation' model or provide a custom file? (default/custom): ").strip().lower()
    
    if choice == 'custom':
        filename = input("Enter the path to your custom file: ").strip()
        app.load_model(filename)
        app.current_model = 'custom-model'
    else:
        app.load_model('pre-digitalisation.json')
    
    # Add new risks and update the attack tree
    print("Adding riks interactively...")
    app.add_risk_interactively()
    
    print("Adding probability values...")
    app.add_probability_values()
    
    # Save the updated model to 'post-digitalisation.json'
    app.save_attack_tree('post-digitalisation.json')
    
    total_value = app.aggregate_values()
    print(f"Total threat assessment rating value : {total_value}")

    print(f"Visualizing {app.current_model} attack tree...")
    app.visualize_attack_tree()

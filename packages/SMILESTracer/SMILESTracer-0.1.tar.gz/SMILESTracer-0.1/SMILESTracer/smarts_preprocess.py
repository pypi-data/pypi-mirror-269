from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import AllChem, Draw
import pandas as pd
import re
import os
import numpy as np


def get_correct_order_of_rxn_smarts(rxn_smarts):
    
    try:
        reactants, products = rxn_smarts.split(">>")
        atom_tags = re.findall(r'\[.*?:\d+\]', reactants)

        list_old_tag = re.findall(r':(\d+)', reactants)
        list_old_tag = [int(i) for i in list_old_tag]
        list_old_tag_sorted= sorted(list_old_tag)
        dict_mapping = {key: value for key, value in zip(list_old_tag, list_old_tag_sorted)}
        # print(list_old_tag)
        # print(list_old_tag_sorted)
        # print(dict_mapping)
        # for old, new in tag_to_new.items():
        #     reactants = reactants.replace(old, f"[{old[1:].split(':')[0]}:{new}]")
        
        # for old, new in tag_to_new.items():
        #     pattern = re.compile(r'\[' + re.escape(old[1:].split(':')[0]) + r'[^]]*:' + re.escape(old.split(':')[1][:-1]) + r'\]')
        #     products = re.sub(pattern, lambda match: match.group(0).rsplit(':', 1)[0] + f':{new}]', products)
        for index,i in enumerate(list_old_tag):
            reactants = re.sub(f":{i}]", f':new{list_old_tag_sorted[index]}]', reactants)
            # print(reactants)
            products = re.sub(f":{list(dict_mapping.keys())[index]}]", f':new{list(dict_mapping.values())[index]}]', products)
            # print(products)
        reactants = reactants.replace("new", "")
        products = products.replace("new", "")

        list_new_tag_react = re.findall(r':(\d+)\]', reactants)
        list_new_tag_react = [int(i) for i in list_new_tag_react]
        list_new_tag_prod = re.findall(r':(\d+)\]', products)
        list_new_tag_prod = [int(i) for i in list_new_tag_prod]
        # list_new_tag_react_sorted = sorted(list_new_tag_react)
        dict_mapping_new = {key:value for key, value in zip(list_new_tag_react, [i+1 for i in range(len(list_new_tag_react))])}

        for key,value in dict_mapping_new.items():
            reactants = re.sub(f":{key}]", f':new{value}]', reactants)
            # print(reactants)
            products = re.sub(f":{key}]", f':new{value}]', products)
            # print(products)
        reactants = reactants.replace("new", "")
        products = products.replace("new", "")

        return reactants + ">>" + products

    except:
        raise ValueError(f"Failed to preprocess this reaction SMARTS:{rxn_smarts}, check if the reaction SMARTS is valid")
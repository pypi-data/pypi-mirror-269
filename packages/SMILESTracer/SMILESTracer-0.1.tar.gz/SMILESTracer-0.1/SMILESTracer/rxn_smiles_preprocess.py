from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import AllChem, Draw
import pandas as pd
import re
import os
import numpy as np


def is_rxn_smiles_pattern(rxn_smi):
    pattern = r'(.+)>+([^>]*?)>(.+)'
    if pd.isna(rxn_smi):
        return False
    elif re.match(pattern,rxn_smi):
        return True
    else:
        return False
    

def clean_rxn_smiles(rxn_smi, rxn_smarts, remove_wildcard=True):

    if not is_rxn_smiles_pattern(rxn_smi):
        raise ValueError("Not a valid reaction SMILES")
    if remove_wildcard:
        if "*" in rxn_smi:
            return None
        
    react_smarts, sol_smarts, prod_smarts = rxn_smarts.split(">")
    react_smarts_mol_list = [Chem.MolFromSmarts(smi) for smi in react_smarts.split(".")]
    react_smiles, sol_smiles, prod_smiles = rxn_smi.split(">")
    react_list = react_smiles.split(".")
    react_smarts_list = react_smarts.split(".")
    react_mol_list = [Chem.MolFromSmiles(smi) for smi in react_list]

    reactant_list_new = []

    for i in range(len(react_smarts_list)):
        for mol in react_mol_list:
            if mol.HasSubstructMatch(react_smarts_mol_list[i]):
                reactant_list_new.append(Chem.MolToSmiles(mol))
                break

    correct_order_reactant_smi = ".".join(reactant_list_new)
    return correct_order_reactant_smi
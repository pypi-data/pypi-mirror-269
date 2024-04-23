from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem import AllChem, Draw
import pandas as pd
import re
import os
import numpy as np


'''
Count Num of atoms in SMARTS
'''
def count_atom_in_smarts(smarts:str):
    
    pattern = r':[0-9]+'
    matches = re.findall(pattern, smarts)
    return len(matches)


def get_molecule_labeled(smi:str, init:int):

    try:
        mol = Chem.MolFromSmiles(smi)
        num = mol.GetNumAtoms()
        for atom in mol.GetAtoms():
            atom.SetAtomMapNum(init)
            init += 1
        labeled_smi = Chem.MolToSmiles(mol)
        return labeled_smi, num
    except Exception as e:
        raise ValueError(f"Failed to convert SMILES string {smi} to Mol object")
    



def get_substructure_mapped(smi:str,sub_struct:str,react_list:list):

    mol = Chem.MolFromSmiles(smi)
    sub_struct_mol = Chem.MolFromSmarts(sub_struct)

    if mol == None:
        raise ValueError(f"Failed to convert SMILES string {smi} to Mol object")
    sub_tup = mol.GetSubstructMatches(sub_struct_mol)
    num = 0
    
    try:
        for idx in sub_tup[0]:
            atom = mol.GetAtomWithIdx(idx)
            atom.SetAtomMapNum(react_list[num])
            num += 1
            if num >= len(react_list):
                break
        return Chem.MolToSmiles(mol)
    
    except Exception as e:
        raise ValueError(f"SMILES string {smi} can't match the substructure SMARTS {sub_struct} ")
    

'''
Input: rxn_smarts, Reactant separated by "."(rxn_smiles)
Output: Labeled rxn_smiles
'''
def labling_rxn(rxn_smarts, rxn_smiles):
    
    # Read SMARTS from input
    rxn = AllChem.ReactionFromSmarts(rxn_smarts)
    reactant_smarts, sol_smarts, product_smarts = rxn_smarts.split(">")
    reactant_smarts_list = reactant_smarts.split(".")
    num_of_atom_in_reactant_smarts_list = [count_atom_in_smarts(smart) for smart in reactant_smarts_list]

    # Read SMILES from input
    reactant_smi_list = rxn_smiles.split(".")

    # Label reactants, atoms which involved in the rxn is labeled from 100
    idx = num_of_atom_total = num_of_atom_involved_in_rxn = 0
    labeled_reactant_smi_list = []

    for smi in reactant_smi_list:

        labeled_smi, num_of_atoms = get_molecule_labeled(smi, num_of_atom_total + 1)
        labeled_smi = get_substructure_mapped(labeled_smi, reactant_smarts_list[idx],  [(i + 200 + num_of_atom_involved_in_rxn) for i in range(num_of_atom_in_reactant_smarts_list[idx])])
        labeled_reactant_smi_list.append(labeled_smi)
        
        num_of_atom_total += num_of_atoms
        num_of_atom_involved_in_rxn += num_of_atom_in_reactant_smarts_list[idx]
        idx += 1
        # oxo_acid_labeled_smi, num_of_oxo_acid_atoms = get_molecule_labeled(oxo_acid_smiles, num_of_amine_atoms + 1)
        # oxo_acid_labeled_smi = get_substructure_mapped(oxo_acid_labeled_smi, oxo_acid_smarts,  [i + 100 + num_of_amine_smarts for i in range(num_of_oxo_acid_atoms)])

        # isocyanide_labeled_smi, num_of_isocyanide_atoms = get_molecule_labeled(isocyanide_smiles, num_of_oxo_acid_atoms + num_of_amine_atoms + 1)
        # isocyanide_labeled_smi = get_substructure_mapped(isocyanide_labeled_smi, isocyanide_smarts,  [i + 100 + num_of_amine_smarts + num_of_oxo_acid_atoms for i in range(num_of_isocyanide_atoms)])


    # Generate product SMILES and label the product
    
    # Read order of atoms involved in rxn from product SMARTS
    numbers = re.findall(r':(\d+)', product_smarts)
    prod_mapping_num_list = [199 + int(num) for num in numbers]
    
    # Generate product SMILES
    defined_rxn = AllChem.ReactionFromSmarts(rxn_smarts)
    # amine_mol, oxo_acid_mol, nc_mol = [Chem.MolFromSmiles(smi) for smi in labeled_reactant_smi_list]
    products = defined_rxn.RunReactants(tuple([Chem.MolFromSmiles(smi) for smi in labeled_reactant_smi_list]))
    semi_labeled_prod_smi_list = [Chem.MolToSmiles(prod_mol) for prod_mol in products[0]]
    
    # Get smarts for each product
    prod_smarts = product_smarts.split(".")
    
    # Label each product in semi_labeled_prod_smi_list
    labeled_prod_smi_list = []
    i = 0
    for prod in semi_labeled_prod_smi_list:
        prod = get_substructure_mapped(prod, prod_smarts[i], prod_mapping_num_list)
        labeled_prod_smi_list.append(prod)
        num_of_atom_in_prod = count_atom_in_smarts(prod_smarts[i])
        i += 1
        prod_mapping_num_list = prod_mapping_num_list[num_of_atom_in_prod:]

    # labeled_prod_smi = labeled_prod_smi_0 + "." + labeled_prod_smi_1
    labeled_prod_smi = ".".join(labeled_prod_smi_list)

    # Label product(s)
    # labeled_prod_smi = get_substructure_mapped(semi_labeled_prod_smi, product_smarts, prod_mapping_num_list)

    return ".".join(labeled_reactant_smi_list) + ">>" + labeled_prod_smi
"""Molecular Featurization Pipeline"""

from rdkit import Chem
from rdkit.Chem import rdMolDescriptors

from .utils import InvalidSMILESError


class FingerprintCalculator:
    def __init__(self, descriptor="morgan2"):
        self.descriptor = descriptor
        self.descriptors = {
            "rdkit": lambda m: Chem.RDKFingerprint(m),
            "maccs": lambda m: rdMolDescriptors.GetMACCSKeysFingerprint(m),
            "morgan2": lambda m: rdMolDescriptors.GetMorganFingerprintAsBitVect(m, 2, 2048),
            "morgan3": lambda m: rdMolDescriptors.GetMorganFingerprintAsBitVect(m, 3, 2048),
        }

    def calculate_fingerprint(self, smi):
        mol = Chem.MolFromSmiles(smi)
        if mol:
            fn = self.descriptors[self.descriptor]
            return fn(mol)
        raise InvalidSMILESError

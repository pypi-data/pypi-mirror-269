from qcelemental import constants
from qcelemental.models import Molecule
from qcmanybody.models.manybody_output_pydv1 import AtomicSpecification, ManyBodyKeywords, ManyBodyInput
from qcmanybody.qcng_computer import ManyBodyComputerQCNG, qcvars_to_manybodyproperties

def he_tetramer():
    a2 = 2 / constants.bohr2angstroms
    return Molecule(symbols=["He", "He", "He", "He"], fragments=[[0], [1], [2], [3]], geometry=[0, 0, 0, 0, 0, a2, 0, a2, 0, 0, a2, a2])

def he_dimer():
    a2 = 2 / constants.bohr2angstroms
    return Molecule(symbols=["He", "He"], fragments=[[0], [1]], geometry=[0, 0, 0, 0, 0, a2])

def mbe_data_multilevel_631g():
    # note that spherical/cartesian irrelevant for He & 6-31G, and fc/ae irrelevant for He
    c4_kwds = {}
    gms_kwds = {"basis__ngauss": 6, "ccinp__ncore": 0, "ccinp__iconv": 9, "scf__conv": 9}
    nwc_kwds = {"scf__thresh": 1.0e-8, "ccsd__thresh": 1.e-8}
    p4_kwds = {"scf_type": "pk", "mp2_type": "conv"}

    protocols = {"stdout": False}
    driver = "gradient"
    return {
        "specification": {
            "specification": {
                "c4-hf": {
                    "model": {
                        "method": "hf",
                        "basis": "6-31g",
                    },
                    "driver": driver,
                    "program": "cfour",
                    "keywords": c4_kwds,
                    "protocols": protocols,
                },
                "c4-mp2": {
                    "model": {
                        "method": "mp2",
                        "basis": "6-31g",
                    },
                    "driver": driver,
                    "program": "cfour",
                    "keywords": c4_kwds,
                    "protocols": protocols,
                },
                "c4-ccsd": {
                    "model": {
                        "method": "ccsd",
                        "basis": "6-31g",
                    },
                    "driver": driver,
                    "program": "cfour",
                    "keywords": c4_kwds,
                    "protocols": protocols,
                },
                "gms-hf": {
                    "model": {
                        "method": "hf",
                        "basis": "n31",
                    },
                    "driver": driver,
                    "program": "gamess",
                    "keywords": gms_kwds,
                    "protocols": protocols,
                },
                "gms-mp2": {
                    "model": {
                        "method": "mp2",
                        "basis": "n31",
                    },
                    "driver": driver,
                    "program": "gamess",
                    "keywords": gms_kwds,
                    "protocols": protocols,
                },
                "gms-ccsd": {
                    "model": {
                        "method": "ccsd",
                        "basis": "n31",
                    },
                    "driver": driver,
                    "program": "gamess",
                    "keywords": gms_kwds,
                    "protocols": protocols,
                },
                "nwc-hf": {
                    "model": {
                        "method": "hf",
                        "basis": "6-31g",
                    },
                    "driver": driver,
                    "program": "nwchem",
                    "keywords": nwc_kwds,
                    "protocols": protocols,
                },
                "nwc-mp2": {
                    "model": {
                        "method": "mp2",
                        "basis": "6-31g",
                    },
                    "driver": driver,
                    "program": "nwchem",
                    "keywords": nwc_kwds,
                    "protocols": protocols,
                },
                "nwc-ccsd": {
                    "model": {
                        "method": "ccsd",
                        "basis": "6-31g",
                    },
                    "driver": driver,
                    "program": "nwchem",
                    "keywords": nwc_kwds,
                    "protocols": protocols,
                },
                "p4-hf": {
                    "model": {
                        "method": "hf",
                        "basis": "6-31g",
                    },
                    "driver": driver,
                    "program": "psi4",
                    "keywords": p4_kwds,
                    "protocols": protocols,
                },
                "p4-mp2": {
                    "model": {
                        "method": "mp2",
                        "basis": "6-31g",
                    },
                    "driver": driver,
                    "program": "psi4",
                    "keywords": p4_kwds,
                    "protocols": protocols,
                },
                "p4-ccsd": {
                    "model": {
                        "method": "ccsd",
                        "basis": "6-31g",
                    },
                    "driver": driver,
                    "program": "psi4",
                    "keywords": p4_kwds,
                    "protocols": protocols,
                },
            },
            "keywords": None,
            "driver": driver, 
        },
        "molecule": None,
    }

{"bsse_type": ["nocp", "cp"]},


mbe_keywords = ManyBodyKeywords(
    levels={1: "c4-ccsd", 2: "c4-mp2"},
    bsse_type="nocp",
)

mbe_data_multilevel_631g = mbe_data_multilevel_631g()
mbe_data_multilevel_631g["molecule"] = he_dimer()
mbe_data_multilevel_631g["specification"]["keywords"] = mbe_keywords
mbe_model = ManyBodyInput(**mbe_data_multilevel_631g)

ret = ManyBodyComputerQCNG.from_qcschema_ben(mbe_model)
print(f"MMMMMMM {request.node.name}")
pprint.pprint(ret.dict(), width=200)


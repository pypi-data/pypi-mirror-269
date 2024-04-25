from enum import IntEnum, Enum, StrEnum

class BsseEnum2(str, Enum):
    """Available basis-set superposition error (BSSE) treatments."""

    nocp = "nocp"  # plain supramolecular interaction energy
    cp = "cp"      # Boys-Bernardi counterpoise correction; site-site functional counterpoise (SSFC)
    vmfc = "vmfc"  # Valiron-Mayer function counterpoise
    ssfc = "cp"

for name, member in BsseEnum2.__members__.items():
    print(name, member)

print('a')
print(BsseEnum2.cp)
print(BsseEnum2.ssfc)
print('b')
print(BsseEnum2['cp'])
print(BsseEnum2['ssfc'])
#print(BsseEnum2.getitem('ssfc'))
print('c')
print(BsseEnum2('cp'))
print(BsseEnum2('ssfc'))



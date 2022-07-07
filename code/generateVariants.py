filePath = r""
fileName = r"HexaCyano-1_Water.gjf"
fileObject = open(filePath+fileName)
fileContent = fileObject.readlines()

# extract molecule name from first line
# ASSUMPTION that name will always have "-#_phase" if incorrect, find solution 
moleculeName = fileContent[0].split("=")[1].split("_")[0][:-2]
print(moleculeName) # %chk=Hexacyano-0_Water.chk -> Hexacyano or 
                        # %chk=12DiCO2-2-1_Water.chk -> 12DiCO2-2

# grab line 9 charges
line9charges = fileContent[8]

# close init file reader
fileObject.close()

# molecule class for storing values and functions related to the molecule itself
class molecule:
    def __init__(self,name,charge,phase,line9charge):
        self.name = name
        self.charge = charge
        self.phase = phase
        self.line9charge = line9charge
    
    def generateFullMoleculeName(self):
        return f'{self.name}-{self.charge}_{self.phase}'

    def generateFirstLine(self):
        return f'%chk={self.generateFullMoleculeName()}.chk'

    def generateFileName(self):
        return f'{self.generateFullMoleculeName()}.gjf'
    
    def modifyLine9Charge(self):
        charges = self.line9charge.split(" ")
        if self.charge == "-1" or self.charge == "1" or self.charge == -1:
            return self.line9charge
        elif self.charge == "-0"or self.charge == "0" or self.charge == 0:
            charges[0] = int(charges[0]) + 1
            charges[1] = 1
        else: # if -2
            charges[0] = int(charges[0]) - 1
            charges[1] = 1
        # print(charges)
        if charges[0] == "0":
            self.line9charge = f'-{charges[0]} {charges[1]}'
        else:
            self.line9charge = f'{charges[0]} {charges[1]}'
        
        # print(self.line9charge)


# generate all molecules being generated just comment out lines that aren't being used and don't add to list
# also comment out which one is being read from as you don't need to generate a file for that molecule
molecules = []
molecules += [molecule(moleculeName,"0",'Water',line9charges)]
# molecules += [molecule(moleculeName,1,'Water',line9charges)] # commented out as I used 1_Water to generate other files
molecules += [molecule(moleculeName,"2",'Water',line9charges)]
molecules +=  [molecule(moleculeName,"0",'Gas',line9charges)]
molecules += [molecule(moleculeName,"1",'Gas',line9charges)]
molecules += [molecule(moleculeName,"2",'Gas',line9charges)]


for molecule in molecules:
    molecule.modifyLine9Charge()
    
    with open(filePath+fileName, 'r') as givenMoleculeFile:
        with open(filePath+molecule.generateFileName(), 'w') as generatedMoleculeFile:
            count = 1
            for line in givenMoleculeFile:
                if count == 1:
                    generatedMoleculeFile.write(molecule.generateFirstLine()+'\n')
                elif line.__contains__("scrf"):
                    if(molecule.phase != 'Gas'): # if it is gas then it wont write line
                        generatedMoleculeFile.write(line)
                elif count == 7:
                    generatedMoleculeFile.write(molecule.generateFullMoleculeName()+'\n')
                elif count == 9:
                    generatedMoleculeFile.write(molecule.line9charge + '\n')
                else:
                    generatedMoleculeFile.write(line)
                    if count >= 10:
                        break
                count += 1
            
            for line in givenMoleculeFile:
                generatedMoleculeFile.write(line)




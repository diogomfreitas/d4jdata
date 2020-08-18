import xml.dom.minidom
import json
import sys
import os
import mutants.mutationVariables

def writeMutVariablesJSON(programDir, program, tSet):
    verFile = open(programDir + program + '/' + tSet, 'r')
    versions = verFile.read().rstrip('\n').split(' ')

    for ver in versions:
        MutVariablesList = mutants.mutationVariables.mutationVariables(programDir, program, ver)
        # with open(programDir + program + '/pickle/' + program + '-' + str(ver), 'wb') as fp:
        #     pickle.dump(itemlist, fp)

        # mutantsByLines contem os indices das versoes de cada vetor
        # codeLines contem o endereco da linha que sofreu a mutacao. Eh preciso replicar para as linhas que tem mais de um mutante
        Codelines = list()
        for i in range(len(MutVariablesList.mutantsByLines)):
            for j in range(len(MutVariablesList.mutantsByLines[i])):
                Codelines.append(MutVariablesList.codeLines[i])

        data_from_xml = []
        for i in range(MutVariablesList.mutants):
            aux = {}
            aux["type"] = "LINE"
            SplitCodelines = Codelines[i].split("#")
            aux["name"] = SplitCodelines[0]
            aux["location"] = SplitCodelines[1]
            aux["mkp"] = MutVariablesList.kp[i]
            aux["mkf"] = MutVariablesList.kf[i]
            aux["mnp"] = MutVariablesList.np[i]
            aux["mnf"] = MutVariablesList.nf[i]

            data_from_xml.append(aux)
            # print (aux)

        with open(programDir + program + '/' + str(ver) + "/mutation.json", 'w') as file:
            file.write(json.dumps(data_from_xml, indent=2))

    verFile.close()

class MutationJSON:
    def __init__(self, programDir, program, tSet):
        verFile = open(programDir + program + '/' + tSet, 'r')
        versions = verFile.read().rstrip('\n').split(' ')

        self.ver = len(versions)
        self.faultyLines = list()
        self.mutantsByLines = list()
        self.lines = list()
        self.mutants = list()
        self.kp = list() # added to PGcov
        self.kf = list() # added to PGcov
        self.np = list() # added to PGcov
        self.nf = list() # added to PGcov

        for v in versions:
            Vars = self.readMutVariables(programDir + program + '/JSON/', program, v)
            self.faultyLines.append(Vars.faultyLines)
            self.mutantsByLines.append(Vars.mutantsByLines)
            self.lines.append(Vars.lines)
            self.mutants.append(Vars.mutants)
            self.kp.append(Vars.kp) # added to PGcov
            self.kf.append(Vars.kf) # added to PGcov
            self.np.append(Vars.np) # added to PGcov
            self.nf.append(Vars.nf) # added to PGcov

        verFile.close()

    def readMutVariables(self, programDir, program, ver):
        pass # TODO função para ler variaveis do JSON
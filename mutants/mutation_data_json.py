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

        # mutantsByLines contem os indices das versoes de cada vetor
        # codeLines contem o endereco da linha que sofreu a mutacao. Eh preciso replicar para as linhas que tem mais de um mutante
        Codelines = list()
        for i in range(len(MutVariablesList.mutantsByLines)):
            for j in range(len(MutVariablesList.mutantsByLines[i])):
                Codelines.append(MutVariablesList.codeLines[i])

        json_mutation_data = []
        for i in range(MutVariablesList.lines):
            json_aux = {}
            json_aux["type"] = "MUTANT"

            # SplitCodelines = Codelines[i].split("#")
            # json_aux["name"] = SplitCodelines[0]
            # json_aux["location"] = SplitCodelines[1]

            SplitCodelines = MutVariablesList.codeLines[i].split("#")
            json_aux["name"] = SplitCodelines[0]
            json_aux["location"] = SplitCodelines[1]

            for m in MutVariablesList.mutantsByLines[i]:
                mutant_json = {}
                mutant_json["Mutation Operator"] = MutVariablesList.mutationLog[m][1]
                mutant_json["Original Operator Symbol"] = MutVariablesList.mutationLog[m][2]
                mutant_json["Replacement Operator Symbol"] = MutVariablesList.mutationLog[m][3]
                mutant_json["Fully Qualified Name"] = MutVariablesList.mutationLog[m][4]
                mutant_json["Line Numer In Original Source File"] = MutVariablesList.mutationLog[m][5]
                mutant_json["Applied Transformation"] = MutVariablesList.mutationLog[m][6]

                mutant_json["mkp"] = MutVariablesList.kp[m]
                mutant_json["mkf"] = MutVariablesList.kf[m]
                mutant_json["mnp"] = MutVariablesList.np[m]
                mutant_json["mnf"] = MutVariablesList.nf[m]
                json_aux[MutVariablesList.mutationLog[m][0]] = mutant_json

            json_mutation_data.append(json_aux)
            # print (json_aux)

        with open(programDir + program + '/' + str(ver) + "/mutation.json", 'w') as file:
            file.write(json.dumps(json_mutation_data, indent=2))

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
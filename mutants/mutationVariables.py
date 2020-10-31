import csv
import math
import sys
import re

from pathlib import Path

import gc


class mutationVariables:
    def __init__(self, programDir, program, ver):
        self.codeLines, self.mutantsByLines, self.mutationLog= self.readMutantsByLines(programDir, program, ver)
        self.readMutMat(programDir, program, ver, self.codeLines)

        self.tests = len(self.pTests) + len(self.nTests)

        self.lines = len(self.codeLines)
        self.mutants = len(self.pTests[0])

        self.kp = self.KPs()
        self.kf = self.KFs()
        self.np = self.NPs()
        self.nf = self.NFs()

# Texto extraido do manual da ferramenta Major para definir cada campo dos arquivos mutants.log
# The Major Mutation Framework - (Version 1.3.4 / November 10, 2018)
# 3.2.1 Log file for generated mutants
# Major’s compiler generates the log file mutants.log, which provides detailed information about the generated mutants and uses a colon (:) as separator. The log file contains one row per generated mutant, where each row in turn contains 7 columns with the following information:
# 	1. Mutants’ unique number (id)
# 	2. Name of the applied mutation operator
# 	3. Original operator symbol
# 	4. Replacement operator symbol
# 	5. Fully qualified name of the mutated method
# 	6. Line number in original source file
# 	7. Visualization of the applied transformation (from |==> to)
# The following example gives the log entry for a ROR mutation that has the mutant id 11 and is generated for the method classify (line number 18) of the class Triangle:
# 11:ROR:<=(int,int):<(int,int):Triangle@classify:18:a <= 0 |==> a < 0
    def readMutantsByLines(self, programDir, program, ver):

        sf = open(programDir + program + '/' + str(ver) + '/mutants.log', 'r')
        mutantsLog = sf.read().split('\n')
        sf.close()

        MutationLog = list()
        mutatedCodeLines = list()
        mutantsByLines = list()
        aux = 0
        for logLine in mutantsLog:
            logLine = logLine.split(':')
            if len(logLine) >= 7:
                MutationLog.append(logLine)

                mutLine = logLine[4].split('@')[0]+'#'+logLine[5]
                if len(mutatedCodeLines) == 0 or mutLine != mutatedCodeLines[-1]:
                    mutatedCodeLines.append(mutLine)
                    mutantsByLines.append(list())
                mutantsByLines[-1].append(aux)
                aux += 1

        return mutatedCodeLines, mutantsByLines, MutationLog


    def readFaultyLines(self, programDir, program, ver, codeLines):

        faultyLines = list()

        blf = open(programDir + program + '/' + program + '-' + str(ver) + '.buggy.lines', 'r')
        reader = csv.reader(blf, delimiter='#')
        lines = list(reader)
        blf.close()

        if Path(programDir + program + '/' + program + '-' + str(ver) + '.candidates').is_file():
            cf = open(programDir + program + '/' + program + '-' + str(ver) + '.candidates', 'r')
            reader = csv.reader(cf, delimiter=',')
            candidates = list(reader)
            cf.close()

        print(ver)
        for l in lines:
            if 'FAULT_OF_OMISSION' in l[2]:
                faultyLines.append(list())
                for c in candidates:
                    if c[0] == l[0] + '#' + l[1]:
                        if c[1] in codeLines:
                            faultyLines[-1].append(codeLines.index(c[1]))

            elif re.compile(r'^ *}$').search(l[2]) or re.compile(r'^ *}* *else *{*$').search(l[2]) or \
                    re.compile(r'^ *try *{*$').search(l[2]) or re.compile(r'^ *static *{*$').search(l[2]) or \
                    re.compile(r'^ *private boolean canInline\(\) *{*$').search(l[2]) or re.compile(
                r'^ *\) *{*$').search(l[2]):
                faultyLines.append(list())
                for c in candidates:
                    if c[0] == l[0] + '#' + l[1]:
                        if c[1] in codeLines:
                            faultyLines[-1].append(codeLines.index(c[1]))
            else:
                faultyLines.append(list())
                faultyLines[-1].append(codeLines.index(l[0] + '#' + l[1]))


        print(faultyLines)
        return faultyLines

    def readMutMat(self, programDir, program, ver, codeLines):
        self.nTests = list()
        self.pTests = list()

        matrixFile = open(programDir + program + '/' + str(ver) + '/killage.csv', 'r')
        CovMat = list(csv.reader(matrixFile, delimiter=' '))  # append all lines as a list
        matrixFile.close()
        self.faultyLines = self.readFaultyLines(programDir, program, ver, codeLines)

        for j in range(len(CovMat)):  # iterate over number of tests
            if CovMat[j][-1] == '-':
                del CovMat[j][-1]
                self.nTests.append(list(map(int, CovMat[j])))
            else:
                del CovMat[j][-1]
                self.pTests.append(list(map(int, CovMat[j])))

        CovMat.clear()
        gc.collect()

    # def KPs(self):
    #     kp = list()
    #     for mutants in self.mutantsByLines:  # agrupa as variaveis dos mutantes em sub lists conforme a linha mutada
    #         aux = list()
    #         for m in mutants:
    #             aux.append(self.kpRuns(m))
    #         kp.append(aux)
    #     return kp

    def KPs(self):
        kp = list()
        for i in range(self.mutants):
            kp.append(self.kpRuns(i))
        return kp

    def kpRuns(self, mutant):
        kp = 0
        for i in self.pTests:
            if i[mutant] == 1:
                kp += 1
        return kp

    def KFs(self):
        kf = list()
        for i in range(self.mutants):
            kf.append(self.kfRuns(i))
        return kf

    def kfRuns(self, mutant):
        kf = 0
        for i in self.nTests:
            if i[mutant] == 1:
                kf += 1
        return kf

    def NPs(self):
        np = list()
        for i in range(self.mutants):
            np.append(self.npRuns(i))
        return np

    def npRuns(self, mutant):
        np = 0
        for i in self.pTests:
            if i[mutant] == 0:
                np += 1
        return np

    def NFs(self):
        nf = list()
        for i in range(self.mutants):
            nf.append(self.nfRuns(i))
        return nf

    def nfRuns(self, mutant):
        nf = 0
        for i in self.nTests:
            if i[mutant] == 0:
                nf += 1
        return nf

if __name__ == "__main__":
    mut = mutationVariables('/Users/diogofreitas/PycharmProjects/d4jdata/data/killmaps/', 'Chart', 2)

    print(mut.mutants)
    print(mut.kp)
    print(mut.kf)
    print(mut.np)
    print(mut.nf)
    print(mut.mutantsByLines)

import csv
import math
import sys
import re

from pathlib import Path

import gc


class mutationVariables:
    def __init__(self, programDir, program, ver):
        self.codeLines, self.mutantsByLines = self.readMutantsByLines(programDir, program, ver)
        self.readMutMat(programDir, program, ver, self.codeLines)

        self.tests = len(self.pTests) + len(self.nTests)

        self.lines = len(self.codeLines)
        self.mutants = len(self.pTests[0])

        self.kp = self.KPs()
        self.kf = self.KFs()
        self.np = self.NPs()
        self.nf = self.NFs()

    def readMutantsByLines(self, programDir, program, ver):

        sf = open(programDir + program + '/' + str(ver) + '/mutants.log', 'r')
        mutantsLog = sf.read().split('\n')
        sf.close()

        codeLines = list()
        mutantsByLines = list()
        mutantID = 0
        for mut in mutantsLog:
            mut = mut.split(':')
            if len(mut) >= 5:
                mutLine = mut[4].split('@')[0]+'#'+mut[5]
                if len(codeLines) == 0 or mutLine != codeLines[-1]:
                    codeLines.append(mutLine)
                    mutantsByLines.append(list())
                mutantsByLines[-1].append(mutantID)
                mutantID += 1

        return codeLines, mutantsByLines


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
    mut.readMutantsByLines('/Users/diogofreitas/PycharmProjects/d4jdata/data/killmaps/', 'Chart', 2)

import csv
import gc
import re

from src.spectrum.spectrum import Spectrum

class DataFlow(Spectrum):
    def __init__(self, dataset_dir, program, ver, file):
        self.code_lines, self.methods, self.vars, self.defs, self.uses = self.count_instrumented_elements(dataset_dir, program, ver, file)
        super().__init__(dataset_dir, program, ver , self.code_lines, 'jaguar/.jaguar/matrix/' + file + '.matrix', False)

        self.cep = self.sum_elements(1, self.positive_tests)
        self.cef = self.sum_elements(1, self.negative_tests)
        self.cnp = self.sum_elements(0, self.positive_tests)
        self.cnf = self.sum_elements(0, self.negative_tests)

    # def read_coverage_matrix(self, dataset_dir, program, ver, code_lines, matrix_file_name):
    #     self.negative_tests = list()
    #     self.positive_tests = list()
    #
    #     matrix_file = open(dataset_dir + program + '/' + str(ver) + '/' + matrix_file_name, 'r')
    #     CovMat = list(csv.reader(matrix_file, delimiter=' '))  # append all lines as a list
    #     matrix_file.close()
    #     # self.faultyLines = self.read_faulty_lines(dataset_dir, program, ver, code_lines)
    #
    #     for j in range(len(CovMat)):  # iterate over number of tests
    #         if CovMat[j][-1] == '-':
    #             del CovMat[j][-1]
    #             self.negative_tests.append(list(map(int, CovMat[j])))
    #         else:
    #             del CovMat[j][-1]
    #             self.positive_tests.append(list(map(int, CovMat[j])))
    #
    #     CovMat.clear()
    #     gc.collect()

    def count_instrumented_elements(self, dataset_dir, program, ver, file):

        sf = open(dataset_dir + program + '/' + str(ver) + '/jaguar/.jaguar/spectra/' + file + '.spectra', 'r')
        spectra_file = sf.read().split('\n')

        classes = list()
        methods = list()
        vars = list()
        defs = list()
        uses = list()

        for line in spectra_file:
            if not line:
                break
            line = line.split(':')
            class_name, method_name = line[0].split('#')
            classes.append(class_name)
            methods.append(method_name)

            line = line[1].split(',')

            definition = re.sub(r'[\(\)]', '', line[0])  # semove parentesis
            defs.append(definition)

            if (len(line) == 3):
                use = re.sub(r'[\(\)]', '', line[1])  # semove parentesis
                uses.append(use)
            else:
                use = '(' + re.sub(r'[\(\)]', '', line[1]) + ',' + re.sub(r'[\(\)]', '', line[2]) + ')'
                uses.append(use)

            var_name = re.sub(r'[\(\)]', '', line[-1])  # semove parentesis
            vars.append(var_name)


        sf.close()

        return classes, methods, vars, defs, uses

    # def read_coverage_matrix(self, dataset_dir, program, ver, code_lines, matrix_file_name):
    #     super().read_coverage_matrix()

def read_spectra():
    spectra_file = ['org.jfree.chart.annotations.AbstractXYAnnotation#addEntity:(154,(154,155), info)',
                'org.jfree.chart.annotations.AbstractXYAnnotation#addEntity:(154,(154,157), info)',
                'org.jfree.chart.annotations.AbstractXYAnnotation#addEntity:(154,157, info)',
                'org.jfree.chart.annotations.AbstractXYAnnotation#addEntity:(154,161, hotspot)']

    classes = list()
    methods = list()
    vars = list()
    defs = list()
    uses = list()

    for line in spectra_file:
        line = line.split(':')
        class_name, method_name = line[0].split('#')
        classes.append(class_name)
        methods.append(method_name)

        line = line[1].split(',')

        definition = re.sub(r'[\(\)]','',line[0]) #semove parentesis
        defs.append(definition)

        if (len(line) == 3):
            use = re.sub(r'[\(\)]', '', line[1])  # semove parentesis
            uses.append(use)
        else:
            use = '(' + re.sub(r'[\(\)]', '', line[1]) + ',' + re.sub(r'[\(\)]', '', line[2]) + ')'
            uses.append(use)

        var_name = re.sub(r'[\(\)]','',line[-1]) #semove parentesis
        vars.append(var_name)

if __name__ == "__main__":
    data = DataFlow('/Users/diogofreitas/PycharmProjects/d4jdata/data/', 'Chart', '1b', 'org.jfree.chart.BufferedImageRenderingSource')
    # "/Users/diogofreitas/PycharmProjects/jaguar-data-flow-experiments-main/dataset/Chart/12b/jaguar/.jaguar/spectra"

    print(data.elements)
    print(data.cep)
    print(data.cef)
    print(data.cnp)
    print(data.cnf)
    print(data.code_lines)
    print(len(data.code_lines))
    print(data.methods)
    print(data.vars)
    print(data.defs)
    print(data.uses)
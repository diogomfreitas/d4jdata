import csv
import math
import sys
import re

from pathlib import Path

import gc


class Spectrum:
    def __init__(self, program_dir, program, ver, code_lines, matrix_file_name):
        self.code_lines = code_lines #code_lines is initialized at the child class with count_elements_by_line
        # self.codeLines = self.count_elements_by_line(program_dir, program, ver)

        self.read_coverage_matrix(program_dir, program, ver, self.code_lines, matrix_file_name)

        self.tests = len(self.positive_tests) + len(self.negative_tests)

        self.lines = len(self.code_lines)
        self.elements = len(self.positive_tests[0])#elements in the coverage matrix column: commands; mutantes; etc...

    def count_instrumented_elements(self, program_dir, program, ver):
        """"Overrite in the child class"""
        pass


    def read_faulty_lines(self, program_dir, program, ver, code_lines):

        faulty_lines = list()

        blf = open(program_dir + program + '/' + program + '-' + str(ver) + '.buggy.lines', 'r')
        reader = csv.reader(blf, delimiter='#')
        lines = list(reader)
        blf.close()

        if Path(program_dir + program + '/' + program + '-' + str(ver) + '.candidates').is_file():
            cf = open(program_dir + program + '/' + program + '-' + str(ver) + '.candidates', 'r')
            reader = csv.reader(cf, delimiter=',')
            candidates = list(reader)
            cf.close()

        print(ver)
        for l in lines:
            if 'FAULT_OF_OMISSION' in l[2]:
                faulty_lines.append(list())
                for c in candidates:
                    if c[0] == l[0] + '#' + l[1]:
                        if c[1] in code_lines:
                            faulty_lines[-1].append(code_lines.index(c[1]))

            elif re.compile(r'^ *}$').search(l[2]) or re.compile(r'^ *}* *else *{*$').search(l[2]) or \
                    re.compile(r'^ *try *{*$').search(l[2]) or re.compile(r'^ *static *{*$').search(l[2]) or \
                    re.compile(r'^ *private boolean canInline\(\) *{*$').search(l[2]) or re.compile(
                r'^ *\) *{*$').search(l[2]):
                faulty_lines.append(list())
                for c in candidates:
                    if c[0] == l[0] + '#' + l[1]:
                        if c[1] in code_lines:
                            faulty_lines[-1].append(code_lines.index(c[1]))
            else:
                faulty_lines.append(list())
                faulty_lines[-1].append(code_lines.index(l[0] + '#' + l[1]))


        print(faulty_lines)
        return faulty_lines

    def read_coverage_matrix(self, program_dir, program, ver, code_lines, matrix_file_name):
        self.negative_tests = list()
        self.positive_tests = list()

        matrix_file = open(program_dir + program + '/' + str(ver) + '/' + matrix_file_name, 'r')
        CovMat = list(csv.reader(matrix_file, delimiter=' '))  # append all lines as a list
        matrix_file.close()
        self.faultyLines = self.read_faulty_lines(program_dir, program, ver, code_lines)

        for j in range(len(CovMat)):  # iterate over number of tests
            if CovMat[j][-1] == '-':
                del CovMat[j][-1]
                self.negative_tests.append(list(map(int, CovMat[j])))
            else:
                del CovMat[j][-1]
                self.positive_tests.append(list(map(int, CovMat[j])))

        CovMat.clear()
        gc.collect()

    """
    Usage:
    value: must be 1 for elements that touch the test or 0 for elements that do not;
    test_list must me self.positive_tests for positive tests or self.negative_tests;
    self.positive_tests and self.negative_tests are populated by read_coverage_matrix function at the class constructor.
    """
    def sum_elements(self, value, tests_list):
        if (value not in [0, 1]):
            raise Exception("Element value must be either 0 or 1")

        sum_elements_list = list()
        for i in range(self.elements):
            sum_elements_list.append(self.count_runs(i, value, tests_list))
        return sum_elements_list

    def count_runs(self, element, value, tests_list):
        sum_ones = 0
        for i in tests_list:
            if i[element] == value:
                sum_ones += 1
        return sum_ones
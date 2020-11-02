from src.spectrum.spectrum import Spectrum

class Coverage(Spectrum):
    def __init__(self, program_dir, program, ver):
        self.code_lines = self.count_instrumented_elements(program_dir, program, ver)

        super().__init__(program_dir, program, ver, self.code_lines, 'matrix', True)

        self.cep = self.sum_elements(1, self.positive_tests)
        self.cef = self.sum_elements(1, self.negative_tests)
        self.cnp = self.sum_elements(0, self.positive_tests)
        self.cnf = self.sum_elements(0, self.negative_tests)

    def count_instrumented_elements(self, program_dir, program, ver):

        sf = open(program_dir + program + '/' + str(ver) + '/spectra', 'r')
        spectra = sf.read().split('\n')
        sf.close()

        return spectra

if __name__ == "__main__":
    cov = Coverage('/Users/diogofreitas/PycharmProjects/d4jdata/data/', 'Chart', 2)

    print(cov.elements)
    print(cov.lines)
    print(cov.cep)
    print(cov.cef)
    print(cov.cnp)
    print(cov.cnf)
    print(cov.code_lines)

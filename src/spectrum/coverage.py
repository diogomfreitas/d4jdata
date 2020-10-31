from src.spectrum.spectrum import Spectrum

class Coverage(Spectrum):
    def __init__(self, program_dir, program, ver):
        self.code_lines = self.count_instrumented_elements(program_dir, program, ver)

        super().__init__(program_dir, program, ver, self.code_lines, 'matrix')

        self.ep = self.sum_elements(1, self.positive_tests)
        self.ef = self.sum_elements(1, self.negative_tests)
        self.np = self.sum_elements(0, self.positive_tests)
        self.nf = self.sum_elements(0, self.negative_tests)

    def count_instrumented_elements(self, program_dir, program, ver):

        sf = open(program_dir + program + '/' + str(ver) + '/spectra', 'r')
        spectra = sf.read().split('\n')
        sf.close()

        return spectra

if __name__ == "__main__":
    mut = Coverage('/Users/diogofreitas/PycharmProjects/d4jdata/data/', 'Chart', 2)

    print(mut.elements)
    print(mut.ep)
    print(mut.ef)
    print(mut.np)
    print(mut.nf)
    print(mut.code_lines)

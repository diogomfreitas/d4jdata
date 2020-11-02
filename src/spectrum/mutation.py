from src.spectrum.spectrum import Spectrum

class Mutation(Spectrum):
    def __init__(self, program_dir, program, ver):
        self.code_lines, self.mutants_by_lines, self.mutation_log= self.count_instrumented_elements(program_dir, program, ver)

        super().__init__(program_dir, program, ver, self.code_lines, 'killage.csv', True)

        self.kp = self.sum_elements(1, self.positive_tests)
        self.kf = self.sum_elements(1, self.negative_tests)
        self.np = self.sum_elements(0, self.positive_tests)
        self.nf = self.sum_elements(0, self.negative_tests)


    """
    Texto extraido do manual da ferramenta Major para definir cada campo dos arquivos mutants.log
    The Major Mutation Framework - (Version 1.3.4 / November 10, 2018)
    3.2.1 Log file for generated mutants
    Major’s compiler generates the log file mutants.log, which provides detailed information about the generated mutants and uses a colon (:) as separator. The log file contains one row per generated mutant, where each row in turn contains 7 columns with the following information:
    	1. Mutants’ unique number (id)
    	2. Name of the applied mutation operator
    	3. Original operator symbol
    	4. Replacement operator symbol
    	5. Fully qualified name of the mutated method
        6. Line number in original source file
    	7. Visualization of the applied transformation (from |==> to)
    The following example gives the log entry for a ROR mutation that has the mutant id 11 and is generated for the method classify (line number 18) of the class Triangle:
    11:ROR:<=(int,int):<(int,int):Triangle@classify:18:a <= 0 |==> a < 0
    """
    def count_instrumented_elements(self, program_dir, program, ver):

        sf = open(program_dir + program + '/' + str(ver) + '/mutants.log', 'r')
        mutants_log = sf.read().split('\n')
        sf.close()

        mutation_log = list()
        mutated_code_lines = list()
        mutants_by_lines = list()
        aux = 0
        for logLine in mutants_log:
            logLine = logLine.split(':')
            if len(logLine) >= 7:
                mutation_log.append(logLine)

                mut_line = logLine[4].split('@')[0]+'#'+logLine[5]
                if len(mutated_code_lines) == 0 or mut_line != mutated_code_lines[-1]:
                    mutated_code_lines.append(mut_line)
                    mutants_by_lines.append(list())
                mutants_by_lines[-1].append(aux)
                aux += 1

        return mutated_code_lines, mutants_by_lines, mutation_log

if __name__ == "__main__":
    mut = Mutation('/Users/diogofreitas/PycharmProjects/d4jdata/data/', 'Chart', 12)

    print(mut.elements)
    print(mut.kp)
    print(mut.kf)
    print(mut.np)
    print(mut.nf)
    print(mut.mutants_by_lines)
    print(mut.code_lines)

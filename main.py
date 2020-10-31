# coding=utf-8
# This is a sample Python script.

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import mutants.mutation_data_json as mJSON
import mutants.MutationPickles as MP
import statistics
import csv

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print("Hi, {0}".format(name))  # Press ⌘F8 to toggle the breakpoint.

def read_pickles(programDir,program,tSet):
    # data = mJSON.MutationJSON(programDir,program,tSet)
    data = MP.MutationPickles(programDir,program,tSet)

    testesPositivos = []
    testesNegativos = []
    testes = []
    for i in range(len(data.mutants)):
        testesPositivos.append(data.kp[i][0] + data.np[i][0])
        testesNegativos.append(data.kf[i][0] + data.nf[i][0])
        testes.append(data.kp[i][0] + data.np[i][0] + data.kf[i][0] + data.nf[i][0])

    print(program)
    print("versoes: " + str(len(data.mutants)))
    print("numero de mutantes:")
    print(data.mutants)
    print("média: " + str(statistics.mean(data.mutants)))
    print("desvio padrão: " + str(statistics.pstdev(data.mutants)))
    print("testes positivos: ")
    print(testesPositivos)
    print("média: " + str(statistics.mean(testesPositivos)))
    print("desvio padrão: " + str(statistics.pstdev(testesPositivos)))
    print("testes negativos: ")
    print(testesNegativos)
    print("média: " + str(statistics.mean(testesNegativos)))
    print("desvio padrão: " + str(statistics.pstdev(testesNegativos)))
    print("teste:")
    print(testes)
    print("média: " + str(statistics.mean(testes)))
    print("desvio padrão: " + str(statistics.pstdev(testes)))

    print("lines:")
    print(data.lines)

    aux = ""
    for faulty_line in data.faultyLines:
        aux += str(len(faulty_line)) + ","
    print(aux)

## Imprime os arquivos buggy.lines
def read_buggy_lines(programDir,program, versions):
    for ver in range(versions):
        blf = open(programDir + program + '/' + program + '-' + str(ver+1) + '.buggy.lines', 'r')
        reader = csv.reader(blf, delimiter=' ')
        lines = list(reader)
        aux = str(ver+1)
        for line in lines:
            aux += "," + line[0]
        print(aux)
        blf.close()

def averageMutants(program):
    pass

import csv

def call_count_test_cases(programDir, program, tSet):
    data = MP.MutationPickles(programDir,program,tSet)

    success_test_cases = []
    failed_test_cases = []
    total = []
    version = []
    for i in range(len(data.mutants)):
        success_test_cases.append(data.kp[i][0] + data.np[i][0])
        failed_test_cases.append(data.kf[i][0] + data.nf[i][0])
        total.append(data.kp[i][0] + data.np[i][0] + data.kf[i][0] + data.nf[i][0])

    print(success_test_cases)
    print(failed_test_cases)
    print(total)


    # with open('count_test_cases.csv', 'a') as csvfile:
    #     filewriter = csv.writer(csvfile, delimiter=',',
    #                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
    #     # version | type | number of positive test cases | number of negative test cases | total of test cases
    #     filewriter.writerow([version, type, success_test_cases, failed_test_cases, total])



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    mJSON.writeMutVariablesJSON("/Users/diogofreitas/PycharmProjects/d4jdata/data/killmaps/", "Chart", "todos1")

    # read_pickles("/Users/diogofreitas/PycharmProjects/d4jdata/data/killmaps/", "Chart", "todos1")
    # read_pickles("/Users/diogofreitas/PycharmProjects/d4jdata/data/killmaps/", "Math", "todos1")
    # read_pickles("/Users/diogofreitas/PycharmProjects/d4jdata/data/killmaps/", "Lang", "todos1")

    # read_buggy_lines("/Users/diogofreitas/PycharmProjects/d4jdata/data/killmaps/", "Lang", 65)
    # read_buggy_lines("/Users/diogofreitas/PycharmProjects/d4jdata/data/killmaps/", "Math", 106)

    # call_count_test_cases("/Users/diogofreitas/PycharmProjects/d4jdata/data/killmaps/", "Lang", "todos1")



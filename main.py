# coding=utf-8
# This is a sample Python script.

# Press ⇧F10 to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import mutants.mutation_data_json as mJSON

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print("Hi, {0}".format(name))  # Press ⌘F8 to toggle the breakpoint.

def read_pickles(programDir,program,tSet):
    data = mJSON.MutationJSON(programDir,program,tSet)
    print(data.faultyLines)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    mJSON.writeMutVariablesJSON("/Users/diogofreitas/PycharmProjects/d4jdata/data/killmaps/", "Chart", "todos1")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

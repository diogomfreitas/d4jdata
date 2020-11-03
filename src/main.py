from src.json import json_data

def write_mutation_json(program_dir, program, version_file):
    verFile = open(program_dir + program + '/' + version_file, 'r')
    versions = verFile.read().rstrip('\n').split(' ')
    json_data.write_mutation_spectra_json(program_dir, program, versions)
    verFile.close()

def write_control_flow_json(program_dir, program, version_file):
    verFile = open(program_dir + program + '/' + version_file, 'r')
    versions = verFile.read().rstrip('\n').split(' ')
    json_data.write_control_flow_json(program_dir, program, versions)
    verFile.close()

def write_data_flow_json(program_dir, program, number_of_versions):
    versions = list()
    for i in range(1, number_of_versions + 1):
        versions.append(str(i) + 'b')
    json_data.write_data_flow_json(program_dir, program, versions)

if __name__ == '__main__':
    # write_mutation_json("/Users/diogofreitas/PycharmProjects/d4jdata/data/", "Chart", "todos1")
    # write_control_flow_json("/Users/diogofreitas/PycharmProjects/d4jdata/data/", "Chart", "todos1")
    write_data_flow_json("/Users/diogofreitas/PycharmProjects/d4jdata/data/", "Chart", 26)
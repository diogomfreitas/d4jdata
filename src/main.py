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

if __name__ == '__main__':
    # write_mutation_json("/Users/diogofreitas/PycharmProjects/d4jdata/data/", "Chart", "todos1")
    write_control_flow_json("/Users/diogofreitas/PycharmProjects/d4jdata/data/", "Chart", "todos1")
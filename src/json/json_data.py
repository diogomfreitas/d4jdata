import json

from src.spectrum.mutation import Mutation
from src.spectrum.coverage import Coverage
from src.spectrum.data_flow import DataFlow


def write_mutation_spectra_json(program_dir, program, versions):
    # verFile = open(program_dir + program + '/' + tSet, 'r')
    # versions = verFile.read().rstrip('\n').split(' ')
    # verFile.close()

    for ver in versions:
        mut_variables_list = Mutation(program_dir, program, ver)

        # mutants_by_lines contem os indices das versoes de cada vetor
        # code_lines contem o endereco da linha que sofreu a mutacao. Eh preciso replicar para as linhas que tem mais de um mutante
        code_lines = list()
        for i in range(len(mut_variables_list.mutants_by_lines)):
            for j in range(len(mut_variables_list.mutants_by_lines[i])):
                code_lines.append(mut_variables_list.code_lines[i])

        root = {
            "version": program + "_" + ver + "b",
            "type": "MUTANT",
            "elements": []
        }
        for i in range(mut_variables_list.elements):
            json_aux = {}

            # split_codelines = code_lines[i].split("#")
            # json_aux["name"] = split_codelines[0]
            # json_aux["location"] = split_codelines[1]

            split_codelines = mut_variables_list.code_lines[i].split("#")
            json_aux["name"] = split_codelines[0]
            json_aux["location"] = split_codelines[1]

            for m in mut_variables_list.mutants_by_lines[i]:
                mutant_json = {}
                mutant_json["Mutation Operator"] = mut_variables_list.mutation_log[m][1]
                mutant_json["Original Operator Symbol"] = mut_variables_list.mutation_log[m][2]
                mutant_json["Replacement Operator Symbol"] = mut_variables_list.mutation_log[m][3]
                mutant_json["Fully Qualified Name"] = mut_variables_list.mutation_log[m][4]
                mutant_json["Line Number In Original Source File"] = mut_variables_list.mutation_log[m][5]
                mutant_json["Applied Transformation"] = mut_variables_list.mutation_log[m][6]

                mutant_json["mkp"] = mut_variables_list.kp[m]
                mutant_json["mkf"] = mut_variables_list.kf[m]
                mutant_json["mnp"] = mut_variables_list.np[m]
                mutant_json["mnf"] = mut_variables_list.nf[m]
                json_aux[mut_variables_list.mutation_log[m][0]] = mutant_json

            root["elements"].append(json_aux)
            # print (json_aux)

        with open(program_dir + program + '/' + str(ver) + "/mutation.json", 'w') as file:
            file.write(json.dumps(root, indent=2))


def write_control_flow_json(program_dir, program, versions):

    for ver in versions:
        control_flow_spectra = Coverage(program_dir, program, ver)

        root = {
            "version": program + "_" + ver + "b",
            "type": "LINE",
            "elements": []
        }
        for i in range(control_flow_spectra.lines):
            json_aux = {}

            # split_codelines = code_lines[i].split("#")
            # json_aux["name"] = split_codelines[0]
            # json_aux["location"] = split_codelines[1]

            split_codelines = control_flow_spectra.code_lines[i].split("#")
            json_aux["name"] = split_codelines[0]
            json_aux["location"] = split_codelines[1]

            json_aux["cep"] = control_flow_spectra.cep[i]
            json_aux["cef"] = control_flow_spectra.cef[i]
            json_aux["cnp"] = control_flow_spectra.cnp[i]
            json_aux["cnf"] = control_flow_spectra.cnf[i]

            root["elements"].append(json_aux)
            # print (json_aux)

        with open(program_dir + program + '/' + str(ver) + "/control_flow.json", 'w') as file:
            file.write(json.dumps(root, indent=2))

def write_data_flow_json(program_dir, program, versions):

    for ver in versions:
        data_flow_spectra = DataFlow(program_dir, program, ver)

        root = {
            "version": program + "_" + ver,
            "type": "DUA",
            "elements": []
        }
        for i in range(data_flow_spectra.lines):
            json_aux = {}

            # split_codelines = code_lines[i].split("#")
            # json_aux["name"] = split_codelines[0]
            # json_aux["location"] = split_codelines[1]

            split_codelines = data_flow_spectra.code_lines[i].split("#")
            json_aux["name"] = split_codelines[0]
            json_aux["location"] = split_codelines[1]

            json_aux["cep"] = data_flow_spectra.cep[i]
            json_aux["cef"] = data_flow_spectra.cef[i]
            json_aux["cnp"] = data_flow_spectra.cnp[i]
            json_aux["cnf"] = data_flow_spectra.cnf[i]
            json_aux["methods"] = json_aux.methods[i]
            json_aux["var"] = json_aux.vars[i]
            json_aux["def"] = json_aux.defs[i]
            json_aux["use"] = json_aux.uses[i]



            root["elements"].append(json_aux)
            # print (json_aux)

        with open(program_dir + program + '/' + str(ver) + "/data_flow.json", 'w') as file:
            file.write(json.dumps(root, indent=2))
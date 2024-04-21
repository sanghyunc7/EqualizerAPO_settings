# first flatten eqapo
# then using dsp_template, create json
# then use json->yml library to make yml output
import sys
import os
import yaml
import json
from copy import deepcopy

from flatten_for_camilladsp import Flat_TXT


filter_template = {
    "description": "",
    "parameters": {"freq": 100, "gain": 0, "q": 1, "type": "Peaking"},
    "type": "Biquad",
}

preamp_template = {
    "description": "",
    "parameters": {"gain": 0, "scale": "dB"},
    "type": "Gain",
}


class Translator:
    def __init__(self, input_file, output_file):
        self.txt = Flat_TXT(input_file).get_flat()
        self.output_file = output_file
        self.yml = None
        with open("dsp_template.json", "r") as file:
            self.jsn = json.load(file)

    # expects array of str
    # outputs json that adheres to dsp formatting

    def extract_data(self, txt_field):
        values = txt_field.split(":")
        words = values[1].split()
        d = {}
        if "Preamp" == values[0]:
            d["data_type"] = "Preamp"
            d["gain"] = float(words[0])
        else:
            d["data_type"] = "Filter"
            d["type"] = "Peaking"
            if words[1] in ["LSC", "LS"]:
                d["type"] = "Lowshelf"
            elif words[1] == ["HSC", "HS"]:
                d["type"] = "Highshelf"
            d["freq"] = float(words[3])
            d["gain"] = float(words[6])
            if words[1] in ["HS", "LS"]:
                d["q"] = 0.9
            else:
                d["q"] = float(words[-1])
        return d

    def padded(self, i, padding):
        left_zeros = padding - len(str(i))
        return "0" * left_zeros + str(i)

    def txt_to_json(self):
        padding = len(str(len(self.txt)))

        for i, v in enumerate(self.txt):
            d = self.extract_data(v)
            if d["data_type"] == "Preamp":
                config = deepcopy(preamp_template)
                name = "Preamp_" + self.padded(i, padding)
                config["description"] = v
                config["parameters"]["gain"] = d["gain"]
            else:
                name = "Filter_" + self.padded(i, padding)
                config = deepcopy(filter_template)
                config["description"] = v
                config["parameters"]["freq"] = d["freq"]
                config["parameters"]["gain"] = d["gain"]
                config["parameters"]["q"] = d["q"]
                config["parameters"]["type"] = d["type"]
            self.jsn["filters"][name] = config
            self.jsn["pipeline"][1]["names"].append(name)  # channel 1 left ear
            self.jsn["pipeline"][2]["names"].append(name)  # channel 2 right ear

    def json_to_yaml(self):
        with open(self.output_file, "w") as yaml_file:
            yaml.dump(self.jsn, yaml_file)


if __name__ == "__main__":
    input_file = sys.argv[1]
    if not input_file.endswith(".txt"):
        print("input text file")
        sys.exit(1)
    output_file = input_file[:-4] + ".yml"
    translator = Translator(input_file, output_file)
    translator.txt_to_json()
    translator.json_to_yaml()
    print("Done")

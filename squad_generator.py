#/usr/bin/env python

import random
import yaml
import argparse
import os
import sys
from appJar import gui

#TODO
class DefineMaps:

    def __init__(self, country):
        self.country = country
        self.first_name_yaml = "yaml_maps/names_first_" + country  + ".yaml"
        self.last_name_yaml  = "yaml_maps/names_last_" + country + ".yaml"
        self.platoon_yaml    = "yaml_maps/squad_map_" + country + ".yaml"
        self.attribute_yaml  = 'yaml_maps/attribute_map.yaml'

        self.rep_dict = {
            'us': [3,3,4,4,4,5],
            'br': [3,4,4,4,4,5],
            'ge': [3,4,4,4,5,5],
            'ru': [3,3,4,4,4,5],
        }

    def load_yaml_files(self, map):
        with open(map) as f:
            return(yaml.load(f))
        f.close()

""" class GenerateUserInterface:

    def __init__(self, *args, **kwargs):
        pass


    
    def file_menu(self, country_code, platoon_type):
        while True:
            directory = input("Enter a directory to save files: ")
            if not (os.path.isdir(directory)):
                print("Directory does not exist: %s" % directory)
            else:

                yaml_file = os.path.join(directory, country_code + platoon_type + ".yaml")
                html_file = os.path.join(directory, country_code + platoon_type + ".html")
                if os.path.exists(yaml_file) or os.path.exists(html_file):
                    print("Files %s or %s already exist.  Will not over write." % (yaml_file, html_file))
                    print("Move or delete these files manaually first")
                    input("Press any key to quit")
                    sys.exit()
                else:
                    return(yaml_file, html_file) """


if __name__ == "__main__":
    top_level = [
        "Generate New Platoon",
  #      "Update Existing Platoon",
    ]

    country_codes = {
            "United States": "us",
            "Britain": "br",
            "Germany": "ge",
            "Russia": "ru",
    }

    platoon_types = {
        "us": ["Infantry", "Paratroopers", "Rangers", "Armored_Infantry"],
        "ru": ["Infantry", "SMG", "Tank_Riders"],
        "ge": ["Infantry", "Volks_Grenadiers", "Airborne"],
        "br": ["Infantry", "Paratroopers"],
    }

    def get_country_code():
        country_list = []
        for key in country_codes:
            country_list.append(key)
        country_key = gen_menu.menu_ui(country_list)
        return(country_codes[country_key])


    gen_menu = GenerateMenu()
    menu_choice = gen_menu.menu_ui(top_level)
    if menu_choice == "Generate New Platoon":
        country_code = get_country_code()
        platoon_type = gen_menu.menu_ui(platoon_types[country_code])
        gen_platoon = GeneratePlatoon(country_code, platoon_type)
        platoon = gen_platoon.get_platoon()
        man_files = ManageFiles("platoons/%s" %  country_code, "%s_%s" % (country_code, platoon_type) )
        man_files.check_yaml_overwrite()
        man_files.write_files(platoon)
    elif menu_choice ==  "Update Existing Platoon":
        country_code = get_country_code()
        platoon_type = gen_menu.menu_ui(platoon_types[country_code])
        man_files = ManageFiles("platoons/%s" %  country_code, "%s_%s" % (country_code, platoon_type))
        yaml_map = man_files.get_yaml()
        update_status = UpdatePlatoon(country_code, platoon_type, yaml_map)
        update_status.update_squad()





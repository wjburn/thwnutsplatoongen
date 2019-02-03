#/usr/bin/env python

import random
import yaml
import argparse
import os
import sys

class DefineMaps:

    def __init__(self, country):
        self.country = country
        self.first_names_map = {
            'us': 'yaml_maps/names_first_us.yaml',
            'ge': 'yaml_maps/names_first_ge.yaml',
            'br': 'yaml_maps/names_first_br.yaml',
            'ru': 'yaml_maps/names_first_ru.yaml',
        }
        self.last_names_map = {
            'us': 'yaml_maps/names_last_us.yaml',
            'ge': 'yaml_maps/names_last_ge.yaml',
            'br': 'yaml_maps/names_last_br.yaml',
            'ru': 'yaml_maps/names_last_ru.yaml',
        }
        self.platoon_map = {
            'us': 'yaml_maps/squad_map_us.yaml',
            'ge': 'yaml_maps/squad_map_ge.yaml',
            'br': 'yaml_maps/squad_map_br.yaml',
            'ru': 'yaml_maps/squad_map_ru.yaml',
        }
        self.rep_map = {
            'us': [3,3,4,4,4,5],
            'br': [3,4,4,4,4,5],
            'ge': [3,4,4,4,5,5],
            'ru': [3,3,4,4,4,5],
        }
        self.attribute_map = 'yaml_maps/attribute_map.yaml'

    def load_attributes(self):
        self.attribute_dict = self.load_yaml_files(self.attribute_map)
        return(self.attribute_dict)
    
    def load_names(self):
        self.first_name_dict = self.load_yaml_files(self.first_names_map[self.country])
        self.last_name_dict  = self.load_yaml_files(self.last_names_map[self.country])
        return(self.first_name_dict, self.last_name_dict)
    
    def load_platoons(self):
        self.platoon_dict = self.load_yaml_files(self.platoon_map[self.country])
        return(self.platoon_dict)

    def load_reps(self):
        self.rep_list = self.rep_map[self.country]
        return(self.rep_list)

    def load_yaml_files(self, map):
        with open(map) as f:
            return(yaml.load(f))
        f.close()


class RollDice:
    def __init__(self):
        pass
            
    #generate a number with a base of one to six
    #if d increases the base by a multiple of one and six
    def roll_d6(self, d=1):
        start = 1 * d
        end   = 6 * d
        return(random.randint(start,end))

class GenerateCharacter(DefineMaps):
    def __init__(self, country):
        DefineMaps.__init__(self, country)
        self.attribute_dict = self.load_attributes()
        self.load_names     = self.load_names()
        self.load_reps      = self.load_reps()
        roll_dice = RollDice()
        self.roll_d6 = roll_dice.roll_d6()

    #if attribute_tree is 5 or less, use the v4 attributes table
    #else use compendium attributes table and returns of "reroll" are re-generated until another result is returned
    def get_attribute(self):
        attribute_tree = self.roll_d6()
        while True:
            if attribute_tree < 5:
                attribute = self.attribute_dict["Nuts_v4_Attributes_Table"][self.roll_d6()][self.roll_d6()]
            else:
                attribute = self.attribute_dict["Nuts_Compendium_Attributes_Table"][self.roll_d6()][self.roll_d6()]
            if attribute != "reroll":
                return(attribute)
    
    def get_first_name(self):
        first_name = self.first_name_dict["First_Names"][self.roll_d6()][self.roll_d6()][self.roll_d6()]
        return(first_name)

    def get_last_name(self):
        last_name = self.last_name_dict["Last_Names"][self.roll_d6()][self.roll_d6()][self.roll_d6()]
        return(last_name)

    def get_rep(self):
        rep_val = self.roll_d6()
        rep_val -= 1
        return(self.rep_list[rep_val])


class GeneratePlatoon(GenerateCharacter):

    def __init__(self, country, platoon_type):
        DefineMaps.__init__(self, country)
        GenerateCharacter.__init__(self, country)
        self.platoon_dict = self.load_platoons()
        self.platoon_type = platoon_type
        roll_dice = RollDice()
        self.roll_d6 = roll_dice.roll_d6

#generate a platoon from squads
    def get_platoon(self):
        squad_list = []
        platoon_size = int(self.platoon_dict[self.platoon_type]['platoon'])
        for x in range(platoon_size):
            squad_list.append(self.generate_squad())
        return(squad_list)

#generate squads from characters
    def generate_squad(self):
        squad_members = []
        #numer of roles per squad, NCO 1 where as rifle may be 7
        roles = {
            "NCO": int(self.platoon_dict[self.platoon_type]['NCO']),
            "JrNCO": int(self.platoon_dict[self.platoon_type]['JrNCO']),
            "LMG": int(self.platoon_dict[self.platoon_type]["LMG"]),
            "LMG_Assist": int(self.platoon_dict[self.platoon_type]["LMG_Assist"]),
            "SA_Genernade_Rifle": int(self.platoon_dict[self.platoon_type]["SA_Gerenade_Rifle"]),
            "Rifle": int(self.platoon_dict[self.platoon_type]["Rifle"]),
        }
        #squad size is determined by base size and then add xd6 (e.g. 1d6)
        squad_size = self.platoon_dict[self.platoon_type]['base'] + self.roll_d6(self.platoon_dict[self.platoon_type]['d6'])
        #if the above value is greater than squad max size, set size to max
        if squad_size > self.platoon_dict[self.platoon_type]['max']:
            squad_size = self.platoon_dict[self.platoon_type]['max']
        #assign a role to each character and remove 1 from the role value, ensuring that the correct number of roles are assigned per squad
        for x in range(squad_size):
            for key, value in roles.items():
                if roles[key] > 0:
                    role = key
                    roles[key] -= 1
                    break

        #each character has, (last_name,first_name/role/attribute/rep/status)
            character = {
                'name': "%s, %s" % (self.get_last_name(), self.get_first_name()),
                'role': role,
                'rep': self.get_rep(),
                'attribute':  self.get_attribute(),
                'status': 'active'
            }
            squad_members.append(character)
        return(squad_members)


class GenerateUserInterface:

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
                    return(yaml_file, html_file)


class ManageFiles:
    def __init__(self, directory):
        self.directory = directory
        self.yaml_file = os.path.join(directory, header + ".yaml")
        self.html_file = os.path.join(directory, header + ".html")


    def check_yaml_overwrite(self):
        try:
            if not os.path.exists(self.directory):
                os.makedirs(self.directory)
            # check to see if file is an overwrite
            file_path = os.path.abspath(self.yaml_file)
            if os.path.exists(file_path):
                inp = input("File exists %s\n Do you want to overwrite? (y/n): " % file_path)
                if inp == 'y' or inp == 'yes':
                    return(1)
                else:
                    return
            else:
                return(1)
        except (PermissionError, FileNotFoundError):
            print("Permission denied writing file to %s\n" % file_path)
            input("Press any key to exit")
            sys.exit()
        
    def write_files(self, content, header):
        self.write_yaml(content, header)
        self.write_html()
            

    def save_file(self, save_file, file_content):
        try:
            with open(save_file, "w") as f:
                for line in file_content:
                    f.write("%s\n" % line)
            f.close()
            file_path = os.path.abspath(save_file)
            print("wrote to file: %s" % file_path)
            input("Press any key")
        except (PermissionError, FileNotFoundError):
            print("Permission denied writing file to %s\n" % save_file)
            input("Press any key to exit")
            sys.exit()
            

    def write_yaml(self, content_dict, header, section_title='squad', entry_title='name'):
        x = 0
        content_yaml = []
        content_yaml.append("%s:" % header)
        for section in content_dict:
            content_yaml.append("    %s_%s:" % (section_title, x + 1))
            for entry in section:
                for key in entry:
                    if key == entry_title:
                        content_yaml.append("        - %s: %s" % (key, entry[key]))
                    else:
                        content_yaml.append("          %s: %s" % (key, entry[key]))
            x += 1
        
        self.save_file(self.yaml_file, content_yaml)
        return(self.yaml_file)

    def write_html(self):
        with open(self.yaml_file) as f:
            yaml_map = yaml.load(f)
        f.close()

        content_html = []
        for key in yaml_map:
            content_html.append("<html>\n<body>\n")
            content_html.append("<style>\ntable {\nfont-family: arial, sans-serif;\nborder-collapse: collapse;\n  width: 100%;\n}\n")
            content_html.append("td, th {\n  border: 3px solid #dddddd;\n text-align: left;\n  padding: 2px;\nvertical-align: bottom;\n}\n")
            content_html.append("tr:nth-child(even) {\n  background-color: #dddddd;\n}\n")
            content_html.append("</style>\n</head>\n<body>\n")
            content_html.append("<B>%s</B><p>\n" % key)
            content_html.append("<table>\n")
            for sub_key1 in yaml_map[key]:
                content_html.append("<tr>\n")
                content_html.append("<th width=\"1px\">%s</th>\n" % sub_key1)
                content_html.append("<th>Name</th>\n")
                content_html.append("<th>Role</th>\n")
                content_html.append("<th>Rep</th>\n")
                content_html.append("<th>Attribute</th>\n")
                content_html.append("<th>Status</th>\n")
                content_html.append("</tr>\n")
                x = 1
                for value in yaml_map[key][sub_key1]:
                    content_html.append("<tr>\n")
                    content_html.append("<td>%s</td>" % x)
                    content_html.append("<td>%s</td>\n" % value['name'])
                    content_html.append("<td>%s</td>\n" % value['role'])
                    content_html.append("<td>%s</td>\n" % value['rep'])
                    content_html.append("<td>%s</td>\n" % value['attribute'])
                    content_html.append("<td>%s</td>\n" % value['status'])
                    content_html.append("</tr>\n")
                    x += 1
        content_html.append("</table>\n")
        content_html.append("</body>\n")
        content_html.append("</html>\n")

        self.save_file(self.html_file, content_html)



class GenerateMenu:
    def __init__(self):
        pass

    def menu_ui(self, menu_items):
        while True:
            try:
                for item in range(len(menu_items)):
                    print(str(item+1) + ":", menu_items[item])
                inp = int(input("Enter a numeric value: "))
                if inp-1 in range(len(menu_items)):
                    return(menu_items[inp-1])
                else:
                    print("Invalid Menu Option")
            except ValueError:
                print("Invalid Input, use numeric values")



if __name__ == "__main__":
    top_level = [
        "Generate New Platoon",
    #    "Update Existing Platoon",
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
        return(country_codes[gen_menu.menu_ui(country_list)])

    gen_menu = GenerateMenu()
#    menu_choice = gen_menu.menu_ui(top_level)
#    if menu_choice == "Generate New Platoon":
    try:
        country_code = get_country_code()
        platoon_type = gen_menu.menu_ui(platoon_types[country_code])
        gen_platoon = GeneratePlatoon(country_code, platoon_type)
        platoon = gen_platoon.get_platoon()
        header = ("%s_%s" % (country_code, platoon_type))
        directory = ("platoons/%s" %  country_code)
        man_files = ManageFiles(directory)
        man_files.check_yaml_overwrite()
        man_files.write_files(platoon, header)
    except FileNotFoundError as e:
        print(str(e))

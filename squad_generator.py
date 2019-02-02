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
    
class GenerateYaml:

    def __init__(self, yaml_file):
        self.yaml_file = yaml_file

    #manually generate yaml formatting and pass off for writing
    def write_yaml(self, platoon, country_code, platoon_type):
        x = 0
        platoon_yaml = []
        platoon_yaml.append("%s_%s:" % (country_code, platoon_type))
        for squad in platoon:
            platoon_yaml.append("    Squad_%s:" % (x +  1))
            for character in squad:
                for key in character:
                    if key == 'name':
                        platoon_yaml.append("        - %s: %s" % (key, character[key]))
                    else:
                        platoon_yaml.append("          %s: %s" % (key, character[key]))
            x += 1
        self.write_yaml(platoon_yaml)
        return(platoon_yaml)

    def write_yaml(self, data):
        with open(self.yaml_file, "w") as f:
            for item in data:
                f.write("%s\n" % item)
        f.close()

class GenerateHTML:

    def __init__(self, yaml_file, html_file):
        self.html_file = html_file
        self.yaml_file = yaml_file
    
    def write_html(self):
        with open(self.yaml_file) as f:
            yaml_map = yaml.load(f)
        f.close()

        html_data = []
        for key in yaml_map:
            html_data.append("<html>\n<body>\n")
            html_data.append("<style>\ntable {\nfont-family: arial, sans-serif;\nborder-collapse: collapse;\n  width: 100%;\n}\n")
            html_data.append("td, th {\n  border: 3px solid #dddddd;\n text-align: left;\n  padding: 2px;\nvertical-align: bottom;\n}\n")
            html_data.append("tr:nth-child(even) {\n  background-color: #dddddd;\n}\n")
            html_data.append("</style>\n</head>\n<body>\n")
            html_data.append("<B>%s</B><p>\n" % key)
            html_data.append("<table>\n")
            for sub_key1 in yaml_map[key]:
                html_data.append("<tr>\n")
                html_data.append("<th width=\"1px\">%s</th>\n" % sub_key1)
                html_data.append("<th>Name</th>\n")
                html_data.append("<th>Role</th>\n")
                html_data.append("<th>Rep</th>\n")
                html_data.append("<th>Attribute</th>\n")
                html_data.append("<th>Status</th>\n")
                html_data.append("</tr>\n")
                x = 1
                for value in yaml_map[key][sub_key1]:
                    html_data.append("<tr>\n")
                    html_data.append("<td>%s</td>" % x)
                    html_data.append("<td>%s</td>\n" % value['name'])
                    html_data.append("<td>%s</td>\n" % value['role'])
                    html_data.append("<td>%s</td>\n" % value['rep'])
                    html_data.append("<td>%s</td>\n" % value['attribute'])
                    html_data.append("<td>%s</td>\n" % value['status'])
                    html_data.append("</tr>\n")
                    x += 1
        html_data.append("</table>\n")
        html_data.append("</body>\n")
        html_data.append("</html>\n")
        with open(self.html_file, "w") as f:
            for line in html_data:
                    f.write(line)
        f.close()

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
    def __init__(self):
        pass

    def check_overwrite(self, file):
        if os.path.exists(file):
            inp = input("File exists, do you want to overwrite? (y/n): ")
            if inp == 'y' or inp == 'yes':
                return(1)
            else:
                return
                


    def save_file(self, file_name):
        while True:
            directory = input("Enter a directory to save files: ")
            if not os.path.exists(directory):
                os.makedirs(directory)

            yaml_file = os.path.join(directory, file_name + ".yaml")
            html_file = os.path.join(directory, file_name + ".html")
            if self.check_overwrite(yaml_file):
                write_yaml(yaml_file)
                write_html(html_file)
            

#            if os.path.exists(yaml_file):
#                print("File exists, do you want to overwrite (y/n: ")
#                if 
#                 or os.path.exists(html_file):
#                print("Files %s or %s already exist.  Will not over write." % (yaml_file, html_file))
#                print("Move or delete these files manaually first")
#                input("Press any key to quit")
#                sys.exit()
#            else:
#                return(yaml_file, html_file)
#
            


class GenerateMenu:
    def __init__(self):
        pass

    def menu_ui(self, menu_items):
        for item in range(len(menu_items)):
            print(str(item+1) + ":", menu_items[item])
        inp = int(input("Enter a numeric value: "))
        return(menu_items[inp-1])


if __name__ == "__main__":
    top_level = [
        "Generate New Platoon",
        "Update Existing Platoon",
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
    menu_choice = gen_menu.menu_ui(top_level)
    if menu_choice == "Generate New Platoon":
        country_code = get_country_code()
        gen_menu.menu_ui(platoon_types[country_code])


    


#    if not args.country_code:
#        args.country_code = gen_ui.countries_menu()
#    if not args.platoon_type:
#        args.platoon_type = gen_ui.platoon_menu(args.country_code)
#    if not args.file_name:
#        (yaml_file, html_file) = gen_ui.file_menu(args.country_code, args.platoon_type)
#    else:
#       yaml_file = args.file_name + ".yaml"
#       html_file = args.file_name + ".html"
#
#            
#
#
#    #generate a new platoon based on country code and platoon type
#    gen_platoon = GeneratePlatoon(args.country_code, args.platoon_type)
#    platoon = gen_platoon.get_platoon()
#
#    #using the platoon output from above, parse the data into yaml format and store to a file
#    gen_yaml = GenerateYaml(yaml_file)
#    platoon_yaml = gen_yaml.write_platoon(platoon, args.country_code, args.platoon_type)
#
#    #using the above generated yaml file, create an html file for user consumption
#    gen_html = GenerateHTML(yaml_file, html_file)
#    gen_html.write_html()
#
#    print("You can find your html file here: %s" % html_file)
#    input("Press any key to exit")

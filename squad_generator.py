#/usr/bin/env python
#
#import random
#import yaml
#import argparse
#import os
#import sys
#from appJar import gui
import manage_ui
import manage_platoons


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




    menu = manage_ui.MenuManagement()

    menu_choice = menu.menu_ui(top_level)
    if menu_choice == "Generate New Platoon":
        platoon_generation = manage_platoons.GeneratePlatoon()
        platoon_generation.set_roles()
        platoon_generation.set_member_attributes()
        
#        gen_platoon = GeneratePlatoon(country_code, platoon_type)
#        platoon = gen_platoon.get_platoon()
#        man_files = ManageFiles("platoons/%s" %  country_code, "%s_%s" % (country_code, platoon_type) )
#        man_files.check_yaml_overwrite()
#        man_files.write_files(platoon)
#    elif menu_choice ==  "Update Existing Platoon":
#        country_code = get_country_code()
#        platoon_type = gen_menu.menu_ui(platoon_types[country_code])
#        man_files = ManageFiles("platoons/%s" %  country_code, "%s_%s" % (country_code, platoon_type))
#        yaml_map = man_files.get_yaml()
#        update_status = UpdatePlatoon(country_code, platoon_type, yaml_map)
#        update_status.update_squad()





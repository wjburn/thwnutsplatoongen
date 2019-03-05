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
import manage_files


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
    main_menu = [
        "Generate New Platoon",
        "Update Existing Platoon",
    ]




    menu = manage_ui.MenuManagement()

    menu_choice = menu.menu_ui(main_menu)
    if menu_choice == "Generate New Platoon":
        platoon_generation = manage_platoons.GeneratePlatoon()
        (country_code, platoon_type, platoon) = platoon_generation.get_platoon()
        file_generation = manage_files.GenerateContent(country_code, platoon_type, platoon)
        file_generation.write_platoon_files()

    elif menu_choice ==  "Update Existing Platoon":
        update_status = manage_platoons.UpdatePlatoon()
        (platoon, mia_pow, hospital, deceased) = update_status.update_platoon()
        print("Platoon %s" % platoon)
        print("MIA %s" % mia_pow)
        print("Hospital %s" % hospital)
        print("Deceased %s" % deceased)

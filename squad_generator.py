#/usr/bin/env python
#
#import random
#import yaml
#import argparse
import os
#import sys
#from appJar import gui
import manage_ui
import platoon 


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


#if __name__ == "__main__":
#    main_menu = [
#        "Generate New Platoon",
#        "Update Existing Platoon",
# #       "Generate Replacements",
#    ]
#
#
#
#
#    menu = manage_ui.MenuManagement()
country_code = 'us'
infantry_type = 'Paratroopers'
#
#    menu_choice = menu.menu_ui(main_menu)
manage_platoon = platoon.Platoon(country_code, infantry_type, debug=1)
platoon = manage_platoon.get_platoon(generate_new=1)
print(platoon)
#        (country_code, platoon_type, platoon_list) = platoon_generation.get_platoon()
#        file_generation = manage_files.GenerateContent()
#        platoon_file = "%s_%s" % (country_code, platoon_type)
#        file_generation.write_yaml('platoons', country_code, platoon_file, platoon_list)
#        html_content = file_generation.generate_html(country_code, platoon_file)
#        file_generation.write_html('platoons', country_code, platoon_file, html_content)
#
#    if __name__ == "__main__":
#    manage_platoon = Platoon('us', 'Paratroopers')
#    platoon = manage_platoon.get_platoon(generate_new=0)
#    print(platoon)
#        
#
#    elif menu_choice ==  "Update Existing Platoon":
#        update_status = manage_platoons.UpdatePlatoon()
#        (country_code, platoon_type, platoon_list, mia_list, hospital_list, deceased_list) = update_status.update_platoon()
#        file_generation = manage_files.GenerateContent()
#
#        platoon_file = "%s_%s" % (country_code, platoon_type)
#        file_generation.write_yaml('platoons', country_code, platoon_file, platoon_list)
#
#        mia_file = "%s_%s_mia" % (country_code, platoon_type)
#        file_generation.write_yaml('platoons', country_code, mia_file, mia_list, append=1)
#
#        hospital_file = "%s_%s_hospital" % (country_code, platoon_type)
#        file_generation.write_yaml('platoons', country_code, hospital_file, hospital_list, append=1)
#
#        deceased_file = "%s_%s_deceased" % (country_code, platoon_type)
#        file_generation.write_yaml('platoons', country_code, deceased_file, deceased_list, append=1)
#
#    elif menu_choice == "Generate Replacements":
#        replacements = manage_platoons.GenerateReplacements()
#        replacements.replace_leaders()

#    elif menu_choice == "Write HTML":
#        file_generation = manage_files.GenerateContent()
#        yaml_file = 'platoons/us/us_infantry.yaml'
#        html_file = 'platoons/us/us_infantry.html'
#        file_generation.write_hytml(html_file, html_content, append_file=None)
#

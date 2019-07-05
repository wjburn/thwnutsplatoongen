#/usr/bin/env python
import manage_ui
import platoon 
from manage_files import FileManagement


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




debug = 0
country_code_dict = {
    'Britian': 'br',
    'Germany': 'ge',
    'Russia':  'ru',
    'United States': 'us',
}
squad_type_list   =  []
country_code_list =  []
for key in country_code_dict.keys():
    country_code_list.append(key)
print("Generate a Platoon for NUTSv4\n")
print("The following Countrys are available: ")
menu = manage_ui.MenuManagement()
country_code = menu.menu_ui(country_code_list)
fm = FileManagement(country_code_dict[country_code], debug)
squad_attribute_map = fm.load_yaml('squad_map')
print("The following infantry types are available: ")
for attr in squad_attribute_map:
    squad_type_list.append(attr)
infantry_type = menu.menu_ui(squad_type_list)
gen_platoon = platoon.Platoon(country_code_dict[country_code], infantry_type, debug=0)
gen_platoon.write_platoon(generate_new=1)

#country_code = 'us'
#infantry_type = 'Paratroopers'
#
#manage_platoon = platoon.Platoon(country_code, infantry_type, debug=0)
#manage_platoon.get_country_codes()


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
#country_codes = ['br', 'ge', 'ru', 'us']
#print("choose country:")
#i = 1
#for code in country_codes:
#    print(str(i)+": "+ code)
#    i += 1
#user_country = input("Numeric selection: ")
#
#try:

#print(platoon)
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

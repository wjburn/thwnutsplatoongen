import manage_platoon
from manage_files import FileManagement
import os

class Platoon:

    def __init__(self, country_code, infantry_type, generate_new=0, debug=0):
        self.debug = debug
        self.platoon = None
        self.country_code = country_code
        self.infantry_type = infantry_type
        self.mp = manage_platoon.ManagePlatoon(country_code, infantry_type, self.debug) 
        self.fm = FileManagement(self.debug)
        self.platoon = self.get_platoon(generate_new)


    def get_platoon(self, generate_new):
        if generate_new:
            self.platoon = self.mp.generate_platoon()
        else:
            yaml_map_name = self.country_code + '_' + self.infantry_type
            self.platoon_yaml_path = os.path.join(self.country_code, yaml_map_name)
            self.platoon = self.fm.load_yaml('platoons', self.platoon_yaml_path)

        if self.debug:
            print("DEBUG: Platoon class platoon variable value: %s\n" % self.platoon)
        return(self.platoon)


    def update_platoon_member(self, squad, list_val, update_attribute, update_value):
        self.platoon = self.mp.update_squad_member(self.platoon, squad, list_val, update_attribute, update_value)
        print(self.platoon)
        return(self.platoon)

        

if __name__ == "__main__":
    manage_platoon = Platoon('us', 'Paratroopers')
    platoon = manage_platoon.get_platoon(generate_new=0)
    print(platoon)
import manage_platoon
from manage_files import FileManagement
import os

class Platoon:

    def __init__(self, country_code, infantry_type, generate_new=0, debug=0):
        self.debug = debug
        self.platoon = None
        self.country_code = country_code
        self.infantry_type = infantry_type
        self.fm = FileManagement(self.country_code, self.debug)
        self.mp = manage_platoon.ManagePlatoon(country_code, infantry_type, self.debug) 


    def get_platoon(self, generate_new=0):
        if generate_new:
            self.platoon = self.mp.generate_platoon()
        else:
            self.platoon = self.fm.load_yaml('platoon')

        if self.debug:
            print("DEBUG: Platoon class platoon variable value: %s\n" % self.platoon)
        return(self.platoon)


    def update_platoon_member(self, squad, list_val, update_attribute, update_value):
        self.platoon = self.mp.update_squad_member(self.platoon, squad, list_val, update_attribute, update_value)
        print(self.platoon)
        return(self.platoon)

    def write_platoon(self, generate_new=0):
        if generate_new:
            self.get_platoon(generate_new=1)
        self.fm.write_platoon_file(self.platoon, self.infantry_type)

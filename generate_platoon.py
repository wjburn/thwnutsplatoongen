import generate_character
import roll_dice
import manage_files

class ManageSquad:

    def __init__(self, country_code, infantry_type, debug=1):
        self.debug = debug
        self.country_code = country_code
        self.infantry_type = infantry_type
        self.dice_bag = roll_dice.RollDice()
        self.file_management = manage_files.FileManagement()
        self.squad_template = self.load_squad_template()


    def load_squad_template(self):
        #load nuts v4 squad template for country/infantry type  (ie us/paratroopers)
        #template defines member roles and maximum number of characters that can fill that role (ie rifleman:5, bar:1)
        squad_map_file = 'squad_map_' + self.country_code
        squad_map = self.file_management.load_yaml('yaml_map', squad_map_file)
        squad_template = squad_map[self.infantry_type]
        squad_template['country_code'] = self.country_code
        squad_template['infantry_type'] = self.infantry_type 
        return(squad_template)


    def generate_squad(self):
        members = []
        #squad size is the base_size + add_d6 roll
        squad_size = self.squad_template['base_size'] + self.dice_bag.roll_d6()
        #if the generated size is greater than the squad max size, set the squad to max size
        if squad_size > self.squad_template['max_squad_size']:
            squad_size = self.squad_template['max_squad_size']
        for key, value in self.squad_template['roles'].items():
            members += self.fill_squad_role(key, value)
        if self.debug:
            print("\nDEBUG: print squad members: %s\n" % members)


    #fill each role in the squad with a character
    def fill_squad_role(self, role_name, role_count):
        character = {}
        roles = []
        character_objs = [generate_character.GenerateCharacter(self.country_code) for i in range(int(role_count))]
        for obj in character_objs:
            (character['first_name'], character['last_name'], character['rep'], character['attribute']) = obj.get_character()
            character['role'] = role_name
            character['status'] = 'active'
            roles.append(character)
        return(roles)


class ManagePlatoon(ManageSquad):

    def __init__(self, country_code, infantry_type, debug=1):
        self.debug = debug
        self.country_code = country_code
        ManageSquad.__init__(self, country_code, infantry_type)
        self.file_management = manage_files.FileManagement()
        squad_template = self.load_squad_template()
        print("DEBUG: print squads per platoon value:  %s\n" % squad_template['squad_per_platoon'])


    def generate_platoon(self):
        platoon = []
        platoon = [self.generate_squad() for i in range(int(self.squad_template['squad_per_platoon']))]
        return(platoon)


if __name__ == "__main__":
    manage_platoon = ManagePlatoon('us', 'Paratroopers')
    platoon = manage_platoon.generate_platoon()
    print(platoon)
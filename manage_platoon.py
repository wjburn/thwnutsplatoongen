import generate_character
import roll_dice
import manage_files

class ManageSquad:

    def __init__(self, country_code, infantry_type, debug=0):
        self.debug = debug
        self.country_code = country_code
        self.infantry_type = infantry_type
        self.dice_bag = roll_dice.RollDice()
        self.file_management = manage_files.FileManagement()
        self.squad_map_list = ['yaml_maps', 'squad_map_', '.yaml']


    def load_squad_template(self):
        #load nuts v4 squad template for country/infantry type  (ie us/paratroopers)
        #template defines member roles and maximum number of characters that can fill that role (ie rifleman:5, bar:1)
        squad_map_file = self.squad_map_list[1] + self.country_code + self.squad_map_list[2]
        squad_map = self.file_management.load_yaml(self.squad_map_list[0], squad_map_file)
        if self.debug:
            print("country code:%s\ninfantry_type:%s\nsquad_map_file:%s\n" % (self.country_code, self.infantry_type, squad_map_file))
        squad_template = squad_map[self.infantry_type]
        squad_template['country_code'] = self.country_code
        squad_template['infantry_type'] = self.infantry_type 
        return(squad_template)


    def generate_squad(self, squad_template):
        members = []
        #squad size is the base_size + add_d6 roll
        squad_size = squad_template['base_size'] + self.dice_bag.roll_d6()
        #if the generated size is greater than the squad max size, set the squad to max size
        if squad_size > squad_template['max_squad_size']:
            squad_size = squad_template['max_squad_size']
            #roles items
            #roles:
            #NCO: 1
            #JrNCO: 1
            #LMG: 1
            #LMG_Assist: 0
            #SA_Gerenade: 2
            #Rifle: 7
        for key, value in squad_template['roles'].items():
            members += self.fill_squad_role(key, value)
        if self.debug:
            print("\nDEBUG: class ManageSquad variable squad members: %s\n" % members)
        return(members)


    #fill each role in the squad with a character role_count number of times
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

    def __init__(self, country_code, infantry_type, debug=0):
        self.debug = debug
        self.country_code = country_code
        ManageSquad.__init__(self, country_code, infantry_type, debug=self.debug)
        self.file_management = manage_files.FileManagement()

    def generate_platoon(self):
        platoon = []
        squad_template = self.load_squad_template()
        platoon = [self.generate_squad(squad_template) for i in range(int(squad_template['squad_per_platoon']))]
        if self.debug:
            print("DEBUG: class ManagePlatoon variable platoon: %s\n" % platoon)
        return(platoon)

    def update_squad_member(self, platoon, squad, list_val, member_key, member_value):
        list_val = int(list_val)
        platoon[squad][list_val][member_key] = member_value
        if self.debug:
            print("DEBUG: class ManagePlatoon updated member %s  from squad %s with key %s to value %s" % (platoon[squad][list_val]['name'], squad, member_key, member_value))
        return(platoon)

    def get_highest_rep(self, squad, exclude=[]):
        highest_rep = None
        base_rep = 0
        for member in squad:
            if member['rep'] > base_rep and member['name'] not in exclude:
                base_rep = member['rep']
                highest_rep = member
        return(highest_rep)

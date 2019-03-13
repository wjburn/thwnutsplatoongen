import generate_character_attributes
import manage_files
import manage_ui
import sys
import roll_dice
import os

class PlatoonMeta:
    def __init__(self):
        self.file_management    = manage_files.FileManagement()
        self.menu_management    = manage_ui.MenuManagement()
        self.country_code       = None
        self.platoon_type       = None

    def set_country_code(self):
        country_codes = self.file_management.load_yaml('yaml_map','country_codes')
        country_list = []
        for key in country_codes:
            country_list.append(key)
        country_key = self.menu_management.menu_ui(country_list)
        self.country_code = country_codes[country_key]

    def set_type(self):
        try:
            platoon_type_map = self.file_management.load_yaml('yaml_map','platoon_types')
            self.platoon_type = self.menu_management.menu_ui(platoon_type_map[self.country_code])
        except KeyError as e:
            print(str(e))
            return
    
    def set_attributes(self):
        if not self.country_code:
            self.set_country_code()
        if not self.platoon_type:
            self.set_type()
        try:
            self.platoon_map = self.file_management.load_yaml('yaml_map','squad_map_' + self.country_code)
            platoon_attributes = self.platoon_map[self.platoon_type]
            platoon_attributes['country_code'] = self.country_code
            platoon_attributes['platoon_type'] = self.platoon_type
        except KeyError as e:
            print(str(e))
            return
        return(platoon_attributes)

        
class GeneratePlatoon(PlatoonMeta):
    def __init__(self):
        PlatoonMeta.__init__(self)
        self.platoon_attributes = self.set_attributes()
        self.dice_bag = roll_dice.RollDice()
        self.character_attributes = generate_character_attributes.GenerateCharacter(self.platoon_attributes['country_code'])
        self.platoon_roles = []
        self.platoon = []


    def set_roles(self):
        #number of squads in a platoon
        for squad_number in range(int(self.platoon_attributes['squad_per_platoon'])):
            #squad size is the base_size + add_d6 roll
            squad_size = self.platoon_attributes['base_size'] + self.dice_bag.roll_d6()
            #if the generated size is greater than the squad max size, set the squad to max size
            if squad_size > self.platoon_attributes['max_squad_size']:
                squad_size = self.platoon_attributes['max_squad_size']
            squad_members = []
            #iterate through each role and associated value, the value indicates the max role each squad can contain
            for key, value in self.platoon_attributes['roles'].items():
                for roles in range(int(value)):
                    if squad_size > 0:
                        squad_members.append(key)
                        squad_size -= 1
            self.platoon_roles.append(squad_members)

    def set_member_attributes(self):
        squad_num = 1
        for squads in self.platoon_roles:
            squad_list = []
            squad = {}
            for role in squads:
                member = self.character_attributes.get_attributes(role)
                squad_list.append(member)
            squad_label = "squad_%s" % str(squad_num)
            squad[squad_label] = squad_list
            self.platoon.append(squad)
            squad_num += 1
                

    def get_platoon(self):
        lt_dict = {}
        platoon_lt = []
        platoon_lt.append(self.character_attributes.get_attributes('Lieutenant'))
        lt_dict['platoon_lieutenant'] = platoon_lt
        self.platoon.append(lt_dict)
        self.set_roles()
        self.set_member_attributes()
        return(self.platoon_attributes['country_code'], self.platoon_attributes['platoon_type'], self.platoon)



class UpdatePlatoon(PlatoonMeta):

  
    def __init__(self):
        PlatoonMeta.__init__(self)
        self.dice_bag = roll_dice.RollDice()
        self.platoon_attributes = self.set_attributes()
        self.yaml_top_key = "%s_%s" % (self.platoon_attributes['country_code'], self.platoon_attributes['platoon_type'])
        self.character_attributes = generate_character_attributes.GenerateCharacter(self.platoon_attributes['country_code'])
        self.platoon_yaml_map = self.file_management.load_yaml(os.path.join('platoons', self.platoon_attributes['country_code'], self.platoon_attributes['country_code'] + "_" + self.platoon_attributes['platoon_type'] + ".yaml"))
        self.platoon_roles = []
        self.platoon = []
        self.mia_pow = []
        self.hospital = []
        self.deceased = []


    def update_platoon(self):
        while True:
            squad_num = self.get_squad()
            self.update_squad(squad_num)
            continue_update_squad = input("Update another squad(y/n): ")
            if continue_update_squad == 'y' or continue_update_squad == 'yes':
                continue
            else:
                return(self.country_code, self.platoon_type, self.platoon_yaml_map, self.mia_pow, self.hospital, self.deceased)

    
  
    def update_squad(self, squad_num):
        while True:
            squad_member_id = self.get_squad_member(squad_num)
            if squad_member_id is not None:
                self.set_member_status(squad_num, squad_member_id)
                continue_update_members =  input("Update another member of this squad(y/n): ")
                if continue_update_members == 'y' or continue_update_members == 'yes':
                    continue
            else:
                print("No members left in this squad")
            
            return 

    def get_squad(self):
        squads = []
        for key in self.platoon_yaml_map[self.yaml_top_key]:
            squads.append(key)
        squad_num = self.menu_management.menu_ui(squads)
        return(squad_num)
  
    def get_squad_member(self, squad_num):
        squad_members = []
        for key in self.platoon_yaml_map[self.yaml_top_key][squad_num]:
            squad_members.append(key)
        if len(squad_members) > 0:
            squad_member_id = self.menu_management.menu_ui(squad_members, return_menu_val=1)
            return(squad_member_id)
        else:
            return


    def set_member_status(self, squad_num, squad_member_id):
        status_updates = ['active', 'pow/mia', 'hospital', 'deceased']
        status = self.menu_management.menu_ui(status_updates)
        self.platoon_yaml_map[self.yaml_top_key][squad_num][squad_member_id]['status'] = status
        if status == 'pow/mia':
            self.mia_pow.append(self.platoon_yaml_map[self.yaml_top_key][squad_num][squad_member_id])
            del self.platoon_yaml_map[self.yaml_top_key][squad_num][squad_member_id]
        elif status == 'hospital':
            self.hospital.append(self.platoon_yaml_map[self.yaml_top_key][squad_num][squad_member_id])
            del self.platoon_yaml_map[self.yaml_top_key][squad_num][squad_member_id]
        elif status == 'deceased':
            self.deceased.append(self.platoon_yaml_map[self.yaml_top_key][squad_num][squad_member_id])
            del self.platoon_yaml_map[self.yaml_top_key][squad_num][squad_member_id]



class GenerateReplacements(PlatoonMeta):

  
    def __init__(self):
        PlatoonMeta.__init__(self)
        self.dice_bag = roll_dice.RollDice()
        self.platoon_attributes = self.set_attributes()
        self.yaml_top_key = "%s_%s" % (self.platoon_attributes['country_code'], self.platoon_attributes['platoon_type'])
        self.character_attributes = generate_character_attributes.GenerateCharacter(self.platoon_attributes['country_code'])
        self.platoon_yaml_map = self.file_management.load_yaml(os.path.join('platoons', self.platoon_attributes['country_code'], self.platoon_attributes['country_code'] + "_" + self.platoon_attributes['platoon_type'] + ".yaml"))
#        self.platoon_roles = []
#        self.platoon = []
#        self.mia_pow = []
#        self.hospital = []
#        self.deceased = []

    def replace_leaders(self):
        n = 1
        nco = None
        squad = "squad_%s" % str(n)
        squads_in_platoon = len(self.platoon_yaml_map[self.yaml_top_key])
        while n <= squads_in_platoon:
            for member in self.platoon_yaml_map[self.yaml_top_key][squad]:
                if 'NCO' in member.values():
                    nco = 1
            if not nco:
                print('no nco in squad %s' % squad)
                next_squad = n + 1
                promote_from_squad = "squad_%s" % str(next_squad)
                while next_squad <= squads_in_platoon:
                    for member in self.platoon_yaml_map[self.yaml_top_key][promote_from_squad]:
                        if 'NCO' in member.values():
                            print("promote member %s" % member)
                            return
                        else:
                            next_squad += 1 
                            promote_from_squad = "squad_%s" % str(next_squad)
            n += 1
            nco = None
            squad = "squad_%s" % str(n)



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


class UpdatePlatoon(PlatoonMeta):

  
    def __init__(self):
        PlatoonMeta.__init__(self)
        self.dice_bag = roll_dice.RollDice()
        self.platoon_attributes = self.set_attributes()
        self.yaml_top_key = "%s_%s" % (self.platoon_attributes['country_code'], self.platoon_attributes['platoon_type'])
        self.character_attributes = generate_character_attributes.GenerateCharacter(self.platoon_attributes['country_code'])
        self.platoon_yaml_map = self.file_management.load_yaml('platoons',  self.platoon_attributes['country_code'] + "_" + self.platoon_attributes['platoon_type'],self.platoon_attributes['country_code'])
#        self.platoon_roles = []
#        self.platoon = []
#        self.mia_pow = []
#        self.hospital = []
#        self.deceased = []


    def update_platoon(self):
        while True:
            (squad_num) = self.get_squad()
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
                self.set_squad_member_attributes(squad_num, squad_member_id)
                continue_update_members =  input("Update another member of this squad(y/n): ")
                if continue_update_members == 'y' or continue_update_members == 'yes':
                    continue
            else:
                print("No members left in this squad")
            
            return 

    def get_squad(self):
        squad_nums = []
        for element in self.platoon_yaml_map:
            for key in element:
                squad_nums.append(key)
        squad_num = self.menu_management.menu_ui(squad_nums, return_menu_val=1)
        return(squad_num)
  
    def get_squad_member(self, squad_num):
        attribute_list = ['name', 'role', 'rep', 'attribute', 'status']
        squad_list = []
        for key in self.platoon_yaml_map[squad_num]:
            if len(self.platoon_yaml_map[squad_num][key]) > 0:
                 #yaml dump does not honor python dictionary sorting, re-sort the keys into an order for display
                 for element in self.platoon_yaml_map[squad_num][key]:
                     character_attributes = {}
                     for attribute in attribute_list:
                         character_attributes[attribute] = element[attribute]
                     squad_list.append(character_attributes)
                 squad_member_id = self.menu_management.menu_ui(squad_list, return_menu_val=1)
                 return(squad_member_id)
            else:
                return


    def set_squad_member_attributes(self, squad_num, squad_member_id):
        status_menu_list = []
        status_menu_dict = {
          #  'change squad': self.change_squad(),#squad_num, squad_member_id),
            'change role': self.change_role(squad_num, squad_member_id),
#            'add attribute': self.change_role(),#(squad_num, squad_member_id),
#            'update rep': self.change_role(),#(squad_num, squad_member_id),
#            'update status': self.change_role(),#(squad_num, squad_member_id),
        }
        for key in status_menu_dict.keys():
            status_menu_list.append(key)
        status_option = self.menu_management.menu_ui(status_menu_list)
        print(status_option)
        status_menu_dict[status_option](squad_num, squad_member_id)


    def change_squad(self):
        pass

    def change_role(self, squad_num, squad_member_id):
        print(self.platoon_yaml_map[squad_num])
        

    def add_attribute(self):
        pass

    def update_rep(self):
        pass

    def update_status(self):
        pass
#        status_updates = ['active', 'pow/mia', 'hospital', 'deceased']
#        status = self.menu_management.menu_ui(status_updates)
#        self.platoon_yaml_map[self.yaml_top_key][squad_num][squad_member_id]['status'] = status
#        if status == 'pow/mia':
#            self.mia_pow.append(self.platoon_yaml_map[self.yaml_top_key][squad_num][squad_member_id])
#            del self.platoon_yaml_map[self.yaml_top_key][squad_num][squad_member_id]
#        elif status == 'hospital':
#            self.hospital.append(self.platoon_yaml_map[self.yaml_top_key][squad_num][squad_member_id])
#            del self.platoon_yaml_map[self.yaml_top_key][squad_num][squad_member_id]
#        elif status == 'deceased':
#            self.deceased.append(self.platoon_yaml_map[self.yaml_top_key][squad_num][squad_member_id])
#            del self.platoon_yaml_map[self.yaml_top_key][squad_num][squad_member_id]



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



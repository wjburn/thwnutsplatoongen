from manage_characters import GenerateCharacter
import manage_files
import manage_ui
import sys
import roll_dice

class PlatoonMeta:
    def __init__(self):
        self.file_management    = manage_files.FileManagement()
        self.menu_management    = manage_ui.MenuManagement()
        self.country_code       = None
        self.platoon_type       = None

    def set_country_code(self):
        country_codes = self.file_management.load_yaml('country_codes')
        country_list = []
        for key in country_codes:
            country_list.append(key)
        country_key = self.menu_management.menu_ui(country_list)
        self.country_code = country_codes[country_key]

    def set_type(self):
        try:
            platoon_type_map = self.file_management.load_yaml('platoon_types')
            self.platoon_type = self.menu_management.menu_ui(platoon_type_map[self.country_code])
        except KeyError as e:
            print(str(e))
            return
    
    def get_attributes(self):
        if not self.country_code:
            self.set_country_code()
        if not self.platoon_type:
            self.set_type()
        try:
            self.platoon_map = self.file_management.load_yaml('squad_map_' + self.country_code)
            platoon_attributes = self.platoon_map[self.platoon_type]
        except KeyError as e:
            print(str(e))
            return
        return(platoon_attributes)

        
class GeneratePlatoon(PlatoonMeta):
    def __init__(self):
        self.dice_bag = roll_dice.RollDice()
        self.platoon_meta = PlatoonMeta()
        self.platoon_attributes = self.platoon_meta.get_attributes()


    def get_platoon(self):
        squads = []
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
            squads.append(squad_members)
        print(squads[1])


# class UpdatePlatoon(GenerateCharacter):

    
#     def __init__(self, country, platoon_type, yaml_map):
#         DefineMaps.__init__(self, country)
#         GenerateCharacter.__init__(self, country)
#         GenerateMenu.__init__(self)
#         self.menu = GenerateMenu()
#         self.yaml_map = yaml_map
#         self.platoon_type = platoon_type
#         self.top_key = "%s_%s" % (self.country, self.platoon_type)
#         roll_dice = RollDice()
#         self.roll_d6 = roll_dice.roll_d6
    
#     def update_squad(self):
#         while True:
#             squad_num = self.get_squad()
#             while True:
#                 squad_member_id = self.get_squad_member(squad_num)
#                 status = self.get_member_status()
#                 self.update_member_status(squad_num, squad_member_id, status)
#                 cont_member_loop =  input("Update another member of this squad(y/n): ")
#                 if cont_member_loop is not 'y':
#                    break 
#             cont_squad_loop = input("Update another squad(y/n): ")
#             if cont_squad_loop is not 'y':
#                 break
#             return

#     def get_squad(self):
#         squads = []
#         for key in self.yaml_map[self.top_key]:
#             squads.append(key)
#         squad_num = self.menu.menu_ui(squads)
#         return(squad_num)
    
#     def get_squad_member(self, squad_num):
#         squad_members = []
#         for key in self.yaml_map[self.top_key][squad_num]:
#             squad_members.append(key)
#         squad_member_id = self.menu.menu_ui(squad_members, return_menu_val=1)
#         return(squad_member_id)


#     def get_member_status(self):
#         status_updates = ['active', 'pow', 'hospital', 'deceased']
#         status = self.menu.menu_ui(status_updates)
#         return(status)

#     def update_member_status(self, squad_num, squad_member_id, member_status):
#         self.yaml_map[self.top_key][squad_num][squad_member_id]['status'] = member_status
#         print(squad_member_id)
#         print(self.yaml_map[self.top_key][squad_num][squad_member_id])


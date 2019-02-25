

class UpdatePlatoon(GenerateCharacter):

    
    def __init__(self, country, platoon_type, yaml_map):
        DefineMaps.__init__(self, country)
        GenerateCharacter.__init__(self, country)
        GenerateMenu.__init__(self)
        self.menu = GenerateMenu()
        self.yaml_map = yaml_map
        self.platoon_type = platoon_type
        self.top_key = "%s_%s" % (self.country, self.platoon_type)
        roll_dice = RollDice()
        self.roll_d6 = roll_dice.roll_d6
    
    def update_squad(self):
        while True:
            squad_num = self.get_squad()
            while True:
                squad_member_id = self.get_squad_member(squad_num)
                status = self.get_member_status()
                self.update_member_status(squad_num, squad_member_id, status)
                cont_member_loop =  input("Update another member of this squad(y/n): ")
                if cont_member_loop is not 'y':
                   break 
            cont_squad_loop = input("Update another squad(y/n): ")
            if cont_squad_loop is not 'y':
                break
            return

    def get_squad(self):
        squads = []
        for key in self.yaml_map[self.top_key]:
            squads.append(key)
        squad_num = self.menu.menu_ui(squads)
        return(squad_num)
    
    def get_squad_member(self, squad_num):
        squad_members = []
        for key in self.yaml_map[self.top_key][squad_num]:
            squad_members.append(key)
        squad_member_id = self.menu.menu_ui(squad_members, return_menu_val=1)
        return(squad_member_id)


    def get_member_status(self):
        status_updates = ['active', 'pow', 'hospital', 'deceased']
        status = self.menu.menu_ui(status_updates)
        return(status)

    def update_member_status(self, squad_num, squad_member_id, member_status):
        self.yaml_map[self.top_key][squad_num][squad_member_id]['status'] = member_status
        print(squad_member_id)
        print(self.yaml_map[self.top_key][squad_num][squad_member_id])

class GeneratePlatoon(GenerateCharacter):

    def __init__(self, country, yaml_file):
        DefineMaps.__init__(self, country)
        GenerateCharacter.__init__(self, country)
        self.platoon_dict = self.load_yaml_files(self.platoon_yaml)
        self.platoon_type = platoon_type
        roll_dice = RollDice()
        self.roll_d6 = roll_dice.roll_d6

#generate a platoon from squads
    def get_platoon(self):
        squad_list = []
        platoon_size = int(self.platoon_dict[self.platoon_type]['platoon'])
        for x in range(platoon_size):
            squad_list.append(self.generate_squad())
        return(squad_list)

#generate squads from characters
    def generate_squad(self):
        squad_members = []
        #numer of roles per squad, NCO 1 where as rifle may be 7
        roles = {
            "NCO": int(self.platoon_dict[self.platoon_type]['NCO']),
            "JrNCO": int(self.platoon_dict[self.platoon_type]['JrNCO']),
            "LMG": int(self.platoon_dict[self.platoon_type]["LMG"]),
            "LMG_Assist": int(self.platoon_dict[self.platoon_type]["LMG_Assist"]),
            "SA_Genernade_Rifle": int(self.platoon_dict[self.platoon_type]["SA_Gerenade_Rifle"]),
            "Rifle": int(self.platoon_dict[self.platoon_type]["Rifle"]),
        }
        #squad size is determined by base size and then add xd6 (e.g. 1d6)
        squad_size = self.platoon_dict[self.platoon_type]['base'] + self.roll_d6(self.platoon_dict[self.platoon_type]['d6'])
        #if the above value is greater than squad max size, set size to max
        if squad_size > self.platoon_dict[self.platoon_type]['max']:
            squad_size = self.platoon_dict[self.platoon_type]['max']
        #assign a role to each character and remove 1 from the role value, ensuring that the correct number of roles are assigned per squad
        for x in range(squad_size):
            for key in roles:
                if roles[key] > 0:
                    role = key
                    squad_members.append(self.get_character(role))
                    roles[key] -= 1
        return(squad_members)

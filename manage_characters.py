
class GenerateCharacter(DefineMaps):
    def __init__(self, country):
        DefineMaps.__init__(self, country)
        self.attribute_dict  = self.load_yaml_files(self.attribute_yaml)
        self.rep_list        = self.rep_dict[country]
        self.first_name_dict = self.load_yaml_files(self.first_name_yaml)
        self.last_name_dict  = self.load_yaml_files(self.last_name_yaml)
        roll_dice = RollDice()
        self.roll_d6 = roll_dice.roll_d6()

    #if attribute_tree is 5 or less, use the v4 attributes table
    #else use compendium attributes table and returns of "reroll" are re-generated until another result is returned
    def get_attribute(self):
        attribute_tree = self.roll_d6()
        while True:
            if attribute_tree < 5:
                attribute = self.attribute_dict["Nuts_v4_Attributes_Table"][self.roll_d6()][self.roll_d6()]
            else:
                attribute = self.attribute_dict["Nuts_Compendium_Attributes_Table"][self.roll_d6()][self.roll_d6()]
            if attribute != "reroll":
                return(attribute)
    
    def get_first_name(self):
        first_name = self.first_name_dict["First_Names"][self.roll_d6()][self.roll_d6()][self.roll_d6()]
        return(first_name)

    def get_last_name(self):
        last_name = self.last_name_dict["Last_Names"][self.roll_d6()][self.roll_d6()][self.roll_d6()]
        return(last_name)

    def get_rep(self):
        rep_val = self.roll_d6()
        rep_val -= 1
        return(self.rep_list[rep_val])

    def get_character(self, role, **kwargs):
        rep = kwargs.get('rep', self.get_rep())
        character = {
            'name': "%s, %s" % (self.get_last_name(), self.get_first_name()),
            'role': role,
            'rep': rep,
            'attribute':  self.get_attribute(),
            'status': 'active'
        }
        return(character)
        

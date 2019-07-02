import roll_dice
import manage_files
import os

class GenerateCharacter:

    def __init__(self, country_code, infantry_type):
        self.country_code = country_code
        self.infantry_type = infantry_type
        self.dice_bag        = roll_dice.RollDice()
        self.fm = manage_files.FileManagement(self.country_code, self.infantry_type)
        #reputation generation from nuts v4 via country_code
        rep_dict = {
            'us': [3,3,4,4,4,5],
            'br': [3,4,4,4,4,5],
            'ge': [3,4,4,4,5,5],
            'ru': [3,3,4,4,4,5],
        }
        self.rep_list = rep_dict[country_code]
        self.attribute_dict  = self.fm.load_yaml('attribute')
        self.first_name_dict = self.fm.load_yaml('first_name')
        self.last_name_dict  = self.fm.load_yaml('last_name')



    #if attribute_tree is 5 or less, use the v4 attributes table
    #else use compendium attributes table and returns of "reroll" are re-generated until another result is returned
    def get_attribute(self):
        attribute_tree = self.dice_bag.roll_d6()
        while True:
            if attribute_tree < 5:
                attribute = self.attribute_dict["Nuts_v4_Attributes_Table"][self.dice_bag.roll_d6()][self.dice_bag.roll_d6()]
            else:
                attribute = self.attribute_dict["Nuts_Compendium_Attributes_Table"][self.dice_bag.roll_d6()][self.dice_bag.roll_d6()]
            if attribute != "reroll":
                return(attribute)
    
    #names based on country code
    def get_first_name(self):
        first_name = self.first_name_dict["First_Names"][self.dice_bag.roll_d6()][self.dice_bag.roll_d6()][self.dice_bag.roll_d6()]
        return(first_name)

    def get_last_name(self):
        last_name = self.last_name_dict["Last_Names"][self.dice_bag.roll_d6()][self.dice_bag.roll_d6()][self.dice_bag.roll_d6()]
        return(last_name)

    def get_rep(self):
        rep_val = self.dice_bag.roll_d6()
        rep_val -= 1
        return(self.rep_list[rep_val])

     #returns(string, string, string, dict)
    def get_character(self):
        return(self.get_first_name(), self.get_last_name(), self.get_rep(), self.get_attribute())

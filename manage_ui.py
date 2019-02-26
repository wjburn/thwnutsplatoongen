
class MenuManagement:
    def __init__(self):
        pass

    def menu_ui(self, menu_items, return_menu_val=None):
        while True:
            try:
                for item in range(len(menu_items)):
                    print(str(item+1) + ":", menu_items[item])
                inp = int(input("Enter a numeric value: "))
                if inp-1 in range(len(menu_items)):
                    if not return_menu_val:
                        return(menu_items[inp-1])
                    else:
                        return(inp-1)
                else:
                    print("Invalid Menu Option")
            except ValueError:
                print("Invalid Input, use numeric values")


import os
import yaml
import sys

class FileManagement:

    def __init__(self, country_code, infantry_type, debug=0):
        self.debug = debug
        self.country_code = country_code
        self.infantry_type = infantry_type
        platoon_file_name = self.country_code + '_' + self.infantry_type + '.yaml'
        platoon_path = os.path.join('platoons', self.country_code, platoon_file_name)
        attribute_path = os.path.join('yaml_maps', 'attribute_map.yaml')
        first_name_path = os.path.join('yaml_maps', 'names_first_' + self.country_code + '.yaml',)
        last_name_path = os.path.join('yaml_maps', 'names_last_' + self.country_code + '.yaml',)
        squad_attributes_map = os.path.join('yaml_maps', 'squad_map_' + self.country_code + '.yaml')
        self.file_name_map = {
            'attribute': attribute_path,
            'first_name': first_name_path,
            'last_name': last_name_path,
            'platoon':    platoon_path,
            'squad_map': squad_attributes_map,
        }


    def load_yaml(self, map_name):
        try:
            with open(self.file_name_map[map_name], "r") as f:
                 yaml_map = yaml.load(f)
            f.close()
            return(yaml_map)
        except (PermissionError, FileNotFoundError) as e:
            print("ERROR: failed to open file: %s" % str(e))
            os._exit(1)

    def write_platoon_file(self, platoon):
        if self.check_overwrite(self.file_name_map['platoon']):
            print("MESSAGE: not overwriting file: %s" % self.file_name_map['platoon'])
            os._exit(1)
#        yaml_content = yaml.dump(platoon, default_flow_style=False)
        self.write_yaml(self.file_name_map['platoon'], platoon)
#        html_file_path = self.file_name_map['platoon'].replace(".yaml", ".html")
#        self.write_html(html_file_path, yaml_content)
        
    def check_overwrite(self, file_path):
        if os.path.exists(os.path.abspath(file_path)):
            overwrite = input("File exists %s\n Do you want to overwrite?(y/n): " % file_path)
            if overwrite == 'y' or overwrite == 'yes':
                return
            else:
                return(1)
        else:
            return

    def write_yaml(self, file_name, yaml_content):
        if self.debug:
            print("DEBUG: class FileManagement variable yaml_file  %s" % file_name)
        try:
            with open(file_name, 'w') as f:
                yaml.dump(yaml_content, f, default_flow_style=False)
#                f.write(yaml_content)
            f.close
        except (PermissionError, FileNotFoundError) as e:
            print("ERROR: Failed to write file: %s" % str(e))
            return(1)
        return
        

    def write_html(self, file_name, yaml_content):
        if self.debug:
            print("DEBUG: class FileManagement variable html_file  %s" % file_name)
        html_content = self.generate_html(yaml_content)
        try:
            with open(file_name, 'w') as f:
                for line in html_content:
                    f.write("%s\n" % line)
            f.close
        except (PermissionError, FileNotFoundError) as e:
            print("ERROR: Failed to write file: %s" % str(e))
            return(1)
        return
            
    def generate_html(self, yaml_content):
        platoon_keys = ["name", "role", "rep", "attribute", "status"]
        content_html = []
        content_html.append("<html>\n<body>\n")
        content_html.append("<style>\ntable {\nfont-family: arial, sans-serif;\nborder-collapse: collapse;\n  width: 100%;\n}\n")
        content_html.append("td, th {\n  border: 3px solid #dddddd;\n text-align: left;\n  padding: 2px;\nvertical-align: bottom;\n}\n")
        content_html.append("tr:nth-child(even) {\n  background-color: #dddddd;\n}\n")
        content_html.append("</style>\n</head>\n<body>\n")
        content_html.append("<table>\n")
        for list_item in yaml_content:
            for yaml_key in list_item:
                content_html.append("<tr>\n")
                content_html.append("<th width=\"1px\">%s</th>\n" % yaml_key)
                content_html.append("</tr>\n")
                content_html.append("<tr>\n")
                for key in platoon_keys:
                    content_html.append("<th width=\"1px\">%s</th>\n" % key)

                content_html.append("</tr>\n")
                for member in list_item[yaml_key]:
                    content_html.append("<tr>\n")
                    for key in platoon_keys:
                        content_html.append("<td>%s</td>\n" % member[key])
                    content_html.append("</tr>\n")
                        
        return(content_html)

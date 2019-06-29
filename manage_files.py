import os
import yaml
import sys

class FileManagement:

    def __init__(self, debug=0):
        self.debug = debug

    def load_yaml(self, dir_path, file_name):
        file_path = os.path.join(dir_path, file_name)
        try:
            with open(file_path, "r") as f:
                 yaml_map = yaml.load(f)
            f.close()
            return(yaml_map)
        except (PermissionError, FileNotFoundError) as e:
            print("ERROR: failed to open file: %s" % str(e))
            return(1)
        
    def write_files(self, dir_path, file_name):
        file_path = os.path.join(dir_path, file_name)
        if self.check_overwrite(file_path):
            print("MESSAGE: not overwriting file: %s" % file_path)
            return(1)
        if self.check_directory(dir_path):
            print("ERROR: diretory does not exist and can not create directory: %s" % dir_path)
            return(1)
        
    def check_overwrite(self, file_path):
        if os.path.exists(os.path.abspath(file_path)):
            overwrite = input("File exists %s\n Do you want to overwrite?(y/n): " % file_path)
            if overwrite == 'y' or overwrite == 'yes':
                return
            else:
                return(1)
        else:
            return

    def check_directory(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except (PermissionError, FileNotFoundError) as e:
            print("ERROR: Failed to create directory: %s" % str(e))
            return(1)
        return

    def write_yaml(self, file_name, yaml_content):
        if self.debug:
            print("DEBUG: class FileManagement variable yaml_file  %s" % yaml_file)
        try:
            with open(file_name, 'w') as f:
                yaml.dump(yaml_content, f, default_flow_style=False)
            f.close
        except (PermissionError, FileNotFoundError) as e:
            print("ERROR: Failed to write file: %s" % str(e))
            return(1)
        return
        

    def write_html(self, file_name, html_content):
        if self.debug:
            print("DEBUG: class FileManagement variable html_file  %s" % html_file)
        try:
            with open(file_name, 'w') as f:
                for line in html_content:
                    f.write("%s\n" % line)
            f.close
        except (PermissionError, FileNotFoundError) as e:
            print("ERROR: Failed to write file: %s" % str(e))
            return(1)
        return
            
    def generate_html(self, platoon):
        platoon_keys = ["name", "role", "rep", "attribute", "status"]
        content_html = []
        content_html.append("<html>\n<body>\n")
        content_html.append("<style>\ntable {\nfont-family: arial, sans-serif;\nborder-collapse: collapse;\n  width: 100%;\n}\n")
        content_html.append("td, th {\n  border: 3px solid #dddddd;\n text-align: left;\n  padding: 2px;\nvertical-align: bottom;\n}\n")
        content_html.append("tr:nth-child(even) {\n  background-color: #dddddd;\n}\n")
        content_html.append("</style>\n</head>\n<body>\n")
        content_html.append("<table>\n")
        for list_item in platoon:
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

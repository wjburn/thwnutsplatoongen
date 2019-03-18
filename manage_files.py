import os
import yaml
import sys

class FileManagement:

    def __init__(self):
        self.directory_map = {
            'platoons': 'platoons',
            'yaml_map': 'yaml_maps',
        }

    def file_error(self, file, error):
        print("Failed file: %s " % file + str(error))
        sys.exit()

    def load_yaml(self, map_key, file_name, country_code=None):
        if country_code:
            yaml_file = os.path.join(self.directory_map[map_key], country_code, file_name + ".yaml")
        else:
            yaml_file = os.path.join(self.directory_map[map_key], file_name + ".yaml")
        try:
            with open(yaml_file, "r") as f:
                 yaml_map = yaml.load(f)
            f.close()
            return(yaml_map)

        except (PermissionError, FileNotFoundError) as e:
            self.file_error(yaml_file, str(e))

    def check_overwrite(self, file_path):
        if os.path.exists(os.path.abspath(file_path)):
            overwrite = input("File exists %s\n Do you want to overwrite?(y/n): " % file_path)
            if overwrite == 'y' or overwrite == 'yes':
                return(1)
            else:
                return
        else:
            return(1)

    def check_directory(self, directory):
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except (PermissionError, FileNotFoundError) as e:
            self.file_error(directory, str(e))

    def write_html(self, map_key, country_code, file_name, html_content):
        write_file = "w"
        html_file = os.path.join(self.directory_map[map_key], country_code, file_name + ".html")
        try:
            with open(html_file, write_file) as f:
                for line in html_content:
                    f.write("%s\n" % line)
            f.close()
            print("wrote to file: %s" % html_file)
            input("Press the any key")
            return
        except (PermissionError, FileNotFoundError) as e:
            self.file_error(html_file, str(e))

            
    def write_yaml(self, map_key, country_code, file_name, yaml_content, append=None):
        write_file = 'w'
        if append:
            write_file = 'a+'
        yaml_file = os.path.join(self.directory_map[map_key], country_code, file_name + ".yaml")
        os.path.join(self.directory_map[map_key], country_code)
        self.check_directory(self.directory_map[map_key])
        if not append and not self.check_overwrite(yaml_file):
            print("Will not overwrite file: %s" % yaml_file)
            sys.exit()

        with open(yaml_file, write_file) as f:
            yaml.dump(yaml_content, f, default_flow_style=False)
        f.close
        print("TEST %s" % yaml_file)
        

            
class GenerateContent(FileManagement):

    def __init__(self):
        FileManagement.__init__(self)

    #TODO fix the yaml load here to not need a yaml file path
    def generate_html(self, country_code, file_name):
        platoon_keys = ["name", "role", "rep", "attribute", "status"]
        content_html = []
        content_yaml = self.load_yaml('platoons', file_name, country_code)
        content_html.append("<html>\n<body>\n")
        content_html.append("<style>\ntable {\nfont-family: arial, sans-serif;\nborder-collapse: collapse;\n  width: 100%;\n}\n")
        content_html.append("td, th {\n  border: 3px solid #dddddd;\n text-align: left;\n  padding: 2px;\nvertical-align: bottom;\n}\n")
        content_html.append("tr:nth-child(even) {\n  background-color: #dddddd;\n}\n")
        content_html.append("</style>\n</head>\n<body>\n")
        content_html.append("<table>\n")
        for list_item in content_yaml:
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


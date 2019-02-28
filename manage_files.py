import os
import yaml
import sys

class FileManagement:
#TODO
#move this to generate platoon
    def __init__(self):
        self.map_dir     = 'yaml_maps'
        self.platoon_dir = 'platoons'


    def file_error(self, file, error):
        print("Failed file: %s " % file + str(error))
        sys.exit()

    def load_yaml(self, yaml_file):
        file_path = os.path.join(self.map_dir, yaml_file + ".yaml")
        try:
            with open(file_path, "r") as f:
                 yaml_map = yaml.load(f)
            f.close()
            return(yaml_map)

        except (PermissionError, FileNotFoundError) as e:
            self.file_error(yaml_file, str(e))

#TODO
    def check_overwrite(self, file):
        if os.path.exists(os.path.abspath(file_path)):
            overwrite = input("File exists %s\n Do you want to overwrite?(y/n): " % file_path)
            if overwrite == 'y' or overwrite == 'yes':
                return(1)
            else:
                return
#TODO
    def check_directory(self, file_path):
        (directory, write_file) = os.path.split(file_path)
        try:
            if not os.path.exists(file_path):
                os.makedirs(directory)
        except (PermissionError, FileNotFoundError):
            self.file_error(yaml_file, str(e))
#TODO
    def write_file(self, file_path, file_content):
        file_path = os.path.abspath(file_path)
        try:
            with open(file_path, "w") as f:
                for line in file_content:
                    f.write("%s\n" % line)
            f.close()
            print("wrote to file: %s" % file_path)
            input("Press the any key")
            return
        except (PermissionError, FileNotFoundError):
            self.file_error(yaml_file, str(e))
            
#TODO this needs to be refactored
class GenerateContent(FileManagement):

    def __init__(self, header, content, section_title='squad', entry_title='name'):
        self.header = header
        self.content = content
        self.section_title = section_title
        self.entry_title = entry_title

    def generate_yaml(self):
        x = 0
        self.content_yaml = []
        self.content_yaml.append("%s:" % self.header)
        for section in self.content:
            self.content_yaml.append("    %s_%s:" % (self.section_title, x + 1))
            for entry in section:
                for key in entry:
                    if key == self.entry_title:
                        self.content_yaml.append("        - %s: %s" % (key, entry[key]))
                    else:
                        self.content_yaml.append("          %s: %s" % (key, entry[key]))
            x += 1
        return(self.content_yaml)       

    def generate_html(self):
        content_html = []
        for key in self.content_yaml:
            content_html.append("<html>\n<body>\n")
            content_html.append("<style>\ntable {\nfont-family: arial, sans-serif;\nborder-collapse: collapse;\n  width: 100%;\n}\n")
            content_html.append("td, th {\n  border: 3px solid #dddddd;\n text-align: left;\n  padding: 2px;\nvertical-align: bottom;\n}\n")
            content_html.append("tr:nth-child(even) {\n  background-color: #dddddd;\n}\n")
            content_html.append("</style>\n</head>\n<body>\n")
            content_html.append("<B>%s</B><p>\n" % key)
            content_html.append("<table>\n")
            for sub_key1 in self.content_yaml[key]:
                content_html.append("<tr>\n")
                content_html.append("<th width=\"1px\">%s</th>\n" % sub_key1)
                content_html.append("<th>Name</th>\n")
                content_html.append("<th>Role</th>\n")
                content_html.append("<th>Rep</th>\n")
                content_html.append("<th>Attribute</th>\n")
                content_html.append("<th>Status</th>\n")
                content_html.append("</tr>\n")
                x = 1
                for value in self.content_yaml[key][sub_key1]:
                    content_html.append("<tr>\n")
                    content_html.append("<td>%s</td>" % x)
                    content_html.append("<td>%s</td>\n" % value['name'])
                    content_html.append("<td>%s</td>\n" % value['role'])
                    content_html.append("<td>%s</td>\n" % value['rep'])
                    content_html.append("<td>%s</td>\n" % value['attribute'])
                    content_html.append("<td>%s</td>\n" % value['status'])
                    content_html.append("</tr>\n")
                    x += 1
        content_html.append("</table>\n")
        content_html.append("</body>\n")
        content_html.append("</html>\n")
        return(content_html)

    def write_platoon(self):

        
    

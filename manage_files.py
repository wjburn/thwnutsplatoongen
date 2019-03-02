import os
import yaml
import sys

class FileManagement:

    def __init__(self):
        pass


    def file_error(self, file, error):
        print("Failed file: %s " % file + str(error))
        sys.exit()

    def load_yaml(self, file_path):
        try:
            with open(file_path, "r") as f:
                 yaml_map = yaml.load(f)
            f.close()
            return(yaml_map)

        except (PermissionError, FileNotFoundError) as e:
            self.file_error(file_path, str(e))

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
        except (PermissionError, FileNotFoundError) as e:
            self.file_error(file_path, str(e))
            
class GenerateContent(FileManagement):

    def __init__(self, country_code, platoon_type, content, section_title='squad', entry_title='name'):
        self.platoon_dir = 'platoons'
        self.country_code = country_code
        self.platoon_type = platoon_type
        self.content = content
        self.section_title = section_title
        self.entry_title = entry_title
        self.directory_path = os.path.join(self.platoon_dir, self.country_code)
        self.yaml_file = os.path.join(self.directory_path, self.country_code + "_" + self.platoon_type + ".yaml")
        self.html_file = os.path.join(self.directory_path, self.country_code + "_" + self.platoon_type + ".html")

    def generate_yaml(self):
        x = 0
        content_yaml = []
        content_yaml.append("%s_%s:" % (self.country_code, self.platoon_type))
        for section in self.content:
            content_yaml.append("    %s_%s:" % (self.section_title, x + 1))
            for entry in section:
                for key in entry:
                    if key == self.entry_title:
                        content_yaml.append("        - %s: %s" % (key, entry[key]))
                    else:
                        content_yaml.append("          %s: %s" % (key, entry[key]))
            x += 1
        return(content_yaml)       

#add platoon sergeant field
#add morale and investment level field
#make this a dynamic table generation
    def generate_html(self, yaml_file):
        content_html = []
        content_yaml = self.load_yaml(yaml_file)
        for key in content_yaml:
            content_html.append("<html>\n<body>\n")
            content_html.append("<style>\ntable {\nfont-family: arial, sans-serif;\nborder-collapse: collapse;\n  width: 100%;\n}\n")
            content_html.append("td, th {\n  border: 3px solid #dddddd;\n text-align: left;\n  padding: 2px;\nvertical-align: bottom;\n}\n")
            content_html.append("tr:nth-child(even) {\n  background-color: #dddddd;\n}\n")
            content_html.append("</style>\n</head>\n<body>\n")
            content_html.append("<B>%s</B><p>\n" % key)
            content_html.append("<table>\n")
            for sub_key1 in content_yaml[key]:
                content_html.append("<tr>\n")
                content_html.append("<th width=\"1px\">%s</th>\n" % sub_key1)
                content_html.append("<th>Name</th>\n")
                content_html.append("<th>Role</th>\n")
                content_html.append("<th>Rep</th>\n")
                content_html.append("<th>Attribute</th>\n")
                content_html.append("<th>Status</th>\n")
                content_html.append("</tr>\n")
                x = 1
                for value in content_yaml[key][sub_key1]:
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

    def write_platoon_files(self):
        self.check_directory(self.directory_path)
        if self.check_overwrite(self.yaml_file):
            yaml_content = self.generate_yaml()
            self.write_file(self.yaml_file, yaml_content)
            html_content = self.generate_html(self.yaml_file)
            self.write_file(self.html_file, html_content)
        else:
            print("Will not overwrite file: %s" % self.yaml_file)
            sys.exit()
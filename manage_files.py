import os
import yaml
import sys

class FileManagement:
    def __init__(self):
        self.map_dir     = 'yaml_maps'
        self.platoon_dir = 'platoons'
#        self.header = header
#        self.yaml_file = os.path.join(directory, self.header + ".yaml")
#        self.html_file = os.path.join(directory, self.header + ".html")

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


    def check_yaml_overwrite(self):
        try:
            if not os.path.exists(self.directory):
                os.makedirs(self.directory)
            # check to see if file is an overwrite
            file_path = os.path.abspath(self.yaml_file)
            if os.path.exists(file_path):
                inp = input("File exists %s\n Do you want to overwrite? (y/n): " % file_path)
                if inp == 'y' or inp == 'yes':
                    return(1)
                else:
                    return
            else:
                return(1)
        except (PermissionError, FileNotFoundError):
            print("Permission denied writing file to %s\n" % file_path)
            input("Press any key to exit")
            sys.exit()
      
    def write_files(self, content):
        self.generate_yaml(content)
        self.generate_html()
          

    def save_file(self, save_file, file_content):
        try:
            with open(save_file, "w") as f:
                for line in file_content:
                    f.write("%s\n" % line)
            f.close()
            file_path = os.path.abspath(save_file)
            print("wrote to file: %s" % file_path)
            input("Press any key")
        except (PermissionError, FileNotFoundError):
            print("Permission denied writing file to %s\n" % save_file)
            input("Press any key to exit")
            sys.exit()
        

            
#TODO this needs to be refactored
class GenerateContent(FileManagement):

     def generate_yaml(self, content_dict, header, section_title='squad', entry_title='name'):
         x = 0
         content_yaml = []
         content_yaml.append("%s:" % header)
         for section in content_dict:
             content_yaml.append("    %s_%s:" % (section_title, x + 1))
             for entry in section:
                 for key in entry:
                     if key == entry_title:
                         content_yaml.append("        - %s: %s" % (key, entry[key]))
                     else:
                         content_yaml.append("          %s: %s" % (key, entry[key]))
             x += 1
       
#         self.save_file(self.yaml_file, content_yaml)
#         return(self.yaml_file)

     def generate_html(self):
         with open(self.yaml_file) as f:
             yaml_map = yaml.load(f)
         f.close()

         content_html = []
         for key in yaml_map:
             content_html.append("<html>\n<body>\n")
             content_html.append("<style>\ntable {\nfont-family: arial, sans-serif;\nborder-collapse: collapse;\n  width: 100%;\n}\n")
             content_html.append("td, th {\n  border: 3px solid #dddddd;\n text-align: left;\n  padding: 2px;\nvertical-align: bottom;\n}\n")
             content_html.append("tr:nth-child(even) {\n  background-color: #dddddd;\n}\n")
             content_html.append("</style>\n</head>\n<body>\n")
             content_html.append("<B>%s</B><p>\n" % key)
             content_html.append("<table>\n")
             for sub_key1 in yaml_map[key]:
                 content_html.append("<tr>\n")
                 content_html.append("<th width=\"1px\">%s</th>\n" % sub_key1)
                 content_html.append("<th>Name</th>\n")
                 content_html.append("<th>Role</th>\n")
                 content_html.append("<th>Rep</th>\n")
                 content_html.append("<th>Attribute</th>\n")
                 content_html.append("<th>Status</th>\n")
                 content_html.append("</tr>\n")
                 x = 1
                 for value in yaml_map[key][sub_key1]:
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

#         self.save_file(self.html_file, content_html)
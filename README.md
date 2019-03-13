# thwnutsplatoongen
a platoon generator for [twohourwargames NUTS game](http://www.twohourwargames.com/ww2.html)

generates a platoon based on the country code and platoon type specified 

generates last,first name/role/reputation/attribute using NUTS v4 and NUTS Compendium rule sets

the last, first name genration is pulled from common given and surnames via google searches

generated via tables that can be replicated with manual six sided dice roles. 

found in yaml_maps/names_first_xx.yaml and names_last_xx.yaml

#### Requirements

    Python 3.7 or higher 
    https://www.python.org/downloads/

    pip
    https://pip.pypa.io/en/stable/installing/

    pyyaml
    pip install pyyaml
    https://pyyaml.org/wiki/PyYAMLDocumentation

   

#### Usage

    Make sure to extract the zip file to the directory you want to save your files
    You will be guided through options via a numerical menu
    After this two files will be written an HTML file and a YAML file
    The HTML file is inteded to be printed and used for the NUTS game
    

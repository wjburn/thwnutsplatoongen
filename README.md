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

    make sure the directory C:\thw_nuts_platoons\ exists or specify a different directory

    python squad_generator.py --country-code=us --file-name=C:\thw_nuts_platoons\us_infantry_platoon

    --country-code=us 
        required  options: us(United States), ge(German), br(British), ru(Russian)
    --platoon-type=Infantry
        defaults to Infantry, 
            options: 
                us: Infantry, Paratroopers, Rangers, Armored_Infantry
                ge: Infantry, Volks_Grenadiers, Airborne
                br: Infantry, Paratroopers
                ru: Infantry, SMG, Tank_Riders
    --file-name=C:\thw_nuts_platoons\us_infantry_platoon
        set this to where ever you would like the platoon files saved.  Two files will be created, a yaml file and an html file.  
        The yaml file is used for future features.  The HTML file can be opened with a browser and printed for game use.


### TODO:
    - enable status to be updated

    - add replacements to the squad

    - allow NCOs and Jr. NCOs to be replaced per NUTS rules
    

"""
cc_json_utils.py
This file contains the methods to take a json file and turn it into a dat file
"""
import json
import cc_data
import cc_dat_utils
import sys

def make_layer_from_json(json_layer_data):
    """Constructs layer data (a 1024 list of ints) from the given json level data
    Should the json data come in in a different format?
    Args:
        json_layer_data : the information regarding the layer we are currently constructing
                            should be an array of numbers (1024)
    Returns:
        A list of ints initialized with the layer data
    """
    #Make an array of 0s
    layer_data = []
    index = 0
    while index < len(json_layer_data):
        #while there are still numbers left to read in the array
        val = json_layer_data[index]
        #get the int value at that place in the list
        index += 1
        #move to the next element
        layer_data.append(val)
        #add the value to the layer
    print("Layer size: " + str(len(layer_data)))
    return layer_data

def make_field_from_json(field_type,field_data):
    """Constructs and returns the appropriate cc field
    Args:
        field_type (int) : what type of field to construct
        field_data : the json data to be used to create the field
    """
    if field_type == cc_data.CCMapTitleField.TYPE:
        #If we are making a map title, field data will be a string of the map title
        return cc_data.CCMapTitleField(field_data)
    elif field_type == cc_data.CCTrapControlsField.TYPE:
        #If we are making trap controls, field_data will be a dict of trap coordinates
        #It will look something like: [{"trap":[{"button":[2,5],"trap":[3,5]}]}]
        #Make an empty list to store trap and button set positional data
        all_traps = []
        for i in field_data:
            #So for each trap sub heading in the dict
            #Get button coordinates
            print("This is i " + str(i))
            bx = i["trap"][0]["button"][0]
            by = i["trap"][0]["button"][1]
            #Get trap coordinates
            tx = i["trap"][0]["trap"][0]
            ty = i["trap"][0]["trap"][1]
            #add the trap and button coordinates to the list of traps
            print("These are the traps being added: " + str(cc_data.CCTrapControl(bx,by,tx,ty)))
            all_traps.append(cc_data.CCTrapControl(bx,by,tx,ty))
        #Now that we have position data for all the sets of traps and buttons,make the trap field
        print("All traps are: "+ str(all_traps[0]))
        return  cc_data.CCTrapControlsField(all_traps)
    elif field_type == cc_data.CCCloningMachineControlsField.TYPE:
        #If we are making trap controls, field_data will be a dict of machine coordinates
        #It will look something like: [{"trap":[{"button":[2,5],"machine":[3,5]}]}]
        #Make an empty list to store machine and button set positional data
        all_machines = []
        for i in field_data:
            #So for each trap sub heading in the dict
            #Get button coordinates
            bx = i["machine"][0]["button"][0]
            by = i["machine"][0]["button"][1]
            #Get trap coordinates
            tx = i["machine"][0]["machine"][0]
            ty = i["machine"][0]["machine"][1]
            #add the trap and button coordinates to the list of traps
            all_machines.append(cc_data.CCCloningMachineControl(bx,by,tx,ty))
        #Now that we have position data for all the sets of machines and buttons,make the machine field
        return  cc_data.CCCloningMachineControlsField(all_machines)
    elif field_type == cc_data.CCEncodedPasswordField.TYPE:
        # passwords are encoded as a list of ints
        #if we are making a password, the field_data will be a list of ints
        password = []
        #GO through each element of the array of password numbers and add it the password
        for b in field_data:
            password.append(b)
        print ("Constructing Encoded Password. It is: " + str(password))
        return cc_data.CCEncodedPasswordField(password)
    elif field_type == cc_data.CCMapHintField.TYPE:
        #If we are making a hint, the field_data will be a string
        return cc_data.CCMapHintField(field_data)
    elif field_type == cc_data.CCPasswordField.TYPE:
        #This is a string password?
        return cc_data.CCPasswordField(field_data)
    elif field_type == cc_data.CCMonsterMovementField.TYPE:
        #If we are making monsters, the field data will be an array of positions of monsters?
        #It will look something like: [{"monster":[4,4]}]
        #make empty array to store monster position data
        monsters = []
        for i in field_data:
            #i is the "monster" key entry/heading, its subs are coordinate values
            monster_x = i["monster"][0]
            print("Monster x is " + str(monster_x))
            monster_y = i["monster"][1]
            print("Monster y is " + str(monster_y))
            monsters.append(cc_data.CCCoordinate(monster_x, monster_y))
        #print(monsters)
        return cc_data.CCMonsterMovementField(monsters)
    else:
        if __debug__:
            raise AssertionError("Unsupported field type: " + str(field_type))
        return cc_data.CCField(field_type, field_data)


def make_optional_fields_from_json(json_level_data):
    """Reads all the optional fields in from the level data.
    Map Title, Traps, Cloning Machines, password, hint text, and monsters
    This code sort of checks for invalid data
    Args:
        json_level_data : info about the level we are making
    Returns:
        A list of all the constructed optional fields
    """
    #Make an empty array to hold all the fields we will be making
    fields = []
    ###
    #Check for Map Title
    if("Map Title Field" in json_level_data):
        map_title = json_level_data['Map Title Field']
        fields.append(make_field_from_json(3,map_title))
    ###
    #Check for Encoded Password
    if("Encoded Password Field" in json_level_data):
        #print("Encoded Password" + str(json_level_data["Encoded Password Field"][0]))
        level_password = json_level_data['Encoded Password Field']
        fields.append(make_field_from_json(6, level_password))
    ###
    #Check for String Password
    if("Password Field" in json_level_data):
        #print("Password" + json_level_data["Password Field"])
        level_password = json_level_data['Password Field']
        fields.append(make_field_from_json(8, level_password))
    ###
    #Check for hint text
    if("Map Hint Field" in json_level_data):
        level_hint = json_level_data['Map Hint Field']
        fields.append(make_field_from_json(7,level_hint))
    ###
    #Check for Traps: will be given as a json array
    if("Trap Controls Field" in json_level_data):
        level_traps = json_level_data['Trap Controls Field']
        fields.append(make_field_from_json(4, level_traps))
    ###
    #Check for Cloning Machines:  will be given as a json array
    if("Cloning Machine Controls Field" in json_level_data):
        level_cloning_machines = json_level_data['Cloning Machines Controls Field']
        fields.append(make_field_from_json(5, level_cloning_machines))
    ###
    #Check for Monsters:  will be given as a json array
    if("Monster Movement Field" in json_level_data):
        level_monsters = json_level_data['Monster Movement Field']
        print("Level Monsters " + str(level_monsters))
        fields.append(make_field_from_json(10, level_monsters))
    return fields


def make_level_from_json(json_level_data):
    """Reads all the data to construct a single level from the active reader
    This code does not error check for invalid data
    Args:
        json_level_data  : the data regarding the level we are currently constructing
    Returns:
        A CCLevel object constructed with the read data
    """
    print("This is the level header:" + str(json_level_data["Level Number"]))
    #Make a blank level to add things to
    level = cc_data.CCLevel()
    #Get/Set level #, make sure its an int and not a string; cast to int
    level.level_number = json_level_data["Level Number"]
    #Get/Set level time (in seconds); cast to int?
    level.time = json_level_data["Time Limit"]
    #Get/Set number of chips in the level; cast to int?
    level.num_chips = json_level_data["Chip Count"]
    #Get/Set Upper Layer
    level.upper_layer = make_layer_from_json(json_level_data["Upper Layer"])
    #Get/Set lower layer
    level.lower_layer = make_layer_from_json(json_level_data["Lower Layer"])
    #Get/Set Optional Fields: Map Title, Traps, Cloning Machines, password, hint text, and monsters
    level.optional_fields = make_optional_fields_from_json(json_level_data)
    return level

def make_cc_data_from_json(input_json_filename):
    """
    Reads a json file and constructs a CCDataFile object out of it
    This code assumes a valid DAT file and does not error check for invalid data
    Args:
        json_file : the filename of the json file to read in
    Returns:
        A CCDataFile object constructed with the data from the given file
    """
    #Make a CC data file to write to and name it what was given as input
    data = cc_data.CCDataFile()
    #Open the input file and set it to reader. Then load that into something usable.
    reader = open(input_json_filename, "r")
    json_data = json.load(reader)
    #print("Here goes " + json_data["Level Pack"]["Level #2"]["Map Title Field"])
    #Parse the json data and collect all the level numbers in the file
    #This is how many levels we need to make
    #So, for each element in "Level Pack[]", make a level out of the element
    index = 1
    for i in json_data["Level Pack"]:
        #This should enter into one sub heading of the dictionary per entry
        level_heading = "Level #" + str(index)
        print("Testing level header" + level_heading)
        level = make_level_from_json(i[level_heading])
        data.levels.append(level)
        index = index+1
    print("Number of levels:" + str(len(data.levels)))
    return data

"""
#Ask for the input file
input_json_filename = input("Enter your input json filename, then press enter:")
#Ask for the output file
output_dat_filename = input("Enter your output dat filename, then press enter:")
"""
#Get command line data
command_line_input = sys.argv
#Note that the 0th element is the name of this script
input_json_filename = command_line_input[1]
print("Args" + str(command_line_input))
output_dat_filename = command_line_input[2]
print("Now taking data from" +input_json_filename + "and turning it into a playable CC level.")
print("Look for the playable level as "+ output_dat_filename)
#Make a CCdatafile; change name to output dat file name?
cc_data_file = make_cc_data_from_json(input_json_filename)
#Make a dat file from the cc_data
cc_dat_utils.write_cc_data_to_dat(cc_data_file, output_dat_filename)




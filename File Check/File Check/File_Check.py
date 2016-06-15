import os, arcpy, csv
from datetime import datetime
from os.path import split, join

def main():

    print_header()

    #.....................................................
    # SETTING UP THE DIRECTORY AND DEFAULT FILE NAMES/LOCATIONS
    #.....................................................
    INPUT_PATH = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.dirname(os.path.normpath(INPUT_PATH))
    INPUT_DIR = os.path.join(BASE_DIR, "input")
    OUTPUT_DIR = os.path.join(BASE_DIR, "output")
    rootPath = r"X:\Tidelands GIS Hyperlinks" #rootPath = raw_input("Please input the rootpath for images: ")

##    number_of_groups = raw_input("Number of file groups to be procesed: ")
##    group_name = file_groups(int(number_of_groups))
    group_dict = image_set_attributes(rootPath)

    #Extract the Grid IDs for features that are Claimed
    FC_PATH = r"V:\gis\data\Data Team Review\Tidelands\Grid_tidelands\Data\Tidelands Data Layers.gdb\Tidelands_Layers\Tidelands_Grid"
    status_field = "Claim_Status"
    grid_field = "Map_ID"
    value = "CLAIMED"
    grids_ids = get_grid_ids(FC_PATH, grid_field, status_field, value)

#Check to see if file path exists
    grid_file_paths = file_check(grids_ids,group_dict)

#Output .csv of final file paths
##    output_csv = os.path.join(OUTPUT_DIR,"output.csv")
    output_csv = os.path.join(r"C:\Users\sdochert2\Source\Repos\File-Existance\File Check\File Check\output","output.csv")
    output_header = []
    output_header.append(grid_field)
    [output_header.append(key) for key in group_dict]
    output_to_csv(grid_file_paths,output_csv,output_header)

def print_header():
    print(".................................................")
    print("   File Finder - Tidelands Image Sets")
    print(".................................................")

##def file_groups(groupNum):
##	grp_name = []
##	print "User has identified {} groups of files to search for.".format(groupNum)
##	for num in range(groupNum):
##		grp_name.append(raw_input("Enter the group name {}: ".format(num+1)))
##	return grp_name

##def create_dict(name_list, rootPath):
##    name_dict = dict()
##    for name in name_list:
##        name_dict[name] = list()
##       group_dict[name]

def image_set_attributes(root_path):
    image_set_names = [
        "Tideland Basemap Overlays",
        "Tideland Claim Line Overlays",
        "Tideland Conveyance Overlays",
        "Tideland Source Selection Scanned Maps"
        ]

    image_set_formats = {
        "Tideland Basemap Overlays":"yyy-xxxx bm.tif",
        "Tideland Claim Line Overlays":"yyy-xxxx ol.tif",
        "Tideland Conveyance Overlays":"yyy-xxxx.tif",
        "Tideland Source Selection Scanned Maps":"tyyy-xxxxss_a.jpg"
        }

    iamge_set_filepathes = dict((x,os.path.join(root_path,x)) for x in image_set_names)

    image_set_dict = dict()
    for name in image_set_names:
        format = image_set_formats[name]
        path = iamge_set_filepathes[name]
        temp_ls = [path, format]
        image_set_dict[name] = temp_ls

    return image_set_dict

#Load a ArcMap table and that is convereted into a list of tuples
def get_grid_ids(feature_class, grid_field, status_field, value):
    records=[]
    expression = arcpy.AddFieldDelimiters(feature_class, status_field) + " = '{}'".format(value)
    with arcpy.da.SearchCursor(feature_class, grid_field, where_clause=expression) as cursor:
        for row in cursor:
            records.append(str(row[0]))
    return records

def file_check(grids_ids,group_dict):
    print "Preping to look for files in the following image sets:"
    for key in group_dict.keys():
        print key
    file_check_collection = []
    for grid in grids_ids:
        file_check = []
        file_check.append(grid)
        for key, [path, format] in group_dict.items():
            format = replace_X(grid[4:],format)
            format = replace_Y(grid[:3],format)
            file_status = file_lookup(path,format)
            file_check.append(file_status)
        file_check_collection.append(file_check)
    return file_check_collection



def replace_X(item, format):
    format_update = format.replace("xxxx",item)
    return format_update

def replace_Y(item, format):
    format_update = format.replace("yyy",item)
    return format_update

def file_lookup(path,format):
    try:
        with open(os.path.join(path,format)) as file:
            return os.path.join(path,format)
    except:
        return "DOES NOT EXIST"
##        print "Image for {} does not exist for grid {}".format(key,grid)

def output_to_csv(input_list,output_file,header):
    #Ouput Word Count to .csv
    with open(output_file, 'wb') as ofile:
        writer = csv.writer(ofile, dialect='excel', delimiter = ',')
        writer.writerow(header)
        for item in input_list:
            writer.writerow(item)
    ofile.close()

startTime = datetime.now()
print startTime
main()
print "......................................................................End Runtime: ", datetime.now()-startTime

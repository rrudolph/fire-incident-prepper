'''
Prepares a 2022 folder structure and aprx template for a new fire incident as described here:
https://www.nwcg.gov/publications/pms936-1/data-preparation/directory-structure

2022 is hard coded into this script, so it will need to be changed for next year when a 
new folder structure template is generated.

Instructions

1) Edit variables as desired and run

2) If there's a problem downloading the zip file, manually download it here
https://nifc.maps.arcgis.com/sharing/rest/content/items/e8459196b0324fa187ba3f407e08141e/data
Name it "Current_GeoOps_Folder_Structure.zip" and place it in the same directory as this py file.


rocky_rudolph@nps.gov
Channel Islands National Park
3/23/2022

'''

### Variables unique to fire
destination_dir = r"C:\GISSS341"
incident_name = "Alamo"
incident_id = "AZCNF0020"
year = "2008"
pro_version = "2_9"

from os.path import dirname, join, realpath, exists
from os import rename, walk
import requests
import zipfile
import arcpy
import re


def get_gdb_paths(dir_):
	"""
	A directory walking generator. 
	Use: dirs = get_gdb_paths(some_dir)
	Then for loop over dirs
	"""
	for root, dirs, files in walk(dir_, topdown=True):
		for d in dirs:
			# Only get gdb files and not the BLANK one.
			if d.endswith(".gdb") and not "BLANK" in d:
				yield join(root, d)


def strip_non_alphanum(string):
    return re.sub('[^0-9a-zA-Z]+', '', string)

def download_project_zip(out_file):
	print("Downloading file structure zip")
	url = "https://nifc.maps.arcgis.com/sharing/rest/content/items/e8459196b0324fa187ba3f407e08141e/data"
	r = requests.get(url)
	with open(out_file, 'wb') as f:
		f.write(r.content)

def main():
	dir_path = dirname(realpath(__file__))
	file_to_unzip = join(dir_path, "Current_GeoOps_Folder_Structure.zip")

	if not exists(file_to_unzip):
		download_project_zip(file_to_unzip)

	zip_ref = zipfile.ZipFile(file_to_unzip, 'r')
	zip_ref.extractall(destination_dir)
	zip_ref.close()

	new_folder_name = f"{year}_{strip_non_alphanum(incident_name)}"

	rename(join(destination_dir, "2022_Template"), join(destination_dir, new_folder_name))

	gdbs = get_gdb_paths(join(destination_dir, new_folder_name))

	print("Renaming project gdb's")
	for gdb in gdbs:
		# print(gdb)
		new_gdb_name = gdb.replace("{incidentName}", strip_non_alphanum(incident_name)).\
		replace("{incidentID}", strip_non_alphanum(incident_id)).\
		replace("2022", year).\
		replace("2_8", pro_version)
		
		rename(gdb, new_gdb_name)

	new_template_map_name = f"{{MapType}}_{year}_{strip_non_alphanum(incident_name)}"

	print("Renaming template map")
	aprx_path = join(destination_dir, new_folder_name, "projects", "2022_ProProjectTemplate.aprx")
	aprx = arcpy.mp.ArcGISProject(aprx_path)
	for m in aprx.listMaps():
		if m.name == "{MapType}_2022_{IncidentName}":
			m.name = new_template_map_name

	print("Fixing broken dynamic text update table")
	old_path = join(destination_dir,
		new_folder_name,
		"incident_data",
		"2022_{incidentName}_{incidentID}_other_incident_data_ArcPro_2_8.gdb")
	new_path = join(destination_dir,
		new_folder_name,
		"incident_data",
		f"{year}_{strip_non_alphanum(incident_name)}_{strip_non_alphanum(incident_id)}_other_incident_data_ArcPro_{pro_version}.gdb")

	aprx.updateConnectionProperties(old_path, new_path)

	print("Pre-populating dynamic text table with fire data")
	dynamic_table = join(new_path, "DynamicTextUpdate")
	arcpy.management.CalculateField(dynamic_table, "IncidentName", f'"{incident_name}"', "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")
	arcpy.management.CalculateField(dynamic_table, "UniqueFireID", f'"{incident_id}"', "PYTHON3", '', "TEXT", "NO_ENFORCE_DOMAINS")

	new_template_path = join(destination_dir, new_folder_name, "projects", f"{year}_{strip_non_alphanum(incident_name)}")
	aprx.saveACopy(new_template_path)

	end_message = f"""
	You'll still need to manually do a few things.
	Don't forget to...
	1) Open up the template aprx: {new_template_path}.aprx
	2) Verify map name is good: {new_template_map_name}
	3) Verify dynamic text labels are good
	4) Add new gdb paths to project favorites, save
	5) Save as an edit_ aprx 
	6) Open edit_ aprx, set to local projection, and download an offline copy of the fire
	7) Remap event layers to the .geodatabase file
	8) Update the feature templates for all features in the Manage Templates window
	9) Save edit_ aprx
	10) Update the file namer xlsx

	"""
	print(end_message)


if __name__ == '__main__':
	main()

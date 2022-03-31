'''
This is a script that backs up an incident database and aprx files.  You will need to
customize the incident name and ID, as well as the location to your mobile geodatabase file.  Use with caution, 
it is set to overwrite data.

The GISS S-341 class data is hard coded in this script for reference. 

3/31/2022
'''

import arcpy
import time
import shutil
from os.path import join, basename, isdir
from os import mkdir
from glob import glob

# Optional debugger if installed
try:
	from icecream import ic 
except:
	print("Skipping icecream import")

arcpy.env.overwriteOutput = True

# now = time.localtime() # get struct_time
now = time.strptime("22 Apr 08 10:45:30", "%d %b %y %H:%M:%S") # Force a specified time (training/practice)

year, month, day, hour, minute = now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min

folderDay = f"{year}{month:02}{day:02}"
backup_timestamp = f"{year}{month:02}{day:02}_{hour}{minute}"

incident_name = "Alamo"
incident_id = "AZCNF0020"
base_dir = r"C:\GISSS341\2008_Alamo"

event_fgdb = join(base_dir, "incident_data", f"{year}_{incident_name}_{incident_id}_Event_ArcPro_2_9.gdb")
backup_path = join(base_dir, "incident_data", "backups", folderDay, f"{backup_timestamp}_{incident_name}_{incident_id}_Event_ArcPro_2_9.gdb")
mobile_gdb = join(base_dir, "incident_data", "edit", "Training_GISSEdit_NIFS_2022_337B1417F6D24B299940DDDEAE9CB9DA.geodatabase")
prog_to_backup = join(base_dir, "incident_data", f"{year}_{incident_name}_{incident_id}_progression_ArcPro_2_9.gdb")
prog_backup_path = join(base_dir, "incident_data", "backups", folderDay, f"{backup_timestamp}_{incident_name}_{incident_id}_progression_ArcPro_2_9.gdb")

aprx_files = glob(join(base_dir, "projects", "*.aprx"))

print(f"Saving backup to {backup_path}")
arcpy.conversion.MobileGdbToFileGdb(mobile_gdb, backup_path)

print("Backing up progression GeoDB")
arcpy.management.Copy(prog_to_backup, prog_backup_path, "Workspace", None)

print("Copying to main event GeoDB")
arcpy.management.Copy(backup_path, event_fgdb, "Workspace", None)

print("Backing up aprx files")
for aprx in aprx_files:
	aprx_name = basename(aprx)
	#iap_20090330_1053_Ninko_Creek_MTFNF0050.aprx
	aprx_backup = aprx_name.replace(str(year), f"{backup_timestamp}")
	aprx_destination_dir = join(base_dir, "projects", "backups", folderDay)
	if not isdir(aprx_destination_dir):
		mkdir(aprx_destination_dir)
	aprx_destination_file = join( aprx_destination_dir , aprx_backup)
	print(f" - Backing up to {aprx_destination_file}")
	shutil.copyfile(aprx, aprx_destination_file )

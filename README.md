# fire-incident-prepper
Instantly prepare a NWCG standard file folder structure for a fire incident.

Prepares a 2022 folder structure and aprx template for a new fire incident as described here:
https://www.nwcg.gov/publications/pms936-1/data-preparation/directory-structure

2022 is hard coded into this script, so it will need to be changed for next year when a 
new folder structure template is generated.

- Downloads official zipped folder structure from NIFC
- Unzips to desired folder
- Renames the project geodatabases for the specific fire
- Renames the template map name inside the aprx
- Fixes broken dynamic text update table 
- Populates dynamic text table with fire data

Instructions

1) Edit variables as desired and run

2) If there's a problem downloading the zip file, manually download it here
https://nifc.maps.arcgis.com/sharing/rest/content/items/e8459196b0324fa187ba3f407e08141e/data
Name it "Current_GeoOps_Folder_Structure.zip" and place it in the same directory as this py file.

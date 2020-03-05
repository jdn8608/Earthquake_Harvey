#Joseph Nied
#Sep 19, 2019
#This algorithm displays earthquakes dots of where different readings for earthquake Morgan Hill from 1984

#import modules
import arcpy
import sys
import os
import csv

# To allow overwriting the outputs change the overwrite option to true.
arcpy.env.overwriteOutput = True


root_directory = "C:\\temp\\"


#setup the output feature class
#https://pro.arcgis.com/en/pro-app/tool-reference/data-management/create-feature-class.htm#C_GUID-F0C78B6A-A7D6-40CC-8AFD-667A2FC4771C
#arcpy.env.workspace = "C:/data"

#need to define a projection to display correctly
prj = root_directory + "wgs_84.prj"
#determines if the map earthquake is created already and if not, creates it, if already created, renders the graduated symbols
not_created = False
#print(prj)

def RenderFeatureClass():
    
    #access current map project
    aprx = arcpy.mp.ArcGISProject("CURRENT")
    
    for map in aprx.listMaps():
        for lyr in map.listLayers():
         #only do action on the feature class that was created by this code
            if lyr.isFeatureLayer:
                sym = lyr.symbology
                
                if hasattr(sym, 'renderer'):
                    if sym.renderer.type == "SimpleRenderer" :
                        sym.updateRenderer('GraduatedSymbolsRenderer')
                        #Renders the magnitude based on how large it is so we can render the Graduated Symbol
                        sym.renderer.classificationField = fieldName_Mag
                        sym.renderer.breakCount = 6
                        lyr.symbology = sym
                        
                #labels
                if lyr.supports("SHOWLABELS"):
                    lyr.showLabels = True
                    
                    
    aprx.save()

for i in range(2)	
    if(not_created):
        #CreateFeatureclass(out_path, out_name, {geometry_type}, {template}, {has_m}, {has_z}, {spatial_reference}, {config_keyword}, {spatial_grid_1}, {spatial_grid_2}, {spatial_grid_3}, {out_alias})

        Output_FC = arcpy.CreateFeatureclass_management(root_directory, "earthquakes.shp", "POINT","","DISABLED","DISABLED", prj)
        print ("finished creating new feature class")

        #define the fields for the new feature class
        #https://pro.arcgis.com/en/pro-app/tool-reference/data-management/add-field.htm#C_GUID-8BCD0CDA-41ED-4A98-A902-E92749FD1841
        fieldName_RecordId = "record_id"
        fieldPrecision = 9


        fieldAlias = "refcode"
        """
        fieldName_Type = "type"
        fieldName_Overdue = "overdue"
        fieldLength = 255"""

        #Create the variable for the earthquake file
        fieldName_depth = "depth"
        fieldName_Mag= "magnitude"
        fieldName_QuakePlace = "QuakePlace"
        fieldLength = 255





        #aadd the field names to the map
        arcpy.AddField_management(Output_FC, fieldName_RecordId, "LONG", fieldPrecision, field_alias=fieldAlias, field_is_nullable="NULLABLE")
        arcpy.AddField_management(Output_FC, fieldName_depth, "DOUBLE", fieldPrecision, field_alias=fieldAlias, field_is_nullable="NULLABLE")
        arcpy.AddField_management(Output_FC, fieldName_Mag, "DOUBLE", fieldPrecision, field_alias=fieldAlias, field_is_nullable="NULLABLE")
        arcpy.AddField_management(Output_FC, fieldName_QuakePlace, "TEXT", field_length=fieldLength)




        #the file coming in
        file_in = root_directory + 'earthquakes.csv'

        #define the fields from the CSV
        LAT_field = "latitude"
        LON_field = "longitude"
        MAG_field = "mag"
        DEPTH_field = "depth"
        PLACE_field = "place"
        Output_FeatureClassName = "magnitude"



        #https://docs.python.org/2/library/csv.html - python 2.7
        #class csv.DictReader(f, fieldnames=None, restkey=None, restval=None, dialect='excel', *args, **kwds)
        #Create an object which operates like a regular reader but maps the information read into a dict whose keys are given by the optional fieldnames parameter.

        with open(file_in) as csvfile:
            current_data = csv.DictReader(csvfile)
            #id
            rowidval = 0
            for row in current_data:
                #will delay..
                #print("Coord:" + row[LAT_field] + "," + row[LON_field] + " " + row[TYPE_field] + " " +  row[OVERDUE_field])
                #Writing geometries
                try:
                    #define a series of fields that were created previous
                    fields = [fieldName_RecordId,fieldName_depth, fieldName_Mag, fieldName_QuakePlace, 'SHAPE@XY']
                    
                    cursor = arcpy.da.InsertCursor(Output_FC, fields)
                    
                    #print (fields)
                    
                    #cursor = arcpy.da.InsertCursor(Output_FC, ["SHAPE@XY"])
                    xy = (float(row[LON_field]), float(row[LAT_field]))
                    print(xy)
                    
                    #cursor.insertRow([xy])
                    #creates cursors for the correct fields
                    cursor.insertRow((rowidval, float(row[DEPTH_field]), float(row[MAG_field]), row[PLACE_field],xy))
                    
                    
                    rowidval += 1
                    
                except Exception:
                    e = sys.exc_info()[1]
                    print(e.args[0])


        del cursor
        not_created = False
    else:
        print("The feature class has already been created. Rendering class now with graduated features" )
        RenderFeatureClass()
print ("done")

#!usr/bin/env python

#===============================================================================
# Import modules
#===============================================================================
# Standard Library
import os
import sys
import datetime
import time
import collections
from xml.etree import cElementTree as ET

# Third party modules

# Application modules
import toolbox.log as log
import toolbox.check_process as check_process
import toolbox.xml_tools as xml_tools


#===============================================================================
# MAIN
#===============================================================================
def main():

    '''
    Grabs data from all yearly xml files and consolidates the data for web heat
    calendars.
    '''
   
    script_name = os.path.basename(sys.argv[0])
    folder_loc  = os.path.dirname(os.path.realpath(sys.argv[0]))
    folder_loc  = folder_loc.replace('scripts', '')


    #---------------------------------------------------------------------------
    # Set up logger
    #---------------------------------------------------------------------------
    logger = log.setup('root', '{folder}/logs/{script}.log'.format(
                                                    folder= folder_loc,
                                                    script= script_name[:-3]))

    logger.info('')
    logger.info('--- Script {script} Started ---'.format(script= script_name)) 


    #---------------------------------------------------------------------------
    # CHECK SCRIPT IS NOT ALREADY RUNNING
    #--------------------------------------------------------------------------- 
    if check_process.is_running(script_name):
        logger.info('Script already runnning. Exiting...')
        logger.info(other_script_found)
        sys.exit()  


    try:
        #-------------------------------------------------------------------
        # Get data from yearly files
        #-------------------------------------------------------------------      
        sensors = []
        xml_data = {}

        years = [str(year) for year in range(2016, datetime.datetime.now().year+1)]

        for year_ref in years:

            xml_file = 'wd_all_{d}.xml'.format(d= year_ref)

            logger.info('Getting data from {f}'.format(f= xml_file)) 
            tree = ET.parse('{folder}/data/{xml_file}'.format(
                                                        folder= folder_loc,
                                                        xml_file= xml_file))
            logger.info('Sorting data')
            
            root = tree.getroot()
            xmldict = xml_tools.XmlDictConfig(root)

            for sensor in root.iter('entry'):
                if sensor.text not in sensors:
                    sensors.append(sensor.text)
                    xml_data[sensor.text] = {}

                if year_ref not in xml_data[sensor.text].keys():   
                    xml_data[sensor.text][year_ref] = {}


            # Sort data under sensor and then time
            for child in root[1]:
                for grandchild in child:
                    if grandchild.tag == 't':
                        time = str(int(grandchild.text) / 1000)
                        i = 0
                    elif grandchild.tag == 'v':
                        xml_data[sensors[i]][year_ref][time] = grandchild.text
                        i += 1


        #-------------------------------------------------------------------
        # Remove min and max data sets
        #-------------------------------------------------------------------
        for sensor in xml_data.keys():
            if '_min' in sensor or '_max' in sensor:
                del xml_data[sensor]


        #-------------------------------------------------------------------
        # Write data to xml file
        #-------------------------------------------------------------------

        output_file = 'wd_all_years.xml'
        logger.info('Writting data to {f}'.format(f=output_file))
        # create new xml
        root = ET.Element('root')
        tree = ET.ElementTree(root)
        data = ET.SubElement(root, 'data')

        # populate xml
        for op_xml in xml_data.keys():

            # Create a subelement for each sensor 
            sensor = ET.SubElement(data, 'sensor', name= op_xml) 

            for year_ref in years:
                year = ET.SubElement(sensor, 'year', year= year_ref)

                # Populate time and value in each sensor          
                for time, value in xml_data[op_xml][year_ref].iteritems():
                    ET.SubElement(year, 'entry', time=time).text = value
        

        tree.write('{folder}/data/{xml_file}'.format(folder= folder_loc,
                                                    xml_file= output_file))


    except Exception, e:
        logger.error('ERROR: ({error_v}).'.format(error_v=e), exc_info=True)
        sys.exit()

    finally:
        logger.info('--- Script {script} Finished ---'.format(script= script_name)) 

 


#===============================================================================
# Boiler plate
#===============================================================================
if __name__=='__main__':
    main()

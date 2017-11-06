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
import copy
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
    folder_loc  = folder_loc.replace('garden-web-server/scripts', '')


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

            xml_file = '{folder}/data/wd_all_{d}.xml'.format(folder= folder_loc, d= year_ref)

            logger.info('Getting data from {f}'.format(f= xml_file)) 
            tree = ET.parse('{f}'.format(f= xml_file))
            root = tree.getroot()

            if not xml_data:
                logger.info('First copy')
                xml_data = copy.deepcopy(tree)
                xml_root = xml_data.getroot()
                continue

            data = root[1]

            # append year's data to file if the year matches
            for row in root[1].findall('row'):
                if datetime.datetime.fromtimestamp(int(row[0].text)).strftime('%Y') == year_ref:
                    xml_root[1].append(row)


        #-------------------------------------------------------------------
        # Write data to xml file
        #-------------------------------------------------------------------

        output_file = 'wd_all_years.xml'
        logger.info('Writting data to {folder}/data/{xml_file}'.format(folder= folder_loc,
                                                    xml_file= output_file))
        xml_data.write('{folder}/data/{xml_file}'.format(folder= folder_loc,
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

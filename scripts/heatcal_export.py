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
from xml.etree import cElementTree as ElementTree

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


    #-------------------------------------------------------------------
    # Get data from yearly files
    #-------------------------------------------------------------------
    try:
        tree = ElementTree.parse('{folder}/data/{xml_file}'.format(
                                                    folder= folder_loc,
                                                    xml_file= 'wd_all_2017.xml'))
        root = tree.getroot()
        xmldict = xml_tools.XmlDictConfig(root)

        print xmldict
       

    except Exception, e:
        logger.error('ERROR: ({error_v}).'.format(error_v=e), exc_info=True)
        sys.exit()

 


#===============================================================================
# Boiler plate
#===============================================================================
if __name__=='__main__':
    main()

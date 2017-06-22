# This program moves files from the source folder
# and distributes them to the predefined subfolders
# based on the filename keyword and the hour accessed
# 

import shutil
import sys,os
import argparse
import glob
import shutil
import textwrap
import logging
import logging.handlers
from datetime import datetime, timezone
from confLogger import createLogConf, logDefaultConf 


# Setup argparse
parser = argparse.ArgumentParser(
        description='This script moves files from the <src> folder to the <dest> subfolders by using keywors in the filenames as criteria.',
        #epilog="Ex:" + sys.argv[0] + " -s /home/user/Downloads -d /home/user/Sorted -k dave steve" ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="Ex1 :\n\t" + sys.argv[0] + " -s /home/user/Downloads -d /home/user/Sorted -k dave steve\n"
            "Moves all files from 'Downloads' folder to 'Sorted' folder under subfolders 'dave' and 'steve'\n\n"
            "Ex2 :\n\t" + sys.argv[0] + " -s /home/user/Downloads -d /home/user/Sorted -k dave steve -p 2\n"
            "Moves all files that were created more than 2 hours in the past, from 'Downloads' folder to 'Sorted' folder under subfolders 'dave' and 'steve'\n\n"
            "Ex3 :\n\t" + sys.argv[0] + " -s /home/user/Downloads -d /home/user/Sorted -k dave steve -p 2 -l\n"
            "List the files that wil be moved\n\n"
            " "
        )


parser.add_argument('-s','--src', help='Source folder',required=True)
parser.add_argument('-d','--dst', help='Destination folder', required=True)
parser.add_argument('-k','--key', help='Keywords to be used', required=True, nargs='+')
parser.add_argument('-p','--past', help='Only affects files that were created more than [no] hours in the past ')
parser.add_argument('-l','--list', help='Dont actually run, just list the files to be changed', action='store_true', default=False )
parser.add_argument('-v','--verbose', help='Verbose output in debug', action='store_true', default=False)

args = parser.parse_args()

# print program name
# print ('parser.prog: %s' %parser.prog)
scriptName = parser.prog.replace(".py","")
# print ("scriptname: %s" %scriptName )

# Setup Logging
# logging folder
logFolder = '/var/log/' + scriptName

#### Disabled. Look into confLogger.py 
##############################################
# check exit code 
#if (createLogConf(scriptName, "george", "george" ) != 0):
#    # unable to create log files and folders
#    exit ()
###############################################

# create a file handler
#handler = logging.FileHandler('Log_' + scriptName + '.log')
handler = logging.handlers.RotatingFileHandler(logFolder + '/' + scriptName + '.log', maxBytes=10000, backupCount=5 )

#
# Log only if verbose output is true in the command
if args.verbose is True:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

#logger = logging.getLogger(__name__)
logger = logging.getLogger(scriptName)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)

# Testing
#logger.debug ("-s %s" %args.src)
#logger.debug ("-d %s" %args.dst)
#logger.debug ("-k %s" %args.key)
#logger.debug ("-p %s" %args.past)
#logger.debug ("-l %s" %args.list)

# just for test . pls remove
#exit ()


## show values ##
if args.list is True:
    # Debug
    logger.info('Dry Run')

    # Print
    print ("")
    print ("\t[Dry Run]")
    print ("No files will be affected.")
    print ("")
    print ("Input folder: \t[%s]" % args.src )
    print ("Output folder: \t[%s]" % args.dst )
    print ("Keywords: \t%s" % args.key )
    
    if args.past is not None:
        print ("Evaluating files older than %s hours" %args.past)
        logger.info('Evaluating files older than %s hours' %args.past)
    else:
        print ("Evaluating ALL files")
        logger.info('Evaluating all files')

    print (" ")

# Debug Info
logger.debug("Input folder: \t[%s]" % args.src )
logger.debug("Output folder: \t[%s]" % args.dst )
logger.debug("Keywords: \t%s" % args.key )

# List files in source directory
#listOfFiles = os.listdir(args.src)

# Print the files found
#for f in listOfFiles:
#    fullPath = args.src + "/" + f
#    #subprocess.Popen("mv" + " " + fullPath + " " + dst,shell=True)
#    print ("Filename %s" %fullPath )

# Move files
for key in args.key:
    
    # target directory name
    dest = args.dst + "/%s/" %key
    #print (dest)

    # Create the target directory if it does not exist
    if not os.path.exists(dest):
        
        # dont actually run, just list if the arguement is set
        if args.list is True:
            print ("\nThe following directory will be created: %s" %dest)
            logger.info("The following directory will be created: %s" %dest)
        else:
            print ("\nCreating directory : %s" %dest)
            logger.info("Creating directory: %s" %dest )
            os.makedirs(dest)

        print ("")

    # Check for --past option
    if args.past is not None:

        # Get (unix timestamp) time now
        #now = datetime.datetime.utcnow().timestamp()
        tnow= datetime.today().timestamp()

        # move files older than <no> of hours
        for file in glob.glob(args.src + "/*%s*" %key ):
            
            # Get time file was last accessed
            taccess = os.path.getmtime(file)

            # calculate difference betweeen then and now
            tdiff = tnow - taccess
            diff = datetime.fromtimestamp(tdiff)

            # Some prints to check dates
            #print ("Run for " + key + ": "  + file)
            #print ("Time accessed: %s " %taccess)
            #print ("Time difference is : %s" %tdiff)
            #print ("Time difference is (includes timezone but the result above is correct) : %s" %diff)
            
            # Subtract the supplied (-p) hours from the current time. This is the latest time that a file can be moved.
            tpast = tnow - (int (args.past) * 60 * 60 )
            #print ("tpast %s" %tpast)

            # If the timestamp of a file is smaller (earlier) than the latest time, then the file can be moved
            if taccess < tpast :
                
                # dont actually run, just list if the argument is set
                if args.list is True:
                    print ("File %s will be moved to %s" %(file, dest ))
                    logger.info("File %s will be moved to %s" %(file, dest ))

                else:
                    #print ("The file was accessed on %s, and the time in the past is %s " %( taccess, tpast ) )
                    print ("Moving file %s to %s" %(file, dest ))
                    logger.info("Moving file %s to %s" %(file, dest ))

                    #Move the file
                    shutil.move(file, dest)

            else :
                if args.list is True:
                    print ("File %s will not be moved" %file)
                    logger.info("File %s will not be moved" %file)

                else:
                    print ("File %s is not moved" %file )
                    logger.info("File %s is not moved" %file)

    else:
        # Move all the files
        for file in glob.glob(args.src + "/*%s*" %key ):
            
            # dont actually run
            if args.list is True:
                print ("File %s will be moved to %s" %(file, dest ))
                logger.info("File %s will be moved to %s" %(file, dest ))

            else:
                print ("Moving file %s to %s" %(file, dest ))
                logger.info("Moving file %s to %s" %(file, dest ))
                # move the file
                shutil.move(file, dest)

exit()


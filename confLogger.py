import os
#import os.path

# This code is buggy and needs to be looked into.
# The functions are disabled pending review.
# in the meantime the following needs to be in place ( by hand ) for the program to work:
#       1) a file in /etc/logrotate.d/moveRec
#           with the following configuration:
#
#               /var/log/moveRec/*.log {
#                   weekly
#                   rotate 5
#                   size 10M
#                   missingok
#                   compress
#                   delaycompress
#                   create 644 george george
#                   su george george
#                   }
#
#
#       2) a folder needs to be available in the /var/log/moveRec
#


def fix_ownership(path):
    """Change the owner of the file to SUDO_UID"""

    uid = os.environ.get('SUDO_UID')
    gid = os.environ.get('SUDO_GID')

    if uid is not None:
        #os.chown(path, int(uid), int(gid))
        # change to user "george"
        os.chown(path,1000,1000)

def check_sudo():

    uid = os.environ.get('SUDO_UID')

    if uid is None:
        return 1
    else:
        return 0

def get_file(path, mode="a+"):
    """Create a file if it does not exists, fix ownership and return it open"""

    # first, create the file and close it immediatly
    open(path, 'a').close()

    # then fix the ownership
    fix_ownership(path)

    # open the file and return it
    return open(path, mode)


# function to return a logrotate configuration for /var/log
def logDefaultConf( folder, user, group ):
    conf = "/var/log/" + folder +  "/* {\n\tweekly\n\trotate 5\n\tsize 10M\n\tmissingok\n\tcompress\n\tdelaycompress\n\tcreate 644 " + user + " " + group + "\n} \n\n"
    
    #print (conf)
    return conf

# creates the logfile configuration under the /etc/logrotate.d
# creates the logfile under /var/log/{scriptname}/{scriptname}.log
def createLogConf( scriptName, user, group ):

    # Check sudo first.
    #if check_sudo():
    #    print ("First run requires sudo privileges.\nSudo is only used to create the log file directory and setup logrotate")
    #    return 1

    #print("Script: %s, user: %s, group: %s" %(scriptName, user, group))
    #get_file("/etc/logrotate.d/myScript")

    logConffile ="/etc/logrotate.d/" + scriptName
    logfile = "/var/log/" + scriptName + "/" + scriptName + ".log"

    if (not os.path.exists(logConffile)):
        try:
            f = open ("/etc/logrotate.d/" + scriptName ,"w")
            f.write(logDefaultConf(scriptName,"george","george"))
            f.close
        except OSError:
            print("First run requires sudo privileges.\nSudo is only used to create the log file directory and setup logrotate")
            return 1
        
    if (not os.path.exists(logfile)):
        try:
            print("logfile: %s, scriptName: %s" %(logfile, scriptName))
            os.makedirs("/var/log/" + scriptName)
            open(logfile, 'a').close()
            fix_ownership(logfile)
        
        except OSError:
            print("First run requires sudo privileges.\nSudo is only used to create the log file directory and setup logrotate")
            return 1

        
        
    return 0





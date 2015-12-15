#!/usr/bin/env python
import pexpect
import sys
import time

debug = True                                                            
bluetooth_addr = sys.argv[1] 
TIMEOUT = 15

converttosignedbyte = lambda n: float(n-0x100) if n>0x7f else float(n)

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print (timeformat)
        time.sleep(1)
        t -= 1

def main():
    print "\nPreparing to connect..."
    print "You might need to press the side button on Sensor Tag within 5 sec..."
    countdown (5)
    if(debug == True): print "5 secs is over"

    child = pexpect.spawn('gatttool -b ' + bluetooth_addr + ' -I')
    if(debug == True): print "\nInitiating coonection to sensor tag using gatttool"
    device_connected = False    
    try:
	child.timeout = TIMEOUT
    	child.expect('\[LE\]>')
    	child.sendline('connect')
   
#   	test for success of connect
    	child.expect('Connection successful')
    	if(debug == True): print "\nConnection suceesful"
	device_connected = True
	notification_enable = query_yes_no("Do you wanna enable notification mode.? ")
	print "notification enable: ", notification_enable
	if(notification_enable == True):
	    child.sendline('char-write-cmd 0x2E 0100')
	    child.sendline('char-write-cmd 0x31 01')
            if(debug == True): print "\nAccelerometer Service is On"
 		
	    if(debug == True): print "\nWaiting for the Accelerometer event"
    	    for elem in child:
		item = elem.split()
#		print item
                item_length = len(item)
		if(item_length == 4):
			pass
		elif (item_length == 9):
    			(xyz, m) = calcAccel(int(item[6], 16), int(item[7], 16), int(item[8], 16))
			print "\nAccel X, Y and Z: "+str(xyz)
			print "Magnitude: "+str(m)
		else:
			pass
	
	else:
            child.sendline('char-write-cmd 0x31 01')
	    child.expect('\[LE\]>')
	    while True:
    		time.sleep(1)
    		child.sendline('char-read-hnd 0x2D')
    		child.expect('descriptor: .*') 
    		rval = child.after.split()
#		print rval
    		(xyz, m) = calcAccel(int(rval[1], 16), int(rval[2], 16), int(rval[3], 16))
		print "Accel X, Y and Z: "+str(xyz)
                print "Magnitude: "+str(m)
    except pexpect.TIMEOUT:
	print "\nTimeout."
	if(device_connected == False):
	    print "No devices found"
	    if(child.isalive()):                                                 
                child.close()                                                    
		if(child.terminate(True)):
		    print "Successfully terminated."
        print "End."
    except KeyboardInterrupt:
        print "\nKeyboard Interrupt detected."
	if(child.isalive()):
	    if(notification_enable):
                child.sendline('char-write-cmd 0x2E 0000')
            child.sendline('char-write-cmd 0x31 00')
	    child.close()
	    if(child.terminate(True)):
	        print "Successfully terminated."
        print "End."

    except:
        print "\nGeneral Exception."
	if(child.isalive()):
	    if(notification_enable):
                child.sendline('char-write-cmd 0x2E 0000')
            child.sendline('char-write-cmd 0x31 00')
	    child.close()
	    if(child.terminate(True)):
	        print "Successfully terminated."
        print "End."   

# This algorithm borrowed from 
# http://processors.wiki.ti.com/index.php/SensorTag_User_Guide#Gatt_Server
# but combining all three axis values, gives the magnitude.
#

def calcAccel(rawX, rawY, rawZ):
    accel = lambda v: converttosignedbyte(v) / 64.0  # Range -2G, +2G
    xyz = [accel(rawX), accel(rawY), accel(rawZ)]
    mag = (xyz[0]**2 + xyz[1]**2 + xyz[2]**2)**0.5
    return (xyz, mag)


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n]: "
    elif default == "yes":
        prompt = " [y/n]: "
    elif default == "no":
        prompt = " [y/n]: "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


if __name__=='__main__':

	print "===================================================================="
	print "                  Intel Edison & Sensor Tag comm                    "
	print "===================================================================="
	main()

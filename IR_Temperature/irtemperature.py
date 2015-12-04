#!/usr/bin/env python
import pexpect
import sys
import time

debug = True                                                            
bluetooth_addr = sys.argv[1] 
TIMEOUT = 15

def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print (timeformat)
        time.sleep(1)
        t -= 1

def floatfromhex(h):
    t = float.fromhex(h)
    if t > float.fromhex('7FFF'):
        t = -(float.fromhex('FFFF') - t)    
    return t

def main():
    print "\nPreparing to connect..."
    print "You might need to press the side button on Sensor Tag within 5 sec..."
    countdown (5)
    if(debug == True): print "5 secs is over"

    child = pexpect.spawn('gatttool -b ' + bluetooth_addr + ' -I')
    if(debug == True): print "\nInitiating connection to sensor tag using gatttool"
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
	    child.sendline('char-write-cmd 0x26 0100')
	    child.sendline('char-write-cmd 0x29 01')
            if(debug == True): print "\nIR Temperature Service is On"
 		
            it = iter(child)
#            next(it, None)  # skip first item.
	    if(debug == True): print "\nWaiting for the IR Temperature event"
    	    for elem in child:
		item = elem.split()
                item_length = len(item)
		if(item_length == 4):
			pass
		elif (item_length == 10):
			objT = floatfromhex(item[7] + item[6])
    			ambT = floatfromhex(item[9] + item[8])
    			#print rval
    			calcTmpTarget(objT, ambT)
		else:
			pass
	
	else:
            child.sendline('char-write-cmd 0x29 01')
	    while True:
    		time.sleep(1)
    		child.sendline('char-read-hnd 0x25')
    		child.expect('descriptor: .*') 
    		rval = child.after.split()
#		print rval
		objT = floatfromhex(rval[2] + rval[1])
    		ambT = floatfromhex(rval[4] + rval[3])
    		#print rval
    		calcTmpTarget(objT, ambT)
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
                child.sendline('char-write-cmd 0x26 0000')
            child.sendline('char-write-cmd 0x29 00')
	    child.close()
	    if(child.terminate(True)):
	        print "Successfully terminated."
        print "End."
    except:
        print "\nGeneral Exception."
	if(child.isalive()):
	    if(notification_enable):
                child.sendline('char-write-cmd 0x26 0000')
            child.sendline('char-write-cmd 0x29 00')
	    child.close()
	    if(child.terminate(True)):
	        print "Successfully terminated."
        print "End."   


# This algorithm borrowed from 
# http://processors.wiki.ti.com/index.php/SensorTag_User_Guide#Gatt_Server
# I've not tested it
#
def calcTmpTarget(objT, ambT):
    m_tmpAmb = ambT/128.0
    Vobj2 = objT * 0.00000015625
    Tdie2 = m_tmpAmb + 273.15
    S0 = 6.4E-14            # Calibration factor
    a1 = 1.75E-3
    a2 = -1.678E-5
    b0 = -2.94E-5
    b1 = -5.7E-7
    b2 = 4.63E-9
    c2 = 13.4
    Tref = 298.15
    S = S0*(1+a1*(Tdie2 - Tref)+a2*pow((Tdie2 - Tref),2))
    Vos = b0 + b1*(Tdie2 - Tref) + b2*pow((Tdie2 - Tref),2)
    fObj = (Vobj2 - Vos) + c2*pow((Vobj2 - Vos),2)
    tObj = pow(pow(Tdie2,4) + (fObj/S),.25)
    tObj = (tObj - 273.15)
    print "%.2f C" % tObj

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

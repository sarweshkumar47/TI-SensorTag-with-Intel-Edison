#!/usr/bin/env python
import pexpect
import time
import sys

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

def main():
    print "\nPreparing to connect..."
    print "You might need to press the side button on Sensor Tag within 5 sec..."
    countdown (5)
    if(debug == True): print "5 secs is over"

    tool = pexpect.spawn('gatttool -b ' + bluetooth_addr + ' -I')
    if(debug == True): print "\nInitiating connection to sensor tag using gatttool"
    device_connected = False    
    try:
	tool.timeout = TIMEOUT
    	tool.expect('\[LE\]>')
    	tool.sendline('connect')
   
#   	test for success of connect
    	tool.expect('Connection successful')
    	if(debug == True): print "\nConnection suceesful"
	device_connected = True
    	tool.sendline('char-write-cmd 0x60 0100')  # 0x60 - depends on sensorTag version, please check the userguide properly
    	if(debug == True): print "\nSimple Key Service is On"
 
        it = iter(tool)
        next(it, None)  # skip first item.
	if(debug == True): print "\nWaiting for the keypress event"
    	for elem in it:
	    item = elem.split()[6]
#           print (item)
	    if(item == '01'):
		print "\nRight Key Pressed"
	    elif(item == '02'):
		print "\nLeft Key Pressed"
	    elif(item == '03'):
		print "\nLeft Key and Right Key, both pressed"
	    else:
		print "\nOff"

    except pexpect.TIMEOUT:
	print "\nTimeout."
	if(device_connected == False):
	    print "No devices found"
	else:
	    print "No Key Event in ", TIMEOUT, " secs, Exited"
    except KeyboardInterrupt:
        tool.sendline('char-write-cmd 0x60 0000')
        tool.close()
	tool.terminate()
        print "\nKeyboard Interrupt detected."
        print "End."
    except:
        tool.sendline('char-write-cmd 0x60 0000') 
        tool.close()
	tool.terminate()
        print "\nGeneral Exception."
        print "Terminated."    

if __name__=='__main__':

	print "===================================================================="
	print "                  Intel Edison & Sensor Tag comm                    "
	print "===================================================================="
	main()

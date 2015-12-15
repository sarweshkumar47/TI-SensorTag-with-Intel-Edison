#!/usr/bin/env python
import pexpect
import sys
import time
import mraa

debug = True                                                            
bluetooth_addr = sys.argv[1] 
TIMEOUT = 15
GPIOPIN = 13

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
    	child.sendline('char-write-cmd 0x60 0100')
    	if(debug == True): print "\nSimple Key Service is On"
    	child.expect('\[LE\]>')
	led = mraa.Gpio(GPIOPIN)
	led.dir(mraa.DIR_OUT) 
	ledstatus = False
        it = iter(child)
        next(it, None)  # skip first item.
	if(debug == True): print "\nWaiting for the keypress event"
    	for elem in it:
	    item = elem.split()[6]
#           print (item)
	    if(item == '01'):
#		print "\nRight Key Pressed"
		if (ledstatus == False):
		    ledstatus = True
		    led.write(1)
		    print "\n> led on"
		else:
		    print "\n> led is already in on state"
	    elif(item == '02'):
#		print "\nLeft Key Pressed"
		if (ledstatus == True):
		    ledstatus = False
                    led.write(0)
		    print "\n> led off"
		else:
		    print "\n> led is already in off state"		    
	    elif(item == '03'):
#		print "\nLeft Key and Right Key, both pressed"
		if (ledstatus == True):
		    ledstatus = False
		    led.write(0)
		    print "\n> led off"
		else:
		    print "\n> led is already in off state"
	    else:
#		print "\nOff"
		pass

    except pexpect.TIMEOUT:
	print "\nTimeout."
	if(device_connected == False):
	    print "No devices found"
            if (child.isalive()):                                                    
                child.close()     
                if(child.terminate(True)):
		    print "Successfully terminated."
	    print "End."
	else:
	    print "No Key Event in ", TIMEOUT, " secs, Exited"
	    if (child.isalive()):                                                    
                child.sendline('char-write-cmd 0x60 0000')                           
                child.close()                                                        
                if(child.terminate(True)):
		    print "Successfully terminated."
	    print "End."
    except KeyboardInterrupt:
        print "\nKeyboard Interrupt detected."
	if (child.isalive()):
            child.sendline('char-write-cmd 0x60 0000')
            child.close()
	    if(child.terminate(True)):
		print "Successfullt terminated."
        print "End."
    except:
        print "\nGeneral Exception."
	if (child.isalive()):
            child.sendline('char-write-cmd 0x60 0000') 
            child.close()
	    if(child.terminate()):
		print "Successfully terminated."
        print "End."    

if __name__=='__main__':

	print "===================================================================="
	print "                  Intel Edison & Sensor Tag comm                    "
	print "===================================================================="
	main()

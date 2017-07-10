## Simple Key Notification from SensorTag

SensorTag 2561 has two key switches (except the side one). Pressing of these keys generate key events. This program
enables Simple Key Service (UUID: FFE1) and whenver right/left key is pressed, receives notification from SensorTag
and prints on a screen.


The Simple Key service is used to enable notifications for key hits on the sensor tag. 


**Attribute Table**

|handle(hex)|Type (hex)|   Type (#DEFINE)    |GATT Server Permissions| Notes      |
|-----------|----------|---------------------|-----------------------|------------|
|  0x60     |  0x2902  |GATT_CLIENT_CHAR_CFG_UUID|GATT_PERMIT_READ or GATT_PERMIT_WRITE |Write "0100" to enable notifications, "0000" to disable


**Simple Key Service**

|Type    |UUID   |   Notify 	        |  Format|
|--------|-------|--------------------|--------|
| Data   |	FFE1 |  Notification Only |	Bit 2: side key, Bit 1- Left key, Bit 0 – Right key |

The SensorTag can be configured to send notifications for every sensor by writing “01 00” to the characteristic configuration < GATT_CLIENT_CHAR_CFG_UUID> for the corresponding sensor data, the data is then sent as soon as the data has been updated.

## Get Key Pressed Notifications
Run the python program and give mac addess of the sensortag as an argument

      python simplekey_press_service.py 78:xx:xx:xx:xx:B6

### Note: 
The side key will only provided notifications in test mode, as it is normally used to disconnect a connected device 
or toggle advertising on/off. 

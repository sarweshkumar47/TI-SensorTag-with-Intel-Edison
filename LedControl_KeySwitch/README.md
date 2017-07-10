## Led Control based on Key Notification from SensorTag

SensorTag 2561 has two key switches (except the side one). Pressing of these keys generate key events. We can use 
these key events to control various things (Ex: sensors, leds...). As an example I'm controlling an on-board led (GPIO 13)
which is present on Intel Edison. This program enables Simple Key Service (UUID: FFE1) and whenver right/left key is pressed,
receives notification from SensorTag and turns on/off the led (GPIO 13)

The Simple Key service is used to enable notifications for key hits on the sensor tag. 


**Simple Key Service**

| Type | UUID | Handle | Type (#DEFINE) | Notes      |
|------|------|--------|----------------|------------|
| Data | FFE1 | 0x60   | GATT_CLIENT_CHAR_CFG_UUID | Write "0100" to enable notifications, "0000" to disable |

The SensorTag can be configured to send notifications for every sensor by writing “01 00” to the characteristic configuration < GATT_CLIENT_CHAR_CFG_UUID> for the corresponding sensor data, the data is then sent as soon as the data has been updated.

## Led Control from SensorTag
Run the python program and give mac addess of sensortag as an argument

      python ledcontrol_simplekey.py 78:xx:xx:xx:xx:B6

### Note: 
The side key will only provided notifications in test mode, as it is normally used to disconnect a connected device 
or toggle advertising on/off. 

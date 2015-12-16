#IR Temperature Sensor in SensorTag

SensorTag has IR Temerature sensor, can measure both object and ambient temperature.


__Sensor Overview__


| Name   | Update  | Size per Update | I2C Address | I2C Speed |
|--------|---------|------------|--------|---------|
| TMP006 | > 250 ms |  2 x 16bit |	0x44 |  < 3.4 MHz |


__IR Temperature Sensor__

Two types of data are obtained from the IR Temperature sensor TMP006: object temperature and ambient temperature. 

| Type   | UUID  | Handle | Type (#DEFINE) | Format | Notes |
|--------|-------|--------|----------------|--------|-------|
| Data   |	AA01 | 	0x25  | IRTEMPERATURE_DATA_UUID |	ObjLSB ObjMSB AmbLSB AmbMSB (4 bytes) |  4 bytes data |
| Data Notification | | 0x26 | GATT_CLIENT_CHAR_CFG_UUID | 2 bytes | Write "0100" to enable notifications, "0000" to disable|
|Configuration| AA02 | 0x29 | IRTEMPERATURE_CONF_UUID | 1 byte | Write "01" to start Sensor and Measurements, "00" to put to sleep |


When the enable command is issued, the sensor starts to perform measurements each second (average over four measurements) and the data is stored in the <Data> each second as well. When the disable command is issued, the sensor is put in stand-by mode. To obtain data OTA either use notifications or read the data directly

The SensorTag can be configured to send notifications for every sensor by writing “01 00” to the characteristic configuration < GATT_CLIENT_CHAR_CFG_UUID> for the corresponding sensor data, the data is then sent as soon as the data has been updated. The sensors are enabled by writing 0x01 (NB: Gyroscope has a different code) to the corresponding Configuration and then disabled by writing 0x00

##Get Temperature from SensorTag
Run the python program and give mac addess of the sensortag as an argument

     python irtemperature.py 78:xx:xx:xx:xx:B6
     
  

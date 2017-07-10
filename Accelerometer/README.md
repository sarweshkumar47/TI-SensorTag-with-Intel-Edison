# Accelerometer in SensorTag

SensorTag has Accelerometer, can measure acceleration in 3 axis with programmable resolution up to 14 bit.


__Sensor Overview__


| Name   | Update  | Size per Update | I2C Address | I2C Speed |
|--------|---------|------------|--------|---------|
| KXTJ9  | > 20 ms |  3 x 8bit  | 0x0F   |  < 400 kHz |


__Accelerometer__


| Type   | UUID  | Handle | Type (#DEFINE) | Format | Notes |
|--------|-------|--------|----------------|--------|-------|
| Data   |	AA11 | 	0x2D  | ACCELEROMETER_DATA_UUID |	X : Y : Z (3 bytes) |  X : Y : Z Coordinates |
| Data Notification | | 0x2E | GATT_CLIENT_CHAR_CFG_UUID | 2 bytes | Write "0100" to enable notifications, "0000" to disable|
|Configuration| AA12 | 0x31 | ACCELEROMETER_CONF_UUID | 1 byte | Write "01" to start Sensor and Measurements, "00" to put to sleep |
| Period | AA13 | 0x34 | ACCELEROMETER_PERI_UUID | 1 byte | Period = [Input*10] ms, default 1000 ms, lower limit 100 ms |


When the enable command is issued, the sensor starts to perform measurements each second and the data is stored in each second as well. When the disable command is issued, the sensor is put to sleep. To obtain data OTA either use notifications or read the data directly. The default period for the data is one second, which can be changed by writing to the __Period__ (unit 10 ms). Range is set to +/-2g

The SensorTag can be configured to send notifications for every sensor by writing “01 00” to the characteristic configuration < GATT_CLIENT_CHAR_CFG_UUID> for the corresponding sensor data, the data is then sent as soon as the data has been updated. The sensors are enabled by writing 0x01 (NB: Gyroscope has a different code) to the corresponding Configuration and then disabled by writing 0x00

## Get Accelerometer values from SensorTag
Run the python program and give mac addess of the sensortag as an argument

     python accelerometer.py 78:xx:xx:xx:xx:B6
     
  

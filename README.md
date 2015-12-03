# TI-SensorTag-with-Intel-Edison
## SensorTag 2561 with Intel Edison over BLE

The [TI SensorTag](http://www.ti.com/tool/cc2541dk-sensor) is a portable low-power module that uses Blueooth Low Energy (BLE, Bluetooth 4.0) and various sensors to communicate data to any BLE reciever. 

Intel Edison has built-in Bluetooth, so no need of external USB Bluetooth dongle.

The python scripts that interface with the Intel Edison were gently modified from _[msaunby's Raspberry Pi Scripts.](https://github.com/msaunby/ble-sensor-pi)_

##Hardware
* Intel Edison
* TI SensorTag

##Software
* BlueZ software package on Intel Edison

The TI SensorTag, along with many other Bluetooth devices, uses the Generic Attribute Profile (GATT) to interface with your computer and other devices. Gatttool is a standard tool included in the BlueZ software package, but it is not installed on the Intel Edison board by default.

To install Bluez software package on Intel Edison, please follow [this post.](https://software.intel.com/en-us/articles/using-the-generic-attribute-profile-gatt-in-bluetooth-low-energy-with-your-intel-edison)

## References
* [https://github.com/msaunby/ble-sensor-pi](https://github.com/msaunby/ble-sensor-pi)
* [https://software.intel.com/en-us/articles/intel-edison-board-getting-started-with-bluetooth](https://software.intel.com/en-us/articles/intel-edison-board-getting-started-with-bluetooth)

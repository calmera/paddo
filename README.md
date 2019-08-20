# FiberOrb

## Installing Micropython

### Erase
```
esptool.py --chip esp32 --port /dev/ttyASM0 erase_flash
```

### Flash
```
esptool.py --chip esp32 --port /dev/ttyUSB0 --baud 460800 write_flash -z 0x1000 esp32-20190125-v1.10.bin
```

# Read temperature of RPI

Reference

1. [raspberrypi document `vcgencmd`](https://github.com/raspberrypi/documentation/blob/0e2b6afed4dd6d7d0fa2560256c57cc2f2d08d3c/raspbian/applications/vcgencmd.md)

## 1. Test with command line

Use the following command to get the RPI's throttling and power status.

```bash
vcgencmd get_throttled
```

It will return:

```bash
throttled=0x50005
```

Returns the throttled state of the system. This is a bit pattern.

| Bit | Meaning                             |
| :-: | ----------------------------------- |
|  0  | Under-voltage detected              |
|  1  | Arm frequency capped                |
|  2  | Currently throttled                 |
|  3  | Soft temperature limit active       |
| 16  | Under-voltage has occurred          |
| 17  | Arm frequency capped has occurred   |
| 18  | Throttling has occurred             |
| 19  | Soft temperature limit has occurred |

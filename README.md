# Install
No dependecies are required

# How it works
- Map the key codes based on **/usr/include/linux/input-event-codes.h**
- Program looks into the **/proc/bus/input/devices** for the keyboard **$input**
- Then it reads the inputs from **/dev/input/$input**

# Usage
1) Download the file **keylogger.py**
2) Inside the same folder where the file is run:

```
sudo python3 keylogger.py 1 > keylogger.txt
```

3) The output will be inside **keylogger.txt**, inside the same folder

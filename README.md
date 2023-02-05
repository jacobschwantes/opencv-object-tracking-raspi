# opencv-object-tracking-raspi


## Setup

This project uses a webcam to stream video. Before running the code, make sure to configure the webcam on your device.


## Installing Dependencies

Install the dependencies for the project

```
pip install -r requirements.txt
```

## Customization


Notably, you can use a different object detector by changing the path `"models/fullbody_recognition_model.xml"` in `object_classifier = cv2.CascadeClassifier("models/fullbody_recognition_model.xml")`.

to a new model in the models directory.

```
facial_recognition_model.xml
fullbody_recognition_model.xml
upperbody_recognition_model.xml
```

## Running the Program

Run the program

```
python main.py
```

You can view a live stream by visiting the ip address of your pi in a browser on the same network. You can find the ip address of your Raspberry Pi by typing `ifconfig` in the terminal and looking for the `inet` address. 

Visit `<raspberrypi_ip>:5000` in your browser to view the stream.

## Credit

This repository is a modified version of [Smart-Security-Camera](https://github.com/HackerShackOfficial/Smart-Security-Camera)

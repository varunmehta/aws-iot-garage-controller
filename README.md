# aws-iot-garage-opener

As part of the Slalom hackathon, reviving an old local only project, and extending it to be cloud enabled. This code will now use aws-iot-core and other libraries to communicate with the server. For now it's a simple repo, will break it down to smaller sections once the lambda and other pieces of code take shape.

There are many projects on the internet which emulate this problem, the idea to use a Pi to control a garage is not new, but most of them warrant you to open ports on your router to the Pi, and also expose the Pi to the internet. This opens your Pi and in turn your network to attack. If there is any vulnerability you have not patched on your pi, your network is toast!

Using the AWS IoT API, the Pi stays local to your network, and also due to the whole certificate exchange and other IoT core security measures you know how the data is travelling b/w your pi and the n/w.   

## Wiring Diagram

![Alt text](motor-pi-wiring-diagram.png?raw=true "Motor-Relay-Pi Wiring Diagram")

## Task List

 - [X] Connect Pi to motor and sensor, and control via python program.
 - [ ] Write in AWSIoT component and get the code moving via iot messages.
 - [ ] Build UI and Lambda function to control it.   

 
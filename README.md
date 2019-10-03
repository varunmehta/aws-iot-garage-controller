# aws-iot-garage-opener

As part of the Slalom hackathon, reviving an old local only project, and extending it to be cloud enabled. This code will now use aws-iot-core and other libraries to communicate with the server. For now it's a simple repo, will break it down to smaller sections once the lambda and other pieces of code take shape.

There are many projects on the internet which emulate this problem, the idea to use a Pi to control a garage is not new, but most of them warrant you to open ports on your router to the Pi, and also expose the Pi to the internet. This opens your Pi and in turn your network to attack. If there is any vulnerability you have not patched on your pi, your network is toast!

Using the AWS IoT API, the Pi stays local to your network, and also due to the whole certificate exchange and other IoT core security measures you know how the data is travelling b/w your pi and the n/w.   

## Setup across the system
We are still working on the terraform scripts to make it a viable solution to make it work end to end. For now, check the individual folders for details on how to deploy each of the sections.

## YouTube Video
https://youtu.be/RUC5E85iKgs

# Architecture

## AWS Setup

![Alt text](IotHackathonFlow.png?raw=true "AWS Ecosystem")

## GPIO Wiring Diagram

![Alt text](fritzing_wiring_diagram.png?raw=true "Motor-Relay-Pi Wiring Diagram")

## UI [New, We now have an updated UI on cloudfront]

![Alt text](CloudFront-UI-Screenshot.jpg?raw=true "Angular UI screenshot")

## Phase 2 (not implemented)

Use the AWS ML/AI services and perform image recognition using face profiles. If the user in video is unknown, send intruder alert.

![Alt text](IotHackathonFlow_Phase2.png?raw=true "Use ML/AI to perform image recognition")

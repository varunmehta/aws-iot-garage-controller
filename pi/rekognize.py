import boto3
import config
import time
import json
from datetime import datetime

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

client = AWSIoTMQTTClient('')


class Watcher:
    DIRECTORY_TO_WATCH = "/var/lib/motioneye/MainCamera"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


def get_rk_client():
    return boto3.client('rekognition')


def set_iot_client(iot_client):
    global client
    client = iot_client


def get_iot_client():
    return client


def check_face(rk_client, file):
    face_detected = False
    with open(file, 'rb') as image:
        response = rk_client.detect_faces(Image={'Bytes': image.read()})
        if not response['FaceDetails']:
            face_detected = False
        else:
            face_detected = True

    return face_detected, response


def check_matches(rk_client, file):
    face_matches = False
    with open(file, 'rb') as image:
        response = rk_client.search_faces_by_image(CollectionId='CarPen9000', Image={'Bytes': image.read()},
                                                   MaxFaces=1,
                                                   FaceMatchThreshold=85)
        if not response['FaceMatches']:
            face_matches = False
        else:
            face_matches = True

    return face_matches, response


def lps(message):
    """
        L: Log
        P: Print to console
        S: Send to AWS

        This method is supposed to log the message to log4j, print to console (for testing),
        and send the message to be logged as an event. All events are logged.
    """
    now = datetime.now().strftime("%m/%d/%Y, %H:%M:%S.%f")

    print('[ ' + now + ' ] ' + message)
    message = '{ "state": "' + message + '", "timestamp": "' + now + '"}'
    message = json.dumps(message)
    message = json.loads(message)
    try:
        # This should publish on a different topic, but for lack of time, adding here.
        get_iot_client().publishAsync(config.TOPIC_SENSOR, message, 0)
    except AWSIoTMQTTClient.exception.AWSIoTExceptions.publishTimeoutException as e:
        print(e)


def process(image):
    rk_client = get_rk_client()

    print('[+] Running face checks against image...')
    result, resp = check_face(rk_client, image)

    if result:
        print("[+] Face(s) detected with %r confidence..." % (round(resp['FaceDetails'][0]['Confidence'], 2)))
        print("[+] Checking for a face match...")
        resu, res = check_matches(rk_client, image)

        if resu:
            message = "[+] Identity matched %s with %r similarity and %r confidence..." % (
                res['FaceMatches'][0]['Face']['ExternalImageId'], round(res['FaceMatches'][0]['Similarity'], 1),
                round(res['FaceMatches'][0]['Face']['Confidence'], 2))
            print(message)
            lps("Matched %s - %r similarity and %r confidence" % (
                res['FaceMatches'][0]['Face'], round(res['FaceMatches'][0]['Similarity'], 1),
                round(res['FaceMatches'][0]['Face']['Confidence'], 2)))
        else:
            print("[-] No face matches detected...")
            lps("INTRUDER_ALERT")
    else:
        print("[-] No faces detected...")


def main(iot_client):
    print('starting facial rekognition tracker')
    set_iot_client(iot_client)
    w = Watcher()
    w.run()


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)
            process(event.src_path)

        # Skip modified for now, just created event
        # elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            # print("Received modified event - %s." % event.src_path)
            # process(event.src_path)

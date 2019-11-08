import boto3
import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


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


def get_client():
    return boto3.client('rekognition')


def check_face(client, file):
    face_detected = False
    with open(file, 'rb') as image:
        response = client.detect_faces(Image={'Bytes': image.read()})
        if not response['FaceDetails']:
            face_detected = False
        else:
            face_detected = True

    return face_detected, response


def check_matches(client, file):
    face_matches = False
    with open(file, 'rb') as image:
        response = client.search_faces_by_image(CollectionId='CarPen9000', Image={'Bytes': image.read()},
                                                MaxFaces=1,
                                                FaceMatchThreshold=85)
        if not response['FaceMatches']:
            face_matches = False
        else:
            face_matches = True

    return face_matches, response


def process(image):
    client = get_client()

    print('[+] Running face checks against image...')
    result, resp = check_face(client, image)

    if result:
        print("[+] Face(s) detected with %r confidence..." % (round(resp['FaceDetails'][0]['Confidence'], 2)))
        print("[+] Checking for a face match...")
        resu, res = check_matches(client, image)

        if resu:
            print("[+] Identity matched %s with %r similarity and %r confidence..." % (
                res['FaceMatches'][0]['Face']['ExternalImageId'], round(res['FaceMatches'][0]['Similarity'], 1),
                round(res['FaceMatches'][0]['Face']['Confidence'], 2)))
        else:
            print("[-] No face matches detected...")
    else:
        print("[-] No faces detected...")


class Handler(FileSystemEventHandler):

    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None

        elif event.event_type == 'created':
            # Take any action here when a file is first created.
            print("Received created event - %s." % event.src_path)
            process(event.src_path)

        elif event.event_type == 'modified':
            # Taken any action here when a file is modified.
            print("Received modified event - %s." % event.src_path)
            process(event.src_path)


if __name__ == '__main__':
    w = Watcher()
    w.run()

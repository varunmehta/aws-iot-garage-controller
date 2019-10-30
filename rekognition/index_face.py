import boto3
from pprint import pprint
import argparse

def add_faces_to_collection(bucket, folder, collection_id):    
    client=boto3.client('rekognition')
    bucket_client = boto3.client('s3')

    photos = bucket_client.list_objects_v2(Bucket=bucket, Prefix=folder)
    #pprint(photos)
    face_count = 0
    for photo_dict in photos['Contents']:
        photo = photo_dict['Key']
        print('Procerssing {0}'.format(photo))
        if folder == photo:
            continue
        response=client.index_faces(CollectionId=collection_id,
                                    Image={'S3Object':{'Bucket':bucket,'Name':photo}},
                                    ExternalImageId=photo.replace('/','_'),
                                    MaxFaces=1,
                                    QualityFilter="AUTO",
                                    DetectionAttributes=['ALL'])

        print ('Results for ' + photo) 	
        print('Faces indexed:')						
        for faceRecord in response['FaceRecords']:
            print('  Face ID: ' + faceRecord['Face']['FaceId'])
            print('  Location: {}'.format(faceRecord['Face']['BoundingBox']))

        print('Faces not indexed:')
        for unindexedFace in response['UnindexedFaces']:
            print(' Location: {}'.format(unindexedFace['FaceDetail']['BoundingBox']))
            print(' Reasons:')
            for reason in unindexedFace['Reasons']:
                print('   ' + reason)
        face_count = face_count + len(response['FaceRecords'])
    return face_count

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--folder', '-f', help='Folder in the S3 bucket carpen9000-rekognition to process photos', required=True)
    args = parser.parse_args()

    bucket='carpen9000-rekognition'
    collection_id='CarPen9000'
    folder = 'john/'
    
    indexed_faces_count=add_faces_to_collection(bucket, args.folder, collection_id)
    print("Faces indexed count: " + str(indexed_faces_count))


if __name__ == "__main__":
    main()
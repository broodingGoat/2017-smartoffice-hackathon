import requests
from flask import Flask, render_template
from myutils import loadenv
import boto3


app = Flask(__name__)


#s3_users = "poc-smartoffice-users"
#s3_location = "poc-smartoffice-capturedimages"
s3_users = "reinvent2017-reference"
s3_location = "reinvent2017-captured"
user_db = "smartoffice-user"
location_db = "smartoffice-location"
aws_access_key_id = loadenv.get_env_variable('AWS_ACCESS_KEY_ID')
aws_secret_access_key = loadenv.get_env_variable('AWS_SECRET_ACCESS_KEY')
aws_region = loadenv.get_env_variable('AWS_DEFAULT_REGION')


def _get_s3_images_for_all_users():
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,region_name=aws_region)
    all_objects = s3_client.list_objects(Bucket = s3_users)
    user_dict = {}
    for items in all_objects["Contents"]:
        if "jpg" in items["Key"]:
            item =  items["Key"]
            user = item.split("/")[0]
            user_dict[user] = item

    return user_dict


def _get_s3_images_for_captured_events(time):
    if time == "all":
        s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,region_name=aws_region)
        all_objects = s3_client.list_objects(Bucket = s3_location)
        events_dict = {}
        for items in all_objects["Contents"]:
            if "jpg" in items["Key"] or "JPG" in items["Key"]:
                item =  items["Key"]
                item_list = item.split("/")
                #/break room/11-29-2017/09-00-00
                location = item_list[0]
                date = item_list[1]
                time = item_list[2]
                s3_key = item
                events_dict[s3_key] = "%s,%s,%s" %(location, date, time)
        return events_dict



def parse_image():
    """
       takes location, date, time, s3 image
       parses image to compare all users
       parses image to do label extraction
    """
    db_client = boto3.client('dynamodb', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,region_name=aws_region)
    s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,region_name=aws_region)
    rk_client = boto3.client('rekognition', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,region_name=aws_region)
    #print _get_s3_images_for_all_users()
    captured_events = _get_s3_images_for_captured_events("all")
    reference_users = _get_s3_images_for_all_users()
    for item in captured_events.keys():
        print item
        
        # object label extraction
        labels = rk_client.detect_labels(
                                Image = {
                                'S3Object' : {
                                    'Bucket': s3_location,
                                    'Name' : item
                                }
                                },
                                MinConfidence = 50)
        #store objects in a list
        object_list_in_image = []
        for label in labels['Labels']:
            object_list_in_image.append(label['Name'])
        print object_list_in_image
    
        # find faces
        for user in reference_users.keys():
            s3_user_image_key = reference_users[user]
            print s3_user_image_key
            print item
            boto3.set_stream_logger('')
            response = rk_client.compare_faces(
                                SourceImage={
                                'S3Object': {
                                    'Bucket': s3_users,
                                    'Name': s3_user_image_key
                                               }},
                                TargetImage={
                                'S3Object': {
                                    'Bucket': s3_location,
                                    'Name': item
                                }
                                }
                                )
                                
                                
                                
            print response
    return "image parsed"


def index_faces():
    rk_client = boto3.client('rekognition', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,region_name=aws_region)
    user_list = _get_s3_images_for_all_users()
    for user in user_list.keys():
        user_s3_key = user_list[user]
        print user
        print user_s3_key
        response = rk_client.index_faces(
                                         CollectionId='faces',
                                         Image={
                                         'S3Object': {
                                         'Bucket': s3_users,
                                         'Name': user_s3_key,
                                         }
                                         },
                                         ExternalImageId=user
                                         )
        print response
    

def search_face_by_image():
    rk_client = boto3.client('rekognition', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key,region_name=aws_region)
    captured_events = _get_s3_images_for_captured_events("all")
    for item in captured_events.keys():
        print item
        try:
            response = rk_client.search_faces_by_image(
                                                        CollectionId='faces',
                                                        Image={
                                                        'S3Object': {
                                                        'Bucket': s3_location,
                                                        'Name': item,
                                                        }
                                                        },
                                                        MaxFaces=123
                                                        )
            print response
        except Exception:
            print "no face in image"


def main():
    #aws:rekognition:us-west-2:329862102863:collection/faces    2.0    200
    #get_image()
    #parse_image()
    #index_faces()
    search_face_by_image()

main()

"""
if __name__ == '__main__':
    app.run(debug=True)
"""

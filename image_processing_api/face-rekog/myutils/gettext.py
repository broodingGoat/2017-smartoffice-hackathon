import boto
import json
import os
import boto3
import pprint

pp = pprint.PrettyPrinter(indent=4)
# our boto3 rekognition client
AWS_ACCESS_KEY_ID="AKIAIZG5ENLFC4ZQSTMQ"
AWS_SECRET_ACCESS_KEY="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"

conn = boto.connect_s3(AWS_ACCESS_KEY_ID,
                AWS_SECRET_ACCESS_KEY)
rekognition_client=boto3.client('rekognition')

bucket_name="poc-myparkinglot"
bucket = conn.get_bucket(bucket_name)

def find_text(key,bucket,plate):
     rekognition_client=boto3.client('rekognition')
     response =  rekognition_client.detect_text(
       Image={
        'S3Object': {
            'Bucket': bucket,
            'Name': key,
        }
    }
   )

     data = response['TextDetections']
     #pp.pprint(data)
     for items in data:
        print " items are " , items
        v = items['DetectedText']
        v.replace(' ','')
        print " found :: " , v 
        if v == plate:
           print " I got you MR X ! Game Over"
           return key

def find_label(key,bucket):
    rekognition_client=boto3.client('rekognition')
    response =  rekognition_client.detect_labels(
       Image={
        'S3Object': {
            'Bucket': bucket,
            'Name': key,
        }
     }
    )
    labeldata = response['Labels']
    pp.pprint(labeldata)
    for items in labeldata:
        data = " Sorry no parking slot for you"
        if items['Name'] == "Car" and items['Confidence'] < 75:
           data =  " i got a parking spot for you come on in "
           print "here"
           return data
           #else:
           #data = "sorry no parking slot for you"
    return  data

def find_s3_items():
   for items in bucket:
       key = str(items.key)
       if not key.endswith('/'):
          print key

def find_my_slot(slotname):
   #find_text('234.jpg', bucket_name)
   data = find_label('latest.jpg', bucket_name)
   return data
def find_my_plate(plate):
    print " in my slot"
    found = find_text('123.jpg', bucket_name , plate)
    return found 
#data = find_my_slot('apple')
#pick = find_my_plate('HSD 4671')

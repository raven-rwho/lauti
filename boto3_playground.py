import boto3
import os
import keyboard
import datetime

client = boto3.client('s3')
S3BUCKET = 'raspi-lauti-files'

def remote_time(button):
    files = client.list_objects_v2(Bucket=S3BUCKET, Prefix=button)
    first_element = files['Contents'][0]
    return (first_element['LastModified'].date(), first_element['Key'])

def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file

def local_time(button):
    # in methode auslagern
    fpath = os.getcwd() + '/' + button
    for file in files(fpath):
        filepath = fpath + '/' + file
    mod_timestamp = datetime.datetime.fromtimestamp(os.path.getmtime(filepath)).date()
    return (mod_timestamp, filepath)

def download_if_newer(button):
    try:
        local, filepath = local_time(button)
        remote, key = remote_time(button)
        if remote < local:
            new_filepath = button + '/' + key
            client.download_file(S3BUCKET, key, new_filepath)
            os.remove(filepath)
            return new_filepath
        else:
            return filepath
    except:
        print('An error occured')

while True: 
    if keyboard.is_pressed('1'):
        download_if_newer('1')
    if keyboard.is_pressed('2'):
        download_if_newer('2')

import os
import re
import subprocess
from datetime import datetime
from time import sleep
from django.conf import settings
import random


from celery import shared_task
from django.shortcuts import render
from upload.forms import SearchWordForm, UploadFileForm
from upload.models import Subtitles, Video 
import boto3


dynamodb = boto3.resource(
    'dynamodb',
    region_name=settings.AWS_REGION,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    )
table_name = 'Sub'  
table = dynamodb.Table(table_name)


def upload_display_video(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            url = 'https://videosubs.s3.us-east-2.amazonaws.com/media'
            obj = handle_uploaded_file(file)
            id=generate_subtitles(obj)
            print(id)

            # print(path)
            
            return render(request, "upload/index.html", {'filename': file.name, 'url':url,'id':id})
        


    else:
        form = UploadFileForm()
    return render(request, 'upload/index.html', {'form': form})

@shared_task
def handle_uploaded_file(f):
    # saving to model(s3)
    obj = Video(name=f.name, video=f)
    obj.save()
    print("file upploaded to s3")

    return obj

@shared_task
def generate_subtitles(file):
        sleep(20)
        with open(file.name, 'wb+') as f:
            for chunk in file.video.chunks():
                f.write(chunk)

        abs_path = os.path.abspath(file.name)
        try:
            subprocess.run(["upload/script.sh",abs_path],check=True)
            with open(file.name.replace('.mp4','.srt'),'r') as s:
                subs = s.read()
            id = insert_file_to_dynamodb(file,subs)

            return id
        except subprocess.CalledProcessError as e:
        # Handle any errors that occur during script execution
            print(f"Error: {e}")
        

def insert_file_to_dynamodb(vid, file):
    id = str(random.random())
    item = {
        'id':id,
        'video_name': vid.name,
        'subtitle_text': str(file),
    }
    response = table.put_item(Item=item)
    # saving to local db, is not used
    subtitle = Subtitles(video=vid, subtitle=file)
    subtitle.save()
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        return id
    else:
        return False

# without dynamodb 
# def search_subs(request,filename):
#     form = SearchWordForm(request.POST)
#     url = 'https://videosubs.s3.us-east-2.amazonaws.com/media'

#     if request.method == 'POST':
#         if form.is_valid():
#             keyword = form.cleaned_data['keyword']
#             # print(keyword)
#             if keyword:
#                 keyword = keyword.upper()
#                 vid = Video.objects.filter(name = filename)
#                 sub = Subtitles.objects.get(video = vid[0].id)
#                 # print(str(sub.subtitle))

#                 file = str(sub.subtitle)


#                 timestamps = file.split("\n\n")
#                 # print(timestamps)
#                 for timestamp in timestamps:
#                     # print(timestamp)
#                     if timestamp.find(keyword) != -1:
#                         # print(timestamp.find(keyword))
#                         pattern = r"(\d{2}:\d{2}:\d{2},\d{3}).*?"
#                         match = re.search(pattern, timestamp, re.IGNORECASE)
#                         if match:
#                             result = match.group(1)
#                             break

#                 # print(result)


#         return render(request, "upload/index.html", {'filename': filename, 'url':url,'timestamp':return_seconds(result)})

# with dynamodb
def search_subs(request,id):
    form = SearchWordForm(request.POST)
    url = 'https://videosubs.s3.us-east-2.amazonaws.com/media'

    if request.method == 'POST':
        if form.is_valid():
            keyword = form.cleaned_data['keyword']
            # print(id)
            if keyword:
                keyword = keyword.upper()
                # fetching data from dynamodb
                result = table.get_item(
                    Key={
                        'id': id
                    }
                )

                filename = str(result["Item"]["video_name"])
                sub = result["Item"]["subtitle_text"]

                file = str(sub)
                print(file)

                timestamps = file.split("\n\n")
                for timestamp in timestamps:
                    if timestamp.find(keyword) != -1:
                        pattern = r"(\d{2}:\d{2}:\d{2},\d{3}).*?"
                        match = re.search(pattern, timestamp, re.IGNORECASE)
                        if match:
                            result = match.group(1)
                            break

                # print(result)

        return render(request, "upload/index.html", {'filename': filename, 'url':url,'timestamp':return_seconds(result),'id':id})

# for converting timestamps to seconds string
def return_seconds(timestamp):
    time_format = "%H:%M:%S,%f"
    duration = datetime.strptime(timestamp, time_format) - datetime.strptime("00:00:00,000", time_format)
    seconds = duration.total_seconds()
    return str(int(seconds))
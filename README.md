# Render-VideoSubs

This project aims to create a website where users can upload videos, which will be processed in the background, and then allow searching within the videos using subtitles as keywords. The application will extract subtitles from the uploaded videos, store the videos in Amazon S3, and store the subtitles in Amazon DynamoDB for efficient searching.


## Functionality
- User can upload video(s) to the website.
- Videos will be processed in the background to extract subtitles using the ccextractor.
- Processed videos will be stored in Amazon S3 for efficient and secure storage.
- Subtitle's text will be stored in Amazon DynamoDB for quick searching.
- Users can search for keywords or phrases within the subtitles of the uploaded videos.
- Search results will provide the time segments within the video where the keywords or phrases appear in the subtitles.

## Requirements
- Python 3.x
- Django
- Celery
- Amazon S3
- Amazon DynamoDB
- ccextractor binary
- 
## Run Locally

- Fork the repo `https://github.com/mathuranish/Render-VideoSubs` 
- Clone the repo and type the following command in terminal
    `git clone git@github.com:mathuranish/Render-VideoSubs.git`
- Create a virtual environment using the python command
    `python3 -m venv env`
- Install the dependencies
    `pip install -r requirements.txt`
- After the dependencies are install run the migration using command
    `python3 manage.py makemigrations && python3 manage.py migrate`
- Set up AWS credentials and configure your S3 bucket and DynamoDB table.
  -Create an AWS account if you don't have one.
  -Obtain your AWS access key ID and secret access key.
  -Set up an S3 bucket to store the videos.
  -Set up a DynamoDB table to store the subtitles.
  -Update the AWS credentials, S3 bucket name, and DynamoDB table name in settings.py.
- Start the server through the following command
    `python3 manage.py runserver` -> To run Django Server.

## Usage
- Upload a video file through the website.
- The uploaded video will be processed in the background to extract subtitles.
- Processed videos will be stored in Amazon S3.
- Extracted subtitles will be stored in Amazon DynamoDB.
- Use the search functionality on the website to search for keywords or phrases within the subtitles.
- Search results will display the time segments in the video where the keywords or phrases are mentioned in the subtitles.

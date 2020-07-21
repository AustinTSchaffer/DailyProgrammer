# GDELT Data Pipeline

This repository contains a Python pipeline that pulls GDELT data from a publicly
available stream, maps the data down to a subset of the data's features, then
pushes the data to another service.

- https://blog.gdeltproject.org/gdelt-2-0-our-global-world-in-realtime/
- https://registry.opendata.aws/gdelt/
- http://data.gdeltproject.org/documentation/GDELT-Event_Codebook-V2.0.pdf

The purpose of this application was to create a sample application that had a Flask component and a database component, while also running a 

## Application Flow 

On startup, the application sets up the routes for a Flask app, then uses
APScheduler to schedule the data fetch process. The data fetch and upload
process does not run right away, so that it does not block the startup of the
Flask app.

This application flow has a few tradeoffs and could definitely benefit from
using more async and await functionality. It's possible that a dump of GDELT
data will overwhelm the system, causing it to miss the next dump of GDELT data.

### Flask App

The Flask component of this application has 4 GET endpoints and 0 POST
endpoints.

- `/`: This endpoint serves a raw HTML file which has links to the other
  endpoints and information about the author (Austin Schaffer), including GitHub
  and LinkedIn. This endpoint also serves to show that the application is
  running, and allows users to navigate.
- `/data`: This endpoint shows the data that the application stored in the
  `data` table of its MySQL database. The intent of this endpoint is to show
  all of the data that the application has processed.
- `/files`: This endpoint shows the CSV files that the application downloaded
  and processed along with a boolean flag which shows whether the application
  was able to successfully process the file.
- `/readme`: This endpoint shows a plain HTML version of this README, which was
  created using `pandoc` and modified only slightly (to remove image links that
  I couldn't get working).

### Data Process

The process that pulls data zipped CSV data and uploads the mapped records to
the recipient runs on a timer, 5 mintues by default. This process:

1. Pulls down the latest file from
   http://data.gdeltproject.org/gdeltv2/lastupdate.txt and checks the md5 hash
   of the `export.csv.zip` file to make sure that the file has not yet been
   processed by the app. If the database already contains the hash, then thes
   process exits early.
2. Creates a record in the `processed_files` table of the database for the file,
   to protect against race conditions and to prevent the file from being
   uploaded twice.
3. Downloads the `export.csv.zip` to a temporary file.
4. Creates a stream from the zip file so that it can process each row of the CSV
   one at a time without loading the entire file into memory and without
   extracting the entire CSV into the file system.
5. For each record in the CSV, uploads a subset of the record's fields to the
   recipient, catches the response, then saves both into the `data` table of the
   database. This is the component of the application that would greatly benefit
   from using `asyncio` functionality.
6. Deletes the temporary file, then updates the `processed_files` table to
   reflect that the file was processed successfully.

## Listening for New Data

Getting this component of the application working was my biggest decision point,
so I'd like to take the opportunity to expand on it a little bit.

### Using the "Simple Notification Service" (SNS)

The [AWS Open Data Registry page for GDELT](https://registry.opendata.aws/gdelt/)
mentions a "Simple Notification Service" (SNS) that posts updates that were made
to the S3 bucket that contains the GDELT data. I am unfamiliar with SNS feeds,
and most of AWS in general, but I presume that using the SNS would be the best
way to make sure that the app only streams the latest data from the GDELT S3
bucket. I initially attempted to subscribe to the provided SNS, but it appears
that you need to be given explicit permission to subscribe to the SNS. It is not
clear who you need to contact in order to request access.

```python
import boto3
sns = boto3.resource("sns")
topic = sns.Topic("arn:aws:sns:us-east-1:928094251383:gdelt-csv")
topic.subscribe(Protocol="application")
# botocore.errorfactory.AuthorizationErrorException:
# An error occurred (AuthorizationError) when calling the Subscribe operation:
# User: arn:aws:iam::867209682223:user/austin
# is not authorized to perform: SNS:Subscribe
# on resource: arn:aws:sns:us-east-1:928094251383:gdelt-csv
```

Just to be sure that the issue was not related to my limited understanding of
AWS's boto3 library, I tried to subscribe my email address to the SNS using the
web interface. That route also failed.

For a production application, I would prefer to get the SNS working.

### Using a Web Resource that has a GET Endpoint

I managed to find
[http://data.gdeltproject.org/gdeltv2/lastupdate.txt](http://data.gdeltproject.org/gdeltv2/lastupdate.txt),
which returns a plaintext resource that contains 3 lines of data:

```
<file size in bytes> <MD5 hash> <base url>/<timestamp>.export.CSV.zip
<file size in bytes> <MD5 hash> <base url>/<timestamp>.mentions.CSV.zip
<file size in bytes> <MD5 hash> <base url>/<timestamp>.gkg.csv.zip
```

I was unable to find any documentation on the format of this file, but the order
of the 3 ZIP files seems constant, the arrangement of the 3 columns seems
constant, and the resource refreshes every 15 minutes.

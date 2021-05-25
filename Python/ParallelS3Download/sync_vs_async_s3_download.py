#%% Init

import boto3
import time   

# Bucket/Prefix constants, bring your own
BUCKET_NAME = "austin-schaffer"
DATA_PREFIX = "egress-test/"

# Creates a test CSV with a single column, and 500 rows of "content"
TEST_DATA = b"column_name\n" + (b"test data please ignore just some bytes totalling a few KB\n" * 500)

# synchronous AWS S3 clients/resources
s3 = boto3.client("s3")
s3_resource = boto3.resource("s3")

#%% Load Data

print("Loading data into S3...")
print("You can comment out the `s3.put_object` call after the first run.")

keys = []
for i in range(101):
    key = f"{DATA_PREFIX}test_data.{i}.csv"
    keys.append(key)
    # s3.put_object(Body=TEST_DATA, Bucket=BUCKET_NAME, Key=key)

#%% Synchronous Download (Prefix)

import io

time.sleep(2)
print("Initiating synchronous S3 object download (by prefix) in 2 seconds...")
time.sleep(2)

data = {}
bucket = s3_resource.Bucket(BUCKET_NAME)
for obj_handle in bucket.objects.filter(Prefix=DATA_PREFIX):
    print("Downloading:", obj_handle.key)
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=obj_handle.key)
    data[obj_handle.key] = obj["Body"].read()

print("Objects Downloaded (synchronous prefix method):", len(data))

#%% Synchronous Download (Keys)

import io
import time

time.sleep(2)
print("Initiating synchronous S3 object download (list of keys) in 2 seconds...")
time.sleep(2)

data = {}
bucket = s3_resource.Bucket(BUCKET_NAME)
for key in keys:
    print("Downloading:", key)
    obj = s3.get_object(Bucket=BUCKET_NAME, Key=key)
    data[key] = obj["Body"].read()

print("Objects Downloaded (synchronous keys method):", len(data))

#%% Async Method (Prefix)

import aiobotocore
import asyncio

time.sleep(2)
print("Initiating async S3 object download (by prefix) in 2 seconds...")
time.sleep(2)

async def get_objects_by_prefix(bucket, prefix):
    data = {}
    session = aiobotocore.get_session()
    async with session.create_client('s3') as s3_client:
        async def _get_object(key):
            if isinstance(key, dict):
                key = key["Key"]
            return (key, await s3_client.get_object(Bucket=bucket, Key=key))

        paginator = s3_client.get_paginator('list_objects')
        async for result in paginator.paginate(Bucket=bucket, Prefix=prefix):
            contents = result.get('Contents', [])
            for future in asyncio.as_completed(map(_get_object, contents)):
                key, s3_object = await future
                print("Downloaded:", key)
                data[key] = await s3_object["Body"].read()

    return data

data = asyncio.run(get_objects_by_prefix(BUCKET_NAME, DATA_PREFIX))
print("Objects Downloaded (async prefix method):", len(data))

#%% Async Method (Keys)

time.sleep(2)
print("Initiating async S3 object download (list of keys) in 2 seconds...")
time.sleep(2)

async def get_objects(bucket, keys):
    data = {}
    session = aiobotocore.get_session()
    async with session.create_client('s3') as s3_client:

        async def _get_object(key):
            if isinstance(key, dict):
                key = key["Key"]
            return (key, await s3_client.get_object(Bucket=bucket, Key=key))

        for future in asyncio.as_completed(map(_get_object, keys)):
            key, s3_object = await future
            print("Downloaded:", key)
            data[key] = await s3_object["Body"].read()

    return data

data = asyncio.run(get_objects(BUCKET_NAME, keys))
print("Objects Downloaded (async keys method):", len(data))

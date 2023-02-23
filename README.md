# Byte Stream Uploader for S3
This command line utility uploads a byte stream received via the standard input to an object in an S3 bucket.

## Requirements

* Python 3
* Boto3 library (can be installed with pip install boto3)

## Usage

`cat largefile | python uploader.py --endpoint ENDPOINT_URL --access-key ACCESS_KEY --secret-key SECRET_KEY --bucket BUCKET_NAME --object OBJECT_KEY
`

ex: 
`cat largefile | python uploader.py  --endpoint http://127.0.0.1:9000/ --access-key minioadmin  --secret-key minioadmin  --bucket testbucket  --object obj-1
`

The utility takes the following command line arguments:

* --endpoint: the URL of the S3 endpoint to use (required)
* --access-key: the access key for the S3 account (required)
* --secret-key: the secret key for the S3 account (required)
* --bucket: the name of the S3 bucket to upload the byte stream to (required)
* --object: the key of the S3 object to create (required)


The size of the byte stream is unknown to the utility, and it considers the stream done when a read syscall on the standard input returns EOF.


## Testing

You can test the utility by deploying a MinIO locally. MinIO is a high-performance, distributed object storage system that is API-compatible with Amazon S3. To deploy MinIO:

Download the MinIO server from the official website: https://min.io/download.

Create largefile:
`dd if=/dev/zero of=largefile bs=1M count=1000
`
![Screenshot from 2023-02-23 12-28-55.png](..%2F..%2F..%2FPictures%2FScreenshots%2FScreenshot%20from%202023-02-23%2012-28-55.png)
Upload using following cli, also calculate md5sum
![Screenshot from 2023-02-23 12-30-44.png](..%2F..%2F..%2FPictures%2FScreenshots%2FScreenshot%20from%202023-02-23%2012-30-44.png)

Once upload is finished, check the object in the bucket from minio console
![Screenshot from 2023-02-23 12-33-43.png](..%2F..%2F..%2FPictures%2FScreenshots%2FScreenshot%20from%202023-02-23%2012-33-43.png)

Verify the md5sum of uploaded file by downloading it or checking md5sum in object info tab 
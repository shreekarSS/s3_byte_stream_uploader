import boto3
import argparse
import sys
import hashlib
import io


def s3_byte_stream_uploader(endpoint_url, access_key, secret_key, bucket_name, object_key):
    # Create an S3 client
    try:
        s3 = boto3.client('s3', endpoint_url=endpoint_url, aws_access_key_id=access_key,
                          aws_secret_access_key=secret_key)
    except Exception as e:
        print(f"Error: {e}")
        return

    # Read the input stream into an in-memory buffer and calculate the MD5 hash
    buffer = io.BytesIO()
    md5_hash = hashlib.md5()
    while True:
        try:
            data = sys.stdin.buffer.read()
        except KeyboardInterrupt:
            print("Upload interrupted by user")
            return
        if not data:
            break
        buffer.write(data)
        md5_hash.update(data)

    # Reset the buffer to its beginning
    buffer.seek(0)
    # Upload the buffer to S3 with the MD5 hash as a custom metadata field
    try:
        s3.upload_fileobj(buffer, bucket_name, object_key, ExtraArgs={'Metadata': {'md5': md5_hash.hexdigest()}})
        print("Upload complete")
    except Exception as e:
        print(f"Error: {e}")
        return


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload a byte stream to S3')
    parser.add_argument('--endpoint', required=True, help='S3 endpoint URL')
    parser.add_argument('--access-key', required=True, help='S3 access key')
    parser.add_argument('--secret-key', required=True, help='S3 secret key')
    parser.add_argument('--bucket', required=True, help='S3 bucket name')
    parser.add_argument('--object', required=True, help='S3 object key')
    args = parser.parse_args()

    s3_byte_stream_uploader(args.endpoint, args.access_key, args.secret_key, args.bucket, args.object)

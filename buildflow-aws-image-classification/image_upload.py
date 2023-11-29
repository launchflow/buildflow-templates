import argparse
import os
from pprint import pprint
import sys
import time

from buildflow.io.snowflake import read_private_key_file_bytes
import dotenv
import s3fs
import snowflake.connector


dotenv.load_dotenv()


SNOWFLAKE_ACCOUNT = os.environ["SNOWFLAKE_ACCOUNT"]
SNOWFLAKE_USER = os.environ["SNOWFLAKE_USER"]
SNOWFLAKE_PRIVATE_KEY_FILE = os.environ["SNOWFLAKE_PRIVATE_KEY_FILE"]


def upload(args):
    parser = argparse.ArgumentParser()

    parser.add_argument("--image", help="image to upload", default="founders_dog.jpg")
    parser.add_argument("--bucket", help="bucket to upload to", required=True)
    parser.add_argument(
        "--database", help="name of database to query", default="buildflow-walkthrough"
    )
    parser.add_argument(
        "--table", help="name of table to query", default="image_classification"
    )
    parser.add_argument(
        "--schema",
        help="name of schema to query",
        default="buildflow-schema",
    )
    parsed = parser.parse_args(args)

    print("uploading image to bucket")
    s3 = s3fs.S3FileSystem()
    s3.put(parsed.image, f"s3://{parsed.bucket}/{parsed.image}")

    print("waiting for 90 seconds for image to be processed")
    print("...we only push to snowflake once per minute to reduce costs...")
    time.sleep(90)

    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        account=SNOWFLAKE_ACCOUNT,
        private_key=read_private_key_file_bytes(SNOWFLAKE_PRIVATE_KEY_FILE),
    )
    cur = conn.cursor()
    query = cur.execute(
        f'SELECT * FROM "{parsed.database}"."{parsed.schema}"."{parsed.table}"'
    )
    print("results")
    print("-------")
    pprint(query.fetchall())


if __name__ == "__main__":
    upload(sys.argv[1:])

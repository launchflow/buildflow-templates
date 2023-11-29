import argparse
import os
from pprint import pprint
import shutil
import sys
import time

import duckdb


def upload(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--image", help="image to upload", default="founders_dog.jpg")
    parser.add_argument(
        "--image-folder", help="bucket to upload to", default="image_folder"
    )
    parser.add_argument(
        "--duckdb-database",
        help="duckdb database to connect to",
        default="buildflow.duckdb",
    )
    parser.add_argument(
        "--duckdb-table",
        help="duckdb table to read from",
        default="image_classification",
    )
    parsed = parser.parse_args(args)

    print("copying file to watch dir")
    shutil.copy(parsed.image, parsed.image_folder)
    print("waiting for 5 seconds for image to be processed")
    time.sleep(5)

    try:
        with duckdb.connect(parsed.duckdb_database) as conn:
            conn.execute(f"SELECT * FROM {parsed.duckdb_table}")
            print("results")
            print("-------")
            pprint(conn.fetchall())

    finally:
        # remove the file so we can run this again
        os.remove(os.path.join(parsed.image_folder, parsed.image))


if __name__ == "__main__":
    upload(sys.argv[1:])

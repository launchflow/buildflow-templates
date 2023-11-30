from buildflow.io.local import LocalFileChangeStream
from buildflow.io.duckdb import DuckDBTable


file_stream = LocalFileChangeStream(file_path="image_folder")
table = DuckDBTable(database="buildflow.duckdb", table="image_classification")

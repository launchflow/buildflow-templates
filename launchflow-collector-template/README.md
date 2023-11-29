# launchflow-collector-template

Welcome to BuildFlow!

This is a simple example of [collector](https://docs.buildflow.dev/programming-guide/collector) that takes in an HTTP request containing and integer and writes a JSON object containing the integer divided by 2 to a sink.

Collectors are useful for simple data ingestion tasks such as writing data to a data warehouse or queue.

## Running the Template

To get started you will first need to define a [primitive](https://docs.buildflow.dev/programming-guide/primitives) sink in [primitives.py](launchflow_collector_template/primitives.py). Some examples could be:

**Sinks**
- [GCP Pub/Sub Subscription](https://docs.buildflow.dev/primitives/gcp/pubsub#gcp-pub-sub-subscription)
- [GCS File Change Stream](https://docs.buildflow.dev/primitives/gcp/gcs_file_change_stream)
- [AWS SQS](https://docs.buildflow.dev/primitives/aws/sqs)
- [S3 File Change Stream](https://docs.buildflow.dev/primitives/gcp/gcs_file_change_stream)

For a full list of primitives see: https://docs.buildflow.dev/primitives

### Create Infrastructure

Once you've defined your primitives you can run:

```
buildflow apply
```

To create the sink.

### Run the Collector

Now simply run:
```
buildflow run
```

Once running you can visit http://localhost:8000/docs to send a request to your collector. Below is an example payload:

```json
{
    "int_field": 2
}
```

And that should output the following in your sink:

```json
{
    "float_field": 1.0
}
```

## Directory Structure

At the root level there are three important files:

- `buildflow.yml` - This is the main configuration file for your project. It contains all the information about your project and how it should be built.
- `main.py` - This is the entry point to your project and where your `Flow` is initialized.
- `requirements.txt` - This is where you can specify any Python dependencies your project has.

Below the root level we have:

**launchflow_collector_template**

This is the directory where your project code lives. You can put any files you want in here and they will be available to your project. We create a couple directories and files for you:

- **processors**: This is where you can put any custom processors you want to use in your project. In here you will see we have defined a *collector.py* to define our [collector](https://docs.buildflow.dev/programming-guide/collectors).
- **primitives.py**: This is where you can define any custom [primitive](https://docs.buildflow.dev/primitives) resources that your project will need. Note it is empty right now since your initial project is so simple.
- **dependencies.py**: This is where you can define any custom [dependencies](https://docs.buildflow.dev/programming-guide/dependencies) you might need.
- **schemas.py**: This file contains our dataclass schemas for requests and responses from our endpoints.
- **settings.py**: This file loads in our environment variables and makes them available to our project.

**.buildflow**

This is a hidden directory that contains all the build artifacts for your project. You can general ignore this directory and it will be automatically generated for you. If you are using github you probably want to put this in your *.gitignore* file.


## Customizing your project

You project is pretty simple now but you can customize it to do anything you want. Here are some ideas:

- Attach [primitives](https://docs.buildflow.dev/programming-guide/primitives) to your project to add resources like [databases](https://docs.buildflow.dev/primitives/gcp/cloud_sql), [queues](https://docs.buildflow.dev/primitives/aws/sqs), [buckets](https://docs.buildflow.dev/primitives/aws/s3), or [data warehouses](https://docs.buildflow.dev/primitives/gcp/bigquery)
- Use [depedencies](https://docs.buildflow.dev/programming-guide/dependencies) to attach dependencies to your processors. Such as [google auth](https://docs.buildflow.dev/dependencies/auth#authenticated-google-user), [SQLAlchemy Session](https://docs.buildflow.dev/dependencies/sqlalchemy), or push data to a [sink](https://docs.buildflow.dev/dependencies/sink)
- Add additional processors for [serving APIs](https://docs.buildflow.dev/programming-guide/endpoints) or [async processing](https://docs.buildflow.dev/programming-guide/consumers)
- Manage your entire stack with [BuildFlow's pulumi integration](https://docs.buildflow.dev/programming-guide/buildflow-yaml#pulumi-configure)


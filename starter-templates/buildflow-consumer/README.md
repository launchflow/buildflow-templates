# launchflow-consumer-template

Welcome to BuildFlow!

This is a simple example of [consumer](https://docs.launchflow.com/buildflow/programming-guide/consumers) that takes in a JSON object containing and integer and returns a JSON object containing the integer divided by 2.

## Running the Template

To get started you will first need to define a [primitive](https://docs.launchflow.com/buildflow/programming-guide/primitives) source and a sink in [primitives.py](buildflow_consumer/primitives.py). Some examples could be:

**Sinks**

- [GCP Pub/Sub Subscription](https://docs.launchflow.com/buildflow/primitives/gcp/pubsub#gcp-pub-sub-subscription)
- [GCS File Change Stream](https://docs.launchflow.com/buildflow/primitives/gcp/gcs_file_change_stream)
- [AWS SQS](https://docs.launchflow.com/buildflow/primitives/aws/sqs)
- [S3 File Change Stream](https://docs.launchflow.com/buildflow/primitives/gcp/gcs_file_change_stream)

**Sources**

- [GCP BigQuery Table](https://docs.launchflow.com/buildflow/primitives/gcp/bigquery#bigquerytable)
- [GCP Pub/Sub Topic](https://docs.launchflow.com/buildflow/primitives/gcp/pubsub#gcp-pub-sub-topic)
- [AWS SQS](https://docs.launchflow.com/buildflow/primitives/aws/sqs)
- [DuckDB Table](https://docs.launchflow.com/buildflow/primitives/duckdb)

For a full list of primitives see: https://docs.launchflow.com/buildflow/primitives

### Create Infrastructure

Once you've defined your primitives you can run:

```
buildflow apply
```

To create the source and sink.

### Run the Consumer

Now simply run:

```
buildflow run
```

Once running you can send a JSON payload to your source and see the results in your sink. Below is an example payload:

```json
{
  "int_field": 2
}
```

And that should output the following:

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

**buildflow_consumer**

This is the directory where your project code lives. You can put any files you want in here and they will be available to your project. We create a couple directories and files for you:

- **processors**: This is where you can put any custom processors you want to use in your project. In here you will see we have defined a _consumer.py_ to define our [consumer](https://docs.launchflow.com/buildflow/programming-guide/consumers).
- **primitives.py**: This is where you can define any custom [primitive](https://docs.launchflow.com/buildflow/primitives) resources that your project will need. Note it is empty right now since your initial project is so simple.
- **dependencies.py**: This is where you can define any custom [dependencies](https://docs.launchflow.com/buildflow/programming-guide/dependencies) you might need.
- **schemas.py**: This file contains our dataclass schemas for requests and responses from our endpoints.
- **settings.py**: This file loads in our environment variables and makes them available to our project.

**.buildflow**

This is a hidden directory that contains all the build artifacts for your project. You can general ignore this directory and it will be automatically generated for you. If you are using github you probably want to put this in your _.gitignore_ file.

## Customizing your project

You project is pretty simple now but you can customize it to do anything you want. Here are some ideas:

- Attach [primitives](https://docs.launchflow.com/buildflow/programming-guide/primitives) to your project to add resources like [databases](https://docs.launchflow.com/buildflow/primitives/gcp/cloud_sql), [queues](https://docs.launchflow.com/buildflow/primitives/aws/sqs), [buckets](https://docs.launchflow.com/buildflow/primitives/aws/s3), or [data warehouses](https://docs.launchflow.com/buildflow/primitives/gcp/bigquery)
- Use [depedencies](https://docs.launchflow.com/buildflow/programming-guide/dependencies) to attach dependencies to your processors. Such as [google auth](https://docs.launchflow.com/buildflow/dependencies/auth#authenticated-google-user), [SQLAlchemy Session](https://docs.launchflow.com/buildflow/dependencies/sqlalchemy), or push data to a [sink](https://docs.launchflow.com/buildflow/dependencies/sink)
- Add additional processors for [serving APIs](https://docs.launchflow.com/buildflow/programming-guide/endpoints) or [data ingestion](https://docs.launchflow.com/buildflow/programming-guide/collectors)
- Manage your entire stack with [BuildFlow's pulumi integration](https://docs.launchflow.com/buildflow/programming-guide/buildflow-yaml#pulumi-configure)

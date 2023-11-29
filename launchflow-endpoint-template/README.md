# launchflow-endpoint-template

Welcome to BuildFlow!

This is a simple example of serving the string "Hello World!" from an [endpoint](https://docs.buildflow.dev/programming-guide/endpoints)

If you want to just get started quickly you can run start your project with:

```
buildflow run
```

Then you can visit http://localhost:8000 to see your project running.

## Directory Structure

At the root level there are three important files:

- `buildflow.yml` - This is the main configuration file for your project. It contains all the information about your project and how it should be built.
- `main.py` - This is the entry point to your project and where your `Flow` is initialized.
- `requirements.txt` - This is where you can specify any Python dependencies your project has.

Below the root level we have:

**launchflow_endpoint_template**

This is the directory where your project code lives. You can put any files you want in here and they will be available to your project. We create a couple directories and files for you:

- **processors**: This is where you can put any custom processors you want to use in your project. In here you will see we have defined a *service.py* for a service in your project and a *hello_world.py* file for a custom [endpoint](https://docs.buildflow.dev/programming-guide/endpoints) processor.
- **primitives.py**: This is where you can define any custom [primitive](https://docs.buildflow.dev/primitives) resources that your project will need. Note it is empty right now since your initial project is so simple.
- **dependencies.py**: This is where you can define any custom [dependencies](https://docs.buildflow.dev/programming-guide/dependencies) you might need.
- **settings.py**: This file loads in our environment variables and makes them available to our project.

**.buildflow**

This is a hidden directory that contains all the build artifacts for your project. You can general ignore this directory and it will be automatically generated for you. If you are using github you probably want to put this in your *.gitignore* file.


## Customizing your project

You project is pretty simple now but you can customize it to do anything you want. Here are some ideas:

- Attach [primitives](https://docs.buildflow.dev/programming-guide/primitives) to your project to add resources like [databases](https://docs.buildflow.dev/primitives/gcp/cloud_sql), [queues](https://docs.buildflow.dev/primitives/aws/sqs), [buckets](https://docs.buildflow.dev/primitives/aws/s3), or [data warehouses](https://docs.buildflow.dev/primitives/gcp/bigquery)
- Use [depedencies](https://docs.buildflow.dev/programming-guide/dependencies) to attach dependencies to your processors. Such as [google auth](https://docs.buildflow.dev/dependencies/auth#authenticated-google-user), [SQLAlchemy Session](https://docs.buildflow.dev/dependencies/sqlalchemy), or push data to a [sink](https://docs.buildflow.dev/dependencies/sink)
- Add additional processors for [async processing](https://docs.buildflow.dev/programming-guide/consumers) or [data ingestion](https://docs.buildflow.dev/programming-guide/collectors)
- Manage your entire stack with [BuildFlow's pulumi integration](https://docs.buildflow.dev/programming-guide/buildflow-yaml#pulumi-configure)


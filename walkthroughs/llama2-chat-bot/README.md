# launchflow-model-serving

Welcome to BuildFlow!

In this example we'll show you how to load in a model from a GCS or S3 bucket and serve it using a custom endpoint. We've prepopulated the repo with a chatbot using Llama2 and use the [llama-cpp](https://github.com/ggerganov/llama.cpp) interface for calling it, so you want to just see it in action without changing anything run:

NOTE: It may take the model a couple minutes to download on your first iteration.

```
pip install -r requirements.txt
buildflow run
```

Then you can visit http://localhost:8000 to test it out!

## Directory Structure

At the root level there are three important files:

- `buildflow.yml` - This is the main configuration file for your project. It contains all the information about your project and how it should be built.
- `main.py` - This is the entry point to your project and where your `Flow` is initialized.
- `requirements.txt` - This is where you can specify any Python dependencies your project has.

Below the root level we have:

**launchflow_model_serving**

This is the directory where your project code lives. You can put any files you want in here and they will be available to your project. We create a couple directories and files for you:

- **processors**: This is where we define out custom processors. We have one, `service.py` with two endpoints. One for serving our HTML page, and one for serving our model.
- **primitives.py**: This is where we define a primitive to reference a GCS bucket.
- **dependencies.py**: Here we define a dependency that loads in our model from the GCS bucket. This dependency is shared across multiple requests so we don't have to reload the model every time.
- **schemas.py**: This file contains our dataclass schemas for requests and responses from our endpoints.
- **settings.py**: This file loads in our environment variables and makes them available to our project.

**.buildflow**

This is a hidden directory that contains all the build artifacts for your project. You can general ignore this directory and it will be automatically generated for you. If you are using github you probably want to put this in your *.gitignore* file.

## Customize your project

### Loading from S3

By default we load the model from GCS, but you can switch that by updating setting `USE_GCP=false` in the `.env` file.

### Loading a custom model

To load in a custom model you will need to update a couple files:

- `.env`: update this file to point to your bucket
- `flow.py`: mark your bucket as managed by uncommenting this line `app.manage(model_bucket)`
- `dependencies.py`: update the `__init__` function of `ModelDep` to load in your model
- `service.py`: Update your endpoints with your custom business logic

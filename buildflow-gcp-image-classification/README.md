# Walkthrough of using BuildFlow with GCS File Events 

This walk through shows how you can use BuildFlow to upload images to a GCS bucket. once uploaded run them through an image classification model and store the results in BigQuery.

## Running locally

To get started you will need a GCP project where the GCS bucket and BigQuery resources can be created.

Copy the `template.env` to `.env` and update `GCP_PROJECT_ID` to point to your GCP project.

Next create all your resources with:

```
buildflow apply
```

Confirm the output by typing: yes

Now you can run the local server with:

```
buildflow run
```

Once running navigate to https://localhost:8000 to beging upload images and view the results in BigQuery.

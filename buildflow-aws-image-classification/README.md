# Walkthrough of using BuildFlow with S3 File Events 

This walk through shows how you can use BuildFlow to upload images to a S3 bucket. once uploaded run them through an image classification model and store the results in MotherDuck.

## Running locally

Copy the `template.env` to `.env` and update `INPUT_BUCKET_NAME` to what you would like your bucket to be named, and update `MOTHERDUCK_TOKEN` to your [MotherDuck service token](https://motherduck.com/docs/authenticating-to-motherduck#authentication-using-a-service-token).

Next create all your resources with:

```
buildflow apply
```

Confirm the output by typing: yes

Now you can run the local server with:

```
buildflow run
```

Once running navigate to https://localhost:8000 to beging upload images and view the results in MotherDuck.

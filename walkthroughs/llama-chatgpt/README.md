# AI Chat built on LaunchFlow

This is a simple example of how to use LaunchFlow to build a AI chatbot using LLama2.

## Running Locally
Copy the `template.env` to `.env`, and update the following environment variables:

- `LOCAL_GCP_PROJECT_ID` this should point to GCP project that you have access to and can create resources in.
- `MODEL_BUCKET_PROJECT`: this should point to the GCP project containing the bucket that you will put your model in.
- `MODEL_BUCKET_NAME`: this should be the name of the bucket that you will put your model in.

Run: `buildflow apply main:app` or click the `Apply Infra` from the LaunchFlow VSCode extension.

NOTE: You will also need to confirm the infra changes by typing `Y`` in your terminal.

Once your infra is applied you can download and upload the model to the bucket. Our example uses the models found here: 
https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML, specifically we use: https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGML/blob/main/llama-2-7b-chat.ggmlv3.q2_K.bin

Once uploaded you can run locally with `buildflow run main:app`, or click the `Run Locally` button in the VSCode extension.

## Running on LaunchFlow

To run on LaunchFlow you will need to update the `.env` to include the following env variable:

```
GCP_SERVICE_ACCOUNT_INFO=...
```

This should be set to a JSON string of a service account key file obtained from GCP.

NOTE: This info shouldn't be checked in so keep it in the `.env` file which is ignored as part of the .gitignore.
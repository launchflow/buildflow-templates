"""Main file the setups the flow and is our entry point."""

from buildflow import Flow

from llama2_chat_bot.processors.service import service

# Uncomment this line to manage the model bucket.
# from launchflow_model_serving.primitives import model_bucket


# Define our initial flow
app = Flow()

# Uncomment this line to manage the model bucket.
# app.manage(model_bucket)

# Attach the service to the flow.
app.add_service(service)

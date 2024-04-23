# Dockerfile to build the Lambda function's container image

FROM public.ecr.aws/lambda/python:3.11

# Copy the requirements file to the container
COPY requirements.txt ${LAMBDA_TASK_ROOT}/

# Install the Python dependencies
RUN pip install -r requirements.txt

# Copy all files from the ./src directory to the container
COPY src/* ${LAMBDA_TASK_ROOT}/

# Set the ENTRYPOINT to your handler
CMD ["app.lambda_handler"]

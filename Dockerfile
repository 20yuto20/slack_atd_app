# Use the official AWS Lambda Python runtime as a parent image
FROM public.ecr.aws/lambda/python:3.9

# Copy function code and requirements file
COPY app ${LAMBDA_TASK_ROOT}/app
COPY requirements.txt .

# Install the function's dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set the CMD to your handler
CMD [ "app.main.handler" ]
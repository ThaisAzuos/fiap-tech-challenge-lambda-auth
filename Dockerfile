# Use AWS Lambda Python 3.11 base image
FROM public.ecr.aws/lambda/python:3.11

# Copy requirements and install dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

# Copy source code
COPY src/ ${LAMBDA_TASK_ROOT}

# Set the CMD to the Lambda handler
CMD ["handler.lambda_handler"]

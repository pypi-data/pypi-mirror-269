import os

from aws_lambda_powertools import Tracer

tracer = Tracer(service=os.environ.get("SERVICE_NAME"))

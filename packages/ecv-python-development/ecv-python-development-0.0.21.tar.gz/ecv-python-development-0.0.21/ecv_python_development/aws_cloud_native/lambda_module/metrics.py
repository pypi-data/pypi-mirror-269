import os

from aws_lambda_powertools import Metrics

metrics = Metrics(
    namespace=os.environ.get("PROJECT_NAME"),
    service=os.environ.get("SERVICE_NAME"),
)
metrics.set_default_dimensions(environment=os.environ.get("ENVIRONMENT"))  # type: ignore

import boto3
import time
from botocore.exceptions import ClientError

# Create EC2 client
ec2 = boto3.client("ec2", region_name="us-east-1")


def tag_ec2_instances(instance_ids, max_retries=5):
    """
    Tags EC2 instances with:
    Environment = Production
    Owner = DevOps

    Handles AWS throttling with retries.
    """

    tags = [
        {"Key": "Environment", "Value": "Production"},
        {"Key": "Owner", "Value": "DevOps"}
    ]

    for attempt in range(1, max_retries + 1):

        try:
            response = ec2.create_tags(
                Resources=instance_ids,
                Tags=tags
            )

            print(f"Successfully tagged instances: {instance_ids}")
            return response

        except ClientError as e:

            error_code = e.response["Error"]["Code"]

            # Handle throttling errors
            if error_code in ["Throttling", "RequestLimitExceeded"]:

                wait_time = 2 ** attempt

                print(
                    f"Throttled by AWS. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:
                # Any other AWS error
                print(f"AWS Error: {e}")
                raise

    print("Max retries exceeded.")
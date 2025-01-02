import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def list_all_resources():
    session = boto3.session.Session()
    regions = session.get_available_regions('ec2')  # Get all available regions for EC2 as a reference
    services_to_check = [
        'ec2', 's3', 'ecs', 'ecr', 'eks', 'lambda', 'rds', 'cloudwatch', 'dynamodb', 'vpc'
    ]
    
    for region in regions:
        print(f"\n--- Resources in Region: {region} ---")
        session = boto3.session.Session(region_name=region)

        try:
            # EC2 Instances
            if 'ec2' in services_to_check:
                ec2 = session.client('ec2')
                instances = ec2.describe_instances()
                print("\nEC2 Instances:")
                for reservation in instances['Reservations']:
                    for instance in reservation['Instances']:
                        print(f"Instance ID: {instance['InstanceId']}, State: {instance['State']['Name']}")
            
            # S3 Buckets
            if 's3' in services_to_check:
                s3 = session.client('s3')
                buckets = s3.list_buckets()
                print("\nS3 Buckets:")
                for bucket in buckets['Buckets']:
                    print(f"Bucket Name: {bucket['Name']}")

            # ECS Clusters and Services
            if 'ecs' in services_to_check:
                ecs = session.client('ecs')
                clusters = ecs.list_clusters()
                print("\nECS Clusters:")
                for cluster in clusters['clusterArns']:
                    services = ecs.list_services(cluster=cluster)
                    print(f"Cluster: {cluster}")
                    for service in services['serviceArns']:
                        print(f"Service: {service}")
            
            # ECR Repositories
            if 'ecr' in services_to_check:
                ecr = session.client('ecr')
                repositories = ecr.describe_repositories()
                print("\nECR Repositories:")
                for repository in repositories['repositories']:
                    print(f"Repository Name: {repository['repositoryName']}")

            # EKS Clusters
            if 'eks' in services_to_check:
                eks = session.client('eks')
                clusters = eks.list_clusters()
                print("\nEKS Clusters:")
                for cluster in clusters['clusters']:
                    print(f"Cluster Name: {cluster}")

            # Lambda Functions
            if 'lambda' in services_to_check:
                lambda_client = session.client('lambda')
                functions = lambda_client.list_functions()
                print("\nLambda Functions:")
                for function in functions['Functions']:
                    print(f"Function Name: {function['FunctionName']}")

            # RDS Instances
            if 'rds' in services_to_check:
                rds = session.client('rds')
                dbs = rds.describe_db_instances()
                print("\nRDS Instances:")
                for db in dbs['DBInstances']:
                    print(f"DB Identifier: {db['DBInstanceIdentifier']}, Status: {db['DBInstanceStatus']}")

            # DynamoDB Tables
            if 'dynamodb' in services_to_check:
                dynamodb = session.client('dynamodb')
                tables = dynamodb.list_tables()
                print("\nDynamoDB Tables:")
                for table in tables['TableNames']:
                    print(f"Table Name: {table}")

            # VPC and Subnets
            if 'vpc' in services_to_check:
                ec2 = session.client('ec2')
                vpcs = ec2.describe_vpcs()
                print("\nVPCs:")
                for vpc in vpcs['Vpcs']:
                    print(f"VPC ID: {vpc['VpcId']}, CIDR: {vpc['CidrBlock']}")
                
                subnets = ec2.describe_subnets()
                print("\nSubnets:")
                for subnet in subnets['Subnets']:
                    print(f"Subnet ID: {subnet['SubnetId']}, CIDR: {subnet['CidrBlock']}")

            # CloudWatch Alarms (Optional)
            if 'cloudwatch' in services_to_check:
                cloudwatch = session.client('cloudwatch')
                alarms = cloudwatch.describe_alarms()
                print("\nCloudWatch Alarms:")
                for alarm in alarms['MetricAlarms']:
                    print(f"Alarm Name: {alarm['AlarmName']}, State: {alarm['StateValue']}")

        except (NoCredentialsError, PartialCredentialsError) as e:
            print(f"Credentials error: {str(e)}")
        except Exception as e:
            print(f"Error listing resources in region {region}: {str(e)}")

if __name__ == "__main__":
    list_all_resources()


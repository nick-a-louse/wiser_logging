<<<<<<< HEAD
import boto3

#------------------ Get DynamoDB Parameters from keyfile ------------------
with open("dynamo.params", "r") as f:
    data = f.read().split("\n")
aws_access_key_id = ""
aws_secret_access_key = ""
aws_region_name = ""


for lines in data:
    line = lines.split("=")
    if line[0] == "aws_access_key_id":
        aws_access_key_id = line[1]
    if line[0] == "aws_secret_access_key":
        aws_secret_access_key = line[1]
    if line[0] == "region_name":
        aws_region_name = line[1]

print(" AWS access key id = {} \n AWS secret access key = {} \n AWS region = {}".format(aws_access_key_id, aws_secret_access_key, aws_region_name))


client = boto3.client('dynamodb',aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region_name)

# boto3 is the AWS SDK library for Python.
# We can use the low-level client to make API calls to DynamoDB.

try:
    table = client.create_table(
        TableName="Wiser",
        # Declare your Primary Key in the KeySchema argument
        KeySchema=[
            {
                "AttributeName": "Date",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "Time",
                "KeyType": "RANGE"
            }
        ],
        # Any attributes used in KeySchema or Indexes must be declared in AttributeDefinitions
        AttributeDefinitions=[
            {
                "AttributeName": "Date",
                "AttributeType": "S"
            },
            {
                "AttributeName": "Time",
                "AttributeType": "S"
            }
        ],
        # ProvisionedThroughput controls the amount of data you can read or write to DynamoDB per second.
        # You can control read and write capacity independently.
        ProvisionedThroughput={
            "ReadCapacityUnits": 1,
            "WriteCapacityUnits": 1
        }
    )
    #print("Table created successfully!")

    table.meta.client.get_waiter('table_exists').wait(TableName='Wiser')
    print(table.item_count)

except Exception as e:
    print("Error creating table:")
    print(e)


=======
import boto3

#------------------ Get DynamoDB Parameters from keyfile ------------------
with open("dynamo.params", "r") as f:
    data = f.read().split("\n")
aws_access_key_id = ""
aws_secret_access_key = ""
aws_region_name = ""


for lines in data:
    line = lines.split("=")
    if line[0] == "aws_access_key_id":
        aws_access_key_id = line[1]
    if line[0] == "aws_secret_access_key":
        aws_secret_access_key = line[1]
    if line[0] == "region_name":
        aws_region_name = line[1]

print(" AWS access key id = {} \n AWS secret access key = {} \n AWS region = {}".format(aws_access_key_id, aws_secret_access_key, aws_region_name))


client = boto3.client('dynamodb',aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region_name)

# boto3 is the AWS SDK library for Python.
# We can use the low-level client to make API calls to DynamoDB.

try:
    table = client.create_table(
        TableName="Wiser",
        # Declare your Primary Key in the KeySchema argument
        KeySchema=[
            {
                "AttributeName": "Date",
                "KeyType": "HASH"
            },
            {
                "AttributeName": "Time",
                "KeyType": "RANGE"
            }
        ],
        # Any attributes used in KeySchema or Indexes must be declared in AttributeDefinitions
        AttributeDefinitions=[
            {
                "AttributeName": "Date",
                "AttributeType": "S"
            },
            {
                "AttributeName": "Time",
                "AttributeType": "S"
            }
        ],
        # ProvisionedThroughput controls the amount of data you can read or write to DynamoDB per second.
        # You can control read and write capacity independently.
        ProvisionedThroughput={
            "ReadCapacityUnits": 1,
            "WriteCapacityUnits": 1
        }
    )
    #print("Table created successfully!")

    table.meta.client.get_waiter('table_exists').wait(TableName='Wiser')
    print(table.item_count)

except Exception as e:
    print("Error creating table:")
    print(e)


>>>>>>> 3ba719cb2a241dfb835a4aec6a5b271e1d9022a1

from typing import NoReturn
import logging
import secrets
import string
import json
import boto3
import botocore
logger = logging.getLogger()
logger.setLevel(logging.INFO)

client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')


def generate_password() -> str:
    """_summary_

    Returns:
        _type_: _description_
    """
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for i in range(12))
    return password


class CustomerImporter:
    def __init__(self, tablename: str, securitytablename: str):
        """_summary_

        Args:
            tablename (str): _description_
        """
        self.tablename = tablename
        self.customersecuritytablename = securitytablename


    def check_table_exists(self, table_name: str) -> bool:
        """_summary_

        Args:
            table_name (str): _description_

        Returns:
            _type_: _description_
        """
        try:
            # Check if the table exists
            client.describe_table(TableName=table_name)
            return True
        except client.exceptions.ResourceNotFoundException as e:
            logger.error("Error checking table existence: %s", e)
            return False
    

   
    def create_table(self) -> NoReturn:
        """_summary_
        """               
        try:
            response = client.create_table(
            TableName=self.tablename,
            KeySchema=[
                {
                    'AttributeName': 'customer_id',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'email',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'customer_id',
                    'AttributeType': 'S'  # String data type
                },
                {
                    'AttributeName': 'email',
                    'AttributeType': 'S'
                },
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
            )
            logger.info("Table created successfully.")
        except client.exceptions.ResourceInUseException as e:
            logger.error("Table already exists: %s", e)
        except client.exceptions.LimitExceededException as e:
            logger.error("Table creation limit exceeded: %s", e)
        except client.exceptions.ValidationException as e:
            logger.error("Validation exception occurred: %s", e)
        except client.exceptions.ProvisionedThroughputExceededException as e:
            logger.error("Provisioned throughput exceeded:%s", e)
        except client.exceptions.InternalServerError as e:
            logger.error("Internal server error:%s", e)



    def importData(self, customerData: list) -> NoReturn:
        """_summary_

        Args:
            customerData (list): _description_

        Returns:
            NoReturn: _description_
        """
        table = dynamodb.Table(self.tablename)
        try:
            with table.batch_writer() as batch:
                for obj in customerData:
                    if set(['email', 'customer_id', 'country', 'language']).issubset(obj.keys()):
                        password = generate_password()
                        obj['password'] = password
                        batch.put_item(Item=obj)
            logger.info("table imported successfully")
            print("table imported successfully")
        except botocore.exceptions.ClientError as e:
            logger.error("Error occurred during import:%s", e)


    def readCustomerFile(self) -> list:
        """_summary_

        Returns:
            list: _description_
        """
        customer_info = []
        with open('../customer_export.txt', 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip()
                # Parse the JSON object
                try:
                    json_object = json.loads(line)
                    # Process the JSON object as needed
                    customer_info.append(json_object)
                except json.JSONDecodeError as e:
                    logger.error("Error parsing JSON: %s", e)
            return customer_info


if __name__ == "__main__":
    customer_tbl_name = 'carly_customer_info'
    customer_security_tbl_name = 'carly_customer_security_info'


    importer = CustomerImporter(tablename=customer_tbl_name, securitytablename=customer_security_tbl_name)
    
    try:
        tableCheck = importer.check_table_exists(table_name=customer_tbl_name)
        if (tableCheck is False):
            importer.create_table()

        customerinfo = importer.readCustomerFile()
        importer.importData(customerinfo)
        
    except Exception as err:
        logger.error("An error occured: %s", err)

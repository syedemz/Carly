import boto3
from info_logger import dynamo_fetch_record, global_logger
from authorizer import generate_token


dynamodb = boto3.client('dynamodb', region_name='eu-central-1')
table_name = 'carly_customer_info'
index_name = 'email-index'

@dynamo_fetch_record
def fetch_record(email: str) -> object:
    """_summary_

    Args:
        email (str): _description_

    Returns:
        object: _description_
    """
    query_params = {
        'TableName': table_name,
        'IndexName': index_name,
        'KeyConditionExpression': 'email = :val',
        'ExpressionAttributeValues': {
            ':val': {'S': email}
        }
    }

    response = dynamodb.query(**query_params)
   
    if ('Items' in response and len(response['Items']) > 0):
        return response['Items'][0]
    else:
        global_logger('Client Error', 'error', "No matching record found for the provided email")
        return None

@dynamo_fetch_record
def update_record(customer_id: str, email: str, updatefield: dict) -> bool:
    """_summary_

    Args:
        customer_id (str): _description_
        email (str): _description_
        updatefield (dict): _description_

    Returns:
        bool: _description_
    """
    record = fetch_record(email)
    
    if (record is None or record['customer_id']['S'] != customer_id):
        global_logger('Client Error', 'error', "incorrect credentials provided")
        return False

    field_name = list(updatefield.keys())[0]
    field_value = updatefield[field_name]
    #update_expression = "SET password = :password"
    #expression_attribute_values = {':password': {'S': new_password}}
    update_expression = "SET #fd = :field_value"
    expression_attribute_values = {':field_value': {'S': field_value}}
    expression_attribute_names={"#fd": f"{field_name}"}
    response = dynamodb.update_item(
        TableName=table_name,
        Key={'customer_id': {'S': customer_id}, 'email': {'S': email}},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values,
        ExpressionAttributeNames=expression_attribute_names
    )
    if(response['ResponseMetadata']['HTTPStatusCode'] == 200):
        return True
    else:
        global_logger('Server Error', 'error', "Could not update the record")
        return False


def execute_login(email: str, password: str) -> object:
    """_summary_

    Args:
        email (_type_): _description_
        password (_type_): _description_

    Returns:
        _type_: _description_
    """
    record = fetch_record(email)
    print(record)
    try:
        if email == record['email']['S'] and password == record['password']['S']:
            token = generate_token(email)
            return {"customer_id": record['customer_id']['S'], "language": record['language']['S'], "token":token}
    except KeyError as e:
        global_logger('Server Error', 'error',  f"Retrieved record seems to have missing information: {str(e)}")
    return None


def execute_change_password(customer_id: str, email:str, updatefield: dict) -> bool:
    """_summary_

    Args:
        customer_id (str): _description_
        email (str): _description_
        updatefield (dict): _description_

    Returns:
        bool: _description_
    """
    return update_record(customer_id, email, updatefield)


def execute_change_language(customer_id: str, email:str, updatefield: dict) -> bool:
    """_summary_

    Args:
        customer_id (str): _description_
        email (str): _description_
        updatefield (dict): _description_

    Returns:
        bool: _description_
    """
    return update_record(customer_id, email, updatefield)
import json
import boto3
import logging
import datetime

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")
company_table = dynamodb.Table("company")
stocks_table = dynamodb.Table("stocks")


def lambda_handler(event, context):
    logger.info(event)
    http_method = event["httpMethod"]
    path = event["path"]
    company_id = event["queryStringParameters"].get("companyId")

    if http_method == "GET" and path == "/companys":
        response = get_all_companies()
    elif http_method == "GET" and path == "/company":
        if company_id:
            response = get_company(company_id)
        else:
            return {"statusCode": 400, "body": json.dumps("Company ID is required")}
    elif http_method == "POST" and path == "/company":
        body = json.loads(event["body"])
        response = create_company(body)
    elif http_method == "PUT" and path == "/company":
        body = json.loads(event["body"])
        response = update_company(body)
    elif http_method == "DELETE" and path == "/company":
        if company_id:
            response = delete_company(company_id)
        else:
            return {"statusCode": 400, "body": json.dumps("Company ID is required")}
    elif http_method == "GET" and path == "/stocks":
        if company_id:
            if company_exists(company_id):
                response = get_all_stocks(company_id)
            else:
                return {"statusCode": 404, "body": json.dumps("Company not found")}
        else:
            return {"statusCode": 400, "body": json.dumps("Company ID is required")}
    elif http_method == "POST" and path == "/stock":
        body = json.loads(event["body"])
        if company_id:
            if company_exists(company_id):
                response = create_stock(company_id, body)
            else:
                return {"statusCode": 404, "body": json.dumps("Company not found")}
        else:
            return {"statusCode": 400, "body": json.dumps("Company ID is required")}
    elif http_method == "DELETE" and path == "/stock":
        stock_id = event["queryStringParameters"].get("stockId")
        if company_id and stock_id:
            if company_exists(company_id):
                response = delete_stock(company_id, stock_id)
            else:
                return {"statusCode": 404, "body": json.dumps("Company not found")}
        else:
            return {
                "statusCode": 400,
                "body": json.dumps("Company ID and Stock ID are required"),
            }
    else:
        return {"statusCode": 400, "body": json.dumps("Invalid HTTP method")}

    return response


def company_exists(company_id):
    try:
        response = company_table.get_item(Key={"companyId": company_id})
    except Exception as e:
        logger.error(f"Error retrieving company: {str(e)}")
        return False

    return "Item" in response


def get_all_companies():
    try:
        response = company_table.scan()
    except Exception as e:
        logger.error(f"Error retrieving companies: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

    companies = response.get("Items", [])
    return {"statusCode": 200, "body": json.dumps(companies)}


def get_company(company_id):
    try:
        response = company_table.get_item(Key={"companyId": company_id})
    except Exception as e:
        logger.error(f"Error retrieving company: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

    item = response.get("Item")
    if item:
        return {"statusCode": 200, "body": json.dumps(item)}
    else:
        return {"statusCode": 404, "body": json.dumps("Company not found")}


def create_company(data):
    company_id = data.get("companyId")
    name = data.get("name")
    turnover = data.get("turnover")
    ceo = data.get("ceo")

    if not company_id or not name or not turnover or not ceo:
        return {"statusCode": 400, "body": json.dumps("Missing required parameters")}

    try:
        response = company_table.put_item(
            Item={
                "companyId": company_id,
                "name": name,
                "turnover": turnover,
                "ceo": ceo,
            }
        )
    except Exception as e:
        logger.error(f"Error creating company: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

    body = {"Operation": "SAVE", "Message": "SUCCESS", "Item": data}

    return {"statusCode": 200, "body": json.dumps(body)}


def update_company(data):
    company_id = data.get("companyId")
    name = data.get("name")
    turnover = data.get("turnover")
    ceo = data.get("ceo")

    if not company_id or not name or not turnover or not ceo:
        return {"statusCode": 400, "body": json.dumps("Missing required parameters")}

    try:
        response = company_table.update_item(
            Key={"companyId": company_id},
            UpdateExpression="SET #n = :name, turnover = :turnover, ceo = :ceo",
            ExpressionAttributeNames={"#n": "name"},
            ExpressionAttributeValues={
                ":name": name,
                ":turnover": turnover,
                ":ceo": ceo,
            },
        )
    except Exception as e:
        logger.error(f"Error updating company: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

    body = {"Operation": "UPDATE", "Message": "SUCCESS", "Item": data}

    return {"statusCode": 200, "body": json.dumps(body)}


def delete_company(company_id):
    try:
        response = company_table.delete_item(Key={"companyId": company_id})
    except Exception as e:
        logger.error(f"Error deleting company: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

    return {"statusCode": 200, "body": json.dumps("Company deleted successfully")}


def get_all_stocks(company_id):
    try:
        response = stocks_table.query(
            KeyConditionExpression="companyId = :company_id",
            ExpressionAttributeValues={":company_id": company_id},
        )
    except Exception as e:
        logger.error(f"Error retrieving stocks: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

    stocks = response.get("Items", [])
    return {"statusCode": 200, "body": json.dumps(stocks)}


def create_stock(company_id, data):
    stock_id = data.get("stockId")
    price = data.get("price")

    if not stock_id or not price:
        return {"statusCode": 400, "body": json.dumps("Missing required parameters")}
    current_date = datetime.date.today().isoformat()
    data["date"] = str(current_date)

    try:
        response = stocks_table.put_item(Item=data)
    except Exception as e:
        logger.error(f"Error creating stock: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

    body = {"Operation": "SAVE", "Message": "SUCCESS", "Item": data}

    return {"statusCode": 200, "body": json.dumps(body)}


def delete_stock(company_id, stock_id):
    try:
        response = stocks_table.delete_item(
            Key={"companyId": company_id, "stockId": stock_id}
        )
    except Exception as e:
        logger.error(f"Error deleting stock: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}

    return {"statusCode": 200, "body": json.dumps("Stock deleted successfully")}

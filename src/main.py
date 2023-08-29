import json
import boto3
import logging
import pandas as pd

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(asctime)s: %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    handlers=[logging.StreamHandler()],
)

LOGGER = logging.getLogger()


def read_csv(bucket_str, key_str):
    LOGGER.info(f"read_csv {bucket_str} {key_str}")
    s3_client = boto3.client("s3")
    response = s3_client.get_object(Bucket=bucket_str, Key=key_str)
    response.get("ResponseMetadata", {}).get("HTTPStatusCode")
    df_file = pd.read_csv(response.get("Body"))

    return df_file


def get_balance_df(df_account):
    LOGGER.info("get_balance_df")
    df_account["Transaction"] = df_account["Transaction"].astype("float64")
    df_account["Date"] = pd.to_datetime(df_account["Date"])
    df_account["Month"] = df_account["Date"].dt.to_period("M").astype("str")

    df_grouped = (
        df_account.groupby("Month")
        .agg(
            num_transactions=pd.NamedAgg(column="Transaction", aggfunc="count"),
            avg_credit=pd.NamedAgg(
                column="Transaction", aggfunc=lambda x: x[x > 0].mean()
            ),
            avg_debit=pd.NamedAgg(
                column="Transaction", aggfunc=lambda x: x[x < 0].mean()
            ),
        )
        .reset_index()
    )
    df_grouped["avg_credit"] = df_grouped["avg_credit"].round(2)
    df_grouped["avg_debit"] = df_grouped["avg_debit"].round(2)
    df_grouped["total_balance"] = df_account["Transaction"].sum().round(2)

    return df_grouped


def get_balance_dict(df_balance):
    LOGGER.info("get_balance_dict")
    result_lst = []
    result_dict = {}
    balance_fl = 0.0

    for index, row in df_balance.iterrows():
        row_dict = {
            "Month": row["Month"],
            "num_transactions": row["num_transactions"],
            "avg_credit": str(row["avg_credit"]),
            "avg_debit": str(row["avg_debit"]),
        }

        result_lst.append(row_dict)
        balance_fl = row["total_balance"]

    result_dict["months"] = result_lst
    result_dict["total_balance"] = str(balance_fl)
    result_dict["account_id"] = 1

    return result_dict


def send_email(df_balance):
    LOGGER.info("send_email")
    # Create an HTML email body with placeholders
    email_body = """
    <html>
    <head></head>
    <body>
    <h2>Monthly Report</h2>
    {table}
    <img src="cid:company_logo" alt="Company Logo">
    </body>
    </html>
    """

    table_html = df_balance.to_html(index=False)
    email_body = email_body.format(table=table_html)

    sender_email = "sender@gmail.com"
    recipient_email = "receiver@gmail.com"
    subject = "Monthly Report"

    ses_client = boto3.client("ses", region_name="us-east-2")

    msg = MIMEMultipart("related")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    # Attach HTML body
    body = MIMEText(email_body, "html")
    msg.attach(body)

    bucket_name = "bucket-dev"
    logo_object_key = "logo.jpeg"

    s3_client = boto3.client("s3")
    logo_response = s3_client.get_object(Bucket=bucket_name, Key=logo_object_key)
    logo_data = logo_response["Body"].read()
    logo_attachment = MIMEImage(logo_data, "png")
    logo_attachment.add_header("Content-ID", "<company_logo>")
    msg.attach(logo_attachment)

    ses_client.send_raw_email(
        Source=sender_email,
        Destinations=[recipient_email],
        RawMessage={"Data": msg.as_string()},
    )

    return {"statusCode": 200, "body": json.dumps("Email sent successfully")}
    
def dynamo_putItem(balance_dict):
    LOGGER.info(f"dynamo_putItem {balance_dict}")
    dynamo_client = boto3.resource("dynamodb").Table('stori-table')
    dynamo_client.put_item(Item=balance_dict)    


def handler(event, context):
    LOGGER.info(f"Starting handler event:{event}")

    try:
        status_code = 200
        cause_value = ""

        df_account = read_csv("bucket-dev", "stori_ove.csv")
        df_balance = get_balance_df(df_account)

        dynamo_putItem(get_balance_dict(df_balance))

        return send_email(df_balance)        

    except Exception as error:
        LOGGER.error(f"Generic error {error}", exc_info=True)
        cause_value = f"server_error: {error}"
        status_code = 500
        
        
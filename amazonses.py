import boto3
from botocore.exceptions import ClientError

from constants import ENEA_SHORTAGE_LINK

def send_email(SENDER, RECIPIENT, shortages_dict):
    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    CONFIGURATION_SET = "AMAZONSES_CONFIG"
    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "eu-central-1"
    # The subject line for the email.
    SUBJECT = "Enea Power Shortage Alert."
    # The email body for recipients with non-HTML email clients.
    shortage_text = ""
    streets_alert = ""
    for street, shortage in shortages_dict.items():
        streets_alert += f"{street}, "
        if isinstance(shortage, list):
            for date_shortage_dict in shortage:
                shortage_text += f"<p>Date: {date_shortage_dict['date']}," \
                                 f" Location: {date_shortage_dict['localisation']}</p></br>"

    BODY_TEXT = (f"Enea Power Shortage Alert For: \r\n {streets_alert}")

    # The HTML body of the email.
    BODY_HTML = f"""<html>
    <head></head>
    <body>
        {shortage_text}
        <a href={ENEA_SHORTAGE_LINK}>Check ! </a>
    </body>
    </html>
                """
    # The character encoding for the email.
    CHARSET = "UTF-8"
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=AWS_REGION)
    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

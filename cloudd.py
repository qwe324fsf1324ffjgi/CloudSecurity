import boto3
import datetime

# Initialize AWS clients
s3 = boto3.client('s3')
ec2 = boto3.client('ec2')
rds = boto3.client('rds')
dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses')

# Configuration
DYNAMODB_TABLE_NAME = 'CloudSecurityFindings'
SENDER_EMAIL = 'zerahabba1@gmail.com'
RECIPIENT_EMAIL = 'zerahabba1@gmail.com'

def lambda_handler(event, context):
    findings = []

    findings += check_public_s3()
    findings += check_insecure_security_groups()
    findings += check_unencrypted_rds()

    if findings:
        store_in_dynamodb(findings)
        send_alerts(findings)

    return {
        'statusCode': 200,
        'body': f"{len(findings)} findings reported."
    }

def check_public_s3():
    findings = []
    response = s3.list_buckets()

    for bucket in response['Buckets']:
        bucket_name = bucket['Name']
        try:
            acl = s3.get_bucket_acl(Bucket=bucket_name)
            for grant in acl['Grants']:
                if 'AllUsers' in str(grant) or 'AuthenticatedUsers' in str(grant):
                    findings.append({
                        'type': 'S3 Public Access',
                        'resource': bucket_name,
                        'details': 'Bucket allows public access'
                    })
        except Exception as e:
            print(f"Error checking bucket {bucket_name}: {e}")

    return findings

def check_insecure_security_groups():
    findings = []
    response = ec2.describe_security_groups()

    for sg in response['SecurityGroups']:
        for perm in sg['IpPermissions']:
            from_port = perm.get('FromPort')
            to_port = perm.get('ToPort')
            if from_port in [22, 3389] or to_port in [22, 3389]:
                for ip_range in perm.get('IpRanges', []):
                    if ip_range.get('CidrIp') == '0.0.0.0/0':
                        findings.append({
                            'type': 'Insecure Security Group',
                            'resource': sg['GroupId'],
                            'details': f"Port {from_port} open to the world"
                        })

    return findings

def check_unencrypted_rds():
    findings = []
    response = rds.describe_db_instances()

    for db in response['DBInstances']:
        if not db.get('StorageEncrypted'):
            findings.append({
                'type': 'Unencrypted RDS',
                'resource': db['DBInstanceIdentifier'],
                'details': 'RDS instance is not encrypted at rest'
            })

    return findings

def store_in_dynamodb(findings):
    table = dynamodb.Table(DYNAMODB_TABLE_NAME)
    now = datetime.datetime.utcnow().isoformat()

    for finding in findings:
        try:
            table.put_item(Item={
                'id': f"{finding['type']}#{finding['resource']}",
                'timestamp': now,
                'type': finding['type'],
                'resource': finding['resource'],
                'details': finding['details']
            })
        except Exception as e:
            print(f"Error storing finding in DynamoDB: {e}")

def send_alerts(findings):
    subject = '[ALERT] AWS Security Findings'
    body = "\n".join([
        f"{f['type']} - {f['resource']} - {f['details']}"
        for f in findings
    ])

    try:
        response = ses.send_email(
            Source=SENDER_EMAIL,
            Destination={'ToAddresses': [RECIPIENT_EMAIL]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}}
            }
        )
        print(f"Email sent: MessageId {response['MessageId']}")
    except Exception as e:
        print(f"Error sending email via SES: {e}")

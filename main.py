import requests
import boto3
from datetime import datetime
import os
from flask import Flask

BUCKET_NAME: str = 's3-hw15-memes' # PLEASE CHANGE to your desired bucketname
LOG_FILE_PATH = "./log/memes/memes.log"

PORT: int = int(os.environ.get("PORT", 8080))

HEADERS_METADATA_TOKEN_TTL={"X-aws-ec2-metadata-token-ttl-seconds": "21600"} 
HEADERS_METADATA_TOKEN_KEY="X-aws-ec2-metadata-token"

def get_private_ip()->str:
    try:
        token = requests.put('http://169.254.169.254/latest/api/token', headers=HEADERS_METADATA_TOKEN_TTL).text

        localIp:str = requests.get('http://169.254.169.254/latest/meta-data/local-ipv4',timeout=2,
                            headers={HEADERS_METADATA_TOKEN_KEY: token}).text
        return localIp
    except Exception as e:
        return "127.0.0.1"

def get_public_ip()->str:
    try:
        token = requests.put('http://169.254.169.254/latest/api/token', headers=HEADERS_METADATA_TOKEN_TTL).text

        publicIp:str = requests.get('http://169.254.169.254/latest/meta-data/public-ipv4',timeout=2,
                                    headers={HEADERS_METADATA_TOKEN_KEY:token}).text
        return publicIp
    except:
        return "127.0.0.1"

def upload_log(ipPrivate: str, ipPublic:str ,port:int)->None:
    logEntry: str= f"{datetime.utcnow().isoformat()} - Private IP of the instance: {ipPrivate} - Public IP of the instance: {ipPublic}; PORT: {port}\n"
    filename: str= f'logs/{ipPrivate.replace(".","_")}_memes.log'
    
    s3 = boto3.client("s3")
    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=filename,
        Body=logEntry,
        ContentType='text/plain')
    print(f"Log is uploaded to S3://{BUCKET_NAME}/{filename}")
    

app = Flask(__name__)

@app.route("/")
def memes():
    return """1303199992 - Memes Raja Doraja\n1302239126 - Memes""" # Change to your group's member; format (NIM - Name)

@app.route("/ip-public"):
def getIpPublic():
    ipPublic = get_public_ip()
    return f"<h1> {ipPublic}:{PORT}</h1>"

@app.route("/log")
def trigger_memes():
    ipPrivate = get_private_ip()
    ipPublic = get_public_ip()
    upload_log(ipPrivate,ipPublic, PORT)
    return f"Logged {ipPrivate}:{PORT} to S3."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)

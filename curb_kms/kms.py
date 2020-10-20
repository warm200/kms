import base64
import boto3
import os

class CurbKms:
    def __init__(self, region_name="us-east-1"):
        _session = boto3.session.Session(region_name=region_name)
        self.client = _session.client('kms')
        self.alias = "arn:aws:kms:{}:676203907616:alias/{}_CURBCONFIG".format(region_name, os.environ.get("APP_ENV"))

    def encrypt(self, secret):
        ciphertext = self.client.encrypt(
            KeyId=self.alias,
            Plaintext=bytes(secret, encoding='utf8'),
        )
        return base64.b64encode(ciphertext["CiphertextBlob"])


    def decrypt(self, secret):
        plaintext = self.client.decrypt(
            CiphertextBlob=bytes(base64.b64decode(secret))
        )
        return plaintext["Plaintext"].decode('utf-8')

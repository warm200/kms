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


if __name__ == "__main__":
    session = CurbKms()
    print(session.encrypt('some_secret'))
    print(session.decrypt('AQICAHhNHjV69FOqvSOh+p+4zVZHCE4O795o12lTeIqYnAHPugH+c8txVlOPvQZQt8MwB0cQAAAAaTBnBgkqhkiG9w0BBwagWjBYAgEAMFMGCSqGSIb3DQEHATAeBglghkgBZQMEAS4wEQQMXcbZsd2wkv1KAcVwAgEQgCY9cxH95usQDsqfrCkTzVPWF1Y2nSMLuLG0UnZkVwBhvykhKmsjXQ=='))

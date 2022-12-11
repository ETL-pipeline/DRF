import boto3
from datetime import datetime

class S3instant():

    def __init__(self) -> None:

        self.ACCESS_KEY_ID = 'AKIA26P55UQN6IF3KCZR' #s3 관련 권한을 가진 IAM계정 정보
        self.ACCESS_SECRET_KEY = 'UG6q6TLeD5kEChKh/doHs4aPgKiVbS4Vdf+CsGrk'
        self.BUCKET_NAME = 'drf-s3-bucket'
        self.S3 = self.s3connection()

    def s3connection(self):

        try:
            s3 = boto3.client(
                service_name='s3', 
                region_name='ap-northeast-2',
                aws_access_key_id=self.ACCESS_KEY_ID,
                aws_secret_access_key=self.ACCESS_SECRET_KEY)

        except:

            pass

        else:

            print('s3 connected.')

        return s3

    def s3uploadlog(self, path):

        now = datetime.now()
        dt_string = now.strftime("%Y/%m/%d/%H/%M/%S")

        response = self.S3.upload_file(path, self.BUCKET_NAME, f'{dt_string}/loginfo.json.gz')
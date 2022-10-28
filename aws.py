import boto3

s3 = boto3.resource('s3', aws_access_key_id='AKIA6RGYYJLGVLF4VUI2',
                    aws_secret_access_key='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')

client = boto3.client('s3', aws_access_key_id='AKIA6RGYYJLGVLF4VUI2',
                      aws_secret_access_key='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')

"Когда принимаю картинку, её нужно сохранить во временной папке.  " \
"Затем через её адрес сохранить в АВС" \
"После чего удалить картинку во временной папке"

# test
def upload_files(img_name, bucket, object_name=None, args=None):
    """ if object_name is not None?"""
    if object_name is None:
        object_name = img_name
        client.upload_file(img_name, bucket, object_name, ExtraArgs=args)
        print(f"{img_name} upload in {bucket}")
        return f"https://azatuuluamanbucket.s3.ap-northeast-1.amazonaws.com/{img_name}"


args = {'ACL': 'public-read'}
upload_files('media/superman.png', 'azatuuluamanbucket', args=args)

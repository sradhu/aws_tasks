import boto3 as bt
def lambda_handler(event, context):
    source_bucket = <source_bucket_name>
    dest_bucket = <Dest_bucket_name>
    source_list = get_obj_list(source_bucket)
    dest_list = get_obj_list(dest_bucket)

    if dest_list == None:
        upload_2_dest(source_bucket,dest_bucket, source_list)
    else:
        upload_list = {}
        for key, value in source_list.items():
            if dest_list.get(key) == None:
                upload_list[key] = value
        upload_2_dest(source_bucket,dest_bucket, upload_list)

def get_obj_list(buck):
    s3c = bt.client('s3')
    list = s3c.list_objects(Bucket=buck)
    if list.get('Contents') == None:
        return None
    else:
        all_objs = {}
        for obj in list['Contents']:
            all_objs[obj['Key']] = obj['Size']
        return all_objs

def upload_2_dest(source_buck,dest_buck, keys_list):
    s3r = bt.resource('s3')
    for key in keys_list:
        copy_source = {
            'Bucket': source_buck,
            'Key': key
        }
        bucket = s3r.Bucket(dest_buck)
        obj = bucket.Object(key)
        obj.copy(copy_source)
        print key

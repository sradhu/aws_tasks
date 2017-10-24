# get the list of clusters in the account
import boto3
import datetime
import json
import pprint
ecs_client = boto3.client('ecs')
cw_client = boto3.client('cloudwatch', region_name='us-east-1')
ec2_client = boto3.client('ec2')
asg_client = boto3.client('autoscaling')

def cluster_list():
    return ecs_client.list_clusters()

def desc_clusters(a_clustrs):
    return ecs_client.describe_clusters(clusters=a_clustrs)

def service_list(clustr):
    return ecs_client.list_services(cluster=clustr)

def tasks_list(clustr, srvc):
    return ecs_client.list_tasks(cluster=clust,serviceName=srvc)

def task_desc(a_clustr,a_task):
    return ecs_client.describe_tasks(cluster=a_clustr,tasks=[a_task])


def task_def(task_def_arn):
    return ecs_client.describe_task_definition(taskDefinition=task_def_arn)

def cont_inst_list(a_clustr):
    return ecs_client.list_container_instances(cluster=a_clustr)

def desc_ec2_instance(a_inst_id):
    return ec2_client.describe_instances(InstanceIds=[a_inst_id])

def desc_cont_instances(a_clustr, a_cont_instas):
    return ecs_client.describe_container_instances(
        cluster=a_clustr,
        containerInstances= a_cont_instas
        )
def desc_asgs():
    return asg_client.describe_auto_scaling_groups()


def ecs_cluster_metrics(a_clustr,a_srvc,a_metric_name,a_sec):
    clust_metics = cw_client.get_metric_statistics(
        Namespace='AWS/ECS',
        Dimensions=[
            {
                'Name': 'ClusterName',
                'Value': a_clustr.split('/')[-1]
            },
            {
                'Name': 'ServiceName',
                'Value': a_srvc.split('/')[-1]
            }
        ],
        MetricName=a_metric_name,
        StartTime=datetime.datetime.utcnow() - datetime.timedelta(seconds=a_sec),
        EndTime=datetime.datetime.utcnow(),
        Period=300,
        Statistics=[
            'Average'
        ]
    )
    return clust_metics


cluster_ls = cluster_list()
# print cluster_ls['clusterArns']
# print len(cluster_ls['clusterArns'])
# for clust in cluster_ls:
    # ec2_inst_ls = cont_inst_list(clust)
    # pprint.pprint(ec2_inst_ls['containerInstanceArns'][0])
    # service_ls = service_list(clust)
    # pprint.pprint(service_ls)
    # print service_ls['serviceArns']
    # print len(service_ls['serviceArns'])
    # for srvc in service_ls['serviceArns']:
    #     print ecs_cluster_metrics(clust,srvc,'CPUUtilization',1800)
    #     print ecs_cluster_metrics(clust,srvc,'MemoryUtilization',1800)
    #     tasks = tasks_list(clust,srvc)
    #     print tasks['taskArns']
    #     for task in tasks['taskArns']:
    #         task_details = task_desc(clust,task.split('/')[-1])
    #         print task_details
    #         print task_details['tasks'][0]['taskDefinitionArn']
    #         print task_details['tasks'][0]['containerInstanceArn']
    #         task_df = task_def(task_details['tasks'][0]['taskDefinitionArn'])

    # insta_desc = desc_cont_instances(clust,ec2_inst_ls['containerInstanceArns'])
    # pprint.pprint(inst['containerInstances'][0]['ec2InstanceId'])

    # print insta_desc['containerInstances'][0]['ec2InstanceId']
    # pprint.pprint(desc_ec2_instance(insta_desc['containerInstances'][0]['ec2InstanceId']))

asgs = asg_client.describe_auto_scaling_groups()
    # pprint.pprint(asgs)
clusters = desc_clusters(cluster_ls['clusterArns'])
pprint.pprint(clusters)
for asg in asgs['AutoScalingGroups']:
    for tag in asg['Tags']:
        if tag['Key'] == 'Name':
            print(tag['Value'])
            print(tag['Value'].split(' '))
            print clusters
            print type(clusters)
            print clusters['clusters'][0]['clusterName']
            if clusters['clusters'][0]['clusterName'] in tag['Value']:
                print tag['ResourceId']


# pprint.pprint(asgs[])

def launch_ec2_instance():
    response = client.run_instances(
        BlockDeviceMappings=[
        {
            'DeviceName': 'string',
            'VirtualName': 'string',
            'Ebs': {
                'Encrypted': True|False,
                'DeleteOnTermination': True|False,
                'Iops': 123,
                'SnapshotId': 'string',
                'VolumeSize': 123,
                'VolumeType': 'standard'|'io1'|'gp2'|'sc1'|'st1'
            },
            'NoDevice': 'string'
        },
    ],
    ImageId='string',
    InstanceType='t1.micro'|'t2.nano'|'t2.micro'|'t2.small'|'t2.medium'|'t2.large'|'t2.xlarge'|'t2.2xlarge'|'m1.small'|'m1.medium'|'m1.large'|'m1.xlarge'|'m3.medium'|'m3.large'|'m3.xlarge'|'m3.2xlarge'|'m4.large'|'m4.xlarge'|'m4.2xlarge'|'m4.4xlarge'|'m4.10xlarge'|'m4.16xlarge'|'m2.xlarge'|'m2.2xlarge'|'m2.4xlarge'|'cr1.8xlarge'|'r3.large'|'r3.xlarge'|'r3.2xlarge'|'r3.4xlarge'|'r3.8xlarge'|'r4.large'|'r4.xlarge'|'r4.2xlarge'|'r4.4xlarge'|'r4.8xlarge'|'r4.16xlarge'|'x1.16xlarge'|'x1.32xlarge'|'x1e.32xlarge'|'i2.xlarge'|'i2.2xlarge'|'i2.4xlarge'|'i2.8xlarge'|'i3.large'|'i3.xlarge'|'i3.2xlarge'|'i3.4xlarge'|'i3.8xlarge'|'i3.16xlarge'|'hi1.4xlarge'|'hs1.8xlarge'|'c1.medium'|'c1.xlarge'|'c3.large'|'c3.xlarge'|'c3.2xlarge'|'c3.4xlarge'|'c3.8xlarge'|'c4.large'|'c4.xlarge'|'c4.2xlarge'|'c4.4xlarge'|'c4.8xlarge'|'cc1.4xlarge'|'cc2.8xlarge'|'g2.2xlarge'|'g2.8xlarge'|'g3.4xlarge'|'g3.8xlarge'|'g3.16xlarge'|'cg1.4xlarge'|'p2.xlarge'|'p2.8xlarge'|'p2.16xlarge'|'d2.xlarge'|'d2.2xlarge'|'d2.4xlarge'|'d2.8xlarge'|'f1.2xlarge'|'f1.16xlarge',
    Ipv6AddressCount=123,
    Ipv6Addresses=[
        {
            'Ipv6Address': 'string'
        },
    ],
    KernelId='string',
    KeyName='string',
    MaxCount=123,
    MinCount=123,
    Monitoring={
        'Enabled': True|False
    },
    Placement={
        'AvailabilityZone': 'string',
        'Affinity': 'string',
        'GroupName': 'string',
        'HostId': 'string',
        'Tenancy': 'default'|'dedicated'|'host',
        'SpreadDomain': 'string'
    },
    RamdiskId='string',
    SecurityGroupIds=[
        'string',
    ],
    SecurityGroups=[
        'string',
    ],
    SubnetId='string',
    UserData='string',
    AdditionalInfo='string',
    ClientToken='string',
    DisableApiTermination=True|False,
    DryRun=True|False,
    EbsOptimized=True|False,
    IamInstanceProfile={
        'Arn': 'string',
        'Name': 'string'
    },
    InstanceInitiatedShutdownBehavior='stop'|'terminate',
    NetworkInterfaces=[
        {
            'AssociatePublicIpAddress': True|False,
            'DeleteOnTermination': True|False,
            'Description': 'string',
            'DeviceIndex': 123,
            'Groups': [
                'string',
            ],
            'Ipv6AddressCount': 123,
            'Ipv6Addresses': [
                {
                    'Ipv6Address': 'string'
                },
            ],
            'NetworkInterfaceId': 'string',
            'PrivateIpAddress': 'string',
            'PrivateIpAddresses': [
                {
                    'Primary': True|False,
                    'PrivateIpAddress': 'string'
                },
            ],
            'SecondaryPrivateIpAddressCount': 123,
            'SubnetId': 'string'
        },
    ],
    PrivateIpAddress='string',
    ElasticGpuSpecification=[
        {
            'Type': 'string'
        },
    ],
    TagSpecifications=[
        {
            'ResourceType': 'customer-gateway'|'dhcp-options'|'image'|'instance'|'internet-gateway'|'network-acl'|'network-interface'|'reserved-instances'|'route-table'|'snapshot'|'spot-instances-request'|'subnet'|'security-group'|'volume'|'vpc'|'vpn-connection'|'vpn-gateway',
            'Tags': [
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ]
        },
    ]
    )

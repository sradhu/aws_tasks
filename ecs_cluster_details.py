# get the list of clusters in the account
import boto3
import datetime
import json

ecs_client = boto3.client('ecs')
cw_client = boto3.client('cloudwatch', region_name='us-east-1')

def cluster_list():
    return ecs_client.list_clusters()

def service_list(clustr):
    return ecs_client.list_services(cluster=clustr)

def tasks_list(clustr, srvc):
    return ecs_client.list_tasks(cluster=clust,serviceName=srvc)

def task_desc(a_clustr,a_task):
    return ecs_client.describe_tasks(cluster=a_clustr,tasks=[a_task])


def task_def(task_def_arn):
    return ecs_client.describe_task_definition(taskDefinition=task_def_arn)

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
print cluster_ls['clusterArns']
print len(cluster_ls['clusterArns'])

for clust in cluster_ls['clusterArns']:
    service_ls = service_list(clust)
    print service_ls['serviceArns']
    print len(service_ls['serviceArns'])
    for srvc in service_ls['serviceArns']:
        print ecs_cluster_metrics(clust,srvc,'CPUUtilization',1800)
        print ecs_cluster_metrics(clust,srvc,'MemoryUtilization',1800)
        tasks = tasks_list(clust,srvc)
        print tasks['taskArns']
        for task in tasks['taskArns']:
            task_details = task_desc(clust,task.split('/')[-1])
            print task_details
            print task_details['tasks'][0]['taskDefinitionArn']
            print task_details['tasks'][0]['containerInstanceArn']
            task_df = task_def(task_details['tasks'][0]['taskDefinitionArn'])

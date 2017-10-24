import boto3
import datetime
from optparse import OptionParser
import os
import json
import pprint
ecs_client = boto3.client('ecs')
asg_client = boto3.client('autoscaling')
asgs_client = boto3.client('autoscaling')

def get_asg_for_cluster(cluster_name):
    paginator = asg_client.get_paginator('describe_auto_scaling_groups')
    page_iterator = paginator.paginate(
        PaginationConfig={'PageSize': 100}
    )
    filtered_asgs = page_iterator.search(
        'AutoScalingGroups[] | [?contains(Tags[?Key==`{}`].Value, `{}`)]'.format(
            'Name', cluster_name)
    )
    asgs = []
    for asg in filtered_asgs:
        asgs.append(asg['AutoScalingGroupName'])
    if len(asgs) == 0:
        return None
    elif len(asgs) == 1:
        return asgs[0]
    else:
        raise Exception("should find exactly one asg for cluster " + cluster_name)

def cluster_names():
    clusters = ecs_client.list_clusters()
    cluster_names = []
    for cluster_arn in clusters['clusterArns']:
        cluster_name < cluster_arn.partition('/')[2]
    return cluster_names

def service_list(a_clustr):
    return ecs_client.list_services(cluster=a_clustr)

def task_list(a_clustr):
    return ecs_client.list_tasks(cluster=a_clustr,)

def container_instas(a_clustr):
    return ecs_client.list_container_instances(cluster=a_clustr)

def desc_conta_inst(a_clustr, a_cont_inst_arn):
    return ecs_client.describe_container_instances(
        cluster = a_clustr,
        containerInstances = a_cont_inst_arn
    )
def desc_tasks(a_clustr, a_tasks_arr):
    return ecs_client.describe_tasks(
       cluster=a_clustr,tasks= a_tasks_arr
    )

def desc_all_tasks(a_clustr):
    tasks = ecs_client.list_tasks(cluster=a_clustr)
    return ecs_client.describe_tasks(cluster=a_clustr, tasks['taskArns'])

def task_def(a_task_def_arn):
    return ecs_client.describe_task_definition(taskDefinition = a_task_def_arn)


def asg_details(a_asg_names):
    desc_asgs = asgs_client.describe_auto_scaling_groups(AutoScalingGroupNames=a_asg_names)
    asg_desired_capacity = {}
    for asg_params in desc_asgs['AutoScalingGroups']:
        asg_desired_capacity['AutoScalingGroupName'] = asg_params['DesiredCapacity']
    return asg_desired_capacity


def container_instas_details(a_clustr):
    container_instances = container_instas(a_clustr)
    if not container_instances['containerInstanceArns']:
        print 'No container instances exist for cluster', a_clustr
        continue
    container_inst = desc_conta_inst(a_clustr, container_instances['containerInstanceArns'])
    container_instance_resources = []
    cont_inst_resrc = {}
    current_instance_state = None

    for instance in container_inst['containerInstances']:
        print ' currentinstancestate ' , instance['status']
        print 'runningtaskscount', instance['runningTasksCount']

        cont_inst_resrc['instance_id'] = instance['ec2InstanceId']

        for reg_resource in instance['registeredResources']:
            if reg_resource['name'] == 'CPU':
                cont_inst_resrc['cpu_registered'] = reg_resource['integerValue']
            if reg_resource['name'] == 'MEMORY':
                cont_inst_resrc['memory_registered'] = reg_resource['integerValue']
        for remaining_resource in instance['remainingResources']:
            if remaining_resource['name'] == 'CPU':
                cont_inst_resrc['cpu_free'] = remaining_resource['integerValue']
            if remaining_resource['name'] == 'MEMORY':
                cont_inst_resrc['memory_free'] = remaining_resource['integerValue']

        cpu_used = cont_inst_resrc['cpu_registered'] - cont_inst_resrc['memory_registered']
        memory_used = cont_inst_resrc['memory_registered'] - cont_inst_resrc['memory_free']
        cont_inst_resrc['cpu_capacity'] = float(cpu_used) / cont_inst_resrc['cpu_registered']
        cont_inst_resrc['memory_capacity'] = float(memory_used)/ cont_inst_resrc['memory_registered']
        container_instance_resources.append(cont_inst_resrc)
    return container_instance_resources

def terminate_idle_instances(asg_client, container_instance_resources, running_tasks_count, dry_run):
    for container_instance_resource in container_instance_resources:
        if running_tasks_count == 0:
            if dry_run:
                print 'terminating instance', container_instance_resource['instance_id']
            else:
                asg_client.terminate_instance_in_auto_scaling_group(
                    InstanceId=container_instance_resource['instance_id'],
                    ShouldDecrementDesiredCapacity=True
                )

def service_task_details(a_clustr):
    # service_ls = service_list(cluster_name)
    tasks = desc_all_tasks(cluster_name)

    task_definition_resources = {}
    for task in tasks:
        task_defin = task_def(task['taskDefinitionArn'])
        memory = 0
        cpu = 0
        memory_reservation = 0
        for container_definition in task_defin['taskDefinition']['containerDefinitions']:
            cpu += container_definition['cpu']
            if 'memoryReservation' in container_definition:
                memory_reservation += container_definition['memoryReservation']
            else:
                memory += container_definition['memory']
        task_definition_resources[task['taskDefinitionArn']] = {
            'memory': memory,
            'cpu': cpu,
            'memory_reservation': memory_reservation
        }

    highest_cpu = 0
    highest_memory = 0
    highest_memory_reservation = 0
    for task_definition_arn in task_definition_resources:
        if task_definition_resources[task_definition_arn]['cpu'] > highest_cpu:
            highest_cpu = task_definition_resources[task_definition_arn]['cpu']
        if task_definition_resources[task_definition_arn]['memory_reservation'] > highest_memory_reservation:
            highest_memory_reservation = task_definition_resources[task_definition_arn]['memory_reservation']
        print ' Highest CPU = ' , highest_cpu
        print ' Highest MEMORY = ', highest_memory
        print ' Highest Memory Reservation = ', highest_memory_reservation

    add_instances = True
    desired_capacity  = existing_desired_capacity

    for cont_inst_resrc in cont_inst_resrcs:
        print '    ' , cont_inst_resrc
        if highest_memory < cont_inst_resrc['memory_free']:
            pass
        elif highest_cpu < cont_inst_resrc['cpu_free']:
            pass
        elif highest_memory_reservation < cont_inst_resrc['memory_free']:
            pass
        else:
            desired_capacity += 1
        print 'Thenewdesiredcapacity', desired_capacity
    if desired_capacity != existing_desired_capacity:
        terminate_idle_instances(asg_client, cont_inst_resrcs, running_tasks_count, dry_run=True)

    low_capacity_instances = []
    for cont_inst_resrc in cont_inst_resrcs:
        print 'cpucapaccity', cont_inst_resrc['cpu_capacity']
        print 'memorycapacity', cont_inst_resrc['memory_capacity']
        if cont_inst_resrc['memory_capacity'] <= 0.5 and cont_inst_resrc['cpu_capacity'] <= 0.5:
           low_capacity_instances.append(cont_inst_resrc['instance_id'])
    print 'lowcapacityinstances', low_capacity_instances


def main_fun():
    for cluster in cluster_names():
        asg = get_asg_for_cluster('ECS-' + cluster)
        print 'cluster = ' + cluster
        print 'existingdesiredcapacity' , asg_details(str(asg))
        print 'Container instance resources' , container_instas_details(cluster)
        service_task_details(cluster)

main_fun()



# now we have the instances which are running on low capacity set them to draining

    # if len(low_capacity_instances) >= 2 :
    #     instances_to_drain_count = int(len(low_capacity_instances)/2)
    #     for instance_id in low_capacity_instances[:instances_to_drain_count]:
    #         response = client.update_container_instances_state(
    #             cluster=cluster_name,
    #             containerInstances=low_capacity_instances[:instances_to_drain_count],
    #             status='DRAINING'
    #         )

'''
Created on 24 Jul 2017

@author: stack
'''
#import base64
from openstack import connection
from neutronclient.v2_0 import client
from openstack import exceptions
#import time
import subprocess

#from itertools import chain

neutron = client.Client(endpoint_url='http://192.168.100.10:9696', token='985780de69f2488c8b7337ddcfe7d5ad')
auth_args = {
    'auth_url': 'http://192.168.100.10/identity/v3',
    'project_name': 'demo',
    'username': 'admin',
    'password': 'secret',
    'user_domain_id' : 'default',
    'project_domain_id' : 'default'
}
conn = connection.Connection(**auth_args)

#network = conn.network.find_network('private')
#port = conn.network.find_port('port_test1')

def create_port(name, network):
    for p in conn.network.ports():
        if p.name == name:
            print 'Port', name, 'already exists.'
            return -1
    netw = conn.network.find_network(network)
    body_port = {'port' : {'name' : name, 'network_id' : netw.id, 'admin_state_up' : True}}
    neutron.create_port(body_port)  
    print 'Port', name, 'has been created.'

def delete_port(name):
    port = conn.network.find_port(name)
    if port:
        neutron.delete_port(port.id)   
        print 'Port', name, 'has been deleted.' 
    
def create_server_bkp(name, image, flavor, nics, user_data):
    for s in conn.compute.servers():
        if s.name == name:
            print 'Server', name, 'already exists.'
            return -1
    img = conn.compute.find_image(image)
    flv = conn.compute.find_flavor(flavor)

    networks = [] 
    for nic in nics:
        port = conn.network.find_port(nic)
        p = {'port' : port.id} 
        networks.append(p) 
    '''
    instance_args = {
        'name': name,
        'imageRef': img.id,
        'flavorRef': flv.id,
        'key_name': 'default',
        'user_data': user_data,
        #'security_groups': [{'name':'default'}],
        #'availability_zone': 'compute1',
        'networks': networks
        #'availability_zone': 'compute1'
        #'security_groups': [{'name': all_in_one_security_group.name}]
        #'OS-EXT-AZ:availability_zone': 'nova:compute1'
    }
    '''  
    if user_data:
        instance_args = {
            'name': name,
            'imageRef': img.id,
            'flavorRef': flv.id,
            'key_name': 'default',
            'user_data': user_data,
            #'availability_zone': 'nova',
            'networks': networks
        }
    else:
        instance_args = {
            'name': name,
            'imageRef': img.id,
            'flavorRef': flv.id,
            'key_name': 'default',
            #'user_data': user_data,
            #'availability_zone': 'nova',
            'networks': networks
        }
    server = conn.compute.create_server(**instance_args) 
    conn.compute.wait_for_server(server)   
    print 'Server', name, 'has been instantiated.'
    return server

def create_server(name, image, flavor, nics, user_data, availability_zone):
    # openstack server create --image ubuntu-1404 --flavor ds1G --nic port-id="$(openstack port show -f value -c id p_testing)" --key-name default --availability-zone nova:compute2 testing
    '''
    if len(nics)==2:
        nic2 = nics[1]
    else:
        nic2 = 'NA'
    '''
    if len(nics)==3:
        nic2 = nics[1] 
        nic3 = nics[2]
    elif len(nics)==2:
        nic2 = nics[1]
        nic3 = 'NA'
    else:
        nic2 = 'NA'
        nic3 = 'NA'
        
    if user_data is None:
        user_data = 'NA'
    #args = str(name +' '+ image +' '+ flavor +' '+ nics[0] +' '+ nic2 +' '+ user_data +' '+ availability_zone)
    #print args
    subprocess.call(['/opt/stack/create_server.sh', name, image, flavor, nics[0], nic2, user_data, availability_zone, nic3])
    server = conn.compute.find_server(name, True)
    conn.compute.wait_for_server(server)


def finalise_steering(port_name, src_ip, dst_ip):
    port = conn.network.find_port(port_name)
    port_id = port.id
    print port_id, src_ip, dst_ip
    print '/opt/stack/finalise_steering.sh', port_id, src_ip, dst_ip
    subprocess.call(['/opt/stack/finalise_steering.sh', port_id, src_ip, dst_ip])

       
def delete_server(name):
    srv = conn.compute.find_server(name, True)
    if srv:
        #timeout=None
        conn.compute.delete_server(srv.id, force=True)
        #conn.compute.wait_for_delete(srv, wait=timeout) 
        print 'Server', name, 'has been deleted.'
    return

def create_flow_classifier(name, source_ip, destination_ip, 
                protocol, source_port_range, destination_port_range, logical_source_port):
    for fc in neutron.list_flow_classifiers()['flow_classifiers']:
        if fc['name'] == name:
            'Flow classifier', name, 'already exists.'
            return 0
    port = conn.network.find_port(logical_source_port)
    port_id = port.id
    body_fc = {'flow_classifier' : {
                    'source_port_range_min' : source_port_range,
                    'destination_ip_prefix': destination_ip, 
                    'protocol': protocol,
                    'ethertype': 'IPv4',
                    'source_port_range_max' : destination_port_range,
                    'source_ip_prefix': source_ip,
                    'logical_source_port': port_id,
                    'name': name}}
    neutron.create_flow_classifier(body=body_fc) 
    print 'Flow classifier', name, 'has been created.'
    
def get_flow_classifier_id(name):
    for fc in neutron.list_flow_classifiers()['flow_classifiers']:
        if fc['name'] == name:
            return fc['id']
    print 'Flow classifier', name,'does not exist.'
    return -1

def delete_flow_classifier(name):
    fc_id = get_flow_classifier_id(name)
    if fc_id != -1:
        neutron.delete_flow_classifier(fc_id)
        print 'Flow classifier', name, 'has been deleted.'
    
def create_port_pair(name, ports):
    for pp in neutron.list_port_pairs()['port_pairs']:
        if pp['name'] == name:
            'Port pair', name, 'already exists.'
            return 0
    port_in = conn.network.find_port(ports[0])
    port_out = conn.network.find_port(ports[1])
    body_pp = {'port_pair' : {'ingress': port_in.id,
                               'egress': port_out.id,
                                'name': name}}
    neutron.create_port_pair(body=body_pp)
    print 'Port pair', name, 'has been created.'
    
def get_port_pair_id(name):
    for pp in neutron.list_port_pairs()['port_pairs']:
        if pp['name'] == name:
            return pp['id']
    print 'Port pair', name,'does not exist.'
    return -1
    
def delete_port_pair(name):
    pp_id = get_port_pair_id(name)
    if pp_id != -1:
        neutron.delete_port_pair(pp_id)
        print 'Port pair', name, 'has been deleted.'

def create_port_pair_group(name, port_pairs):
    for ppg in neutron.list_port_pair_groups()['port_pair_groups']:
        if ppg['name'] == name:
            'Port pair group', name, 'already exists.'
            return 0   
    port_pair_ids = []
    for pp in port_pairs:
        pp_id = get_port_pair_id(pp)
        port_pair_ids.append(pp_id)
    body_ppg = {'port_pair_group' : {
        'port_pairs': port_pair_ids,
         'name': name}}
    neutron.create_port_pair_group(body=body_ppg)
    print 'Port pair group', name, 'has been created.'

def update_port_pair_group(name, port_pairs):
    ppg_id = get_port_pair_group_id(name)
    if ppg_id != -1:
        port_pair_ids = []
        for pp in port_pairs:
            pp_id = get_port_pair_id(pp)
            port_pair_ids.append(pp_id)
        body_ppg = {'port_pair_group' : {
            'port_pairs': port_pair_ids,
             'name': name}}
        neutron.update_port_pair_group(ppg_id, body=body_ppg)
        print 'Port pair group', name, 'has been updated.'
    
def get_port_pair_group_id(name):
    for ppg in neutron.list_port_pair_groups()['port_pair_groups']:
        if ppg['name'] == name:
            return ppg['id']
    print 'Port pair group', name,'does not exist.'
    return -1
   
def delete_port_pair_group(name):
    ppg_id = get_port_pair_group_id(name)
    if ppg_id != -1:
        neutron.delete_port_pair_group(ppg_id)
        print 'Port pair group', name, 'has been deleted.'
        
def create_port_chain(name, port_pair_groups, flow_classifiers):
    for pc in neutron.list_port_chains()['port_chains']:
        if pc['name'] == name:
            'Port chain', name, 'already exists.'
            return 0
    port_pair_group_ids = []
    for ppg in port_pair_groups:
        ppg_id = get_port_pair_group_id(ppg)
        port_pair_group_ids.append(ppg_id)
    flow_classifier_ids = []
    for fc in flow_classifiers:
        fc_id = get_flow_classifier_id(fc)
        flow_classifier_ids.append(fc_id)    
    body_pc = {'port_chain' : {'port_pair_groups': port_pair_group_ids,
                                'flow_classifiers': flow_classifier_ids,
                                 'name': name}}
    neutron.create_port_chain(body=body_pc)
    print 'Port chain', name, 'has been created.'

def update_port_chain(name, port_pair_groups, flow_classifiers):
    pc_id = get_port_chain_id(name)
    if pc_id != -1:
        port_pair_group_ids = []
        for ppg in port_pair_groups:
            ppg_id = get_port_pair_group_id(ppg)
            port_pair_group_ids.append(ppg_id)
        flow_classifier_ids = []
        for fc in flow_classifiers:
            fc_id = get_flow_classifier_id(fc)
            flow_classifier_ids.append(fc_id)    
        body_pc = {'port_chain' : {'port_pair_groups': port_pair_group_ids,
                                    'flow_classifiers': flow_classifier_ids,
                                     'name': name}}
        neutron.update_port_chain(pc_id, body=body_pc)
        print 'Port chain', name, 'has been updated.'

def get_port_chain_id(name):
    for pc in neutron.list_port_chains()['port_chains']:
        if pc['name'] == name:
            return pc['id']
    print 'Port Chain', name,'does not exist.'
    return -1    

def delete_port_chain(name):
    pc_id = get_port_chain_id(name)
    if pc_id != -1:
        neutron.delete_port_chain(pc_id)
        print 'Port chain', name, 'has been deleted.' 


def list_servers():
    for s in conn.compute.servers():
        print s.name, s.id
            
def list_ports():
    for p in conn.network.ports():
        print p.name, p.id

def find_port(port_name):
    return conn.network.find_port(port_name)

def get_fixed_ip(port):
    return port.fixed_ips[0]['ip_address']+'/32'

def assign_floating_ip(server):
    if server is not None:
        print('Checking if Floating IP is already assigned to testing_instance...')
        testing_instance_floating_ip = None
        for values in server.addresses.values():
            for address in values:
                if address['OS-EXT-IPS:type'] == 'floating':
                    testing_instance_floating_ip = conn.network.find_ip(address['addr'])
    
        unused_floating_ip = None
        if not testing_instance_floating_ip:
            print('Checking for unused Floating IP...')
            for floating_ip in conn.network.ips():
                if not floating_ip.fixed_ip_address:
                    unused_floating_ip = floating_ip
                    break    
                     
        if not testing_instance_floating_ip and not unused_floating_ip:
            print('No free unused Floating IPs. Allocating new Floating IP...')
            public_network_id = conn.network.find_network('public').id
            try:
                unused_floating_ip = conn.network.create_ip(floating_network_id=public_network_id)
                unused_floating_ip = conn.network.get_ip(unused_floating_ip)
                print(unused_floating_ip)
            except exceptions.HttpException as e:
                print(e)
 
#print 'Hello OpenStack!'

# to delete server

### create server testing ###
#delete_port('p1')

#create_port('p_testing','private')

'''
delete_server('testing')
time.sleep(3)

image = 'cirros-0.3.4-x86_64-uec'
flavor = 'ds512M'
nics = ['p_testing']
create_server('testing', image, flavor, nics, None, 'compute1')
'''

#create_server('testing', image, flavor, nics, None)


# create p1 and p2
'''
image = 'cirros-0.3.4-x86_64-uec'
flavor = 'ds512M'
delete_port('p')
nics = ['p']
delete_server('vm')
#time.sleep(3)
#create_port('p','private')
#create_server('vm', image, flavor, nics, None)


delete_port('nf1_p1')
delete_port('nf1_p2')
delete_port('nf2_p1')
delete_port('nf2_p2')
delete_port('src_port')
delete_port('dst_port')

delete_server('nf1')
delete_server('nf2')
delete_server('src')
delete_server('dst')
'''

#userdata = '''#!/bin/bash
#sysctl -w net.ipv4.ip_forward=1
#apt-get -y install apache2
#apt-get -y install hping3
#'''
''' #### start

userdata_b64str = base64.b64encode(userdata)

create_port('p1','private')
create_port('p2','private')
create_port('p_src','private')
create_port('p_dst','private')

image = 'cirros-0.3.4-x86_64-uec'
flavor = 'ds512M'
nics = ['p1','p2']

create_server('srv1', image, flavor, nics, userdata_b64str)
create_server('src', image, flavor, ['p_src'], userdata_b64str)
create_server('dst', image, flavor, ['p_dst'], userdata_b64str)

# get ip of src and dst
p_src = find_port('p_src')
p_dst = find_port('p_dst')

src_ip = p_src.fixed_ips[0]['ip_address']+'/32'
dst_ip = p_dst.fixed_ips[0]['ip_address']+'/32'

print src_ip, '--> srv1 -->', dst_ip


delete_port_chain('pc')
delete_port_pair_group('ppg1')
delete_port_pair('pp1')
delete_flow_classifier('fc1')


create_flow_classifier('fc1', src_ip, dst_ip, 'ICMP', None, None, 'p_src')

ports = ['p1', 'p2']

create_port_pair('pp1', ports)

port_pairs = ['pp1']

create_port_pair_group('ppg1', port_pairs)
update_port_pair_group('ppg1', port_pairs)

port_pair_groups = ['ppg1']
flow_classifiers = ['fc1']

create_port_chain('pc', port_pair_groups, flow_classifiers)
update_port_chain('pc', port_pair_groups, flow_classifiers)

print 'Good bye'

# create chain from graph
# have samples of traffic 
''' #### end

'''    
create_port('p10','private')
create_port('p11','private')
create_port('p12','private')
image = 'cirros-0.3.4-x86_64-uec'
flavor = 'ds512M'
nics = ['p10','p11','p12']

create_server('server_test', image, flavor, nics)
'''

#delete_port_chain('pc')
#delete_port_pair_group('nf1_ppg1')
#delete_port_pair_group('nf1_ppg1')
#delete_port_pair('nf2_ppg1')
#delete_port_pair('nf2_pp1')
#delete_flow_classifier('fc1')

'''
delete_port_chain('pc')
delete_port_pair_group('ppg1')
delete_port_pair_group('ppg2')
delete_port_pair('nf1_pp1')
delete_port_pair('nf2_pp1')
delete_flow_classifier('fc1')
'''
'''
create_flow_classifier('fc1', '10.0.0.4/32', '10.0.0.10/32', 'ICMP', None, None, 'src1_p')
###
ports = ['nf1_p1', 'nf1_p2']
create_port_pair('nf1_pp1', ports)
port_pairs = ['nf1_pp1']
create_port_pair_group('ppg1', port_pairs)
###
ports = ['nf2_p1', 'nf2_p2']
create_port_pair('nf2_pp1', ports)
port_pairs = ['nf2_pp1']
create_port_pair_group('ppg2', port_pairs)
###
port_pair_groups = ['ppg2', 'ppg1']
flow_classifiers = ['fc1']
create_port_chain('pc', port_pair_groups, flow_classifiers)
'''

#print 'End of the program: sfc_utils.'


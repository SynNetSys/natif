'''
Created on 28 Sep 2017

@author: stack
'''
#import base64
import sfc_utils
import sfc_graph
import csv_examples
import collections

### environment definition
# define sources, destinations, and network functions  

# define structures - there should be a method to feed them - e.g. through a file
sources = {}
destinations = {}

nfs = {}
nf_instances = {}

flows = {}

brs = {} # branches of the chain
sub_brs = {}

# define sfc stuff
sfc_port_pairs = collections.defaultdict(list)
sfc_port_pair_group = collections.defaultdict(list)
sfc_port_chain = collections.defaultdict(list)

def data_generation():
    # example: 2 srcs, 2 nf, 1 dst
    sources['src1'] = {'name' : 'src1', 'ip' : 'tbd', 'flavor' : 'ds1G'} # id = name
    sources['src2'] = {'name' : 'src2', 'ip' : 'tbd', 'flavor' : 'ds1G'} # id = name
    sources['src3'] = {'name' : 'src3', 'ip' : 'tbd', 'flavor' : 'ds1G'} # id = name
    sources['src4'] = {'name' : 'src4', 'ip' : 'tbd', 'flavor' : 'ds1G'} # id = name
    sources['src5'] = {'name' : 'src5', 'ip' : 'tbd', 'flavor' : 'ds1G'} # id = name
    sources['src6'] = {'name' : 'src6', 'ip' : 'tbd', 'flavor' : 'ds1G'} # id = name
    
    
    #sources['src2'] = {'name' : 'src2', 'ip' : 'tbd', 'flavor' : 'ds1G'} 
    #sources['src3'] = {'name' : 'src3', 'ip' : 'tbd', 'flavor' : 'ds1G'} 
    '''
    sources['src4'] = {'name' : 'src4', 'ip' : 'tbd', 'flavor' : 'ds1G'} 
    sources['src5'] = {'name' : 'src5', 'ip' : 'tbd', 'flavor' : 'ds1G'} 
    sources['src6'] = {'name' : 'src6', 'ip' : 'tbd', 'flavor' : 'ds1G'} 
    '''
    #sources['src2'] = {'name' : 'src2', 'ip' : 'tbd', 'flavor' : 'ds1G'} 
    nfs['NAT'] = {'type' : 'act_h', 'gdf_h' : '1', 'gdf_p' : '1', 'cap_h' : 3000/7, 'cap_p' : 4.65, 'flavor' : 'ds1G', 'server' : 'A', 'instances' : ['FW1'], 'nb_instances' : 1, 'needed_cap_h' : 0, 'needed_cap_p' : 0}
    nfs['FW'] = {'type' : 'act_h', 'gdf_h' : '1', 'gdf_p' : '1', 'cap_h' : 3000/7, 'cap_p' : 4.65, 'flavor' : 'ds1G', 'server' : 'A', 'instances' : ['FW1'], 'nb_instances' : 1, 'needed_cap_h' : 0, 'needed_cap_p' : 0}
    nfs['IDS'] = {'type' : 'act_p', 'gdf_h' : '1', 'gdf_p' : '1', 'cap_h' : 3000/7, 'cap_p' : 4.65, 'flavor' : 'ds1G', 'server' : 'A', 'instances' : ['IDS1'], 'nb_instances' : 1, 'needed_cap_h' : 0, 'needed_cap_p' : 0}               
    
    brs['br1'] = ['NAT', 'FW', 'IDS'] # definition of the chain
    
    destinations['dst1'] = {'name' : 'dst1', 'ip' : 'tbd', 'flavor' : 'ds1G'}
    destinations['dst2'] = {'name' : 'dst2', 'ip' : 'tbd', 'flavor' : 'ds1G'}
    destinations['dst3'] = {'name' : 'dst3', 'ip' : 'tbd', 'flavor' : 'ds1G'}
    
    # flows - one source can emit more than a single flow
    # example: 2 flows from src1 to dst1, 1 flow from src2 to dst1
    flows['f1'] = {'src' : 'src1', 'dst' : 'dst1', 'pps' : 1000/9, 'thp' : 1.55, 'path' : 'br1'}
    flows['f2'] = {'src' : 'src2', 'dst' : 'dst1', 'pps' : 1000/9, 'thp' : 1.55, 'path' : 'br1'}
    flows['f3'] = {'src' : 'src3', 'dst' : 'dst2', 'pps' : 1000/7, 'thp' : 1.55, 'path' : 'br1'}
    flows['f4'] = {'src' : 'src4', 'dst' : 'dst2', 'pps' : 1000/7, 'thp' : 0.01, 'path' : 'br1'}
    flows['f5'] = {'src' : 'src5', 'dst' : 'dst3', 'pps' : 1000/7, 'thp' : 0.01, 'path' : 'br1'}
    flows['f6'] = {'src' : 'src6', 'dst' : 'dst3', 'pps' : 1000/7, 'thp' : 0.01, 'path' : 'br1'}

### setup the environment
'''
#!/bin/bash
sysctl -w net.ipv4.ip_forward=1
apt-get -y install apache2
apt-get -y install hping3
'''

#userdata = 
'''#!/bin/bash
sysctl -w net.ipv4.ip_forward=1
apt-get -y install hping3
apt-get -y install tcpdump
'''
#userdata_b64str = base64.b64encode(userdata)

userdata_host = '/opt/stack/user_data_host.sh'
userdata_nf = '/opt/stack/user_data_nf.sh'

#create sources by calling sfc_utils subroutines
image = 'ubuntu-1404'
#image = 'cirros-0.3.4-x86_64-uec'
# flavor = ['ds1G', 'ds2G', 'ds3G']
# servers = ['compute1', 'compute2']

#sfc_utils.delete_port('src2_p')
#sfc_utils.delete_server('src2')


def cleanup_sfc():
    # delete port chains
    '''
    for br_id in brs.keys():
        port_chain_name = str('pc_'+br_id)
        sfc_utils.delete_port_chain(port_chain_name)
    '''
    # delete port chains
    for sbr_id in sub_brs.keys():
        port_chain_name = str('pc_'+sbr_id)
        sfc_utils.delete_port_chain(port_chain_name)
    
    # delete port pair groups
    '''
    for nf in brs[br_id]:
        port_pair_group_name = str('ppg_'+nf)
        sfc_utils.delete_port_pair_group(port_pair_group_name)
    '''
    # delete port pair groups
    for sbr_id in sub_brs.keys():
        for nf in sub_brs[sbr_id]:
            port_pair_group_name = str('ppg_'+nf)
            sfc_utils.delete_port_pair_group(port_pair_group_name)
    
           
    # delete port pairs
    for sbr_id in sub_brs.keys():
        for nf in sub_brs[sbr_id]:   
            port_pair_name = str('pp_'+nf)
            sfc_utils.delete_port_pair(port_pair_name)
    
    # delete flow classifiers
    '''
    for flow_id in flows.keys():
        for br_id in brs.keys():
                fc_name = str('fc_'+flow_id+'_'+br_id)
                sfc_utils.delete_flow_classifier(fc_name)
    '''
    # delete flow classifiers
    for flow_id in flows.keys():
        for sbr_id in sub_brs.keys():
                fc_name = str('fc_'+flow_id+'_'+sbr_id)
                sfc_utils.delete_flow_classifier(fc_name)            
    

def cleanup_hosts():
    # delete source hosts
    for s in sources.keys():
        sp = str(s+'_p')
        sfc_utils.delete_port(sp)                                                                                                                                                                         
        sfc_utils.delete_server(s)
        
    # delete destination hosts
    for s in destinations.keys():
        sp = str(s+'_p')
        sfc_utils.delete_port(sp)
        sfc_utils.delete_server(s)
        
    # delete nf hosts
    for s in nfs.keys():
        #print nfs[s]
        if nfs[s]['nb_instances'] == 1:
            si = str(s+'1')    
            p1 = str(si+'_p1')
            p2 = str(si+'_p2')
            sfc_utils.delete_port(p1)
            sfc_utils.delete_port(p2)
            sfc_utils.delete_server(si) 
        else:
            for nf in nfs[s]['instances']:   
                p1 = str(nf+'_p1')
                p2 = str(nf+'_p2')
                sfc_utils.delete_port(nf)
                sfc_utils.delete_port(nf)
                sfc_utils.delete_server(nf)                  
 
   
def create_src_hosts():
    for s in sources.keys():
        #create the nic - always on the private network
        sp = str(s+'_p')
        
        sfc_utils.create_port(sp,'private')
        sfc_utils.create_server(s, image, sources[s]['flavor'], [sp], userdata_host, 'compute1')
        #sfc_utils.assign_floating_ip(server)
        
        port = sfc_utils.find_port(sp)
        s_ip = sfc_utils.get_fixed_ip(port)
        sources[s]['ip'] = s_ip
        #print s_ip
        print sources[s]
    
    print '****** Source hosts instantiation completed ******'

def create_dst_hosts():      
    for s in destinations.keys():
        
        #create the nic - always on the private network
        sp = str(s+'_p')
        
        sfc_utils.create_port(sp,'internal')
        sfc_utils.create_server(s, image, destinations[s]['flavor'], [sp], userdata_host, 'compute1')
        #sfc_utils.assign_floating_ip(server)
        
        port = sfc_utils.find_port(sp)
        s_ip = sfc_utils.get_fixed_ip(port)
        destinations[s]['ip'] = s_ip
        #print s_ip
        print destinations[s]
    
    print '****** Destination hosts instantiation completed ******'


def create_nfs():
    for s in nfs.keys():
        #print nfs[s]
        for nf in nfs[s]['instances']:  
            #si = str(s+'1') 
            p1 = str(nf+'_p1')
            p2 = str(nf+'_p2')
            
            
            if s == 'NAT':
                sfc_utils.create_port(p1,'private')
                ip = sfc_utils.get_fixed_ip(sfc_utils.find_port(p1))
                nf_instances[nf]['ip_in'] = ip
                sfc_utils.create_port(p2,'internal')
                ip = sfc_utils.get_fixed_ip(sfc_utils.find_port(p2))
                nf_instances[nf]['ip_out'] = ip
                image = 'pfSense'
                userdata = userdata_nf
                sfc_utils.create_server(nf, image, nfs[s]['flavor'], [p1, p2], userdata, 'compute2')
            elif s == 'FW':
                sfc_utils.create_port(p1,'internal')
                ip = sfc_utils.get_fixed_ip(sfc_utils.find_port(p1))
                nf_instances[nf]['ip_in'] = ip
                sfc_utils.create_port(p2,'internal')
                ip = sfc_utils.get_fixed_ip(sfc_utils.find_port(p2))
                nf_instances[nf]['ip_out'] = ip
                image = 'pfSense'
                userdata = userdata_nf
                sfc_utils.create_server(nf, image, nfs[s]['flavor'], [p1, p2], userdata, 'compute2')               
            else: # it means it's an IDS
                sfc_utils.create_port(p1,'internal')
                ip = sfc_utils.get_fixed_ip(sfc_utils.find_port(p1))
                nf_instances[nf]['ip_in'] = ip
                sfc_utils.create_port(p2,'internal')
                ip = sfc_utils.get_fixed_ip(sfc_utils.find_port(p2))
                nf_instances[nf]['ip_out'] = ip
                #p3 = str(nf+'_interface') # used for testing - accessible by the WAN network
                #sfc_utils.create_port(p3,'private')
                userdata = userdata_host
                image = 'ubuntu-1404'
                sfc_utils.create_server(nf, image, nfs[s]['flavor'], [p1, p2], userdata, 'compute2')
            
            #sfc_utils.create_server(nf, image, nfs[s]['flavor'], [p1, p2], userdata, 'compute2')

        #sfc_utils.assign_floating_ip(server)
    
        #port = sfc_utils.find_port(str(s+'_p'))
        #s_ip = sfc_utils.get_fixed_ip(port)
        #distinations[s]['ip'] = s_ip
        #print s_ip      
    
    print '****** NF instantiation completed ******' 

def steer_flow(flow_id, sbr_id, from_src):
    #get the flow:
    print flow_id, flows[flow_id]
    #print sbr_id, sub_brs[sbr_id]
    #print 'Objective: steer the flow', flow_id, 'through', sbr_id,'=', sub_brs[sbr_id],'===',
    src_ip = sources[flows[flow_id]['src']]['ip']
    dst_ip = destinations[flows[flow_id]['dst']]['ip'] # exceptionnaly: the destination is a source
    protocol = 'ICMP'
    src_port = None
    dst_port = None
    if from_src:
        src_srv_port = str(from_src + '_p2')
    else:
        src_srv_name = flows[flow_id]['src']
        src_srv_port = str(src_srv_name + '_p') # the port of the source host of the flow, any src/dst has only one port
        
    fc_name = str('fc_'+flow_id+'_'+sbr_id)
    #create the flow classifier
    # for nat - ids, the src_port should be nat's one
    #if sub_brs[sbr_id][0].startswith('NAT'):
    print fc_name, src_ip, dst_ip, protocol, src_port, dst_port, src_srv_port 
    sfc_utils.create_flow_classifier(fc_name, src_ip, dst_ip, protocol, src_port, dst_port, src_srv_port)
    
    #flow_classifiers = [fc_name]
    floating_port = None
    #create the port pairs of each nf in br whose id is br_id
    port_pair_groups = []
    for nf in sub_brs[sbr_id]:
        #print 'list of ports for', nf
        ports = [str(nf+'_p1'), str(nf+'_p2')]
        port_pair_name = str('pp_'+nf) 
        print ports
        
        # floating ports used to finalise the steering 
        
        if str(nf).startswith('IDS'): #only for ids, pfsense doesn't need
            floating_port = str(nf+'_p1')
        
        # create port pair for nf
        if port_pair_name not in sfc_port_pairs[nf]:
            sfc_port_pairs[nf].append(port_pair_name)
            sfc_utils.create_port_pair(port_pair_name, ports)
        # create port pair group of nf - in this case, only one instance for nf
        port_pairs = [port_pair_name]
        # create port pair group, it contains only one port pair
        port_pair_group_name = str('ppg_'+nf)
        if port_pair_group_name not in sfc_port_pair_group[nf]:
            sfc_port_pair_group[nf].append(port_pair_group_name)
            sfc_utils.create_port_pair_group(port_pair_group_name, port_pairs)
        # append the new port pair group to the list port_pair_groups to be used in the port_chain (for one branch)
        port_pair_groups.append(port_pair_group_name)
    
    port_chain_name = str('pc_'+sbr_id) 
    if port_chain_name in sfc_port_chain.keys():
        #sfc_port_chain[port_chain_name][port_pair_groups] = port_pair_groups
        if fc_name not in sfc_port_chain[port_chain_name]:
            sfc_port_chain[port_chain_name].append(fc_name)
        flow_classifiers = sfc_port_chain[port_chain_name]
        print 'flow classifier:', flow_classifiers
        print 'port pair groups:', port_pair_groups
        sfc_utils.update_port_chain(port_chain_name, port_pair_groups, flow_classifiers)
    else:
        sfc_port_chain[port_chain_name].append(fc_name)
        flow_classifiers = sfc_port_chain[port_chain_name]
        print 'flow classifier:', flow_classifiers
        print 'port pair groups:', port_pair_groups
        sfc_utils.create_port_chain(port_chain_name, port_pair_groups, flow_classifiers)
    
    print 'Objective: steer the flow', flow_id, 'through', sbr_id,'=', sub_brs[sbr_id],'===',
    print src_ip, dst_ip, protocol, src_port, dst_port
    if floating_port:
        print 'Run the following on IDS only..', sub_brs[sbr_id] 
        #print 'ip route add', src_ip, 'dev eth0'
        #print 'ip route add', dst_ip, 'dev eth1'
        sfc_utils.finalise_steering(floating_port, src_ip.split('/', 1)[0], dst_ip.split('/', 1)[0])

        
    

if __name__ == '__main__':

    #data_generation()
      
    csv_examples.import_topo(sources, destinations, nfs, brs, flows, sub_brs, nf_instances)
    #sub_brs = sfc_graph.get_sub_brs(nfs, brs) # should run after the instantiation algorithm 
    nf_instances = sfc_graph.get_nf_instances(nfs) # should run after the instantiation algorithm
        
    cleanup_sfc()
    #cleanup_hosts()
    
    #create_src_hosts()
    #create_dst_hosts()
    #create_nfs()
    
    steer_flow('f1', 'sub_ids', 'NAT1')
    steer_flow('f2', 'sub_ids', 'NAT1')
    steer_flow('f3', 'sub_ids', 'NAT1')
    steer_flow('f4', 'sub_ids', 'NAT1')
    steer_flow('f5', 'sub_ids', 'NAT1')
    steer_flow('f6', 'sub_ids', 'NAT1')

    '''
    #p1s1 - good
    steer_flow('f1', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f2', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f3', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f4', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f5', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f6', 'nat1_fw1_ids1', 'NAT1')
    '''
    
    '''
    #p2s1 - useless
    steer_flow('f1', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f2', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f3', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f4', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f5', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f6', 'nat1_fw1_ids1', 'NAT1')   
    '''
    '''
    #p3s1 - useless
    steer_flow('f1', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f2', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f3', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f4', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f5', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f6', 'nat1_fw1_ids1', 'NAT1')  
    '''
        
    '''
    #p1s2 - good - done
    steer_flow('f1', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f2', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f3', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f4', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f5', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f6', 'nat1_fw1_ids1', 'NAT1')
    '''
    
    '''
    #p2s2 - good - done
    steer_flow('f1', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f2', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f3', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f4', 'nat2_fw2_ids2', 'NAT2')
    steer_flow('f5', 'nat2_fw2_ids2', 'NAT2')
    steer_flow('f6', 'nat2_fw2_ids2', 'NAT2')   
    '''
    
    '''
    #p3s2 - good - done
    steer_flow('f1', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f2', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f3', 'nat2_fw2_ids2', 'NAT2')
    steer_flow('f4', 'nat2_fw2_ids2', 'NAT2')
    steer_flow('f5', 'nat2_fw2_ids2', 'NAT2')
    steer_flow('f6', 'nat2_fw2_ids2', 'NAT2')  
    '''

    '''
    #p1s3 - good - done
    steer_flow('f1', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f2', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f3', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f4', 'nat2_fw2_ids1', 'NAT2')
    steer_flow('f5', 'nat2_fw2_ids1', 'NAT2')
    steer_flow('f6', 'nat2_fw2_ids1', 'NAT2')
    '''
    '''
    #p2s3 - good - done
    steer_flow('f1', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f2', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f3', 'nat2_fw2_ids2', 'NAT2')
    steer_flow('f4', 'nat2_fw2_ids2', 'NAT2')
    steer_flow('f5', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f6', 'nat2_fw2_ids2', 'NAT2')   
    '''
    
    '''
    #p3s3 - good - done
    steer_flow('f1', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f2', 'nat2_fw2_ids2', 'NAT2')
    steer_flow('f3', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f4', 'nat1_fw1_ids1', 'NAT1')
    steer_flow('f5', 'nat2_fw2_ids2', 'NAT2')
    steer_flow('f6', 'nat2_fw2_ids2', 'NAT2')  
    '''


    
    '''
    steer_flow('f1', 'sub_br0', 'NAT1')
    steer_flow('f2', 'sub_br0', 'NAT1')
    steer_flow('f3', 'sub_br0', 'NAT1')
    steer_flow('f4', 'sub_br0', 'NAT1')
    steer_flow('f5', 'sub_br0', 'NAT1')
    steer_flow('f6', 'sub_br0', 'NAT1')
    '''
   
    '''
    steer_flow('f1', 'sub_ids', 'FW1')
    steer_flow('f2', 'sub_ids', 'FW1')
    steer_flow('f3', 'sub_ids', 'FW1')
    steer_flow('f4', 'sub_ids', 'FW1')
    steer_flow('f5', 'sub_ids', 'FW1')
    steer_flow('f6', 'sub_ids', 'FW1')
    '''
    
    '''
    steer_flow('f1', 'sub_ids')
    steer_flow('f2', 'sub_ids')
    steer_flow('f3', 'sub_ids')
    steer_flow('f4', 'sub_ids')
    steer_flow('f5', 'sub_ids')
    steer_flow('f6', 'sub_ids')
    '''
    #steer_flow('f1', 'sub_br0', 'FW1')
    
    '''
    steer_flow('f1', 'sub_fw', 'FW1')
    steer_flow('f2', 'sub_fw')
    steer_flow('f3', 'sub_fw')
    steer_flow('f4', 'sub_fw')
    steer_flow('f5', 'sub_fw')
    steer_flow('f6', 'sub_fw')
    '''
    csv_examples.export_topo(sources, destinations, nfs, brs, flows, sub_brs, nf_instances)
    
    #steer_flow('f1', 'br1')
    #steer_flow('f2', 'br1')
    #steer_flow('f3', 'br1')
    
    print 'End of the program: Orchestrator.'




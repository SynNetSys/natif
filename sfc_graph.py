'''
Created on 4 Aug 2017

@author: stack
'''
import itertools
import random
import networkx as nx
import matplotlib.pyplot as plt
import math
import collections
    
'''
def example_chain_b():
    g = nx.DiGraph()
    
    fixed_positions = {'a':(0,0),'b':(0.2,0.3),'c':(0.2,-0.3), 'd':(0.4,0.3),'e':(0.4,-0.1),'f':(0.4,-0.3),'g':(0.6,0)}
    
    fixed_nodes = fixed_positions.keys()
    
    g.add_nodes_from(['a','b','c','d','e','f','g'])
    g.add_edges_from([('a','b'), ('a','c'), ('b','d'), ('c','e'), ('c','f'), ('d','g'), ('e','g'), ('f','g')])
    
    i = 1
    for branch in nx.all_simple_paths(g, source='a', target='g'):
        print'Branch:',i, branch
        i=i+1 
    
    pos=nx.spring_layout(g,pos=fixed_positions, fixed = fixed_nodes) # positions for all nodes
    
    # nodes
    nx.draw_networkx_nodes(g,pos,node_size=1000)
    
    # edges
    nx.draw_networkx_edges(g,pos,edgelist=g.edges(), width=2)
    
    # labels
    nx.draw_networkx_labels(g,pos,font_size=20,font_family='sans-serif')
    
    labels = nx.get_edge_attributes(g,'weight')
    nx.draw_networkx_edge_labels(g,pos,edge_labels=labels)
    
    
    #nx.draw_random(g,with_labels=True)
    plt.draw()
    plt.show()


def example_chain_sb():
    g = nx.DiGraph()
   
    g.add_nodes_from(['a','b1','b2','c1','c2','d','e','f','g'])
    g.add_edges_from([('a','b1'), ('a','b2'), ('a','c1'), ('a','c2'), ('b1','d'), ('b2','d'), 
                      ('c1','e'), ('c2','e'), ('c1','f'), ('c2','f'), ('d','g'), ('e','g'), ('f','g')])
    
    fixed_positions = {'a':(0,0),'b1':(0.2,0.3),'b2':(0.2,0.1),'c1':(0.2,-0.3),'c2':(0.2,-0.1),'d':(0.4,0.3),'e':(0.4,-0.1),'f':(0.4,-0.3),'g':(0.6,0)}
    
    fixed_nodes = fixed_positions.keys()
    
    # branches
    i = 1
    for branch in nx.all_simple_paths(g, source='a', target='g'):
        print'Sub branch:',i, branch
        i=i+1 
    
    pos=nx.spring_layout(g,pos=fixed_positions, fixed = fixed_nodes) # positions for all nodes
    
    # nodes
    nx.draw_networkx_nodes(g,pos,node_size=1000)
    
    # edges
    nx.draw_networkx_edges(g,pos,edgelist=g.edges(), width=2)
    
    # labels
    nx.draw_networkx_labels(g,pos,font_size=20,font_family='sans-serif')
    
    labels = nx.get_edge_attributes(g,'weight')
    nx.draw_networkx_edge_labels(g,pos,edge_labels=labels)
    
    
    #nx.draw_random(g,with_labels=True)
    plt.draw()
    plt.show()
    
'''

def define_sfc_graph():
    # list of network functions + list of instances
    nfs = {}
    brs = {}
    
    for nf_id in 'a', 'b', 'c', 'd', 'e', 'f', 'g':
        pps = random.randint(100, 200) # number of packets per second
        thp = random.randint(500, 1000) # throughput
        gdf_h = round(random.uniform(0.8, 2),2) # gain drop factor - in case it is known
        gdf_p = round(random.uniform(0.8, 2),2) # gain drop factor - in case it is known
        nf_type = random.choice(['act_h', 'act_p']) # header handler or payload handler
        nfs[nf_id] = {'type' : nf_type, 'gdf_h' : gdf_h, 'gdf_p' : gdf_p, 'cap_h' : pps, 'cap_p' : thp, 'server' : 'A', 'instances' : [], 'nb_instances' : 1, 'needed_cap_h' : 0, 'needed_cap_p' : 0}
    
    # no sub branches at the moment, will be added later 
    #nfs['d']['instances'] = ['d1', 'd2']
    #nfs['a']['instances'] = ['a1', 'a2', 'a3']
   
    # list of links or branches
    brs['br1'] = ['a', 'c', 'e', 'g']
    brs['br2'] = ['a', 'c', 'f', 'g']
    brs['br3'] = ['a', 'b', 'd', 'g']
    
    return (nfs, brs)

def get_sub_brs(nfs, brs):
    #list of sub branches 
    sbrs = {}
    i = 0
    for br in brs.keys():
        newbr = []
        for b in brs[br]:
            if len(nfs[b]['instances']) > 0:
                newbr.append(nfs[b]['instances'])
            else:
                newbr.append(b)
        for p in list(itertools.product(*newbr)):
            sbrs['sub_br'+str(i)] = list(p)
            i = i + 1
            
    return sbrs

def get_nf_instances(nfs):
    #list of sub branches 
    nf_instances = {}
    i = 0
    for nf in nfs.keys():
        for i in nfs[nf]['instances']:
            nf_instances[i] = {'ip_in' : 'tbd', 'ip_out' : 'tbd', 'nf' : nf}
      
    return nf_instances
        
def simulate_flows(brs):
    flows = {}
    for i in range(10):
        pps = random.randint(10, 50)
        thp = random.randint(20, 200)
        br = random.choice(brs.keys())
        flows['f'+str(i)] = {'pps' : pps, 'thp' : thp, 'path' : br}
    
    return flows
    #for f in flows.keys():
    #    print f, flows[f]


def accommodate_flows(flows, brs, nfs): # only scaling in/out -- scaling up/down to be done    
    # calculate the equivalent flow on each branch/path
    flows_eq = {}
    for br_key in brs.keys():
        flows_eq[br_key] = {'pps' : 0, 'thp' : 0, 'path' : br_key}
        #print flows_eq[br_key]
                
    for f_key in flows.keys():
        br_key = flows[f_key]['path']
        #print 'br_key', br_key, 'f_key', f_key
        flows_eq[br_key]['pps'] = flows_eq[br_key]['pps'] + flows[f_key]['pps']
        flows_eq[br_key]['thp'] = flows_eq[br_key]['thp'] + flows[f_key]['thp']
        

        
    for br_key in brs.keys():
        #print '-----------', br_key, brs[br_key], '-----------'
        #print '----------- flow entering', br_key, flows_eq[br_key], '-----------'
        new_flow_pps = float(flows_eq[br_key]['pps'])
        new_flow_thp = float(flows_eq[br_key]['thp'])
        #pps_ok = True
        #thp_ok = True
        for nf in brs[br_key]:
            #print nf, '| type -', nfs[nf]['type'], '| cap_h -', 
            #print nfs[nf]['cap_h'], '| cap_p -', nfs[nf]['cap_p'],
            #print '| gdf_h -', nfs[nf]['gdf_h'],'| gdf_p -', nfs[nf]['gdf_p'],
            #print '| fout_h -', round(new_flow_pps * nfs[nf]['gdf_h'], 2),
            #print '| fout_p -', round(new_flow_thp * nfs[nf]['gdf_p'], 2), '|',
            nfs[nf]['needed_cap_p'] = round(nfs[nf]['needed_cap_p'] + new_flow_thp,2)
            #print '***', nfs[nf]['needed_cap_p']
            new_flow_thp = new_flow_thp * nfs[nf]['gdf_p']
            
            nfs[nf]['needed_cap_h'] = round(nfs[nf]['needed_cap_h'] + new_flow_pps,2)
            new_flow_pps = new_flow_pps * nfs[nf]['gdf_h']
            
            '''
            if nfs[nf]['type'] == 'act_h' and new_flow_pps > nfs[nf]['cap_h']:
                #nb_instances = int(math.ceil(round(new_flow_pps,2)/nfs[nf]['cap_h']))
                #print '***', round(new_flow_pps,2), '/' , nfs[nf]['cap_h'], '*** NOK needs', nb_instances, 'instances'
                #new_flow_pps = nfs[nf]['cap_h'] * nfs[nf]['gdf_h']
                nfs[nf]['needed_cap_h'] = round(nfs[nf]['needed_cap_h'] + new_flow_pps,2)
                #print '***', nfs[nf]['needed_cap_h']
                new_flow_pps = new_flow_pps * nfs[nf]['gdf_h']
                
                nfs[nf]['needed_cap_p'] = round(nfs[nf]['needed_cap_p'] + new_flow_thp,2)
                new_flow_thp = new_flow_thp * nfs[nf]['gdf_p']
      
                pps_ok = False
            else:
                nfs[nf]['needed_cap_h'] = round(nfs[nf]['needed_cap_h'] + new_flow_pps,2)
                #print '***', nfs[nf]['needed_cap_h']
                new_flow_pps = new_flow_pps * nfs[nf]['gdf_h']
                
                nfs[nf]['needed_cap_p'] = round(nfs[nf]['needed_cap_p'] + new_flow_thp,2)
                new_flow_thp = new_flow_thp * nfs[nf]['gdf_p']
                
                pps_ok = True
            if nfs[nf]['type'] == 'act_p' and new_flow_thp > nfs[nf]['cap_p']:
                #nb_instances = int(math.ceil(round(new_flow_thp,2)/nfs[nf]['cap_p']))
                #print '***', round(new_flow_thp,2), '/' , nfs[nf]['cap_p'], '*** NOK needs', nb_instances, 'instances'
                #new_flow_thp = nfs[nf]['cap_p'] * nfs[nf]['gdf_p']
                nfs[nf]['needed_cap_p'] = round(nfs[nf]['needed_cap_p'] + new_flow_thp,2)
                #print '***', nfs[nf]['needed_cap_p']
                new_flow_thp = new_flow_thp * nfs[nf]['gdf_p']
                
                nfs[nf]['needed_cap_h'] = round(nfs[nf]['needed_cap_h'] + new_flow_pps,2)
                new_flow_pps = new_flow_pps * nfs[nf]['gdf_h']

                thp_ok = False
            else:
                nfs[nf]['needed_cap_p'] = round(nfs[nf]['needed_cap_p'] + new_flow_thp,2)
                #print '***', nfs[nf]['needed_cap_p']
                new_flow_thp = new_flow_thp * nfs[nf]['gdf_p']
                
                nfs[nf]['needed_cap_h'] = round(nfs[nf]['needed_cap_h'] + new_flow_pps,2)
                new_flow_pps = new_flow_pps * nfs[nf]['gdf_h']
                
                thp_ok = True
            if pps_ok and thp_ok:
                print '*** OK, no need for additional instances'
            ''' 
            # there is a strong dependency between in the chain as each one has a gain drop factor that determines the outgoing traffic to the next NF  
            # there are global and local solutions, depending on how to determine the incoming/outgoing traffic according to the gain drop factor
            # we work on global solution - affecting the whole chain             
            #flows_eq[br_key]['pps']*nfs[nf]['gdf']
            
            # if sum of flows cannot by served by the current nf instances --> scaling out 
            #    if one flow cannot by served by any of the nf instances --> scaling up

    # calculate the number of needed instances
    for nf in nfs.keys():
        if nfs[nf]['type'] == 'act_h':
            nb_instances = int(math.ceil(nfs[nf]['needed_cap_h']/nfs[nf]['cap_h']))
            nfs[nf]['nb_instances'] = nb_instances
            nfs[nf]['instances'] = []
            for i in range(1,nb_instances+1):
                    #print nf + str(i)
                    nfs[nf]['instances'].append(nf + str(i))
        else:
            nb_instances = int(math.ceil(nfs[nf]['needed_cap_p']/nfs[nf]['cap_p']))
            nfs[nf]['nb_instances'] = nb_instances
            nfs[nf]['instances'] = []
            for i in range(1,nb_instances+1):
                    #print nf + str(i)
                    nfs[nf]['instances'].append(nf + str(i))


def mixed_order_h(a):
    return ( a[1], a[2] ) 

def mixed_order_t(a):
    return ( a[2], a[1] ) 

def map_flows(flows, brs, nfs):
    #print 'Begin flow mapping'
    # solution # 
    # update the needed capacity for each nf
    # afterwards, determine the needed instances
    # go through each nf and perform the mapping between it and ALL its traversing flows
    
    # get list of flows on branches
    flows_on_br = collections.defaultdict(list)
    for f in flows.keys():
        flows_on_br[flows[f]['path']].append((f,flows[f]['pps'],flows[f]['thp']))
    
    # get list of nfs with their traversing flows
    flows_on_nf = collections.defaultdict(list) 
    for br_key in flows_on_br.keys():
        flows_on_a_br = flows_on_br[br_key]
        #print br_key, flows_on_a_br
        for nf in brs[br_key]:
            for f in flows_on_a_br:
                flows_on_nf[nf].append(f)             
            if nfs[nf]['type'] == 'act_h': 
                flows_on_nf[nf].sort(key=mixed_order_h, reverse=True)
            else:
                flows_on_nf[nf].sort(key=mixed_order_t, reverse=True)
                                         
    # attach information to the new instances
    instances = collections.defaultdict(list) 
    for nf in nfs.keys():
        for i in nfs[nf]['instances']:
            instances[nf].append([i, nfs[nf]['cap_h'], nfs[nf]['cap_p']])
    

    flow_paths = collections.defaultdict(list)
    for fnf in flows_on_nf.keys():
        #print 'NF', fnf
        #print 'flows_on_nf',flows_on_nf[fnf]
        #print 'instances of', fnf, instances[fnf]
        #print nfs[fnf]['type']
        
        #number of flows traversing fnf
        nb_flows = len(flows_on_nf[fnf])
        negligibility_h  = 10 # it means if the ratio is above 100, the flow traversing the nf doesn't have a considerable on the nf performance is it's mapped based on the packet rate
        negligibility_p  = 10 # same as above but considering the throughput
        
        
        
        # start mapping -- strategy: bigger flows get accommodated first on the nf that has the max available capacity
        for f in flows_on_nf[fnf]:
            if nfs[fnf]['type'] == 'act_h':
                # f[1] : rate
                # f[2] : throughput
                # instances[fnf][0][1] : cap_h of fnf
                # instances[fnf][0][2] : cap_p of fnf
                if instances[fnf][0][1]/(f[1]*nb_flows) > negligibility_h:
                    #then the flow is negligible comparing to the nf cap_h (packet rate capacity)  
                    # check the flow negligibility towards the throughput capacity
                    if instances[fnf][0][2]/(f[2]*nb_flows) > negligibility_p:
                        # the flow is still negligible for the throughput
                        # so let's distribute it based on the nf type (header-handler)               
                        instances[fnf].sort(key=lambda x: x[1], reverse=True)
                        flow_paths[f[0]].append((fnf, instances[fnf][0][0]))
                        old_cap_h = instances[fnf][0][1]
                        old_cap_p = instances[fnf][0][2]
                        instances[fnf][0][1] = old_cap_h - f[1]
                        instances[fnf][0][2] = old_cap_p - f[2]
                    else: 
                        # then distribute it based on the throughput as it's not negligible for the throughput but it is for the packet rate
                        instances[fnf].sort(key=lambda x: x[2], reverse=True)
                        flow_paths[f[0]].append((fnf, instances[fnf][0][0]))
                        old_cap_h = instances[fnf][0][1]
                        old_cap_p = instances[fnf][0][2]
                        instances[fnf][0][1] = old_cap_h - f[1]
                        instances[fnf][0][2] = old_cap_p - f[2]
                else: # the flow is not negligible based on the nf category
                    instances[fnf].sort(key=lambda x: x[1], reverse=True)
                    flow_paths[f[0]].append((fnf, instances[fnf][0][0]))
                    old_cap_h = instances[fnf][0][1]
                    old_cap_p = instances[fnf][0][2]
                    instances[fnf][0][1] = old_cap_h - f[1]
                    instances[fnf][0][2] = old_cap_p - f[2]                                 
            else: # same logic applies for payload-handler nf - inversely
                if instances[fnf][0][2]/(f[2]*nb_flows) > negligibility_p:
                    if instances[fnf][0][1]/(f[1]*nb_flows) > negligibility_h:             
                        instances[fnf].sort(key=lambda x: x[2], reverse=True)
                        flow_paths[f[0]].append((fnf, instances[fnf][0][0]))
                        old_cap_h = instances[fnf][0][1]
                        old_cap_p = instances[fnf][0][2]
                        instances[fnf][0][1] = old_cap_h - f[1]
                        instances[fnf][0][2] = old_cap_p - f[2]
                    else: 
                        instances[fnf].sort(key=lambda x: x[1], reverse=True)
                        flow_paths[f[0]].append((fnf, instances[fnf][0][0]))
                        old_cap_h = instances[fnf][0][1]
                        old_cap_p = instances[fnf][0][2]
                        instances[fnf][0][1] = old_cap_h - f[1]
                        instances[fnf][0][2] = old_cap_p - f[2]
                else: 
                    instances[fnf].sort(key=lambda x: x[2], reverse=True)
                    flow_paths[f[0]].append((fnf, instances[fnf][0][0]))
                    old_cap_h = instances[fnf][0][1]
                    old_cap_p = instances[fnf][0][2]
                    instances[fnf][0][1] = old_cap_h - f[1]
                    instances[fnf][0][2] = old_cap_p - f[2]     
                
                
                '''
                print f
                instances[fnf].sort(key=lambda x: x[2], reverse=True)
                flow_paths[f[0]].append((fnf, instances[fnf][0][0]))
                old_cap_h = instances[fnf][0][1]
                old_cap_p = instances[fnf][0][2]
                instances[fnf][0][1] = old_cap_h - f[1]
                instances[fnf][0][2] = old_cap_p - f[2]              
                '''
    
    

    
    return flow_paths
    
    #for f in flows.keys():
    #    print f, brs[flows[f]['path']]
        
    # order flow_paths now and it is done
    

        
#example_chain_b()
#example_chain_sb()

'''
(nfs, brs)  = define_sfc_graph()
flows = simulate_flows(brs)
print 'Accommodate flows'
accommodate_flows(flows, brs, nfs)
map_flows(flows, brs, nfs)

for nf in nfs.items():
    print nf
'''
        
        
'''
print 'List of NF'
for nf in nfs.items():
    print nf 

print 'List of branches'
for br in brs.items():
    print br

print 'List of flows'
flows = simulate_flows(brs)
for f in flows.keys():
    print f, flows[f]['pps']
'''

'''
print 'List of NF'
for nf in nfs.items():
    print nf 

print 'List of NF'
for nf in nfs.items():
    print nf 

print 'List of sub branches'
sbrs = get_sub_brs(nfs, brs)
for sbr in sbrs.items():
    print sbr
'''


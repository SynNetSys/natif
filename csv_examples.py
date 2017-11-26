'''
Created on 6 Oct 2017

@author: stack
'''
#import base64
import collections
import csv
import sfc_graph
import sfc_graph_thp_based
import sfc_graph_greedy

import random, string, time
import itertools

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

def initialise():
    sources = {}
    destinations = {}
    
    nfs = {}
    nf_instances = {}
    
    flows = {}
    
    brs = {} # branches of the chain
    sub_brs = {}


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
    #nfs['FW'] = {'type' : 'act_h', 'gdf_h' : 1, 'gdf_p' : 1, 'cap_h' : 2000, 'cap_p' : 2000, 'flavor' : 'ds1G', 'server' : 'A', 'instances' : ['FW1'], 'nb_instances' : 1, 'needed_cap_h' : 0, 'needed_cap_p' : 0}
    #nfs['IDS'] = {'type' : 'act_p', 'gdf_h' : 1, 'gdf_p' : 1, 'cap_h' : 2000, 'cap_p' : 2000, 'flavor' : 'ds1G', 'server' : 'A', 'instances' : ['IDS1'], 'nb_instances' : 1, 'needed_cap_h' : 0, 'needed_cap_p' : 0}
    nfs['NAT'] = {'type' : 'act_h', 'gdf_h' : 1, 'gdf_p' : 1, 'cap_h' : 3000/7, 'cap_p' : 4.65, 'flavor' : 'ds1G', 'server' : 'A', 'instances' : ['NAT1'], 'nb_instances' : 1, 'needed_cap_h' : 0, 'needed_cap_p' : 0}
    nfs['FW'] = {'type' : 'act_h', 'gdf_h' : 1, 'gdf_p' : 1, 'cap_h' : 3000/7, 'cap_p' : 4.65, 'flavor' : 'ds1G', 'server' : 'A', 'instances' : ['FW1'], 'nb_instances' : 1, 'needed_cap_h' : 0, 'needed_cap_p' : 0}
    nfs['IDS'] = {'type' : 'act_p', 'gdf_h' : 1, 'gdf_p' : 1, 'cap_h' : 3000/7, 'cap_p' : 4.65, 'flavor' : 'ds1G', 'server' : 'A', 'instances' : ['IDS1'], 'nb_instances' : 1, 'needed_cap_h' : 0, 'needed_cap_p' : 0}               
      
    brs['br1'] = ['NAT', 'FW', 'IDS'] # definition of the chain
    
    destinations['dst1'] = {'name' : 'dst1', 'ip' : 'tbd', 'flavor' : 'ds1G'}
    destinations['dst2'] = {'name' : 'dst2', 'ip' : 'tbd', 'flavor' : 'ds1G'}
    
    # flows - one source can emit more than a single flow
    # example: 2 flows from src1 to dst1, 1 flow from src2 to dst1
    flows['f1'] = {'src' : 'src1', 'dst' : 'dst1', 'pps' : 1000/9, 'thp' : 1.55, 'path' : 'br1'}
    flows['f2'] = {'src' : 'src2', 'dst' : 'dst1', 'pps' : 1000/9, 'thp' : 1.55, 'path' : 'br1'}
    flows['f3'] = {'src' : 'src3', 'dst' : 'dst2', 'pps' : 1000/7, 'thp' : 1.55, 'path' : 'br1'}
    flows['f4'] = {'src' : 'src4', 'dst' : 'dst2', 'pps' : 1000/7, 'thp' : 0.01, 'path' : 'br1'}
    flows['f5'] = {'src' : 'src5', 'dst' : 'dst3', 'pps' : 1000/7, 'thp' : 0.01, 'path' : 'br1'}
    flows['f6'] = {'src' : 'src6', 'dst' : 'dst3', 'pps' : 1000/7, 'thp' : 0.01, 'path' : 'br1'}

def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def data_generation_(nf_nb, ch_nb, f_nb): #100, 30, 1000
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
    #nfs['FW'] = {'type' : 'act_h', 'gdf_h' : 1, 'gdf_p' : 1, 'cap_h' : 2000, 'cap_p' : 2000, 'flavor' : 'ds1G', 'server' : 'A', 'instances' : ['FW1'], 'nb_instances' : 1, 'needed_cap_h' : 0, 'needed_cap_p' : 0}
    #nfs['IDS'] = {'type' : 'act_p', 'gdf_h' : 1, 'gdf_p' : 1, 'cap_h' : 2000, 'cap_p' : 2000, 'flavor' : 'ds1G', 'server' : 'A', 'instances' : ['IDS1'], 'nb_instances' : 1, 'needed_cap_h' : 0, 'needed_cap_p' : 0}
    
    for _ in itertools.repeat(None, nf_nb):
        nf_id = randomword(3)
        cap_h = random.randint(500, 3000) # pps
        cap_p = round(random.uniform(10, 50),2) # Mbps
        default_instance = nf_id+'1'
        nf_type = random.choice(['act_h', 'act_p'])
        gdf_h = round(random.uniform(0.8, 2),2) # gain drop factor - in case it is known
        gdf_p = round(random.uniform(0.8, 2),2) # gain drop factor - in case it is known        
        nfs[nf_id] = {'type' : nf_type, 'gdf_h' : gdf_h, 'gdf_p' : gdf_p, 'cap_h' : cap_h, 'cap_p' : cap_p, 'flavor' : 'ds1G', 'server' : 'A', 'instances' : [default_instance], 'nb_instances' : 1, 'needed_cap_h' : 0, 'needed_cap_p' : 0}
    
    '''
    nfs['NAT'] = {'type' : 'act_h', 'gdf_h' : 1, 'gdf_p' : 1, 'cap_h' : 3000/7, 'cap_p' : 4.65, 'flavor' : 'ds1G', 'server' : 'A', 'instances' : ['NAT1'], 'nb_instances' : 1, 'needed_cap_h' : 0, 'needed_cap_p' : 0}
    nfs['FW'] = {'type' : 'act_h', 'gdf_h' : 1, 'gdf_p' : 1, 'cap_h' : 3000/7, 'cap_p' : 4.65, 'flavor' : 'ds1G', 'server' : 'A', 'instances' : ['FW1'], 'nb_instances' : 1, 'needed_cap_h' : 0, 'needed_cap_p' : 0}
    nfs['IDS'] = {'type' : 'act_p', 'gdf_h' : 1, 'gdf_p' : 1, 'cap_h' : 3000/7, 'cap_p' : 4.65, 'flavor' : 'ds1G', 'server' : 'A', 'instances' : ['IDS1'], 'nb_instances' : 1, 'needed_cap_h' : 0, 'needed_cap_p' : 0}               
    '''
        
    for i in range(ch_nb):
        br_len =  random.randint(5, 10) # length of the branch  
        br_name = 'br'+str(i)
        l = []
        for _ in itertools.repeat(None, br_len):
            nf = random.choice(nfs.keys())
            l.append(nf)
        brs[br_name] = l # definition of the chain
    
    destinations['dst1'] = {'name' : 'dst1', 'ip' : 'tbd', 'flavor' : 'ds1G'}
    destinations['dst2'] = {'name' : 'dst2', 'ip' : 'tbd', 'flavor' : 'ds1G'}
    destinations['dst3'] = {'name' : 'dst3', 'ip' : 'tbd', 'flavor' : 'ds1G'}

    # flows - one source can emit more than a single flow
    # example: 2 flows from src1 to dst1, 1 flow from src2 to dst1
    
    for i in range(f_nb):
        pps = random.randint(100, 600) # pps
        thp = round(random.uniform(1, 15),2) # Mbps
        flow_name = 'f'+str(i)
        br = random.choice(brs.keys())
        src = random.choice(sources.keys())
        dst = random.choice(destinations.keys())
        
        flows[flow_name] = {'src' : src, 'dst' : dst, 'pps' : pps, 'thp' : thp, 'path' : br}
    '''   
    flows['f1'] = {'src' : 'src1', 'dst' : 'dst1', 'pps' : 1000/9, 'thp' : 1.55, 'path' : 'br1'}
    flows['f2'] = {'src' : 'src2', 'dst' : 'dst1', 'pps' : 1000/9, 'thp' : 1.55, 'path' : 'br1'}
    flows['f3'] = {'src' : 'src3', 'dst' : 'dst2', 'pps' : 1000/7, 'thp' : 1.55, 'path' : 'br1'}
    flows['f4'] = {'src' : 'src4', 'dst' : 'dst2', 'pps' : 1000/7, 'thp' : 0.01, 'path' : 'br1'}
    flows['f5'] = {'src' : 'src5', 'dst' : 'dst3', 'pps' : 1000/7, 'thp' : 0.01, 'path' : 'br1'}
    flows['f6'] = {'src' : 'src6', 'dst' : 'dst3', 'pps' : 1000/7, 'thp' : 0.01, 'path' : 'br1'}
    '''
    return (flows, brs, nfs)
    

def export_topo(sources, destinations, nfs, brs, flows, sub_brs, nf_instances):
    # sources
    f = open('/opt/stack/topology_data/sources.csv', 'w')
    writer = csv.writer(f, quoting=csv.QUOTE_NONE, delimiter=',', quotechar='')
    for s in sources.keys():
        row = s +'|'+ sources[s]['ip'] +'|'+ sources[s]['flavor'] +'|'+ sources[s]['name']
        writer.writerow([row])
    f.close()
    # destinations
    f = open('/opt/stack/topology_data/destinations.csv', 'w')
    writer = csv.writer(f, quoting=csv.QUOTE_NONE, delimiter=',', quotechar='')
    for s in destinations.keys():
        row = s +'|'+ destinations[s]['ip'] +'|'+ destinations[s]['flavor'] +'|'+ destinations[s]['name']
        writer.writerow([row])
    f.close()
    # nfs
    f = open('/opt/stack/topology_data/nfs.csv', 'w')
    writer = csv.writer(f, quoting=csv.QUOTE_NONE, delimiter=',', quotechar='')
    for s in nfs.keys():
        row = s +'|'+ nfs[s]['type'] +'|'+ str(nfs[s]['gdf_h']) +'|' \
                                        + str(nfs[s]['gdf_p'])+'|'+ str(nfs[s]['cap_h'])+'|'+ str(nfs[s]['cap_p']) \
                                        +'|'+ nfs[s]['flavor']+'|'+ nfs[s]['server'] +'|' \
                                        +'-'.join(nfs[s]['instances']) \
                                        +'|'+ str(nfs[s]['nb_instances']) +'|'+ str(nfs[s]['needed_cap_h']) \
                                        +'|'+ str(nfs[s]['needed_cap_p'])
                                        
        writer.writerow([row]) 
    f.close()
    # brs
    f = open('/opt/stack/topology_data/brs.csv', 'w')
    writer = csv.writer(f, quoting=csv.QUOTE_NONE, delimiter=',', quotechar='')
    for s in brs.keys():
        row1 = '-'.join(brs[s])
        row = s +'|'+ row1
        writer.writerow([row])   
    f.close()
    # flows
    f = open('/opt/stack/topology_data/flows.csv', 'w')
    writer = csv.writer(f, quoting=csv.QUOTE_NONE, delimiter=',', quotechar='')
    for s in flows.keys():
        row = s +'|'+ flows[s]['src'] +'|'+ flows[s]['dst'] +'|'+ str(flows[s]['pps'])+'|'+ str(flows[s]['thp'])+'|'+ flows[s]['path']
        writer.writerow([row])
    f.close() 
    
    # sub_brs
    f = open('/opt/stack/topology_data/sub_brs.csv', 'w')
    writer = csv.writer(f, quoting=csv.QUOTE_NONE, delimiter=',', quotechar='')
    for s in sub_brs.keys():
        row1 = '-'.join(sub_brs[s])
        row = s +'|'+ row1
        writer.writerow([row])   
    f.close() 

    # nf_instances
    f = open('/opt/stack/topology_data/nf_instances.csv', 'w')
    writer = csv.writer(f, quoting=csv.QUOTE_NONE, delimiter=',', quotechar='')
    for s in nf_instances.keys():
        row = s +'|'+ nf_instances[s]['ip_in'] +'|'+ nf_instances[s]['ip_out'] +'|'+ nf_instances[s]['nf']
        writer.writerow([row])
    f.close()
    
def import_topo(sources, destinations, nfs, brs, flows, sub_brs, nf_instances):
    # sources 
    sources.clear()
    f = open('/opt/stack/topology_data/sources.csv', 'rb')
    reader = csv.reader(f, quoting=csv.QUOTE_NONE, delimiter='|', quotechar='')
    for row in reader:
        sources[row[0]] = {'ip' : row[1], 'flavor' : row[2], 'name' : row[3]}
    f.close() 
    
    # destinations 
    destinations.clear()
    f = open('/opt/stack/topology_data/destinations.csv', 'rb')
    reader = csv.reader(f, quoting=csv.QUOTE_NONE, delimiter='|', quotechar='')
    for row in reader:
        destinations[row[0]] = {'ip' : row[1], 'flavor' : row[2], 'name' : row[3]}
    f.close()
      
    # nfs 
    nfs.clear()
    f = open('/opt/stack/topology_data/nfs.csv', 'rb')
    reader = csv.reader(f, quoting=csv.QUOTE_NONE, delimiter='|', quotechar='')
    for row in reader:
        if row[8] == '':
            row[8] = []
        else:
            row[8] = row[8].split('-')
        nfs[row[0]] = {'type' : row[1], 'gdf_h' : int(row[2]), 'gdf_p' : int(row[3]), 'cap_h' : float(row[4]), \
                       'cap_p' : float(row[5]), 'flavor' : row[6], \
                       'server' : row[7], 'instances' : row[8], 'nb_instances' : int(row[9]), \
                       'needed_cap_h' : float(row[10]), 'needed_cap_p' : float(row[11])}
    f.close() 
     
    # brs 
    brs.clear()
    f = open('/opt/stack/topology_data/brs.csv', 'rb')
    reader = csv.reader(f, quoting=csv.QUOTE_NONE, delimiter='|', quotechar='')
    for row in reader:
        brs[row[0]] = row[1].split('-')
    f.close()
    
    # flows 
    flows.clear()
    f = open('/opt/stack/topology_data/flows.csv', 'rb')
    reader = csv.reader(f, quoting=csv.QUOTE_NONE, delimiter='|', quotechar='')
    for row in reader:
        flows[row[0]] = {'src' : row[1], 'dst' : row[2], 'pps' : float(row[3]), 'thp' : float(row[4]), 'path' : row[5]}
    f.close()

    # sub_brs 
    sub_brs.clear()
    f = open('/opt/stack/topology_data/sub_brs.csv', 'rb')
    reader = csv.reader(f, quoting=csv.QUOTE_NONE, delimiter='|', quotechar='')
    for row in reader:
        sub_brs[row[0]] = row[1].split('-')
    f.close()      

    # nf_instances 
    nf_instances.clear()
    f = open('/opt/stack/topology_data/nf_instances.csv', 'rb')
    reader = csv.reader(f, quoting=csv.QUOTE_NONE, delimiter='|', quotechar='')
    for row in reader:
        nf_instances[row[0]] = {'ip_in' : row[1], 'ip_out' : row[2], 'nf' : row[3]}
    f.close() 


    print 'sources'
    for br in sources.items():
        print br
    print 'destinations'
    for br in destinations.items():
        print br    
    print 'nfs'
    for br in nfs.items():
        print br  
    print 'brs'  
    for br in brs.items():
        print br
    print 'flows'
    for br in flows.items():
        print br
    print 'nf_instances'
    for br in nf_instances.items():
        print br
    print 'sub_brs'
    for br in sub_brs.items():
        print br   


def generate_dataset(nf, ch, f):
    nf_nb = nf
    ch_nb = ch
    f_nb = f
    dataset = []
    for _ in itertools.repeat(None, 10): 
        initialise()
        (flows, brs, nfs) = data_generation_(nf_nb, ch_nb, f_nb) #100, 30, 1000
        dataset.append((flows, brs, nfs))
    return dataset
    
#data_generation()
def greedy(ds):
    #print 'greedy'
    (flows, brs, nfs) = ds
    time.sleep(5)
    #data_generation_(nf_nb, ch_nb, f_nb) #100, 30, 1000
    start_time = time.time()
    
    #print 'Accommodate flows'
    sfc_graph_greedy.accommodate_flows(flows, brs, nfs)
    
    end_time = time.time() - start_time
    print end_time,',',
    start_time = time.time()
    
    #for nf in nfs.keys():
    #    print nf, nfs[nf]['nb_instances']
        
    #print 'Map flows'
    flow_paths = sfc_graph_greedy.map_flows(flows, brs, nfs) 
    
    for f in flow_paths.keys():
        path = []
        for nf in flow_paths[f]:
            path.append(nf[1])
        #print f, path
          
    end_time = time.time() - start_time
    print end_time
    #data_generation_(1000, 300, 10000) #100, 30, 1000
    
    #sub_brs = sfc_graph.get_sub_brs(nfs, brs) # should run after the instantiation algorithm 
    #nf_instances = sfc_graph.get_nf_instances(nfs) # should run after the instantiation algorithm
    #export_topo(sources, destinations, nfs, brs, flows, sub_brs, nf_instances)
    
    #import_topo(sources, destinations, nfs, brs, flows, sub_brs, nf_instances) 
    
    
def nf_aware(ds):
    #print 'nf_aware'
    (flows, brs, nfs) = ds

    #initialise()
    time.sleep(5)
    #data_generation_(nf_nb, ch_nb, f_nb) #100, 30, 1000
    
    start_time = time.time()
    
    #print 'Accommodate flows'
    sfc_graph.accommodate_flows(flows, brs, nfs)
    
    end_time = time.time() - start_time
    print end_time,',',
    start_time = time.time()
    
    #for nf in nfs.keys():
    #    print nf, nfs[nf]['nb_instances']
        
    #print 'Map flows'
    flow_paths = sfc_graph.map_flows(flows, brs, nfs) 
    
    for f in flow_paths.keys():
        path = []
        for nf in flow_paths[f]:
            path.append(nf[1])
        #print f, path
          
    end_time = time.time() - start_time
    print end_time

def stratos_based(ds):
    #print 'stratos_based'
    (flows, brs, nfs) = ds

    #initialise()
    time.sleep(5)
    #data_generation_(nf_nb, ch_nb, f_nb) #100, 30, 1000
    
    start_time = time.time()
    
    #print 'Accommodate flows'
    sfc_graph_thp_based.accommodate_flows(flows, brs, nfs)
    
    end_time = time.time() - start_time
    print end_time,',',
    start_time = time.time()
    
    #for nf in nfs.keys():
    #    print nf, nfs[nf]['nb_instances']
        
    #print 'Map flows'
    flow_paths = sfc_graph_thp_based.map_flows(flows, brs, nfs) 
    
    for f in flow_paths.keys():
        path = []
        for nf in flow_paths[f]:
            path.append(nf[1])
        #print f, path
          
    end_time = time.time() - start_time
    print end_time


'''
#dataset = generate_dataset(100,30,1000)
#dataset = generate_dataset(200,60,2000)
dataset = generate_dataset(300,90,3000)
print 'be prepared to get cpu usage in 10s'
time.sleep(8)
print 'start'

for ds in dataset:
    #print len(ds)
    greedy(ds)
    #nf_aware(ds)
    #stratos_based(ds)
''' 
#greedy(100,30,1000)
#greedy(200,60,2000)
#greedy(300,90,3000)

#nf_aware(100,30,1000)
#nf_aware(200,60,2000)
#nf_aware(300,90,3000)

#stratos_based(100,30,1000)
#stratos_based(200,60,2000)
#stratos_based(300,90,3000)

#print 'End of program: csv_examples' 
        
         





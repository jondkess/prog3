'''
Created on Oct 12, 2016

@author: mwitt_000
'''
import network
import link
import threading
from time import sleep

##configuration parameters
router_queue_size = 0 #0 means unlimited
simulation_time = 3 #give the network sufficient time to transfer all packets before quitting

if __name__ == '__main__':
    object_L = [] #keeps track of objects, so we can kill their threads
    tableA = {0:0, 1:1}
    tableB = {0:0}
    tableC = {1:1}
    tableD = {0:0, 1:0}
    #create network nodes
    host1 = network.Host(1)
    object_L.append(host1)
    host2 = network.Host(2)
    object_L.append(host2)
    host3 = network.Host(3)
    object_L.append(host3)
    router_a = network.Router(tableA, name='A', intf_count=3, max_queue_size=router_queue_size)
    object_L.append(router_a)
    router_b = network.Router(tableB, name='B', intf_count=3, max_queue_size=router_queue_size)
    object_L.append(router_b)
    router_c = network.Router(tableC, name='C', intf_count=3, max_queue_size=router_queue_size)
    object_L.append(router_c)
    router_d = network.Router(tableD, name='D', intf_count=3, max_queue_size=router_queue_size)
    object_L.append(router_d)

    #create a Link Layer to keep track of links between network nodes
    link_layer = link.LinkLayer()
    object_L.append(link_layer)
    
    #add all the links
    link_layer.add_link(link.Link(host1, 0, router_a, 0, 50))
    link_layer.add_link(link.Link(host2, 0, router_a, 1, 50))
    link_layer.add_link(link.Link(router_a, 0, router_b, 0, 50))
    link_layer.add_link(link.Link(router_a, 1, router_c, 1, 50))
    link_layer.add_link(link.Link(router_b, 0, router_d, 1, 50))
    link_layer.add_link(link.Link(router_c, 1, router_d, 1, 50))
    link_layer.add_link(link.Link(router_d, 0, host3, 0, 50))
    link_layer.add_link(link.Link(router_d, 1, host3, 0, 50))


    #start all the objects
    thread_L = []
    thread_L.append(threading.Thread(name=host1.__str__(), target=host1.run))
    thread_L.append(threading.Thread(name=host2.__str__(), target=host2.run))
    thread_L.append(threading.Thread(name=host3.__str__(), target=host3.run))
    thread_L.append(threading.Thread(name=router_a.__str__(), target=router_a.run))
    thread_L.append(threading.Thread(name=router_b.__str__(), target=router_b.run))
    thread_L.append(threading.Thread(name=router_c.__str__(), target=router_c.run))
    thread_L.append(threading.Thread(name=router_d.__str__(), target=router_d.run))
    
    thread_L.append(threading.Thread(name="Network", target=link_layer.run))
    
    for t in thread_L:
        t.start()
    
    
    #create some send events    
    #for i in range(3):
    host2.udt_send(3, 'Sending a message from host 2 to host 3.')
    host1.udt_send(3, 'Sending a message from host 1 to host 3.')
    
    #give the network sufficient time to transfer all packets before quitting
    sleep(simulation_time)
    
    #join all threads
    for o in object_L:
        o.stop = True
    for t in thread_L:
        t.join()
        
    print("All simulation threads joined")



# writes to host periodically
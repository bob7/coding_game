import graphviz as gv
import random
import numpy as np
import datetime
from datetime import tzinfo, timedelta, datetime
import os
import sys

##########INITIAL PARAMETERS#############
foldername=("%s_%s_%s_%s_%s_%s" % (datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute,datetime.now().second))
#foldername="img"
os.mkdir('./'+foldername)
print ""
h=int(sys.argv[1])
print "Length of tree: " + str(h)
# print "Length of the tree: "
# h = int(raw_input(">"))
#h=3
red_iterations=2
a=['']
nu=[]
red_leafs=[]#these are kicked out of the class; the non-randoms
purple_nodes=[]#these are the double-labelled nodes
leaf_number=2**(h+1)-2**(h)

f = open('./'+foldername+'/info.txt', 'w')
f.write('Tree height: '+str(h)+"\n")
f.write("\n")
leaf_nodes=[]
for i in range(2**(h)-1,2**(h+1)-1):
    leaf_nodes.append(str(i))

nodes=[]
for i in range(0,2**(h+1)-1):
    nodes.append(str(i))

sec_label = {}
for i in nodes:
    sec_label[i]=i

##########FUNCTIONS#############
def predec(no):#predecessor function on the tree
    n=int(no)
    if (n==0):
        return str(0)
    elif (2*(n/2)==n):
        return str(n/2-1)
    else: return str((n+1)/2-1)

def predec_mu(no,m):#iterated predecessor function on the tree
    n=int(no)
    j=n
    for i in range (1,m+1):
        j=predec(j)
    return str(j)

def node_distance(no,mo):#distance of nodes: length of nodes minus length of longest common prefix; takes nodes
    n=int(no)
    m=int(mo)
    if (n==m):
        return 0
    else: 
        cou=0
        ns=n
        ms=m
        while (not(ns==ms)):
            ns=predec(ns)
            ms=predec(ms)
            cou=cou+1
        return cou

def g_c_pred(no,mo):#greatest common predecessor
    return predec_mu(no,node_distance(no,mo))

def g_c_pred_list(no,mo):#list of nodes from g_c_pred up to node n itself (predecessors of no). Returns list of strings
    mylist=[]
    for i in range(node_distance(no,mo)):
        mylist.append(predec_mu(no,i))
    return mylist
    
def label_test(new_no,old_no):#testing if node new_no can be labelled with old_no consistently in the current tree. Returns 0/1 for failure/success
    lat=0
    if new_no not in set(leaf_nodes)-set(red_leafs)-set(purple_nodes):
        inconsist=1
    else: inconsist=0
    while inconsist==0 and lat<len(g_c_pred_list(new_no,old_no)) and not ((g_c_pred_list(new_no,old_no)[lat]==g_c_pred_list(old_no,new_no)[lat]) or (g_c_pred_list(old_no,new_no)[lat]==sec_label[g_c_pred_list(new_no,old_no)[lat]])):
#        if not g_c_pred_list(new_no,old_no)[lat]==sec_label[g_c_pred_list(new_no,old_no)[lat]]:
        if g_c_pred_list(new_no,old_no)[lat] in purple_nodes:
            inconsist=1
        lat=lat+1
    return 1-inconsist

def eligible_choices(label_var):#returns list of eligivle choices (numbers). Returns list of strings
    li_var=[]
    for ta in list(set(leaf_nodes)-set(red_leafs)-set(purple_nodes)):
        if label_test(ta,label_var)==1:
            li_var.append(str(ta))
    li_var=map(int,li_var)
    li_var.sort()
    li_var=map(str,li_var)
    return li_var
    
for e in range (0,2**(h+1)-1):
    nu.append(str(e))

##########THE GRAPH#############
styles = {
    'graph': {'label': '','fontsize': '16','fontcolor': 'white','bgcolor': '#333333','rankdir': 'BT',},
    'nodes': {'fontname': 'Helvetica','shape': 'hexagon','fontcolor': 'white','color': 'white','style': 'filled','fillcolor': '#006699',},
    'edges': {'style': 'solid','color': 'white','arrowhead': 'open','fontname': 'Courier','fontsize': '12','fontcolor': 'white',}
}

def apply_styles(graph, styles):
    graph.graph_attr.update(('graph' in styles and styles['graph']) or {})
    graph.node_attr.update(('nodes' in styles and styles['nodes']) or {})
    graph.edge_attr.update(('edges' in styles and styles['edges']) or {})
    return graph


g1 = gv.Graph(format='png')
g1.node(nu[0],shape='ellipse')
g1.node(nu[1],shape='ellipse')
g1.node(nu[2],shape='ellipse')
g1.edge(nu[0], nu[1])
g1.edge(nu[0], nu[2])

for k in range(1,h):
    for t in range(2**(k),2**(k+1)):
        g1.node(nu[2*(t)-1],shape='ellipse')
        g1.node(nu[2*(t)],shape='ellipse')
        g1.edge(nu[t-1], nu[2*(t)-1])
        g1.edge(nu[t-1], nu[2*(t)])
g1 = apply_styles(g1, styles)
g1.render('./'+foldername+'/g0',cleanup=True)
g1.render('./'+foldername+'/g',cleanup=True)
g1.view('./'+foldername+'/g',cleanup=True) 

##########INITIAL CALL#############
Bred=1
cou=1
# print "Leafs for grabs: "
# f.write("Leafs for grabs: ")
grabs=list(set(leaf_nodes)-set(red_leafs))
grabs = map(int,grabs)
grabs.sort()
grabs = map(str,grabs)
# print map(int,grabs)
# for item in grabs:
#   f.write("%s, " % item)
# f.write("\n")
# f.write("\n")
print ""
Bcov2=0
Bred2=0
trip_input = map(int,raw_input("Input red and cover(s): ").split())
Bred = str(trip_input[0])
Bcov = str(trip_input[1])
if len(trip_input)>2:
    Bcov2 = str(trip_input[2])
    Bred2=sec_label[Bred]

while Bred not in grabs or label_test(Bcov,Bred)==0 or (len(trip_input)>2 and label_test(Bcov2,Bred2)==0):
    trip_input = map(int,raw_input("Wrong - input red and cover(s): ").split())
    Bred = str(trip_input[0])
    Bcov = str(trip_input[1])
    if len(trip_input)>2:
        Bcov2 = str(trip_input[2])
        Bred2=sec_label[Bred]
print ""
g1.node(Bred,fillcolor='firebrick')
g1.node(Bcov,fillcolor='darkorchid4')
if len(trip_input)>2:
    g1.node(Bred2,fillcolor='firebrick')
    g1.node(Bcov2,fillcolor='darkorchid4')
g1.render('./'+foldername+'/g',cleanup=True)
elmain=1
elsec=1

##########MAIN LOOP#############

while not Bred=="0" and not elmain==0 and not elsec==0:
    g1.node(Bred,fillcolor='firebrick')
    red_leafs.append(Bred)
    g1.render('./'+foldername+'/g',cleanup=True)
    g1.view('./'+foldername+'/g',cleanup=True)
    # print "Eligible positions table for remaining red: "
    # print ""
    # di=map(int,list(set(leaf_nodes)-set(red_leafs)))
    # di.sort()
    # for tred in di:
    #     da=map(int,eligible_choices(str(tred)))
    #     da.sort()
    #     print str(tred).ljust(3) + ": " + " ".join(str(x) for x in da)
    # print ""
    
    elmain=len(eligible_choices(Bred))
    if not elmain==0 and Bred==sec_label[Bred]:
        la=0
        while la<len(g_c_pred_list(Bcov,Bred)) and not ((g_c_pred_list(Bcov,Bred)[la]==g_c_pred_list(Bred,Bcov)[la]) or (g_c_pred_list(Bred,Bcov)[la]==sec_label[g_c_pred_list(Bcov,Bred)[la]])):
            purple_nodes.append(g_c_pred_list(Bcov,Bred)[la])
            sec_label[g_c_pred_list(Bcov,Bred)[la]]=g_c_pred_list(Bred,Bcov)[la]
            g1.node(g_c_pred_list(Bcov,Bred)[la],g_c_pred_list(Bcov,Bred)[la]+"/"+sec_label[g_c_pred_list(Bcov,Bred)[la]])
            g1.node(g_c_pred_list(Bcov,Bred)[la],fillcolor='darkorchid4')
            g1.render('./'+foldername+'/g',cleanup=True)
            la=la+1
        g1.node(str(Bred),fillcolor='aquamarine4')
        g1.render('./'+foldername+'/g',cleanup=True)
        g1.view('./'+foldername+'/g',cleanup=True)
    if not elmain==0 and not Bred==sec_label[Bred]:
        elsec=len(eligible_choices(Bred2))
        la=0
        while la<len(g_c_pred_list(Bcov,Bred)) and not ((g_c_pred_list(Bcov,Bred)[la]==g_c_pred_list(Bred,Bcov)[la]) or (g_c_pred_list(Bred,Bcov)[la]==sec_label[g_c_pred_list(Bcov,Bred)[la]])):
            purple_nodes.append(g_c_pred_list(Bcov,Bred)[la])
            sec_label[g_c_pred_list(Bcov,Bred)[la]]=g_c_pred_list(Bred,Bcov)[la]
            g1.node(g_c_pred_list(Bcov,Bred)[la],g_c_pred_list(Bcov,Bred)[la]+"/"+sec_label[g_c_pred_list(Bcov,Bred)[la]])
            g1.node(g_c_pred_list(Bcov,Bred)[la],fillcolor='darkorchid4')
            g1.render('./'+foldername+'/g',cleanup=True)
            la=la+1
        la=0
        while la<len(g_c_pred_list(Bcov2,Bred2)) and not ((g_c_pred_list(Bcov2,Bred2)[la]==g_c_pred_list(Bred2,Bcov2)[la]) or (g_c_pred_list(Bred2,Bcov2)[la]==sec_label[g_c_pred_list(Bcov2,Bred2)[la]])):
            purple_nodes.append(g_c_pred_list(Bcov2,Bred2)[la])
            sec_label[g_c_pred_list(Bcov2,Bred2)[la]]=g_c_pred_list(Bred2,Bcov2)[la]
            g1.node(g_c_pred_list(Bcov2,Bred2)[la],g_c_pred_list(Bcov2,Bred2)[la]+"/"+sec_label[g_c_pred_list(Bcov2,Bred2)[la]])
            g1.node(g_c_pred_list(Bcov2,Bred2)[la],fillcolor='darkorchid4')
            g1.render('./'+foldername+'/g',cleanup=True)
            la=la+1
        g1.node(str(Bred),fillcolor='aquamarine4')
        g1.node(str(Bred2),fillcolor='aquamarine4')
        g1.render('./'+foldername+'/g',cleanup=True)
        g1.view('./'+foldername+'/g',cleanup=True)
        
    if not elsec==0:
        img_name='./'+foldername+'/g'+str(cou)
        cou=cou+1
        grabs=list(set(leaf_nodes)-set(red_leafs))
        print "red proportion: "+ str(float(len(red_leafs))/float(len(leaf_nodes)))
        print ""
        trip_input = map(int,raw_input("Input red and cover(s): ").split())
        Bred = str(trip_input[0])
        Bcov = str(trip_input[1])
        if len(trip_input)>2:
            Bcov2 = str(trip_input[2])
            Bred2=sec_label[Bred]

        while Bred not in grabs or label_test(Bcov,Bred)==0 or (len(trip_input)>2 and label_test(Bcov2,Bred2)==0):
            trip_input = map(int,raw_input("Wrong - input red and cover(s): ").split())
            Bred = str(trip_input[0])
            Bcov = str(trip_input[1])
            if len(trip_input)>2:
                Bcov2 = str(trip_input[2])
                Bred2=sec_label[Bred]
        print ""
        g1.node(Bred,fillcolor='firebrick')
        g1.node(Bcov,fillcolor='darkorchid4')
        if len(trip_input)>2:
            g1.node(Bred2,fillcolor='firebrick')
            g1.node(Bcov2,fillcolor='darkorchid4')
        
        g1.render('./'+foldername+'/g',cleanup=True)
        g1.view('./'+foldername+'/g',cleanup=True)

##########EXIT MESSAGES#############   
if Bred=="0":
    print "You stopped the game - bye"
    f.write("You stopped the game - bye")
    f.write("\n")
elif len(eligible_choices(Bred))==0:
        print "your ran out of space -- red proportion: "+ str(float(len(red_leafs))/float(len(leaf_nodes)))
        f.write("your ran out of space - bye")
        f.write("\n")
elif len(eligible_choices(Bred2))==0:
        print "your ran out of space -- red proportion: "+ str(float(len(red_leafs))/float(len(leaf_nodes)))
        f.write("your ran out of space - bye")
        f.write("\n")
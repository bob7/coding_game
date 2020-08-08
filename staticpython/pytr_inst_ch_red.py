import graphviz as gv
import random
import numpy as np
import datetime
from datetime import tzinfo, timedelta, datetime
import os
##########INITIAL PARAMETERS#############
foldername=("%s_%s_%s_%s_%s_%s" % (datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute,datetime.now().second))
#foldername="img"
os.mkdir('./'+foldername)
print ""
h = int(raw_input("Length of the tree: "))
#h=3
red_iterations=2
a=['']
nu=[]
red_leafs=[]#these are kicked out of the class; the non-randoms
red_leafs_r=[] #remaining red leafs
red_leafs_d=[] # red leafs dealt with
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

def eligible_choices(label_var):#returns list of eligible choices (numbers). Returns list of strings
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
print ""
grabs=list(set(leaf_nodes))
grabs = map(int,grabs)
grabs.sort()
grabs = map(int,grabs)
print "Choose red leafs from: "+ str(grabs) #+ " (input the list of number0labels, separated by a space)"
print ""

red_leafs = map(int,raw_input("Enter their numbers, separated by space: ").split())

print ""

# print map(int,grabs)
# for item in grabs:
#   f.write("%s, " % item)
# f.write("\n")
# f.write("\n")

    
# print "Pick red leaf: "
# Bred = str(raw_input(">"))
# while not Bred=="0" and Bred not in grabs:
#         print "Wrong - pick red leaf: "
#         Bred = str(raw_input(">"))
# f.write("Pick red leaf: ")
# f.write(str(Bred))
# f.write("\n")
# f.write("\n")
elmain=1
elsec=1


# for i in range(0,int(0.5*leaf_number)):
#     Bred = random.choice(grabs)
#     g1.node(Bred,fillcolor='red')
#     red_leafs.append(Bred)
#     grabs=list(set(leaf_nodes)-set(red_leafs))
#     grabs=map(int,grabs)
#     grabs.sort()
#     grabs=map(str,grabs)

# red_leafs=map(int,red_leafs)

for i in red_leafs:
    g1.node(str(i),fillcolor='red')

red_leafs=map(int,red_leafs)
red_leafs.sort()
red_leafs=map(str,red_leafs)
# print ""
# print 'Number of red: '+str(len(red_leafs))+' out of '+str(len(leaf_nodes))
# print ""
print "Red leafs are: "+ str(map(int,red_leafs))
print ""
f.write("Red leafs are: "+ str(map(int,red_leafs)))
f.write("\n")
f.write("\n")

g1.render('./'+foldername+'/g',cleanup=True)
g1.view('./'+foldername+'/g',cleanup=True)
# print "Eligible positions table for remaining red: "
# print ""
# f.write("Eligible positions table for remaining red: ")
# f.write("\n")
# f.write("\n")
#
# for Bred in red_leafs:
#     da=map(int,eligible_choices(Bred))
#     da.sort()
#     print str(Bred).ljust(3)+ " : " + str(da)
#     f.write(str(Bred).ljust(3)+ " : " + str(da))
# f.write('Red leafs are: ')
# f.write(red_leafs)
# f.write("\n")
# f.write("\n")





##########MAIN LOOP#############
#while not elmain==0 and not elsec==0:
# while not Bred=="0" and not elmain==0 and not elsec==0:
    # g1.node(Bred,fillcolor='red')
    # red_leafs.append(Bred)
    # g1.view('./'+foldername+'/g',cleanup=True)
    # print "Eligible choices for cover of main label: "
    # f.write("Eligible choices for cover of main label: ")
    # print map(int, eligible_choices(Bred))
    # for item in map(int, eligible_choices(Bred)):
    #   f.write("%s, " % item)
    # f.write("\n")
    # f.write("\n")

elmain=len(eligible_choices(Bred))
#    if not elmain==0:
for Bred in red_leafs:
    # print "Eligible positions table for remaining red: "
    # print ""
    # f.write("Eligible positions table for remaining red: ")
    # f.write("\n")
    # f.write("\n")
    #
    # for tred in list(set(red_leafs)-set(red_leafs_d)):
    #     da=map(int,eligible_choices(tred))
    #     da.sort()
    #     print str(tred).ljust(3) + " : " + str(da)
    #     f.write(str(tred).ljust(3) + " : " + str(da))
    #     f.write("\n")
    # print ""
    # f.write("\n")
    
    # print "Input cover for " + str(Bred) +":" #+ " -- eligible choices: "+ str(map(int,eligible_choices(Bred)))
    # print ""
    Bcov = str(raw_input("Input cover for " + str(Bred)+": "))
    
    print ""
    while label_test(Bcov,Bred)==0:
        da=map(int,eligible_choices(Bred))
        da.sort()
        print "Wrong choice"#" - eligible choices for "+ str(Bred) +" are: "+ str(da)
        # print "Input cover for " + str(Bred)+": "
        print ""
        Bcov = str(raw_input("Input cover for " + str(Bred)+": "))
        print ""
            # f.write("Cover for main label: ")
            # f.write(Bcov)
            # f.write("\n")
            # f.write("\n")
    f.write("Input cover for " + str(Bred)+": "+Bcov)  
    f.write("\n")
    f.write("\n")

    la=0
    while la<len(g_c_pred_list(Bcov,Bred)) and not ((g_c_pred_list(Bcov,Bred)[la]==g_c_pred_list(Bred,Bcov)[la]) or (g_c_pred_list(Bred,Bcov)[la]==sec_label[g_c_pred_list(Bcov,Bred)[la]])):
        g1.node(g_c_pred_list(Bcov,Bred)[la],fillcolor='purple')
        purple_nodes.append(g_c_pred_list(Bcov,Bred)[la])
        sec_label[g_c_pred_list(Bcov,Bred)[la]]=g_c_pred_list(Bred,Bcov)[la]
        g1.node(g_c_pred_list(Bcov,Bred)[la],g_c_pred_list(Bcov,Bred)[la]+"/"+sec_label[g_c_pred_list(Bcov,Bred)[la]])
        la=la+1
    
        g1.render('./'+foldername+'/g',cleanup=True)
        g1.view('./'+foldername+'/g',cleanup=True)
    red_leafs_d.append(Bred)
    img_name='./'+foldername+'/g'+str(cou)
    g1.render(img_name,cleanup=True)
    g1.render('./'+foldername+'/g',cleanup=True)
    g1.view('./'+foldername+'/g',cleanup=True)
    cou=cou+1

img_name='./'+foldername+'/g'+str(cou-1)
g1.render(img_name,cleanup=True)

print "Game completed!"    
print ""    
os.remove('./'+foldername+'/g.png')


        # img_name='./'+foldername+'/g'+str(cou)
        # g1.render(img_name,cleanup=True)
        # g1.render('./'+foldername+'/g',cleanup=True)
        # g1.view('./'+foldername+'/g',cleanup=True)
        # cou=cou+1
        # if not Bred==sec_label[Bred]:
        #         Bred2=sec_label[Bred]
        #         print "Eligible choices for cover of secondary label:"
        #         print map(int,eligible_choices(Bred2))
        #         elsec=len(eligible_choices(Bred2))
        #
        #         if not elsec==0:
        #             print "Cover for secondary label: "
        #             Bcov2 = str(raw_input(">"))
        #
        #             while label_test(Bcov2,Bred2)==0:
        #                 print "Wrong choice - eligible choices for cover of secondary label:"
        #                 print eligible_choices(Bred2)
        #                 print "Cover for secondary label: "
        #                 Bcov2 = str(raw_input(">"))
        #             f.write("Cover for secondary label: ")
        #             f.write(str(Bred2))
        #             f.write("\n")
        #             f.write("\n")
        #             la=0
        #             while la<len(g_c_pred_list(Bcov2,Bred2)) and not ((g_c_pred_list(Bcov2,Bred2)[la]==g_c_pred_list(Bred2,Bcov2)[la]) or (g_c_pred_list(Bred2,Bcov2)[la]==sec_label[g_c_pred_list(Bcov2,Bred2)[la]])):
        #                 g1.node(g_c_pred_list(Bcov2,Bred2)[la],fillcolor='purple')
        #                 purple_nodes.append(g_c_pred_list(Bcov2,Bred2)[la])
        #                 sec_label[g_c_pred_list(Bcov2,Bred2)[la]]=g_c_pred_list(Bred2,Bcov2)[la]
        #                 g1.node(g_c_pred_list(Bcov2,Bred2)[la],g_c_pred_list(Bcov2,Bred2)[la]+"/"+sec_label[g_c_pred_list(Bcov2,Bred2)[la]])
        #                 la=la+1
        # if not elsec==0:
        #     img_name='./'+foldername+'/g'+str(cou)
        #     g1.render(img_name,cleanup=True)
        #     g1.render('./'+foldername+'/g',cleanup=True)
        #     g1.view('./'+foldername+'/g',cleanup=True)
        #     cou=cou+1

#             print "Leafs for grabs: "
#             grabs=list(set(leaf_nodes)-set(red_leafs))
#             grabs=map(int,grabs)
#             grabs.sort()
#             grabs=map(str,grabs)
#             print map(int, grabs)
#             print "Pick red leaf: "
#             Bred = str(raw_input(">"))
#             while not Bred=="0" and Bred not in grabs:
#                     print "Wrong - pick red leaf: "
#                     Bred = str(raw_input(">"))
#             f.write("Leafs for grabs: ")
#             for item in grabs:
#               f.write("%s, " % item)
#             f.write("\n")
#             f.write("\n")
# #########EXIT MESSAGES#############
# if Bred=="0":
#     print "You stopped the game - bye"
#     f.write("You stopped the game - bye")
#     f.write("\n")
# elif len(eligible_choices(Bred))==0:
#         print "your ran out of space - bye"
#         f.write("your ran out of space - bye")
#         f.write("\n")
# elif len(eligible_choices(Bred2))==0:
#         print "your ran out of space - bye"
#         f.write("your ran out of space - bye")
#         f.write("\n")
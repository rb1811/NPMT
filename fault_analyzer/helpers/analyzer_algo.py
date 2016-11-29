import networkx as nx
import matplotlib.pyplot as plt
import math
import operator
import numpy as np

from sympy import *
from sympy import Point as syPoint
from sympy.geometry import *
from itertools import chain, combinations
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import Point as shPoint
import datetime

# print datetime.datetime.now().time()


nvzradius = np.round(75.06, 2)
poly_coord = []
LVZ_edges, LVZ_node_position, pos = [], {}, {}
edge_list, node_positions = [], {}
G = nx.Graph()
exist_ipoints = []
Fipoints = {}


####################################################################################################################################calculates the equation of line
def LinePassingPR(edge, current_pr_center):
    # print edge, current_pr_center
    # print "\n\n, edge and current_pr _center x,y", edge, current_pr_center,current_pr_center[0],current_pr_center[1]
    global node_positions, nvzradius, Fipoints
    current_edge = LineString([shPoint(node_positions[edge[0]]), shPoint(node_positions[edge[1]])])
    current_pr = shPoint(current_pr_center).buffer(nvzradius)

    start_node, end_node = node_positions[edge[0]], node_positions[edge[1]]

    start_node_X, start_node_Y = start_node[0], start_node[1]
    end_node_X, end_node_Y = end_node[0], end_node[1]

    dist_start_node = np.float(np.round(np.sqrt(
        np.power((start_node_X - current_pr_center[0]), 2) + np.power((start_node_Y - current_pr_center[1]), 2)), 2))
    dist_end_node = np.float(np.round(
        np.sqrt(np.power((end_node_X - current_pr_center[0]), 2) + np.power((end_node_Y - current_pr_center[1]), 2)),
        2))

    if (np.less_equal(dist_start_node, nvzradius) and edge[0] not in Fipoints[current_pr_center]):
        Fipoints[current_pr_center].append(edge[0])
    if (np.less_equal(dist_end_node, nvzradius) and edge[1] not in Fipoints[current_pr_center]):
        Fipoints[current_pr_center].append(edge[1])

    # current_edge = Segment(syPoint(node_positions[edge[0]]),syPoint(node_positions[edge[1]]))
    # current_pr = Circle(syPoint(current_pr_center), nvzradius)


    if (current_pr.intersects(current_edge)):
        # if(intersection(current_pr,current_edge)):
        # print "This edge intersects circle", edge, current_pr_center
        # print "\n\n, edge and current_pr _center x,y", edge, current_pr_center,current_pr_center[0],current_pr_center[1]

        # print "THis passed",edge, current_pr_center
        return (edge)


##############################################################################################################################################Check if 2 circles are within 2PRradius distance
def coordist(ipoint, node):
    global nvzradius, node_positions
    # print "p1x {0} p1y {1} p2x {2} p2y {3} ".format(node_positions[p1][0],node_positions[p1][1],node_positions[p2][0],node_positions[p1][1])
    dist = np.float(np.round(np.sqrt(
        np.power((node_positions[node][0] - ipoint[0]), 2) + np.power((node_positions[node][1] - ipoint[1]), 2)), 2))
    # print "\n*************\nDist: ", dist
    # print "NVZradius: ", nvzradius
    # if(np.less_equal(np.round(dist,5),np.round(nvzradius,5))):
    if (np.less_equal(dist, nvzradius)):
        return node
    else:
        return False


#########################################################################################################################Logic for 2 circle intersection and return the intersecting points
def circleintersection(c1, c2):
    # print "Circle intersection", c1,c2
    global node_positions, nvzradius
    # print "This is c1 center {0} this is  c2 center {1}".format(node_positions[c1], node_positions[c2])
    dist = np.float(np.round(np.sqrt(np.power((node_positions[c1][0] - node_positions[c2][0]), 2) + np.power(
        (node_positions[c1][1] - node_positions[c2][1]), 2)), 2))
    if (dist < 2 * nvzradius):
        # print "THis is dist", dist
        c1 = Circle(node_positions[c1], nvzradius)
        c2 = Circle(node_positions[c2], nvzradius)
        # c1 = Point(node_positions[c1]).buffer(nvzradius)
        # c2 = Point(node_positions[c2]).buffer(nvzradius)
        l = []
        # l=intersection(c1,c2)
        for i in intersection(c1, c2):
            # l[i]=(float(l[i][0]),float(l[i][1]))
            l.append((float(i[0]), float(i[1])))
        # print "This 2 cirlces intersec at ", l
        return l

    elif (dist == 2 * nvzradius):
        l = []
        # print "\nThis is dist", dist
        l.append((float((node_positions[c1][0] + node_positions[c2][0]) / 2),
                  float((node_positions[c1][1] + node_positions[c2][1]) / 2)))
        # print "\nThis 2 circles touch at ", l
        return l

    else:
        return False


########################################################################################################################This is where line with line intersection takes place
def lvzintersection(edge1, edge2):
    # print edge1,edge2
    global exist_ipoints
    # print "edge1",LVZ_node_position[edge1[0]],LVZ_node_position[edge1[1]]
    # print "edge2",LVZ_node_position[edge2[0]],LVZ_node_position[edge2[1]]

    # segment1=Segment(Point(LVZ_node_position[edge1[0]]),Point(LVZ_node_position[edge1[1]]))
    # segment2=Segment(Point(LVZ_node_position[edge2[0]]),Point(LVZ_node_position[edge2[1]]))
    segment1 = LineString([shPoint(LVZ_node_position[edge1[0]]), shPoint(LVZ_node_position[edge1[1]])])
    segment2 = LineString([shPoint(LVZ_node_position[edge2[0]]), shPoint(LVZ_node_position[edge2[1]])])
    # l=list(intersection(segment1,segment2))
    x = segment1.intersection(segment2)
    if (x):
        # print "This two are lines intersectat", x.coords[0]
        # exist_ipoints.append( ( round(float(l[0][0]),3), round(float(l[0][1]),3 ) ) )
        return x.coords[0]
        # exist_ipoints.append(x.coords[0])


###############################################################################################################################Lvznvz intersection
def lvznvz(node, edge):
    # print node,edge
    global LVZ_node_position, node_positions
    # lvz=Segment(syPoint(LVZ_node_position[edge[0]]),syPoint(LVZ_node_position[edge[1]]))
    # nvz=Circle(syPoint(node_positions[node]),nvzradius)
    lvz = LineString([shPoint(LVZ_node_position[edge[0]]), shPoint(LVZ_node_position[edge[1]])])
    nvz = shPoint(node_positions[node]).buffer(nvzradius)

    # l=intersection(lvz,nvz)
    x = nvz.intersection(lvz)
    if (x):
        # for i in intersection(lvz,nvz):
        # print "x", x.coords[0],x.coords[1]
        # exist_ipoints.append(x.coords[0])
        # exist_ipoints.append(x.coords[1])
        for xx in x.coords:
            # print "This two lvz are nvx are interesecting",node,edge, xx,np.float(np.round(xx[0],2)),np.float(np.round(xx[1],2))
            xx = (np.float(np.round(xx[0], 2)), np.float(np.round(xx[1], 2)))
            if (xx not in exist_ipoints):
                exist_ipoints.append(xx)
                # exist_ipoints.append(   (float(i[0]) ,  float(i[1])) )


########################################################################################################################This is where Network parameters are calculated
def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1))


def region_connectivity():
    global Fipoints
    reg_connect = []
    for key in Fipoints.keys():
        temp = [element for element in Fipoints[key] if type(element) is not tuple]
        subsets = list(powerset(temp))
        subsets = [list(element) for element in subsets]
        for nodeset in subsets:
            H = G.copy()
            H.remove_nodes_from(nodeset)
            if (len(sorted(nx.connected_components(H), key=len, reverse=True)) > 1):
                reg_connect.append(len(nodeset))
                break
    return min(reg_connect)

def param_cal():
    global Fipoints
    RBCDNlist = RBLCSlist = RBSCSlist = []
    RBCDN_faults = {}
    for key in Fipoints.keys():
        H = G.copy()
        for element in Fipoints[key]:
            if (type(element) is tuple and H.has_edge(*element)):
                H.remove_edge(*element)
            if (H.has_node(element)):
                H.remove_node(element)
        concomplist = sorted(nx.connected_components(H), key=len, reverse=True)
        RBSCSlist.append(min([len(concomp) for concomp in concomplist]))
        RBLCSlist.append(max([len(concomp) for concomp in concomplist]))
        RBCDNlist.append(len(concomplist))
        # RBCDN_faults[key]=len(concomplist)
    RBC = region_connectivity()
    max_rbcdn = max(RBCDNlist)
    RBCDN_faults = dict(zip(Fipoints.keys(), RBCDNlist))
    # for item in RBCDN_faults.items():
    #		print item
    fault_center = [item[0] for item in RBCDN_faults.items() if item[1] == max_rbcdn]
    print "RBLCS,RBCDN,RBSCS,RBC,faults_considered,fault_regions_considered", \
        min(RBLCSlist), max_rbcdn, min(
        RBSCSlist), RBC, len(Fipoints.keys()), fault_center, fault_center


########################################################################################################################Create LVZ

########################################################################################################################Create LVZ

def specific_fault():
    global poly_coord, node_positions, edge_list
    poly_coord = [(-810, 550), (-1100, 375), (-585, 350), (-400, 600)]
    H = G.copy()
    for node in node_positions.keys():
        if ((Polygon(poly_coord).contains(shPoint(node_positions[node])) or Polygon(poly_coord).intersects(
                shPoint(node_positions[node]))) and H.has_node(node)):
            H.remove_node(node)
    for edge in edge_list:
        sh_edge = LineString([Point(node_positions[edge[0]]), Point(node_positions[edge[1]])])
        if ((sh_edge.intersects(LineString(poly_coord))) and H.has_edge(*edge)):
            H.remove_edge(*edge)
    # nx.draw_networkx(H,pos,node_size=300)
    # plt.show(H)
    concomplist = sorted(nx.connected_components(H), key=len, reverse=True)

    print "Surving Edges/Total edges:", len(H.edges()), "/", len(edge_list)
    print "Surving nodes/Total nodes:", len(H.nodes()), "/", len(node_positions.keys())
    print "Number of connected componenets", len(concomplist)
    print "Size of the largest connected components:", max([len(concomp) for concomp in concomplist])
    print "Size of the smallest connected components:", min([len(concomp) for concomp in concomplist])


########################################################################################################################Create LVZ
def LVZ(edge):
    global node_positions, LVZ_edges, LVZ_node_position

    start_node, end_node = edge[0], edge[1]

    start_node_X, start_node_Y = node_positions[start_node][0], node_positions[start_node][1]
    end_node_X, end_node_Y = node_positions[end_node][0], node_positions[end_node][1]

    # print "star", start_node_X, start_node_Y, "end", end_node_X,end_node_Y


    if (np.subtract(start_node_Y, end_node_Y) == 0):
        # print "Line parallel to x "
        edge_slope = 0
        t1x, t1y = start_node_X, np.add(start_node_Y, nvzradius)
        t2x, t2y = start_node_X, np.subtract(start_node_Y, nvzradius)

        t1 = (np.float(np.round(t1x, 2)), np.float(np.round(t1y, 2)))
        t2 = (np.float(np.round(t2x, 2)), np.float(np.round(t2y, 2)))

        # print t1, t2

        t3x, t3y = end_node_X, np.add(end_node_Y, nvzradius)
        t4x, t4y = end_node_X, np.subtract(end_node_Y, nvzradius)

        t3 = (np.float(np.round(t3x, 2)), np.float(np.round(t3y, 2)))
        t4 = (np.float(np.round(t4x, 2)), np.float(np.round(t4y, 2)))

        # print t3,t4
        LVZ_node_position[str(edge[0]) + str(edge[1]) + 'a'] = t1
        LVZ_node_position[str(edge[0]) + str(edge[1]) + 'c'] = t3

        LVZ_node_position[str(edge[0]) + str(edge[1]) + 'b'] = t2
        LVZ_node_position[str(edge[0]) + str(edge[1]) + 'd'] = t4

        LVZ_edges.append((str(edge[0]) + str(edge[1]) + 'a', str(edge[0]) + str(edge[1]) + 'c'))
        LVZ_edges.append((str(edge[0]) + str(edge[1]) + 'b', str(edge[0]) + str(edge[1]) + 'd'))

        return

    elif (np.subtract(start_node_X, end_node_X) == 0):
        # print "Line parallel to y "
        edge_slope = None
        t1x, t1y = np.subtract(start_node_X, nvzradius), start_node_Y
        t2x, t2y = np.add(start_node_X, nvzradius), start_node_Y

        t1 = (np.float(np.round(t1x, 2)), np.float(np.round(t1y, 2)))
        t2 = (np.float(np.round(t2x, 2)), np.float(np.round(t2y, 2)))

        # print t1,t2
        t3x, t3y = np.subtract(end_node_X, nvzradius), end_node_Y
        t4x, t4y = np.add(end_node_X, nvzradius), end_node_Y

        t3 = (np.float(np.round(t3x, 2)), np.float(np.round(t3y, 2)))
        t4 = (np.float(np.round(t4x, 2)), np.float(np.round(t4y, 2)))

        # print t3,t4
        LVZ_node_position[str(edge[0]) + str(edge[1]) + 'a'] = t1
        LVZ_node_position[str(edge[0]) + str(edge[1]) + 'c'] = t3

        LVZ_node_position[str(edge[0]) + str(edge[1]) + 'b'] = t2
        LVZ_node_position[str(edge[0]) + str(edge[1]) + 'd'] = t4

        LVZ_edges.append((str(edge[0]) + str(edge[1]) + 'a', str(edge[0]) + str(edge[1]) + 'c'))
        LVZ_edges.append((str(edge[0]) + str(edge[1]) + 'b', str(edge[0]) + str(edge[1]) + 'd'))

        return
    else:
        # print "other lines"
        edge_slope = np.float(
            np.round(np.divide(np.subtract(end_node_Y, start_node_Y), np.subtract(end_node_X, start_node_X)), 2))
        perp_slope = np.float(np.round(np.divide(-1, edge_slope), 2))

        t1x = np.add(np.divide(nvzradius, np.sqrt(np.add(np.power(perp_slope, 2), 1))), start_node_X)
        t1y = np.add(np.divide(nvzradius, np.sqrt(np.add(np.power(perp_slope, 2), 1))), start_node_Y)

        t1 = (np.float(np.round(t1x, 2)), np.float(np.round(t1y, 2)))

        # print t1
        t2x = np.subtract(start_node_X, np.divide(nvzradius, np.sqrt(np.add(np.power(perp_slope, 2), 1))))
        t2y = np.subtract(start_node_Y, np.divide(nvzradius, np.sqrt(np.add(np.power(perp_slope, 2), 1))))

        t2 = (np.float(np.round(t2x, 2)), np.float(np.round(t2y, 2)))

        # print t2

        t3x = np.add(np.divide(nvzradius, np.sqrt(np.add(np.power(perp_slope, 2), 1))), end_node_X)
        t3y = np.add(np.divide(nvzradius, np.sqrt(np.add(np.power(perp_slope, 2), 1))), end_node_Y)

        t3 = (np.float(np.round(t3x, 2)), np.float(np.round(t3y, 2)))

        # print t3
        t4x = np.subtract(end_node_X, np.divide(nvzradius, np.sqrt(np.add(np.power(perp_slope, 2), 1))))
        t4y = np.subtract(end_node_Y, np.divide(nvzradius, np.sqrt(np.add(np.power(perp_slope, 2), 1))))

        t4 = (np.float(np.round(t4x, 2)), np.float(np.round(t4y, 2)))

        # print t4

        if (np.divide(np.subtract(t3y, t1y), np.subtract(t3x, t1x)) == edge_slope):
            LVZ_node_position[sstr(edge[0]) + str(edge[1]) + 'a'] = t1
            LVZ_node_position[str(edge[0]) + str(edge[1]) + 'c'] = t3

            LVZ_node_position[str(edge[0]) + str(edge[1]) + 'b'] = t2
            LVZ_node_position[str(edge[0]) + str(edge[1]) + 'd'] = t4

            LVZ_edges.append((str(edge[0]) + str(edge[1]) + 'a', str(edge[0]) + str(edge[1]) + 'c'))
            LVZ_edges.append((str(edge[0]) + str(edge[1]) + 'b', str(edge[0]) + str(edge[1]) + 'd'))

            return

        else:
            LVZ_node_position[str(edge[0]) + str(edge[1]) + 'a'] = t1
            LVZ_node_position[str(edge[0]) + str(edge[1]) + 'd'] = t4

            LVZ_node_position[str(edge[0]) + str(edge[1]) + 'b'] = t2
            LVZ_node_position[str(edge[0]) + str(edge[1]) + 'c'] = t3

            LVZ_edges.append((str(edge[0]) + str(edge[1]) + 'a', str(edge[0]) + str(edge[1]) + 'd'))
            LVZ_edges.append((str(edge[0]) + str(edge[1]) + 'b', str(edge[0]) + str(edge[1]) + 'c'))
            return


########################################################################################################################This is networkx part and the graph is defined here
def define_graph():
    global edge_list, node_positions, G, pos
    G = nx.Graph()

    edge_list = [(1, 3), (1, 2), (2, 7), (12, 7), (12, 11), (10, 11), (9, 10), (8, 9), (2, 8), (1, 4), (3, 2), (12, 2)
        , (1, 5), (4, 5), (6, 5), (6, 8), (6, 7), (2, 10)]
    G.add_edges_from(edge_list)
    node_positions = {1: (-136.27, 454.83),
                      2: (-124.76, 395.49),
                      3: (-136.17, 604.12),
                      4: (-124.71, 587.58),
                      5: (-129.35, 540.60),
                      6: (-116.86, 482.80),
                      7: (-106.16, 347.25),
                      8: (-103.82, 561.79),
                      9: (-975.43, 514.23),
                      10: (-959.11, 483.23),
                      11: (-823.62, 497.27),
                      12: (-939.42, 399.51)}

    fixed_nodes = node_positions.keys()
    pos = nx.spring_layout(G, pos=node_positions, fixed=fixed_nodes)
    # print "edge list", edge_list

    calculate_ipoints()


########################################################################################################################The ipoint calculation starts here
def calculate_ipoints():
    # --------------------------------------ALL edges's LVZ creation
    global exist_ipoints, Fipoints, node_positions, LVZ_edges, LVZ_node_position, G, pos
    for edge in edge_list:
        LVZ(edge)

    # print "\n LVZ edges", LVZ_edges
    # print "\n LVZ node position", LVZ_node_position



    # exist_ipoints=[]

    for node in node_positions.keys():
        for lvzedge in LVZ_edges:
            # print node,lvzedge
            ipoint = lvznvz(node, lvzedge)
            if (ipoint):
                ipoint = (np.float(np.round(ipoint[0], 2)), np.float(np.round(ipoint[1], 2)))
                if (ipoint not in exist_ipoints):
                    exist_ipoints.append(ipoint)

    # print "\n\lvz nvz exist_ipoints", exist_ipoints
    # print datetime.datetime.now().time()

    for i in range(len(LVZ_edges)):
        current_lvz_edge, rest_lvzedge = LVZ_edges[i], LVZ_edges[i + 1:]
        for lvzedge_rest in rest_lvzedge:

            ipoint = lvzintersection(current_lvz_edge, lvzedge_rest)
            if (ipoint):
                ipoint = (np.float(np.round(ipoint[0], 2)), np.float(np.round(ipoint[1], 2)))
                if (ipoint not in exist_ipoints):
                    exist_ipoints.append(ipoint)

    # print "\n\nlvz lvz exist_ipoints", exist_ipoints
    # print datetime.datetime.now().time()


    for i in range(len(node_positions.keys())):
        current_node = node_positions.keys()[i]
        rest_node = node_positions.keys()[:]
        rest_node.remove(current_node)
        # print "\n" ,current_node, rest_node
        flag = 0
        for node_rest in rest_node:
            # print "\n\n",current_node, node_rest
            ipoint = circleintersection(current_node, node_rest)
            if (ipoint):
                flag = 1
                for point in ipoint:
                    point = (np.float(np.round(point[0], 2)), np.float(np.round(point[1], 2)))
                    if (point not in exist_ipoints):
                        exist_ipoints.append(point)
                        # print "ipoint", ipoint, current_node,node_rest
                        # print "THis is the runn exist_ipoints", exist_ipoints

        if (flag == 0):
            # print "Current node", current_node
            currentNodeX = np.float(np.round((node_positions[current_node])[0], 2))
            currentNodeY = np.float(np.round((node_positions[current_node])[1], 2))
            currentNodeRounded = (currentNodeX, currentNodeY)
            exist_ipoints.append(currentNodeRounded)

    # print "\n\ncircle circle  exist_ipoints", exist_ipoints



    Fipoints = {key: [] for key in exist_ipoints}
    # print "\n########## exist_ipoints: ", Fipoints
    for key in exist_ipoints:
        for node in node_positions.keys():
            comp = coordist(key, node)
            # comp = Point(node_positions[node]).distance(Point(key))
            if (comp):
                if (comp not in Fipoints[key]):
                    # print "Node:",comp,"Key:",key,"node",node
                    Fipoints[key].append(comp)
                    # else:
                    # print "Node:",comp,"Key:",key,"node",node

    for key in Fipoints.keys():
        if (len(Fipoints[key]) == 1):
            temp_passing_edges = [edge for edge in edge_list if Fipoints[key][0] not in edge]
            # print "\n",temp_passing_edges, " This node should not be there:", exist_ipoints[key]
            for edge in temp_passing_edges:
                edge_return = LinePassingPR(edge, key)
                if (edge_return):
                    Fipoints[key].append(edge_return)
        else:
            temp_passing_edges = edge_list[:]
            for edge in edge_list:
                for node in Fipoints[key]:
                    if (node in edge and edge in temp_passing_edges):
                        # print "\nThis node is there in this edge",node, edge
                        temp_passing_edges.remove(edge)
            # print "\n",temp_passing_edges, " This node should not be there:", exist_ipoints[key]
            for edge in temp_passing_edges:
                edge_return = LinePassingPR(edge, key)
                if (edge_return):
                    Fipoints[key].append(edge_return)
    for key in Fipoints.keys():
        Fipoints[key].sort()

    # print "\n\n\nIpoints with edges",exist_ipoints

    # print Fipoints
    """for key in Fipoints.keys():
        print key,":",Fipoints[key]
    nx.draw_networkx(G,pos,node_size=300)
    plt.show(G)
    """
    param_cal()

    specific_fault()


define_graph()

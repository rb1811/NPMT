import networkx as nx
import mercator as m
import numpy as np
from sympy import *
from itertools import chain, combinations
from sympy.geometry import *
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import Point as shPoint

nvzradius = 0
nvzradius_unreal = 0
edge_list = []
node_positions = {}
G = nx.Graph()
pos = {}
exist_ipoints = []
Fipoints = {}
LVZ_edges = []
LVZ_node_position = {}


def clear_variables():
    global nvzradius, nvzradius_unreal, edge_list, node_positions, G, pos, exist_ipoints, Fipoints, LVZ_edges, LVZ_node_position
    nvzradius = 0
    nvzradius_unreal = 0
    edge_list = []
    node_positions = {}
    G = nx.Graph()
    pos = {}
    exist_ipoints = []
    Fipoints = {}
    LVZ_edges = []
    LVZ_node_position = {}


def coordist(ipoint, node):
    global nvzradius, node_positions, nvzradius_unreal
    # print "p1x {0} p1y {1} p2x {2} p2y {3} ".format(node_positions[p1][0],node_positions[p1][1],node_positions[p2][0],node_positions[p1][1])
    dist = np.float(np.sqrt(
        np.power((node_positions[node][0] - ipoint[0]), 2) + np.power((node_positions[node][1] - ipoint[1]), 2)))
    # print "\n*************\nDist: ", dist
    # print "NVZradius: ", nvzradius
    # if(np.less_equal(np.round(dist,5),np.round(nvzradius,5))):
    if (np.less_equal(dist, nvzradius_unreal)):
        return node
    else:
        return False


def pointfinder(a1, b1, c1, a2, b2, c2):
    a = np.array(((a1, b1), (a2, b2)))
    b = np.array((c1, c2))
    x, y = np.linalg.solve(a, b)
    return (x, y)


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

        t1 = (np.float(t1x, 2), np.float(t1y))
        t2 = (np.float(t2x), np.float(t2y, 2))

        # print t1, t2

        t3x, t3y = end_node_X, np.add(end_node_Y, nvzradius)
        t4x, t4y = end_node_X, np.subtract(end_node_Y, nvzradius)

        t3 = (np.float(t3x), np.float(t3y))
        t4 = (np.float(t4x), np.float(t4y))

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

        t1 = (np.float(t1x), np.float(t1y))
        t2 = (np.float(t2x), np.float(t2y))

        # print t1,t2
        t3x, t3y = np.subtract(end_node_X, nvzradius), end_node_Y
        t4x, t4y = np.add(end_node_X, nvzradius), end_node_Y

        t3 = (np.float(t3x), np.float(t3y))
        t4 = (np.float(t4x), np.float(t4y))

        # print t3,t4
        LVZ_node_position[str(edge[0]) + str(edge[1]) + 'a'] = t1
        LVZ_node_position[str(edge[0]) + str(edge[1]) + 'c'] = t3

        LVZ_node_position[str(edge[0]) + str(edge[1]) + 'b'] = t2
        LVZ_node_position[str(edge[0]) + str(edge[1]) + 'd'] = t4

        LVZ_edges.append((str(edge[0]) + str(edge[1]) + 'a', str(edge[0]) + str(edge[1]) + 'c'))
        LVZ_edges.append((str(edge[0]) + str(edge[1]) + 'b', str(edge[0]) + str(edge[1]) + 'd'))

        return
    else:
        edge_slope = np.float(np.divide(np.subtract(end_node_Y, start_node_Y), np.subtract(end_node_X, start_node_X)))
        perp_slope = np.float(np.divide(-1, edge_slope))

        # edge_c= np.subtract(start_node_Y,np.multiply(edge_slope,start_node_X))
        dm2 = np.multiply(nvzradius, np.sqrt(np.add(1, np.square(edge_slope))))

        upper_edge_c = -np.add(np.subtract(start_node_Y, np.multiply(edge_slope, start_node_X)), dm2)
        upper_edge_a1 = edge_slope
        upper_edge_b1 = -1

        lower_edge_c = -np.subtract(np.subtract(start_node_Y, np.multiply(edge_slope, start_node_X)), dm2)
        lower_edge_a1 = edge_slope
        lower_edge_b1 = -1

        start_perp_c = -np.subtract(start_node_Y, np.multiply(perp_slope, start_node_X))
        start_perp_a1 = perp_slope
        start_perp_b1 = -1

        end_perp_c = -np.subtract(end_node_Y, np.multiply(perp_slope, end_node_X))
        end_perp_a1 = perp_slope
        end_perp_b1 = -1

        t1 = pointfinder(upper_edge_a1, upper_edge_b1, upper_edge_c, start_perp_a1, start_perp_b1, start_perp_c)
        t3 = pointfinder(upper_edge_a1, upper_edge_b1, upper_edge_c, end_perp_a1, end_perp_b1, end_perp_c)

        t2 = pointfinder(lower_edge_a1, lower_edge_b1, lower_edge_c, start_perp_a1, start_perp_b1, start_perp_c)
        t4 = pointfinder(lower_edge_a1, lower_edge_b1, lower_edge_c, end_perp_a1, end_perp_b1, end_perp_c)

        LVZ_node_position[sstr(edge[0]) + str(edge[1]) + 'a'] = t1
        LVZ_node_position[str(edge[0]) + str(edge[1]) + 'c'] = t3

        LVZ_node_position[str(edge[0]) + str(edge[1]) + 'b'] = t2
        LVZ_node_position[str(edge[0]) + str(edge[1]) + 'd'] = t4

        LVZ_edges.append((str(edge[0]) + str(edge[1]) + 'a', str(edge[0]) + str(edge[1]) + 'c'))
        LVZ_edges.append((str(edge[0]) + str(edge[1]) + 'b', str(edge[0]) + str(edge[1]) + 'd'))

        return


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
            xx = (np.float(xx[0]), np.float(xx[1]))
            if (xx not in exist_ipoints):
                exist_ipoints.append(xx)
                # exist_ipoints.append(   (float(i[0]) ,  float(i[1])) )


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


def circleintersection(c1, c2):
    # print "Circle intersection", c1,c2
    global node_positions, nvzradius
    # print "This is c1 center {0} this is  c2 center {1}".format(node_positions[c1], node_positions[c2])
    dist = np.float(np.sqrt(np.power((node_positions[c1][0] - node_positions[c2][0]), 2) + np.power(
        (node_positions[c1][1] - node_positions[c2][1]), 2)))
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


def LinePassingPR(edge, current_pr_center):
    print edge, current_pr_center
    # print "\n\n, edge and current_pr _center x,y", edge, current_pr_center,current_pr_center[0],current_pr_center[1]
    global node_positions, nvzradius, Fipoints, nvzradius_unreal
    current_edge = LineString([shPoint(node_positions[edge[0]]), shPoint(node_positions[edge[1]])])
    current_pr = shPoint(current_pr_center).buffer(nvzradius_unreal)

    start_node, end_node = node_positions[edge[0]], node_positions[edge[1]]

    start_node_X, start_node_Y = start_node[0], start_node[1]
    end_node_X, end_node_Y = end_node[0], end_node[1]

    dist_start_node = np.float(np.sqrt(
        np.power((start_node_X - current_pr_center[0]), 2) + np.power((start_node_Y - current_pr_center[1]), 2)))
    dist_end_node = np.float(
        np.sqrt(np.power((end_node_X - current_pr_center[0]), 2) + np.power((end_node_Y - current_pr_center[1]), 2)))

    if (np.less_equal(dist_start_node, nvzradius_unreal) and edge[0] not in Fipoints[current_pr_center]):
        Fipoints[current_pr_center].append(edge[0])
    if (np.less_equal(dist_end_node, nvzradius_unreal) and edge[1] not in Fipoints[current_pr_center]):
        Fipoints[current_pr_center].append(edge[1])

    # current_edge = Segment(syPoint(node_positions[edge[0]]),syPoint(node_positions[edge[1]]))
    # current_pr = Circle(syPoint(current_pr_center), nvzradius)


    if (current_pr.intersects(current_edge)):
        # if(intersection(current_pr,current_edge)):
        print "This edge intersects circle", edge, current_pr_center
        # print "\n\n, edge and current_pr _center x,y", edge, current_pr_center,current_pr_center[0],current_pr_center[1]

        # print "THis passed",edge, current_pr_center
        return (edge)


def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s) + 1))


def region_connectivity():
    # global Fipoints
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


def calculate_and_create_output_params():
    global Fipoints
    RBCDNlist = []
    RBLCSlist = []
    RBSCSlist = []
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
    # RBC = region_connectivity()
    max_rbcdn = max(RBCDNlist)
    RBCDN_faults = dict(zip(Fipoints.keys(), RBCDNlist))
    fault_centers = [item[0] for item in RBCDN_faults.items() if item[1] == max_rbcdn]
    rbcdn_faults = [{'y': m.x2lon_m(fault[0]), 'x': m.y2lat_m(fault[1])} for fault in fault_centers]
    return {
        'composition_deposition_number': max_rbcdn,
        'largest_component_size': max(RBLCSlist),
        'smallest_component_size': min(RBSCSlist),
        'fault_regions_considered': len(Fipoints),
        'rbcdn_faults': rbcdn_faults
    }


def calculate_ipoints():
    # --------------------------------------ALL edges's LVZ creation
    global exist_ipoints, Fipoints, node_positions, LVZ_edges, LVZ_node_position, G, pos
    for edge in edge_list:
        LVZ(edge)

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
            if ipoint:
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
    # param_cal()

    # specific_fault()


def generate_edge_list(network):
    e_list = []
    for edge in network.edge_set.all():
        e_list.append((edge.start_node.id, edge.end_node.id))
    return e_list


def add_nodes_to_graph(G, network):
    nodes = network.node_set.all()
    G.add_nodes_from([node.id for node in nodes])


def add_edges_to_graph(G, network):
    global edge_list
    edge_list = generate_edge_list(network)
    G.add_edges_from(edge_list)


def generate_node_positions(network):
    n_positions = {}
    nodes = network.node_set.all()
    for node in nodes:
        n_positions[node.id] = (m.lon2x_m(node.y), m.lat2y_m(node.x))
    return n_positions


def analyze_generic(network, fault_radius):
    global edge_list, node_positions, G, pos, nvzradius, nvzradius_unreal
    clear_variables()
    precision_correction_val = 70
    nvzradius = np.round(fault_radius)
    nvzradius_unreal = np.round(fault_radius + precision_correction_val, 2)
    add_nodes_to_graph(G, network)
    add_edges_to_graph(G, network)
    node_positions = generate_node_positions(network)
    fixed_nodes = node_positions.keys()
    pos = nx.spring_layout(G, pos=node_positions, fixed=fixed_nodes)
    calculate_ipoints()
    return calculate_and_create_output_params()


def format_fault_node_positions(fault_nodes):
    return [(m.lon2x_m(fault_node['lng']), m.lat2y_m(fault_node['lat'])) for fault_node in fault_nodes]


def analyze_specified(network, fault_nodes):
    global node_positions, edge_list
    clear_variables()
    add_nodes_to_graph(G, network)
    add_edges_to_graph(G, network)
    poly_coord = format_fault_node_positions(fault_nodes)
    node_positions = generate_node_positions(network)
    H = G.copy()
    for node in node_positions.keys():
        if ((Polygon(poly_coord).contains(shPoint(node_positions[node])) or Polygon(poly_coord).intersects(
                shPoint(node_positions[node]))) and H.has_node(node)):
            H.remove_node(node)
    for edge in edge_list:
        sh_edge = LineString([Point(node_positions[edge[0]]), Point(node_positions[edge[1]])])
        if ((sh_edge.intersects(LineString(poly_coord))) and H.has_edge(*edge)):
            H.remove_edge(*edge)
    concomplist = sorted(nx.connected_components(H), key=len, reverse=True)
    largest_component_size = max([len(concomp) for concomp in concomplist])
    smallest_component_size = min([len(concomp) for concomp in concomplist])
    return {
        'number_of_surviving_nodes': str(len(H.nodes())) + "/" + str(len(node_positions.keys())),
        'number_of_surviving_links': str(len(H.edges())) + "/" + str(len(edge_list)),
        'number_of_connected_components': str(len(concomplist)),
        'largest_connected_component_size': largest_component_size,
        'smallest_connected_component_size': smallest_component_size
    }

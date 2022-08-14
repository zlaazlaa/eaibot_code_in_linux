node_list = []

def load_nodes():
    # for i in (0,27):
    # node_list.append(NodeCoordinate())

    f = open("node_coordinate.txt", "r")
    for i in range(12):
        for j in range(7):
            node_list[i].p.append(f.readline())


    for i in range(12):
        print node_list[i].p_x
        print node_list[i].p_y
        print node_list[i].p_z
        print node_list[i].o_x
        print node_list[i].o_y
        print node_list[i].o_z
        print node_list[i].o_w


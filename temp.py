import time

node_list = []


class NodeCoordinate:
    def __init__(self, p_x, p_y, p_z, o_x, o_y, o_z, o_w):
        self.p_x = p_x
        self.p_y = p_y
        self.p_z = p_z
        self.o_x = o_x
        self.o_y = o_y
        self.o_z = o_z
        self.o_w = o_w


def load_nodes():
    # for i in (0, 27):
    #     node_list.append(NodeCoordinate())

    f = open("node_coordinate.txt", "r")
    for i in range(12):
        p_x = f.readline()
        p_y = f.readline()
        p_z = f.readline()
        o_x = f.readline()
        o_y = f.readline()
        o_z = f.readline()
        o_w = f.readline()
        node_list.append(NodeCoordinate(p_x, p_y, p_z, o_x, o_y, o_z, o_w))


if __name__ == '__main__':


    print (int(time.time()))
    load_nodes()

    for i in range(12):
        print node_list[i].p_x
        print node_list[i].p_y
        print node_list[i].p_z
        print node_list[i].o_x
        print node_list[i].o_y
        print node_list[i].o_z
        print node_list[i].o_w

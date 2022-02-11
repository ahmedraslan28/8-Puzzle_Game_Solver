from copy import deepcopy
from colorama import Fore, Back, Style
# direction matrix
DXY = {"U": [-1, 0], "D": [1, 0], "L": [0, -1], "R": [0, 1]}
# target matrix
Goal = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

left_down_angle = '\u2514'
right_down_angle = '\u2518'
right_up_angle = '\u2510'
left_up_angle = '\u250C'

middle_junction = '\u253C'
top_junction = '\u252C'
bottom_junction = '\u2534'
right_junction = '\u2524'
left_junction = '\u251C'

# bar color
bar = Style.BRIGHT + Fore.CYAN + '\u2502' + Fore.RESET + Style.RESET_ALL
dash = '\u2500'

# Line draw code
first_line = Style.BRIGHT + Fore.CYAN + left_up_angle + dash + dash + dash + top_junction + dash + dash + dash + \
             top_junction + dash + dash + dash + right_up_angle + Fore.RESET + Style.RESET_ALL
middle_line = Style.BRIGHT + Fore.CYAN + left_junction + dash + dash + dash + middle_junction + dash + dash + dash + \
              middle_junction + dash + dash + dash + right_junction + Fore.RESET + Style.RESET_ALL
last_line = Style.BRIGHT + Fore.CYAN + left_down_angle + dash + dash + dash + bottom_junction + dash + dash + dash + \
            bottom_junction + dash + dash + dash + right_down_angle + Fore.RESET + Style.RESET_ALL

# puzzle print function


def print_puzzle(array):
    print(first_line)
    for a in range(len(array)):
        for i in array[a]:
            if i == 0:
                print(bar, Back.RED + ' ' + Back.RESET, end=' ')
            else:
                print(bar, i, end=' ')
        print(bar)
        if a == 2:
            print(last_line)
        else:
            print(middle_line)


class Node:
    def __init__(self, current_grid, parent_grid, g, h, dir):
        self.current_grid = current_grid
        self.parent_grid = parent_grid
        self.h = h
        self.g = g
        self.dir = dir

    def f(self):
        return self.h + self.g


def get_pos(grid, val):
    for i in range(len(grid)):
        if val in grid[i]:
            return i, grid[i].index(val)


def cost(grid):
    cnt = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            pos = get_pos(Goal, grid[i][j])
            cnt += abs(pos[0] - i) + abs(pos[1] - j)
    return cnt


def get_best_node(current_nodes):
    min_f = 99999999
    for node in current_nodes.values():
        if node.f() < min_f:
            bestnode = node
            min_f = bestnode.f()
    return bestnode


def get_adj_nodes(bestnode):
    lst = []
    emptypos = get_pos(bestnode.current_grid, 0)

    for d in DXY.keys():
        newpos = (DXY[d][0] + emptypos[0], DXY[d][1] + emptypos[1])
        if 0 <= newpos[0] < len(bestnode.current_grid) and 0 <= newpos[1] < len(bestnode.current_grid[0]):
            new_grid = deepcopy(bestnode.current_grid)
            new_grid[emptypos[0]][emptypos[1]] = bestnode.current_grid[newpos[0]][newpos[1]]
            new_grid[newpos[0]][newpos[1]] = 0
            lst.append(Node(new_grid, bestnode.current_grid, bestnode.g+1, cost(new_grid), d))
    return lst


def build_bath(visited_lst):
    node = visited_lst[str(Goal)]
    branch = []
    while len(node.dir):
        branch.append({'d': node.dir, 'node': node.current_grid})
        node = visited_lst[str(node.parent_grid)]
    branch.reverse()
    return branch


def main(grid):
    current_nodes = {str(grid): Node(grid, grid, 0, cost(grid), "")}
    visited_nodes = {}

    while True:
        bestnode = get_best_node(current_nodes)
        visited_nodes[str(bestnode.current_grid)] = bestnode

        if bestnode.current_grid == Goal:
            return build_bath(visited_nodes)

        adjnodes = get_adj_nodes(bestnode)

        for node in adjnodes:
            if str(node.current_grid) in visited_nodes.keys():
                continue
            if str(node.current_grid) in current_nodes.keys() and current_nodes[str(node.current_grid)].f() < node.f():
                continue
            current_nodes[str(node.current_grid)] = node
        del current_nodes[str(bestnode.current_grid)]


if __name__ == '__main__':
    print("enter the initial state : \n")
    initial_state = []
    for i in range(3):
        initial_state.append([int(y) for y in input().split()])

    path = main(initial_state)


    print()
    print(dash + dash + right_junction, "INPUT", left_junction + dash + dash)
    print_puzzle([[6, 2, 8],
               [4, 7, 1],
               [0, 3, 5]])
    print("\n-------------------------------------------------------------------------------\n")
    print('total steps : ', len(path), '\n')
    for b in path:
        if b['d'] != '':
            letter = ''
            if b['d'] == 'U':
                letter = 'UP'
            elif b['d'] == 'R':
                letter = "RIGHT"
            elif b['d'] == 'L':
                letter = 'LEFT'
            elif b['d'] == 'D':
                letter = 'DOWN'
            print(dash + dash + right_junction, letter, left_junction + dash + dash)
        print_puzzle(b['node'])
        print()
    print(dash + dash + right_junction, 'ABOVE IS THE OUTPUT', left_junction + dash + dash)






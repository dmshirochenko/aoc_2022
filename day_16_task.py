# NOT SOLVED
# https://adventofcode.com/2022/day/15

import re
import queue
from math import inf
from collections import deque
from heapq import heappop, heappush
from itertools import count


REG_EXP = "Valve (\w{2}) has flow rate=(\d+); tunnel\w* lead\w* to valve\w* ([\w, ]*)"


class PriorityQueue:
    def __init__(self):
        self._elements = {}
        self._counter = count()

    def queue_reordering(self):
        return dict(sorted(self._elements.items(), key=lambda item: item[1], reverse=True))

    def value_change(self, value):
        self._elements[value.node_name] = (value.priority_value, next(self._counter), value)

    def enqueue_with_priority(self, value):
        self._elements[value.node_name] = (value.priority_value, next(self._counter), value)
        # self._elements.append(element)
        # heappush(self._elements, element)

    def dequeue(self):
        value_to_return = next(iter(self._elements.items()))
        del self._elements[value_to_return[0]]
        return value_to_return[1][2]

    def is_empty(self):
        if not self._elements:
            return False

        return True


class GraphNode:
    def __init__(self, node_name, pressure_released, edges_list):
        self.node_name = node_name
        self.pressure_released = int(pressure_released)
        self.edges_list = edges_list
        self.is_opened = self.check_if_valve_is_zero()
        self.is_visited = False
        self.priority_value = -inf

    def __repr__(self) -> str:
        return f"Node name {self.node_name} pressure_released {self.pressure_released} edges {self.edges_list} "

    def check_if_valve_is_zero(self):
        if self.pressure_released == 0:
            self.is_opened = True

        return False


def max_pressure_released(nodes_dict):
    priority_queue = PriorityQueue()
    path_nodes = []
    nodes_dict["AA"].priority_value = 0
    nodes_dict["AA"].is_visited = True
    for nodes in nodes_dict:
        priority_queue.enqueue_with_priority(nodes_dict[nodes])

    priority_queue.queue_reordering()

    while priority_queue.is_empty():
        print("priority_queue", priority_queue._elements)
        node_to_check = priority_queue.dequeue()
        node_to_check.is_visited = True
        print("node_to_check", node_to_check)
        path_nodes.append(node_to_check)
        for vertex in node_to_check.edges_list:
            if not nodes_dict[vertex].is_visited:
                print("Edge", vertex)
                print("Priority before", nodes_dict[vertex].priority_value)
                new_priority_value = nodes_dict[vertex].pressure_released

                print("new_priority_value", new_priority_value)
                if new_priority_value > nodes_dict[vertex].priority_value:
                    nodes_dict[vertex].priority_value = new_priority_value
                    priority_queue.value_change(nodes_dict[vertex])
                    priority_queue._elements = priority_queue.queue_reordering()

                print("Priority after", nodes_dict[vertex].priority_value)

    print("path_nodes", path_nodes)


if __name__ == "__main__":
    nodes_dict = {}
    with open("day_16.txt", "r") as f:
        path_list = [re.match(REG_EXP, l.rstrip()) for l in f.readlines()]

    for match in path_list:
        edges_list = match.group(3).strip().split(", ")
        nodes_dict[match.group(1)] = GraphNode(match.group(1), match.group(2), edges_list)

    max_pressure_released(nodes_dict)

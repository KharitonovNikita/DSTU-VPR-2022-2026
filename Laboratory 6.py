import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    def __init__(
            self,
            with_labels=True,
            node_size=500,
            node_color='orange',
            font_size=12,
            font_color='black',
            font_weight='bold',
            width=1,
            edge_color='black',
            arrowsize=20,
            arrowstyle='->',
            arrows=True,
            connectionstyle='arc3,rad=0.1',
            alpha=0.6,
            label_font_size=15,
            label_font_color='black',
            label_font_weight='bold',
            label_rotate=True,
            label_verticalalignment='bottom',
    ):
        self._with_labels = with_labels
        self._node_size = node_size
        self._node_color = node_color
        self._font_size = font_size
        self._font_color = font_color
        self._font_weight = font_weight
        self._width = width
        self._edge_color = edge_color
        self._arrowsize = arrowsize
        self._arrowstyle = arrowstyle
        self._arrows = arrows
        self._connectionstyle = connectionstyle
        self._alpha = alpha
        self._label_font_size = label_font_size
        self._label_font_color = label_font_color
        self._label_font_weight = label_font_weight
        self._label_rotate = label_rotate
        self._label_verticalalignment = label_verticalalignment

        self._G = nx.DiGraph()
        self._pos = None

        self._node_style = {}

    def add_edge(self, from_vertex: str, to_vertex: str, label: str = None) -> None:
        if not label:
            self._G.add_edge(from_vertex, to_vertex)
            return

        labels = nx.get_edge_attributes(self._G, 'label')
        if (from_vertex, to_vertex) in labels:
            labels[(from_vertex, to_vertex)] += f", {label}"
        self._G.add_edge(from_vertex, to_vertex, label=label)
        nx.set_edge_attributes(self._G, labels, 'label')

    def style_node(self, node: str, **kwargs) -> None:
        self._node_style[node] = kwargs

    def draw(self) -> None:
        self._pos = nx.spring_layout(self._G)

        nx.draw(
            self._G,
            self._pos,
            with_labels=self._with_labels,
            node_size=self._node_size,
            node_color=self._node_color,
            font_size=self._font_size,
            font_color=self._font_color,
            font_weight=self._font_weight,
            width=self._width,
            edge_color=self._edge_color,
            arrowsize=self._arrowsize,
            arrowstyle=self._arrowstyle,
            arrows=self._arrows,
            connectionstyle=self._connectionstyle,
            alpha=self._alpha,
        )
        nx.draw_networkx_edge_labels(
            self._G,
            self._pos,
            edge_labels=nx.get_edge_attributes(self._G, 'label'),
            font_size=self._label_font_size,
            font_color=self._label_font_color,
            font_weight=self._label_font_weight,
            rotate=self._label_rotate,
            verticalalignment=self._label_verticalalignment,
        )
        for node, style in self._node_style.items():
            nx.draw_networkx_nodes(
                self._G,
                self._pos,
                nodelist=[node],
                **style,
            )
        plt.show()

        import copy
import logging
import os
import platform



def removeUnreachableVertices(graph_data: list[dict[str]], new_graph: list[dict[str]], start_vertex: str):
    for route in [el for el in graph_data if el["from"] == start_vertex]:
        new_graph.append(route)

        if route["to"] in [el["from"] for el in new_graph]: #mail if
            continue

        removeUnreachableVertices(graph_data, new_graph, route["to"])


def splittingСlasses(
        classes: list[list[str]],
        graph_data: list[dict[str]],
        alphabet: list[str]
) -> list[list[str]]:
    iters = 0
    while True:
        logging.info(f"Ξ({iters}) = {classes}")
        current_classes: list[list[str]] = copy.deepcopy(classes)
        for _class in classes:
            if len(_class) == 1: # класс минимальный
                continue

            exclude_rels: list[dict[str, list]] = [] # копия списка
            for vertex in _class:
                for alpha in alphabet: # по всем буквам и вершинам

                    if [el for el in exclude_rels if vertex in el["vertex"]]:
                        continue

                    dest_vertex = [el["to"] for el in graph_data if el["from"] == vertex and el["weight"] == alpha][0] # нахождение куда переходит
                    if dest_vertex in _class: 
                        continue

                    dest_class = [_ for _ in classes if dest_vertex in _][0]
                    _ = [el for el in exclude_rels if el["dest_vertex"] == dest_vertex] # в каком классе
                    el_in_exclude_rels = None if not _ else _[0]

                    if el_in_exclude_rels:
                        el_in_exclude_rels["vertex"].append(vertex) #добавляем
                    else:
                        exclude_rels.append(dict(vertex=[vertex], _class=dest_class, dest_vertex=dest_vertex))


            for rel in exclude_rels:
                for el in rel["vertex"]:
                    current_classes[classes.index(_class)].remove(copy.copy(el)) #delete предыдущих классов
                current_classes.append(rel["vertex"])


        for el in range(current_classes.count([])):
            current_classes.remove([])

        if classes != current_classes:
            iters += 1
            classes = current_classes
            continue

        return current_classes


def printGraph(graph_data: list[dict[str]], start_vertex: str = None, end_vertex: list[str] = None):
    if end_vertex is None:
        end_vertex = []

    graph = Graph()
    for row in graph_data:
        label = row["weight"]
        if label is None:
            label = "eps"
        graph.add_edge(row["from"], row["to"], label)

    for el in end_vertex:
        graph.style_node(el, node_color="brown", alpha=0.6)

    if start_vertex:
        graph.style_node(start_vertex, node_color="blue", alpha=0.3, node_size=1000)
    graph.draw()


def ClearTerminal():
    if not os.getenv('TERM', None):
        os.putenv('TERM', 'xterm')

    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')





        import copy
import random


def main():

    alphabet = []
    end_vertex: list[str] = list()
    start_vertex = None
    graph_data = list()
    print("""Ввод алфавита.
          'End' - Завершения ввода""")
    while True:
        value = input("Ввод символа: ")

        if value == 'End':
            break
        if len(value) != 1:
            print("Ошибка! Введено не одно значение")
            continue
        alphabet.append(value)

    while True:
        count_of_vertex = input("Ввод количества вершин автомата: ")
        if not count_of_vertex.isdigit():
            print("Ошибка! Введено не число")
            continue
        count_of_vertex = int(count_of_vertex)
        if count_of_vertex < 1:
            print("Ошибка! Введено не положительное число")
            continue
        break


    graphInpuText = "\nВвод графа\n" \
                  "Вам необходимо ввести вершины: q0, q1, ..., q(n)\n" \
                  "'End' - Завершить ввод\n" \
                  "'eps' - Ввод eps значения\n\n"

    while True:
        ClearTerminal()
        buffer = graphInpuText + "\n Из узла "
        data = []
        for msg in ["{!s} в: ", "{!s} с весом: ", "{!s}"]:
            value = input(buffer).replace(' ', '')

            buffer += msg.format(value)
            ClearTerminal()

            if value == "End":
                data.clear()
                break

            if len(data) in [0, 1]:
                if value not in [f"q{i}" for i in range(count_of_vertex)]:
                    print("Ошибка! Введена не вершина")
                    continue
            elif len(data) == 2:
                if value == "eps":
                    value = None
                elif value not in alphabet:
                    print("Ошибка! Введен не символ алфавита")
                    continue

            data.append(value)

        graphInpuText = buffer
        print(buffer)

        if data:
            graph_data.append(
                {
                    "from": data[0],
                    "to": data[1],
                    "weight": data[2]
                }
            )
        else:
            break


    # ----------------- ------------------------------------------------------------------------------------------------
    print("\nВвод начальной вершины автомата.")
    while True:
        var = input("Ввод: ").replace(" ", "").lower()
        if var not in [f"q{i}" for i in range(count_of_vertex)]:
            print("Ошибка! Введена не вершина")
            continue
        start_vertex = var
        break
 # ----------------- ------------------------------------------------------------------------------------------------
    print()
    print("""Ввод конечных вершин
          'End'- Завершить ввод""")
    while True:
        var = input("Ввод конечной вершины автомата: ")
        if var == 'End':
            break
        if var not in [f"q{i}" for i in range(count_of_vertex)]:
            print("Введена не вершина")
            continue
        end_vertex.append(var)


    printGraph(graph_data, start_vertex, end_vertex)


#Удаление
    new_graph: list[dict[str]] = []
    removeUnreachableVertices(graph_data, new_graph, start_vertex)
    graph_data = new_graph
    all_vertex = list(set(el["from"] for el in graph_data))

    new_end_vertex = []
    for vertex in end_vertex:
        if vertex in all_vertex:
            new_end_vertex.append(vertex)
    end_vertex = new_end_vertex


    printGraph(graph_data, start_vertex, end_vertex)

    #-----------------------------------------------------------------------------------------------------------

    is_determined = True
    for vertex in all_vertex:
        list_of_weight = [route["weight"] for route in graph_data if route["from"] == vertex] # есть ли несколько одинаковых весов
        if None in list_of_weight:

            list_of_weight.remove(None)

        if sorted(alphabet) != sorted(list_of_weight):
            is_determined = False

    if is_determined:
        print("Победа! Автомат детерминирован!")
    else:
        print("Беда! Автомат недетерминирован")


    equivalence_classes: list[list[str]] = [end_vertex, [el for el in all_vertex if el not in end_vertex]]
    classes = splittingСlasses(equivalence_classes, graph_data, alphabet)
    print(f"Класс: {classes} является финальным")

    # ---------------------------------------- ---------------
    result_graph_data = copy.deepcopy(graph_data)
    for _class in classes:
        class_mask = f"[{random.choice(_class)}]"
        for relation in result_graph_data:
            if relation["from"] in _class:
                relation["from"] = class_mask
            if relation["to"] in _class:
                relation["to"] = class_mask


    printGraph(result_graph_data)


if __name__ == '__main__':
    main()
import networkx as nx
import matplotlib.pyplot as plt


def display_transitions(labels):
    # Crear una tabla utilizando pyplot
    table_data = [["Estado Inicial", "Estado Final", "Etiqueta"]]

    for edge, label in labels.items():
        start, end = map(str, edge)
        table_data.append([start, end, label])

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.axis('off')
    ax.table(cellText=table_data, loc='center', cellLoc='center', colLabels=None)

    plt.show()

def getNonTerminals(grammar):
    # global non_terminals,non_terminals_list
    non_terminals = {}
    non_terminals_list = list()
    for production in grammar:
        head, body = production.split(" -> ")
        non_terminals[head.strip()] = set(body.split(" | "))
        non_terminals_list.append(head.strip())

    return non_terminals, non_terminals_list


def iterate(expressions, currentState, rootState, G, rootFinalState):
    # global currentState
    for i, expression in enumerate(expressions):
        print("i:", i, "len:", len(expression), 'expression: ', expression)
        # A a | b A c | d c | b d a

        # remove blank spaces
        expression = expression.replace(" ", "")
        G, rootState, currentState = updateGraph(expression=expression, isFirstItem=True, rootState=rootState,
                                                 currentState=currentState, G=G, rootFinalState=rootFinalState)
        currentState += 1

    return G, currentState, rootState


def updateGraph(expression, G, rootState, currentState, rootFinalState, isFirstItem=False):
    global non_terminals, non_terminals_list

    # get each single character 
    for j, item in enumerate(expression):

        # check if the current item is a non_terminal
        if (item in non_terminals_list):
            # send the matched non_termina as main expression
            expressions = non_terminals[item]

            # add a new node with edge epsilon to join the current node with the end of the new afn from the no_termina
            # (current node)-ε->(start)-Result AFN->(next node)
            G.add_edge(str(currentState), str(currentState + 1), label="ε")
            currentState += 1
            G, currentState, rootAux = iterate(expressions=expressions, currentState=currentState,
                                               rootState=currentState, G=G, rootFinalState=rootFinalState)

            # if this no_terminal have just 1 expression then join the final state with the final node
            if (len(expression) == 1):
                G.add_edge(rootFinalState + str(rootAux), rootFinalState + str(rootState), label="ε")
            else:
                G.add_edge(rootFinalState + str(rootAux), str(currentState + 1), label="ε")

            # skip this iteration - we already added nodes from this no_terminal
            continue

        # if this is the first iteration then add epsilon transition to connect the next node
        currentState += 1
        if (j == 0 and isFirstItem == True):
            G.add_edge(str(rootState), str(currentState), label="ε")
            G.add_edge(str(currentState), str(currentState + 1), label=item)
        elif (j < len(expression) - 1):
            # this is not the first or the last char so we just add the item as new edge
            # (previous node)-item-(current node)
            G.add_edge(str(currentState), str(currentState + 1), label=item)
        else:
            # this is the last char so we add the node and join to the end node with epsilon
            # (previous node)-item-(current node)-ε-(Final node)
            G.add_edge(str(currentState), str(currentState + 1), label=item)
            G.add_edge(str(currentState + 1), rootFinalState + str(rootState), label="ε")

        # is just one expression 
        if (len(expression) == 1):
            G.add_edge(str(currentState + 1), rootFinalState + str(rootState), label="ε")
    return G, rootState, currentState


def bnf_to_afn(grammar, rootState=0, currentState=0):
    # global G, non_terminals,non_terminals_list,rootState,currentState
    G = nx.DiGraph()

    # initial and final state
    rootState = 0
    currentState = 0
    rootFinalState = "F"

    # define first and final state 
    G.add_node(str(rootState), initial=True)
    G.add_node(rootFinalState + str(rootState), final=True)

    # get the first production
    head, body = grammar[0].split(" -> ")
    expressions = body.split(" | ")

    # generate the full graph
    G, _, _ = iterate(expressions=expressions, currentState=currentState, rootState=rootState, G=G,
                      rootFinalState=rootFinalState)

    # Dibuja el grafo
    pos = nx.spring_layout(G, seed=10)
    labels = {edge: G.edges[edge]["label"] for edge in G.edges}
    nx.draw(G, pos, with_labels=True, node_size=300, node_color="lightblue", font_size=5)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

    # Imprimir las transiciones en una tabla
    print("Transiciones:")
    print("| Estado Inicial | Estado Final | Etiqueta |")
    print("|----------------|--------------|----------|")
    for edge, label in labels.items():
        start, end = edge
        print(f"|{start:<5}            | {end:<5}          | {label:<5} |")
    display_transitions(labels)

# Gramática BNF
BNF = [
    "S -> A a | b A c | d c | b d a",
    "A -> d",
]

# get non_terminals
non_terminals, non_terminals_list = getNonTerminals(BNF)
# Convertir la gramática en un AFN
afn = bnf_to_afn(BNF)

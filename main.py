import networkx as nx
import matplotlib.pyplot as plt

def getNonTerminals(grammar):
    global G, non_terminals,non_terminals_list
    # non_terminals = {}
    # non_terminals_list = list()
    for production in grammar:
        head, body = production.split(" -> ")
        non_terminals[head.strip()]  = set(body.split(" | "))
        non_terminals_list.append(head.strip())

    return non_terminals, non_terminals_list

def iterate(expressions):
    global currentState
    for i,expression in enumerate(expressions):
        print("i:",i,"len:",len(expression), 'expression: ',expression)
        # A a | b A c | d c | b d a

        # remove blank spaces
        expression =expression.replace(" ","")
        updateGraph(expression= expression, isFirstItem=True)
        currentState+=1

def updateGraph(expression , isFirstItem = False):
    global G, non_terminals,non_terminals_list,rootState,currentState
    for j,item in enumerate(expression):
        # A a
        # item = A

        # check if the current item is a non_terminal
        # if(item in non_terminals_list):
        #     updateGraphNonTerminal(item,non_terminals[item], isFirstItem= isFirstItem and j == 0, root=)    
        #     continue

        print('item',item, 'j: ',j, 'currentState',currentState)
        currentState += 1
        if(j==0 and isFirstItem == True):
            # (0)-ε->(1)-A->
            G.add_edge(str(rootState),str(currentState),label="ε")
            G.add_edge(str(currentState),str(currentState+1),label=item)
        elif(j < len(expression)-1):
            # rootState += 1
            # (0)-ε->(3)-b->(4)
            # currentState=4
            G.add_edge(str(currentState),str(currentState+1),label=item)
        else:
            # (0)-ε->(1)-A->(2)
            # currentState =2
            G.add_edge(str(currentState),str(currentState+1),label=item)
            G.add_edge(str(currentState+1),"F",label="ε")
        # print('nodes',expression)    


def bnf_to_afn(grammar):

    global G, non_terminals,non_terminals_list,rootState,currentState
    
    
    # get non_terminals
    getNonTerminals(grammar)
    print('non_terminals',non_terminals)

    # define first and final state 
    G.add_node(str(rootState), initial=True)
    G.add_node("F", final=True)

    # get the first production
    head, body = grammar[0].split(" -> ")
    expressions = body.split(" | ")

    # generate the full graph
    iterate(expressions=expressions)
        
    
    # Dibuja el grafo
    pos = nx.spring_layout(G, seed=10)
    labels = {edge: G.edges[edge]["label"] for edge in G.edges}
    nx.draw(G, pos, with_labels=True, node_size=500, node_color="lightblue", font_size=10)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

def updateGraphNonTerminal(element,expression , isFirstItem = False):
    global G, non_terminals,non_terminals_list,rootState,currentState

    for j,item in enumerate(expression):
        # A a
        # item = A

        # check if the current item is a non_terminal
        if(item in non_terminals_list):
            updateGraphNonTerminal(item,non_terminals[item], isFirstItem= isFirstItem and j == 0)    
            continue

        print('item',item, 'j: ',j, 'currentState',currentState)
        currentState += 1
        if(j==0 and isFirstItem == True):
            # (0)-ε->(1)-A->
            G.add_edge(str(rootState),str(currentState),label="ε")
            G.add_edge(str(currentState),str(currentState+1),label=item)
        elif(j < len(expression)-1):
            # rootState += 1
            # (0)-ε->(3)-b->(4)
            # currentState=4
            G.add_edge(str(currentState),str(currentState+1),label=item)
        else:
            # (0)-ε->(1)-A->(2)
            # currentState =2
            G.add_edge(str(currentState),str(currentState+1),label=item)
            G.add_edge(str(currentState+1),"F",label="ε")
        # print('nodes',expression)    


# Gramática BNF

# Crear un grafo dirigido para representar el AFN
G = nx.DiGraph()

non_terminals = {}
non_terminals_list = list()

# initial and final state
rootState = 0
currentState = 0
BNF = [
    "S -> A a | b A c | d c | b d a",
    "A -> d | f",
]

# Convertir la gramática en un AFN
afn = bnf_to_afn(BNF)


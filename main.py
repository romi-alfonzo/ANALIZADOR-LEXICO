import networkx as nx
import matplotlib.pyplot as plt

def getNonTerminals(grammar):
    # global non_terminals,non_terminals_list
    non_terminals = {}
    non_terminals_list = list()
    for production in grammar:
        head, body = production.split(" -> ")
        non_terminals[head.strip()]  = set(body.split(" | "))
        non_terminals_list.append(head.strip())

    return non_terminals, non_terminals_list

def iterate(expressions, currentState, rootState,G, rootFinalState):
    # global currentState
    for i,expression in enumerate(expressions):
        print("i:",i,"len:",len(expression), 'expression: ',expression)
        # A a | b A c | d c | b d a

        # remove blank spaces
        expression =expression.replace(" ","")
        G,rootState,currentState = updateGraph(expression= expression, isFirstItem=True, rootState=rootState, currentState=currentState, G=G, rootFinalState= rootFinalState)
        currentState+=1

    return G, currentState,rootState
def updateGraph(expression ,G ,rootState , currentState,rootFinalState, isFirstItem = False):
    global non_terminals,non_terminals_list
    for j,item in enumerate(expression):
        # A a
        # item = A

        
        # check if the current item is a non_terminal
        if(item in non_terminals_list):
            # get the first production
            print(non_terminals[item])
            # head, body = non_terminals[item].split(" -> ")
            expressions = non_terminals[item]
            print('head,body',expressions)
            
            # Aux = nx.DiGraph()
             # define first and final state 

            G.add_edge(str(currentState),str(currentState+1),label="ε")
            currentState+=1
            
            # Aux.add_edge(str(currentState), initial=True)
            # Aux.add_edge(rootFinalState + str(currentState) , final=True)
            G,currentState,rootAux = iterate(expressions=expressions, currentState=currentState, rootState = currentState,G=G, rootFinalState = rootFinalState)

            print('expression',expression)

            if(len(expression) == 1):
                # G.add_edge(str(currentState+1),rootFinalState + str(rootState) ,label="ε")
                G.add_edge(rootFinalState + str(rootAux),rootFinalState + str(rootState) ,label="ε")
            else:
                G.add_edge(rootFinalState + str(rootAux),str(currentState+1) ,label="ε")

            # print(G)
            # pos = nx.spring_layout(G, seed=10)
            # labels = {edge: G.edges[edge]["label"] for edge in G.edges}
            # nx.draw(G, pos, with_labels=True, node_size=500, node_color="lightblue", font_size=10)
            # nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
            # plt.show()
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
            G.add_edge(str(currentState+1),rootFinalState + str(rootState) ,label="ε")
        # print('nodes',expression)   

        # is just one expression 
        if(len(expression) == 1):
            # G.add_edge(str(currentState),str(currentState+1),label=item)
            G.add_edge(str(currentState+1),rootFinalState + str(rootState) ,label="ε")
    return G,rootState,currentState


def bnf_to_afn(grammar, rootState = 0, currentState = 0):

    # global G, non_terminals,non_terminals_list,rootState,currentState
    G = nx.DiGraph()

    # non_terminals = {}
    # non_terminals_list = list()

    # initial and final state
    rootState = 0
    currentState = 0
    rootFinalState = "F"
    
    
    # define first and final state 
    G.add_node(str(rootState), initial=True)
    G.add_node(rootFinalState + str(rootState) , final=True)

    # get the first production
    head, body = grammar[0].split(" -> ")
    expressions = body.split(" | ")

    # generate the full graph
    G,_,_ = iterate(expressions=expressions, currentState=currentState, rootState = rootState,G=G, rootFinalState = rootFinalState)
        
    
    # Dibuja el grafo
    pos = nx.spring_layout(G, seed=10)
    labels = {edge: G.edges[edge]["label"] for edge in G.edges}
    nx.draw(G, pos, with_labels=True, node_size=300, node_color="lightblue", font_size=5)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

# Gramática BNF

# Crear un grafo dirigido para representar el AFN
# G = nx.DiGraph()

# non_terminals = {}
# non_terminals_list = list()

# # initial and final state
# rootState = 0
# currentState = 0
BNF = [
    "S -> A a | b A c | d c | b d a",
    "A -> d",
]
# BNF = [
#     "S -> A a",
#     "A -> d | f",
# ]
# get non_terminals
non_terminals, non_terminals_list = getNonTerminals(BNF)
# Convertir la gramática en un AFN
afn = bnf_to_afn(BNF)


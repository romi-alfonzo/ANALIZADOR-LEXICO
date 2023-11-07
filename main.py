class AFN:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.start_state = start_state
        self.accept_states = accept_states
def print_afn(transitions):
    
    for states in transitions:
        print("(",f"{states}",")")
    
        for state in transitions[states]:
            print('==>',state)
            
                
            
            
    

def bnf_to_afn(grammar):
    # Inicializa las estructuras de datos del AFN
    states = set()
    alphabet = set()
    transitions = {}
    start_state = None
    accept_states = set()

    # Recorre las producciones BNF y construye el AFN
    for production in grammar:
        head, body = production.split(" -> ")
        non_terminal = head.strip()
        expressions = body.split(" | ")
        
        if start_state is None:
            start_state = non_terminal

        # Agrega los estados y símbolos al AFN
        states.add(non_terminal)
        alphabet.update(list(non_terminal))

        # Crea transiciones para las expresiones en la producción
        # print('expressions', expressions)
        for expression in expressions:
            # print('expression', expression)
            expression = expression.strip()
        
            if expression == 'ε':
                continue
            print('expresion',expression)
            if non_terminal not in transitions:
                transitions[non_terminal] = {}

            for symbol in expression:
                if symbol == ' ':
                    continue
                # print('symbol',symbol)
                if symbol not in transitions[non_terminal]:
                    transitions[non_terminal][symbol] = set()
                transitions[non_terminal][symbol].add(expression)
                # print('transitions',transitions)

        # print('transitions',transitions)
    print_afn(transitions)
    return AFN(states, alphabet, transitions, start_state, accept_states)

# Gramática BNF
BNF = [
    "S -> A a | b A c | d c | b d a",
    "A -> d"
]

# Convertir la gramática en un AFN
afn = bnf_to_afn(BNF)

# Imprimir el AFN
# print("Estados:", afn.states)
# print("Alfabeto:", afn.alphabet)
# print("Transiciones:", afn.transitions)
# print("Estado Inicial:", afn.start_state)
# print("Estados de Aceptación:", afn.accept_states)

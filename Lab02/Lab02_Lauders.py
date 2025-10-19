from automaton import DFA_Automaton

sigma = ['0','1']
state_set = ['q0', 'q1', 'q2', 'q3']
accept_set = ['q2']
start_state = 'q0'
delta = {
        ('q0', '0') : 'q1', 
        ('q0', '1') : 'q0', 

        ('q1', '0') : 'q1', 
        ('q1', '1') : 'q2',

        ('q2', '0') : 'q1',
        ('q2', '1') : 'q2',

        ('q3', '0') : 'q2',
        ('q3', '1') : 'q3',
    }

# automaton = DFA_Automaton(sigma, state_set, accept_set, start_state, delta)

# Optimize
# automaton.optimize() 

sigma = ['0','1']
state_set = ['q0', 'q1', 'q2', 'q3', 'q4', 'q5']
accept_set = ['q1', 'q2', 'q5']
start_state = 'q0'
delta = {
        ('q0', '0') : 'q1', 
        ('q0', '1') : 'q2', 

        ('q1', '0') : 'q3', 
        ('q1', '1') : 'q4',

        ('q2', '0') : 'q4',
        ('q2', '1') : 'q3',

        ('q3', '0') : 'q5',
        ('q3', '1') : 'q5',

        ('q4', '0') : 'q5',
        ('q4', '1') : 'q5',

        ('q5', '0') : 'q5',
        ('q5', '1') : 'q5',
    }

automaton = DFA_Automaton(sigma, state_set, accept_set, start_state, delta)

# Optimize
optimized_dfa = automaton.optimize() 
for item in optimized_dfa:
    print(item)
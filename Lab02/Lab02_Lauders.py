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

automaton = DFA_Automaton(sigma, state_set, accept_set, start_state, delta)

# Optimize
automaton.optimize() 
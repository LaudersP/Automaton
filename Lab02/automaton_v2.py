class DFA_Automaton:
    def __init__(self, sigma, state_set, accept_set, start_state, delta):
        self._sigma = sigma
        self._state_set = state_set
        self._accept_set = accept_set
        self._start_state = start_state
        self._delta = delta

    def run(self, input_string):
        # Set the start state
        current_state = self._start_state

        # Iterate the input string
        for ch in input_string:
            # Check that ch is in sigma
            if ch not in self._sigma: return False

            # Get next state
            current_state = self._delta[(current_state, ch)]

        # Return accepted status
        return (current_state in self._accept_set)
    
    def optimize(self):
        # Copy delta
        optimized_delta = self._delta

        # Get reachable states using BFS
        queue = [self._start_state]
        reachable_states = {self._start_state}
        while queue:
            # Get state from queue
            current_state = queue.pop()

            # Check all possible transitions from current state
            
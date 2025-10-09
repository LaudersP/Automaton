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
            current_state = queue.pop(0)

            # Check all possible transitions from current state
            for transition in self._delta.items():
                state = transition[0][0]
                next_state = transition[1]

                # Check if state is current and the next state has not yet been visited
                if state == current_state and next_state not in reachable_states:
                    queue.append(next_state)
                    reachable_states.add(next_state)

        # Remove unreachable states
        for state in self._state_set:
            # Check if it was reachable
            if state in reachable_states: continue

            # Remove state
            self._state_set.remove(state)
            optimized_delta.pop((state, '0'))
            optimized_delta.pop((state, '1'))

        # Generate all possible pair combinations
        pairs = {}
        for state in self._state_set:
            for pair_state in self._state_set:
                # Skip (state, state) pairs
                if pair_state is state: continue

                # See if the current pair needs added
                if (state, pair_state) not in pairs and (pair_state, state) not in pairs:
                    # Check if one or the other are accept state
                    if (state in self._accept_set and pair_state not in self._accept_set) or (state not in self._accept_set and pair_state in self._accept_set):
                        pairs[(state, pair_state)] = 1
                    else:
                        pairs[(state, pair_state)] = 0
                        
        while True:
            marked_pair = False
            for (state0, state1), marked in pairs.items():
                # Check if state pair is already marked
                if marked == 1: continue

                # Check the destination of the pair using sigma
                end_state = None
                for char in self._sigma:
                    end_state = (self._delta[(state0, char)],self._delta[(state1, char)])
                    reversed_end_state = (end_state[1], end_state[0])

                    # Check if end_state is the same state
                    if end_state[0] is end_state[1]: continue
                    # Check if end_state is marked
                    if pairs[end_state] == 1:
                        pairs[(state0, state1)] = 1
                        marked_pair = True

            if marked_pair is False:
                break

            
        print(pairs)
            
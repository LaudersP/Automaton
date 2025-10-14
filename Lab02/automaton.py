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
            print(f"Removing: {state}")
            self._state_set.remove(state)
            optimized_delta.pop((state, '0'))
            optimized_delta.pop((state, '1'))

        # Generate all possible pair combinations
        pairs = {}
        for state_i in self._state_set:
            for state_j in self._state_set:
                # Skip same state pairs
                if state_j == state_i: continue

                # See if the current pair needs added
                if pairs.get((state_i, state_j)) == None and pairs.get((state_j, state_i)) == None:
                    pairs[(state_i, state_j)] = 0

        # Mark pairs where one or the other are accept states
        for (state_i, state_j), _ in pairs.items():
            # Check if the pair contains a accept state and a non-accept state
            if((state_i in self._accept_set) == (state_j in self._accept_set)): continue

            # Mark pair for being different
            pairs[(state_i, state_j)] = 1

            # Loop until no new pairs are marked
            while True:
                marked_new_pair = False
                for (state_i, state_j), pair_marked in pairs.items():
                    # Skip already marked pairs
                    if pair_marked: continue

                    # Get the possible endings from the current pair
                    for char in self._sigma:
                        ending_pair = (optimized_delta[(state_i, char)], optimized_delta[(state_j, char)])
                        
                        # Check if the ending pair is the same state
                        if ending_pair[0] == ending_pair[1]: continue

                        # Check if the ending_pair is marked
                        if pairs.get((ending_pair[0], ending_pair[1])) == 1 or pairs.get((ending_pair[1], ending_pair[0])) == 1:
                            pairs[(state_i, state_j)] = 1
                            marked_new_pair = 1

                if marked_new_pair is False:
                    break

        # Any pair unmarked are indistinct and can be combined into a single state
        for (state_i, state_j), pair_marked in pairs.items():
            # Skip if pair is marked
            if pair_marked: continue

            # Combine pair into a single state
            print(f"To remove: {(state_i, state_j)}")
            
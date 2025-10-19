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
        # Copy automaton
        optimized_state_set = self._state_set
        optimized_accept_set = self._accept_set
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

        # Get unmarked pairs
        unmarked_pairs = []
        for (state_i, state_j), pair_marked in pairs.items():
            # Skip if pair is marked
            if pair_marked: continue

            unmarked_pairs.append((state_i, state_j))

        # Combine unmarked pairs
        while unmarked_pairs:
            # Get a pair of states
            current_pair = unmarked_pairs.pop(0)

            # Check that the ending states go to the same state
            ending_on_0 = (optimized_delta[(current_pair[0], "0")], optimized_delta[(current_pair[1], "0")])
            ending_on_1 = (optimized_delta[(current_pair[0], "1")], optimized_delta[(current_pair[1], "1")])
            if ending_on_0[0] != ending_on_0[1] or ending_on_1[0] != ending_on_1[1]:
                unmarked_pairs.append(current_pair)
                continue

            # Get the index of the first state in the optimized state set
            list_index = optimized_state_set.index(current_pair[0])

            # Replace it with the new optimized state
            optimized_state_set[list_index] = current_pair[0]+current_pair[1]

            # Remove the second state from the optimized state set
            optimized_state_set.remove(current_pair[1])

            # Replace the states in the optimized accept state
            for accept_state in optimized_accept_set:
                # Check if it is one of the current pair states
                if accept_state != current_pair[0] and accept_state != current_pair[1]: continue

                # Check if the optimized accept state is already present
                if current_pair[0] + current_pair[1] in optimized_accept_set: continue

                # Find the index and replace it with the optimized state name
                list_index = optimized_accept_set.index(accept_state)
                optimized_accept_set[list_index] = current_pair[0] + current_pair[1]

                # Check if the other state is a accept state
                if current_pair[0] in optimized_accept_set:
                    optimized_accept_set.remove(current_pair[0])
                elif current_pair[1] in optimized_accept_set:
                    optimized_accept_set.remove(current_pair[1])

            # Remove states from optimized delta list
            optimized_delta.pop((current_pair[0], "0"))
            optimized_delta.pop((current_pair[0], "1"))
            optimized_delta.pop((current_pair[1], "0"))
            optimized_delta.pop((current_pair[1], "1"))

            # Add the new combined state to delta list
            optimized_delta[(current_pair[0] + current_pair[1], "0")] = ending_on_0[0]
            optimized_delta[(current_pair[0] + current_pair[1], "1")] = ending_on_1[0]
            
            # Add the transitions to prior states to delta list
            for (state, char), end_state in optimized_delta.items():
                # Check if end state is one of the current pair states
                if end_state == current_pair[0] or end_state == current_pair[1]:
                    # Set the transition to point to the new optimized state
                    optimized_delta[(state, char)] = current_pair[0] + current_pair[1]

        return (self._sigma, optimized_state_set, optimized_accept_set, self._start_state, optimized_delta)
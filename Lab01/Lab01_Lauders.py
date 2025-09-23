from automaton import DFA_Automaton

def part_i(input_string):
    sigma = ['M', 'I', 'U']
    state_set = ['q0', 'q1', 'q2', 'q3', 'q4']
    accept_set = ['q2', 'q3']
    start_state = 'q0'
    delta = {
        ('q0', 'M'): 'q1',
        ('q0', 'I'): 'q4',
        ('q0', 'U'): 'q4',

        ('q1', 'M'): 'q4',
        ('q1', 'I'): 'q2',
        ('q1', 'U'): 'q1',

        ('q2', 'M'): 'q4',
        ('q2', 'I'): 'q3',
        ('q2', 'U'): 'q2',

        ('q3', 'M'): 'q4',
        ('q3', 'I'): 'q1',
        ('q3', 'U'): 'q3',

        ('q4', 'M'): 'q4',
        ('q4', 'I'): 'q4',
        ('q4', 'U'): 'q4',
    }

    miu_automaton = DFA_Automaton(sigma, state_set, accept_set, start_state, delta)

    return miu_automaton.run(input_string)

def part_ii(): 
    input_is_valid = False 
    while input_is_valid is False: 
        # Get the user input 
        miu_string = input("Enter a MIU string: ").upper().strip() 

        # Check if the input is valid 
        input_is_valid = part_i(miu_string) 

        # Act on invalid input 
        if input_is_valid is False: 
            print("Invalid MIU string\n") 

    print("\nStart: MI\n")

    # Input is valid, output step by step derivation 
    # ... along with the rule used at each step 
    def rule_1(string):
        print("Rule: If xI is a valid string, then so is xIU")
        result = string + 'U'
        print(f"Result: {result}\n")
        return result

    def rule_2(string):
        print("Rule: If Mx is a valid string, then so is Mxx")
        result = string + string[1:]
        print(f"Result: {result}\n")
        return result

    def rule_3(string, index):
        print("Rule: In any valid string, III can be replaced by U")
        result = string[:index] + 'U' + string[index+3:]
        print(f"Result: {result}\n")
        return result

    def rule_4(string, index):
        print("Rule: UU can be dropped from any valid string")
        result = string[:index] + string[index+2:]
        print(f"Result: {result}\n")
        return result
    
    # Shortest Option: Tree that has all possible outcomes from the current string
    # .. The firs time hitting the desired output is the shortest derivation

    # Smallest Memory Option: Get the number of I's required, then compress them into the final form

    # Get the number of I's required
    num_of_i = 0
    for char in miu_string:
        match(char):
            # Add count of 1
            case 'I':
                num_of_i += 1
            # Add count od 3
            case 'U':
                num_of_i += 3

    # Start the derivation to the number of I's needed
    derivation_string = "MI"
    while derivation_string.count("I") < num_of_i:
        derivation_string = rule_2(derivation_string)

    # Compress the beginning of the derivation string to the desired miu string
    miu_string_length = len(miu_string)
    while derivation_string[:miu_string_length] != miu_string:
        # Get the first none matching index
        index = 0
        for i in range(miu_string_length):
            if derivation_string[i] != miu_string[i]:
                index = i
                break

        # Perform rule 3
        if index != 0:
            derivation_string = rule_3(derivation_string, index)

    # Get the number of remaining I's
    remaining_i_count = len(derivation_string[miu_string_length:])

    # Check if complete
    if (remaining_i_count / 3) == 0: return

    # Check if rule 1 is required
    elif (remaining_i_count / 3) == 1:
        derivation_string = rule_1(derivation_string)   

    # Apply rule 3 to the first three remaining I's
    derivation_string = rule_3(derivation_string, miu_string_length)    

    # Check if rule 3 is required again
    if (remaining_i_count / 3) == 2:
        derivation_string = rule_3(derivation_string, miu_string_length + 1)

    # Apply rule 4 to get only the miu string
    derivation_string = rule_4(derivation_string, miu_string_length)

def main():
    ## Part 1
    # MIU System Strings
    strings = ["MUIIU", "MIUIUIUIU", "MIIUIIU", "MIIIIUI", "U", "MU"]

    # Iterate through the strings to perform 
    for string in strings:
        print(f"String: {string}\nValid: {part_i(string)}\n")

    ## Part 2
    part_ii()

if __name__ == "__main__":
    main()
list_state=['lagos', 'osun', 'ekiti']

def validate_states(myState):
    myState = myState.lower()
    if myState in list_state:
        return myState 

validate_states('EKIti1')
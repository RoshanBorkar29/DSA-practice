

import heapq

def validate_events(events):
    return all(start<=end for start ,end in events)

def can_attend_all(events):

    if not validate_events(events):
         raise ValueError("Event end time cannot be earlier than start time")
    events=sorted(events)

    ## we will check if consecutive events overlap if it does meetings
    ##can't be attended 
    for i in range(1,len(events)):
        if events[i][0]<events[i-1][1]:
            return False
    print("All meetings can be attended!!")
    return True
    

def min_rooms_required(events):
    if not validate_events(events):
         raise ValueError("Event end time cannot be earlier than start time")

    ## so first of all we sort the event with its start time
    ## tc->o(logn) and sc->o(n) as we will get sorted copy which is extra
    events=sorted(events)

    #### after that we will store end times of meetings in heap
    ## create rooms heap where it will take o(logn) and space o(n)

    rooms=[]
    for start,end in events:
        ## this is fro checking whether we can reuse any room if its meeting has ended
        if rooms and rooms[0]<=start:
            heapq.heappop(rooms)

        ## insert into heap the current meeting that need room
        heapq.heappush(rooms,end)

    return len(rooms)## at last this will return the number of rooms used by the all meetings

# Cases
events = [(9, 10), (10, 11), (11, 12)]

print(can_attend_all(events))       
print(f"Total rooms required :{min_rooms_required(events)}")   

events2 = [(9, 11), (10, 12), (11, 13)]

print(can_attend_all(events2))       
print(f"Total rooms required :{min_rooms_required(events2)}")  

events3=[(0,0),(1,0)]

print(can_attend_all(events3))
print(f"Total rooms required :{min_rooms_required(events3)}")

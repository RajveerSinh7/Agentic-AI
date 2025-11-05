#simple reflex agent (if ___ then do ___) not intelligent or adaptive
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time

#define 2X2 environment (the house with 4 rooms)
environment = {
    "Room1":"Clean",
    "Room2":"Dirty", #start with dirt here
    "Room3":"Clean",
    "Room4":"Clean"
}

#mapping the room positions
room_positions = {
    "Room1":(0,1), #top-left                
    "Room2":(1,1), #top-right                   
    "Room3":(0,0), #bottom-left
    "Room4":(1,0), #bottom-right
}

rooms = list(environment.keys())

agent_index=0 #means the agent starts in room1

def reflex_agent(state):
    if state == "Dirty":
        return "Clean"
    else:
        return "Move"
    
#Drawing the rooms
def draw_environment(env, agent_pos, step):
    fig, ax=plt.subplots()
    ax.set_xlim(0,2)
    ax.set_ylim(0,2)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(f"Step {step} - Agent in {rooms[agent_pos]}")

    for room, pos in room_positions.items():
        x,y = pos
        color = 'red' if env[room] == "Dirty" else 'green'
        rect = patches.Rectangle((x,y),1,1,facecolor=color,edgecolor='black')
        ax.add_patch(rect)
        ax.text(x+0.5, y+0.5, room, ha='center', va='center', color='white',fontsize=10)

    #draw agent
    agent_x, agent_y = room_positions[rooms[agent_pos]] #finds the agents position
    agent_patch = patches.Circle((agent_x + 0.5, agent_y + 0.5), 0.1, color='blue')
    ax.add_patch(agent_patch)

    plt.pause(1)
    plt.savefig(f"step_{step}.png")
    plt.close

#run simulation
plt.ion() #"interaction mode on" see results after each step
steps=8

for step in range(steps):
    current_room = rooms[agent_index]
    state = environment[current_room]
    action = reflex_agent(state)

    draw_environment(environment, agent_index, step+1)

    if action == "Clean": #if agent decides to clean, this line updates
        environment[current_room] = "Clean"
    
    else:
        agent_index=(agent_index +1) % len(rooms)

plt.ioff() #stop the interaction mode

print(">> Simulation complete!")
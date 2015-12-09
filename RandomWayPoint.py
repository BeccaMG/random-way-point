import matplotlib.pyplot as plt
import networkx as nx
from Globals import *
import numpy as np


def calculate_mean_speed(action_time, speed, split_minute):
    global simulation_time, mean_speed
    while action_time > 0:
        # Checks if last input in the array is the mean of a complete minute or not
        # i.e. the last input in the array is the mean for only a portion of the last minute of simulation
        if split_minute != 0:
            if action_time + split_minute >= 1:
                # Calculate the final mean speed of this minute
                mean_speed[-1] = mean_speed[-1] * split_minute + speed * (1 - split_minute)
                # Increment the simulation time by the time needed to complete this action
                simulation_time += 1 - split_minute
                action_time -= 1 - split_minute  # Keeping what's left from the movement
                split_minute = 0
            # After incrementing the action the minute is not over yet
            else:
                # Calculate mean speed after this action
                mean_speed[-1] = mean_speed[-1] * split_minute + speed * action_time
                simulation_time += action_time
                # Increment the split_minute with the time of the action
                split_minute += action_time
                action_time = 0
        # If last minute is complete and we are computing a new minute
        elif action_time >= 1:
            action_time -= 1
            simulation_time += 1
            mean_speed.append(speed)
        # If after computing this loop the minute will not be over yet
        else:
            simulation_time += action_time
            # Has the value of the consumed portion of the minute
            split_minute = action_time
            action_time = 0
            mean_speed.append(speed)
        # If at any time the simulation_time reached the STOP_TIME stop the simulation
        if simulation_time >= STOP_TIME:
            break
    return split_minute


def simulate_random_way_point():
    global simulation_time, mean_speed, rwp, node_pos

    # The current time of simulation
    simulation_time = 0
    # Vector containing mean speeds for each minute of the simulation
    mean_speed = []
    # The Random Way Point graph
    rwp = nx.Graph()
    # The spent time of a minute while calculating the mean speed
    split_minute = 0.0

    # Position of each node in the graph
    node_pos = []

    # The initial position (x,y) is chosen uniformly in both the axes
    x_src = np.random.uniform(X_MIN, X_MAX)
    y_src = np.random.uniform(Y_MIN, Y_MAX)
    i = 0
    rwp.add_node(i)
    i += 1
    node_pos.append((x_src, y_src))

    while simulation_time < STOP_TIME:
        # The destination of the agent chosen uniformly in both the axes
        x_dst = np.random.uniform(X_MIN, X_MAX)
        y_dst = np.random.uniform(Y_MIN, Y_MAX)

        # The velocity of the agent chosen uniformly in between the limits
        speed = np.random.uniform(V_MIN, V_MAX)

        rwp.add_node(i)
        rwp.add_edge(i-1, i, weight=round(speed, 2))
        i += 1
        node_pos.append((x_dst, y_dst))

        # Move mobile
        # Distance between src and dst
        distance = math.sqrt((x_src - x_dst)**2 + (y_src - y_dst)**2)

        # Compute time taken to go from src to dst
        current_way_time = distance/speed

        x_src, y_src = x_dst, y_dst

        split_minute = calculate_mean_speed(current_way_time, speed, split_minute)

        # If at any time the simulation_time reached the STOP_TIME stop the simulation
        if simulation_time >= STOP_TIME:
            break

        # The pause time of the agent chosen uniformly in between the limits
        p = np.random.uniform(PAUSE_MIN, PAUSE_MAX)

        # Calls mean_speed_calculator
        split_minute = calculate_mean_speed(p, 0, split_minute)

    return mean_speed


if __name__ == '__main__':
    global rwp, node_pos

    # ------------
    # Run the file
    # ------------

    simulate_random_way_point()

    # ----------------
    # Shows the graph
    # ----------------

    plt.figure('Random Way Point')
    nx.draw_networkx(rwp, node_pos, node_size=100, node_label=False)
    # Show axis of the graph
    plt.axis('on')
    # Shows the graph in (Random Way Point) window
    plt.show()

    # TODO check usefulness
    # Outputs graph to RandomWayPoint.gexf
    nx.write_gexf(rwp, "RandomWayPoint.gexf")

    # -----------------------
    # Write in an output file
    # -----------------------

    # Opens the output file
    fo = open("mean_speeds.txt", "a")
    # Appends mean speeds of each minute to mean_speeds.txt
    np.savetxt(fo, mean_speed, fmt='%f', newline=' ')
    fo.write("\n")
    # Closes the output file
    fo.close()



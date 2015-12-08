from Globals import *
import numpy as np
import math

# Open the output file
fo = open("mean_speeds.txt", "a")
# The current time of simulation
simulation_time = 0
# Vector containing mean speeds for each minute of the simulation
mean_speed = []


def mean_speed_calculator(action_time, speed, split_minute):
    global simulation_time, mean_speed
    while action_time > 0:
        if split_minute != 0:
            if action_time + split_minute >= 1:
                mean_speed[-1] = mean_speed[-1] * split_minute + speed * (1 - split_minute)
                simulation_time += 1 - split_minute
                action_time -= 1 - split_minute  # Keeping what's left from the movement
                split_minute = 0
            else:
                mean_speed[-1] = mean_speed[-1] * split_minute + speed * action_time
                simulation_time += action_time
                split_minute += action_time
                action_time = 0
        elif action_time >= 1:
            action_time -= 1
            simulation_time += 1
            mean_speed.append(speed)
        else:
            simulation_time += action_time
            split_minute = action_time
            action_time = 0
            mean_speed.append(speed)

        if simulation_time >= STOP_TIME:
            break
    return split_minute


def main():
    global simulation_time, mean_speed, fo
    # The spent time of a minute while calculating the mean speed
    split_minute = 0.0

    # Standard deviation of the uniform distribution (velocity)
    # sqrt( (B-A)^2 / 12 )
    std_dev = math.sqrt((V_MAX-V_MIN)**2 / 12)

    # Computing the size of the sample with precision (r) 5%
    # and confidence level 95% (Z-score = 1.96)
    z = 1.96
    r = 5
    # Check http://www.qualtrics.com/blog/determining-sample-size/
    n = ((100 * z * std_dev) / r)**2

    print "Sample size = %f" % n

    # The initial position (x,y) is chosen uniformly in both the axes
    x_src = np.random.uniform(X_MIN, X_MAX)
    y_src = np.random.uniform(Y_MIN, Y_MAX)

    while simulation_time < STOP_TIME:
        # The destination of the agent chosen uniformly in both the axes
        x_dst = np.random.uniform(X_MIN, X_MAX)
        y_dst = np.random.uniform(Y_MIN, Y_MAX)

        # The velocity of the agent chosen uniformly in between the limits
        speed = np.random.uniform(V_MIN, V_MAX)

        # Move mobile
        # Distance between src and dst
        distance = math.sqrt((x_src - x_dst)**2 + (y_src - y_dst)**2)

        # Compute time taken to go from src to dst
        current_way_time = distance/speed

        x_src, y_src = x_dst, y_dst

        split_minute = mean_speed_calculator(current_way_time, speed, split_minute)

        if simulation_time >= STOP_TIME:
            break

        # The pause time of the agent chosen uniformly in between the limits
        p = np.random.uniform(PAUSE_MIN, PAUSE_MAX)

        split_minute = mean_speed_calculator(p, 0, split_minute)

    print "Current Time = %f" % (simulation_time/60)

    np.savetxt(fo, mean_speed, fmt='%f', newline=' ')
    fo.write("\n")


if __name__ == '__main__':
    main()
    fo.close()


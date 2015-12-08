import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math

# The Random Way Point model
RWP = nx.DiGraph()

# The simulation area covers a square 1 km * 1 km.
# Distance in meters
X_MIN, X_MAX = 0, 1000
Y_MIN, Y_MAX = 0, 1000

# The mobile agent moves with speed in [2 km/h, 4 km/h]
# Velocity in meters/seconds
V_MIN = 2*1000/(60 * 60)
V_MAX = 4*1000/(60 * 60)

# The pause time [10 seconds, 1 minute]
# Time in seconds
PAUSE_MIN = 10
PAUSE_MAX = 60


# Standard deviation of the uniform distribution (velocity)
# sqrt( (B-A)^2 / 12 )
std_dev = math.sqrt( (V_MAX-V_MIN)**2 / 12 )

# Computing the size of the sample with precision (r) 5% 
# and confidence level 95% (Z-score = 1.96)
z = 1.96
r = 5
# Check http://www.qualtrics.com/blog/determining-sample-size/
n = ( (100 * z * std_dev ) / r )**2

print "Sample size = %f" % n


# The current time of simulation
simulation_time = 0
print "Current Time = %f" % (simulation_time/(60*60))

# This mobile agent is observed during three hours
STOP_TIME = 3*60*60
print "Stop Time = %f" % STOP_TIME

# The initial position (x,y) is chosen uniformly in both the axes
x_src = np.random.uniform(X_MIN, X_MAX)
y_src = np.random.uniform(Y_MIN, Y_MAX)
print "Initial position =(%f,%f)" % (x_src, y_src)

while simulation_time < STOP_TIME:
    # The destination of the agent chosen uniformly in both the axes
    x_dst = np.random.uniform(X_MIN, X_MAX)
    y_dst = np.random.uniform(Y_MIN, Y_MAX)
    print "Destination =(%f,%f)" % (x_dst, y_dst)

    # The velocity of the agent chosen uniformly in between the limits
    speed = np.random.uniform(V_MIN, V_MAX)
    print "Speed = %f" % speed

    # Move mobile
    # Distance between src and dst
    distance = math.sqrt((x_src - x_dst)**2 + (y_src - y_dst)**2)
    print "Distance between src and dst = %f" % distance

    # Compute time taken to go from src to dst
    print "Time elapsed traveling the distance = %f" % (distance/speed)
    simulation_time += distance/speed
    print "Current Time = %f" % (simulation_time/(60*60))

    x_src, y_src = x_dst, y_dst

    # The pause time of the agent chosen uniformly in between the limits
    p = np.random.uniform(PAUSE_MIN, PAUSE_MAX)
    print "pause time = %f" % p

    simulation_time += p
    print "Current Time = %f" % (simulation_time/(60*60))
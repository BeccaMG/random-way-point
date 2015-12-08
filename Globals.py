import networkx as nx

# The Random Way Point model
RWP = nx.DiGraph()

# The simulation area covers a square 1 km * 1 km.
# Distance in meters
X_MIN, X_MAX = 0, 1000
Y_MIN, Y_MAX = 0, 1000

# The mobile agent moves with speed in [2 km/h, 4 km/h]
# Velocity in meters/minute
V_MIN = 2*1000/60
V_MAX = 4*1000/60

# The pause time [10 seconds, 1 minute]
# Time in minutes
PAUSE_MIN = 10/60
PAUSE_MAX = 1

# This mobile agent is observed during three hours
STOP_TIME = 3*60

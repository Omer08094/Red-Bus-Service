import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import mplcursors
from matplotlib.backend_bases import MouseButton
import tkinter as tk
from tkinter import messagebox

# Load the image
img = mpimg.imread('background.png')

def find_path_with_line_changes(graph, bus_lines, start, end):
    try:
        # Use Dijkstra's algorithm to find the shortest path
        path = nx.dijkstra_path(graph, source=start, target=end, weight='weight')
        path_length = nx.dijkstra_path_length(graph, source=start, target=end, weight='weight')

        # Get bus line mappings
        line_map = bus_lines_mapping(bus_lines)

        # Track bus line switches along the path
        current_line = None
        path_lines = []
        for i in range(len(path) - 1):
            node = path[i]
            next_node = path[i + 1]

            # Identify common lines between the current node and next node
            common_lines = set(line_map[node]) & set(line_map[next_node])

            if common_lines:
                if current_line not in common_lines:
                    # If there's a line switch, add it to the path_lines
                    current_line = list(common_lines)[0]
                    path_lines.append(current_line)

        return path, path_length, path_lines
    except nx.NetworkXNoPath:
        return None, None, []

# Function to calculate the total cost based on distance and bus line changes
def total_journey_cost(path_length, path_lines):
    base_fare_per_unit = 5
    line_switch_cost = total_cost(path_lines)
    return line_switch_cost + (path_length * base_fare_per_unit)


# Function to calculate the cost of switching bus lines
def total_cost(bus_lines):
    cost = 0
    cost_per_line = {
        'Yellow': 20,
        'Red': 30,
        'Blue': 15,
        'Green': 20,
        'Purple': 25,
        'Orange': 20,
        'Violet' : 12
    }
    for line in bus_lines:
        if line in cost_per_line:
            cost += cost_per_line[line]
    return cost


# Define the bus stops with their coordinates and names
bus_stops = {
    'Benazir Bhutto Park': {'pos': (-3.56, 2.639), 'name': 'Benazir Bhutto Park'},
    'Bilawal Chowrangi': {'pos': (-2.1, 1.74), 'name': 'Bilawal Chowrangi'},
    'The Forum': {'pos': (-2.726, 3.413), 'name': 'The Forum'},
    'Delhi Colony': {'pos': (-2.094, 4.0), 'name': 'Delhi Colony'},
    'Punjab Chowrangi': {'pos': (-1.341, 4.7), 'name': 'Punjab Chowrangi'},
    'Defence Phase 2 Library': {'pos': (-0.553, 5.844), 'name': 'Defence Phase 2 Library'},
    'Gold Mark': {'pos': (0.394, 6.65), 'name': 'Gold Mark'},
    'Shaukat Khanam Hospital': {'pos': (1.508, 5.77), 'name': 'Shaukat Khanam Hospital'},
    'Masjid-e-Ayesha Stop': {'pos': (3.574, 4.249), 'name': 'Masjid-e-Ayesha Stop'},
    'Saudi Consulate Bus Stop': {'pos': (-0.194, 3.612), 'name': 'Saudi Consulate Bus Stop'},
    'DHA Medical Centre': {'pos': (1.54, 3.617), 'name': 'DHA Medical Centre'},
    'Shrine of Misri Shah': {'pos': (3.6, 3.54), 'name': 'Shrine of Misri Shah'},
    'Cafe Clifton': {'pos': (-0.18, 1.881), 'name': 'Cafe Clifton'},
    'RPK Hospital': {'pos': (1.542, 1.877), 'name': 'RPK Hospital'},
    'Karachi Haleem Stop': {'pos': (3.603, 1.92), 'name': 'Karachi Haleem Stop'},
    'PSO Phase 8': {'pos': (6.262, 1.871), 'name': 'PSO Phase 8'},
    'Sync Cafe': {'pos': (4.56, 3.53), 'name': 'Sync Cafe'},
    'Savor Public Park': {'pos': (6.27, 3.64), 'name': 'Savor Public Park'},
    'DHA Golf Club': {'pos': (7.49, 3.32), 'name': 'DHA Golf Club'},
    'Creek Vista': {'pos': (7.53, 2.79), 'name': 'Creek Vista'},
    'Urban Forest': {'pos': (-2.6, 0.756), 'name': 'Urban Forest'},
    'Dolmen Mall Clifton': {'pos': (-0.16, 1.03), 'name': 'Dolmen Mall Clifton'},
    'Chunky Monkey': {'pos': (3.61, 0.52), 'name': 'Chunky Monkey'},
    'Clock Tower Seaview': {'pos': (6.258, 0.230), 'name': 'Clock Tower Seaview'},
    'Kolachi Stop': {'pos': (9.0, 0.2), 'name': 'Kolachi Stop'},
    'Do Darya Rocks': {'pos': (9.25, 1.9), 'name': 'Do Darya Rocks'},
    'Marina Bay': {'pos': (9.28, 2.73), 'name': 'Marina Bay'},
}


# Define bus lines with their routes, stations, and transfer points
bus_lines = {
    'Green': {'stations': ['Urban Forest', 'Benazir Bhutto Park', 'The Forum', 'Delhi Colony', 'Punjab Chowrangi', 'Defence Phase 2 Library', 'Gold Mark']},
    'Blue': {'stations': ['Shaukat Khanam Hospital', 'DHA Medical Centre', 'RPK Hospital']},
    'Red': {'stations': ['Urban Forest', 'Dolmen Mall Clifton', 'Chunky Monkey', 'Clock Tower Seaview','Kolachi Stop', 'Do Darya Rocks', 'Marina Bay']},
    'Yellow': {'stations': ['Gold Mark', 'Shaukat Khanam Hospital', 'Masjid-e-Ayesha Stop', 'Shrine of Misri Shah', 'Karachi Haleem Stop', 'Chunky Monkey']},
    'Purple' : {'stations' : ['The Forum', 'Bilawal Chowrangi','Cafe Clifton', 'RPK Hospital','Karachi Haleem Stop', 'PSO Phase 8', 'Do Darya Rocks']},
    'Orange' : {'stations' : ['Delhi Colony','Saudi Consulate Bus Stop', 'DHA Medical Centre', 'Shrine of Misri Shah', 'Sync Cafe', 'Savor Public Park', 'DHA Golf Club', 'Creek Vista', 'Marina Bay']},
    'Violet' : {'stations' : ['Dolmen Mall Clifton', 'Cafe Clifton', 'Saudi Consulate Bus Stop']}
}

# Define road connections with weights (distances between bus stops)
road_connections = [
    ('Urban Forest', 'Benazir Bhutto Park', 1.9),
    ('Benazir Bhutto Park', 'The Forum', 0.9),
    ('The Forum', 'Delhi Colony', 0.7),
    ('Delhi Colony', 'Punjab Chowrangi', 0.9),
    ('Punjab Chowrangi', 'Defence Phase 2 Library', 1.9),
    ('Defence Phase 2 Library', 'Gold Mark', 1.0),

    ('Gold Mark', 'Shaukat Khanam Hospital', 1.2),
    ('Shaukat Khanam Hospital', 'Masjid-e-Ayesha Stop', 2.0),
    ('Masjid-e-Ayesha Stop', 'Shrine of Misri Shah', 0.5),
    ('Shrine of Misri Shah', 'Karachi Haleem Stop', 1.4),
    ('Karachi Haleem Stop', 'Chunky Monkey', 1.0),

    ('The Forum', 'Bilawal Chowrangi', 1.5),
    ('Bilawal Chowrangi', 'Cafe Clifton', 1.6),
    ('Cafe Clifton', 'RPK Hospital', 1.6),
    ('RPK Hospital', 'Karachi Haleem Stop', 1.7),
    ('Karachi Haleem Stop', 'PSO Phase 8', 2.2),
    ('PSO Phase 8', 'Do Darya Rocks', 2.4),

    ('Urban Forest', 'Dolmen Mall Clifton', 2.1),
    ('Dolmen Mall Clifton', 'Chunky Monkey', 2.3),
    ('Chunky Monkey', 'Clock Tower Seaview', 2.1),
    ('Clock Tower Seaview', 'Kolachi Stop', 2.0),
    ('Kolachi Stop', 'Do Darya Rocks', 1.5),
    ('Do Darya Rocks', 'Marina Bay', 0.7),

    ('Marina Bay', 'Creek Vista', 1.5),
    ('Creek Vista', 'DHA Golf Club', 0.4),
    ('DHA Golf Club', 'Savor Public Park', 1.0),
    ('Savor Public Park', 'Sync Cafe', 1.4),
    ('Sync Cafe', 'Shrine of Misri Shah', 0.8),
    ('Shrine of Misri Shah', 'DHA Medical Centre', 1.8),
    ('DHA Medical Centre', 'Saudi Consulate Bus Stop', 1.5),
    ('Saudi Consulate Bus Stop', 'Delhi Colony', 1.6),

    ('Shaukat Khanam Hospital', 'DHA Medical Centre', 1.8),
    ('DHA Medical Centre', 'RPK Hospital', 1.5),
    ('Saudi Consulate Bus Stop', 'Cafe Clifton', 1.4),
    ('Cafe Clifton', 'Dolmen Mall Clifton', 0.7)
]


# Create a graph
G = nx.Graph()

# Add nodes (bus stops) to the graph
for stop, data in bus_stops.items():
    G.add_node(stop, pos=data['pos'], name=data['name'])

# Add weighted edges to the graph
G.add_weighted_edges_from(road_connections)

# Bus lines mapping function
def bus_lines_mapping(bus_lines):
    line_map = {}
    for line_name, data in bus_lines.items():
        for station in data['stations']:
            if station not in line_map:
                line_map[station] = []
            line_map[station].append(line_name)
    return line_map

# Set figure size
plt.figure(figsize=(16, 9))
# Show the image as the background
plt.imshow(img, extent=[-4, 10, -1, 7])  # Adjust extent based on your graph dimensions
# Adjust margins to remove white border around the window
plt.margins(0)
plt.subplots_adjust(left=0, right=1, top=1, bottom=0)


# Draw nodes
pos = nx.get_node_attributes(G, 'pos')
nx.draw_networkx_nodes(G, pos, node_size=700, node_color='black', edgecolors='white', linewidths=1)

# Draw labels
labels = nx.get_node_attributes(G, 'name')
nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_color='white')

# Draw bus lines and stations
for line, data in bus_lines.items():
    route = data['stations']
    line_color = line
    line_width = 2.5
    line_style = '-'
    nx.draw_networkx_edges(G, pos, edgelist=[(route[i], route[i+1]) for i in range(len(route)-1)],
                           edge_color=line_color, width=line_width, style=line_style)
    
# Add edge labels for weights
edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color='white', bbox=dict(facecolor='black', edgecolor='none', boxstyle='round,pad=0.3'))

# Create a click handler to detect mouse clicks
class MouseClickHandler:
    def __init__(self, graph, bus_lines, pos):
        self.graph = graph
        self.bus_lines = bus_lines
        self.pos = pos
        self.clicks = []
        self.default_color = 'black'  # Default node color
        self.clicked_color = 'red'  # Color for clicked nodes

    def redraw_graph(self):
        # Clear previous plot
        plt.clf()
        # Show the image as the background
        plt.imshow(img, extent=[-4, 10, -1, 7])
        
        # Draw bus lines
        for line, data in self.bus_lines.items():
            route = data['stations']
            line_color = line  # Keep original bus line color
            nx.draw_networkx_edges(
                self.graph, 
                self.pos, 
                edgelist=[(route[i], route[i + 1]) for i in range(len(route) - 1)], 
                edge_color=line_color,
                width=2.5,
                style='-'
            )

        # Redraw nodes with updated colors
        nx.draw_networkx_nodes(self.graph, self.pos, node_size=700, node_color=self.node_colors(), edgecolors='white', linewidths=1)
        nx.draw_networkx_labels(self.graph, self.pos, labels=nx.get_node_attributes(self.graph, 'name'), font_size=8, font_color='white')
        # Add edge labels for weights
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color='white', bbox=dict(facecolor='black', edgecolor='none', boxstyle='round,pad=0.3'))

        
        # Set axis labels and display the map
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title('Bus Stops Map with Road Structure, Bus Lines, and Stations')
        plt.gca().set_aspect('equal', adjustable='box')
        plt.axis('off')
        
        plt.draw()

    def node_colors(self):
        colors = {node: self.default_color for node in self.graph.nodes}
        for click in self.clicks:
            if click in colors:
                colors[click] = self.clicked_color
        return list(colors.values())

    def on_click(self, event):
        if event.button == MouseButton.LEFT:
            closest_node = min(self.pos, key=lambda node: (event.xdata - self.pos[node][0])**2 + (event.ydata - self.pos[node][1])**2)

            self.clicks.append(closest_node)

            if len(self.clicks) == 2:
                start_stop = self.clicks[0]
                end_stop = self.clicks[1]

                # Redraw the graph to update colors
                self.redraw_graph()

                # Call the function to get path details
                shortest_path, path_length, path_lines = find_path_with_line_changes(self.graph, self.bus_lines, start_stop, end_stop)

                if shortest_path:
                    total_cost = total_journey_cost(path_length, path_lines)
                    msg = (
                        f"Shortest path from {start_stop} to {end_stop}:\n"
                        f"Path: {shortest_path}\n"
                        f"Distance: {path_length} km\n"
                        f"Bus lines: {', '.join(path_lines)}\n"
                        f"Total cost: Rs{total_cost}"
                    )
                else:
                    msg = f"No path from {start_stop} to {end_stop}."

                # Display the message box with the path details
                root = tk.Tk()
                root.withdraw()  # Hide the tkinter main window
                messagebox.showinfo("Path Information", msg)

                # Clear the clicks for new input
                self.clicks = []

# Connect the click handler to the click event
click_handler = MouseClickHandler(G, bus_lines,pos)
plt.gcf().canvas.mpl_connect("button_press_event", click_handler.on_click)



# Function to find the shortest path between two bus stops and track bus line changes
def find_path_with_line_changes(graph, bus_lines, start, end):
    try:
        # Use Dijkstra's algorithm to find the shortest path
        path = nx.dijkstra_path(graph, source=start, target=end, weight='weight')
        path_length = nx.dijkstra_path_length(graph, source=start, target=end, weight='weight')

        # Get bus line mappings
        line_map = bus_lines_mapping(bus_lines)

        # Track bus line switches along the path
        current_line = None
        path_lines = []
        for i in range(len(path) - 1):
            node = path[i]
            next_node = path[i + 1]

            # Identify common lines between the current node and next node
            common_lines = set(line_map[node]) & set(line_map[next_node])

            if common_lines:
                if current_line not in common_lines:
                    # If there's a line switch, add it to the path_lines
                    current_line = list(common_lines)[0]
                    path_lines.append(current_line)

        return path, path_length, path_lines
    except nx.NetworkXNoPath:
        return None, None, []



# Set axis labels and display the map
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Bus Stops Map with Road Structure, Bus Lines, and Stations')
plt.gca().set_aspect('equal', adjustable='box')
plt.axis('off')

# # Add cursor to display coordinates on click
# mplcursors.cursor(hover=True)

# Show the map
plt.show()
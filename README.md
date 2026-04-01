# Red Bus Service: Karachi Transit Pathfinding System 🚌

## 📌 Project Overview
This application is a Python-based transit optimizer designed for the Clifton and DHA areas of Karachi. By modeling the city's bus network as a weighted graph, the system calculates the most efficient route between any two points based on distance, bus line availability, and fare costs.

## ✨ Key Features
* **Interactive Map GUI:** A custom-mapped interface of Karachi allowing users to select start and end points via mouse clicks.
* **Optimized Routing:** Implements **Dijkstra’s Algorithm** to find the shortest path through 27+ bus stops and 7 color-coded bus lines (Red, Green, Blue, Yellow, Purple, Orange, and Violet).
* **Dynamic Fare Calculation:** Estimates journey costs based on a base fare per kilometer plus flat-rate transfers between lines.
* **Visual Network Representation:** Overlays a real-time graph structure onto a geographic map using `Matplotlib` and `NetworkX`.

## 🛠️ Technical Stack
* **Language:** Python
* **Graph Theory:** `NetworkX` (Shortest path and weighted edge management)
* **Visualization:** `Matplotlib` (Custom coordinate mapping and UI rendering)
* **GUI Components:** `Tkinter` (Interactive alerts and message boxes)

## 📊 Business Logic
The system utilizes a weighted graph $G = (V, E)$ where:
* **Vertices ($V$):** Bus stops defined by precise geographic coordinates.
* **Edges ($E$):** Road connections weighted by actual distance ($km$).
* **Fare Logic:** $Total\ Cost = (Distance \times Base\ Rate) + \sum Transfer\ Costs$

## 🚀 Getting Started
1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Omer08094/Red-Bus-Service.git](https://github.com/Omer08094/Red-Bus-Service.git)
2. **Install dependencies:**
   ```bash
   pip install networkx matplotlib mplcursors
3. **Run the application:**
   ```bash
   python Red_Bus_Service.py

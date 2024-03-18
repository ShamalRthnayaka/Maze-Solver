import random
import tkinter as tk

# Function to generate a maze
def generate_maze():
    # Define the maze dimensions
    maze_width = 6
    maze_height = 6

    # Create an empty maze
    maze = [[' ' for _ in range(maze_width)] for _ in range(maze_height)]

    # Generate random positions for the starting point and goal
    starting_point = (random.randint(0, 1), random.randint(0, maze_height - 1))
    goal_point = (random.randint(4, 5), random.randint(0, maze_height - 1))

    # Make sure the starting point and goal are different
    while starting_point == goal_point:
        goal_point = (random.randint(4, 5), random.randint(0, maze_height - 1))

    # Place the starting point (S) and goal (G)
    maze[starting_point[1]][starting_point[0]] = 'S'
    maze[goal_point[1]][goal_point[0]] = 'G'

    # Define the number of barriers to place
    num_barriers = 4

    # Function to check if a cell is valid for placing barriers
    def is_valid(cell):
        x, y = cell
        return 0 <= x < maze_width and 0 <= y < maze_height and maze[y][x] == ' '

    # Place random barriers
    barrier_count = 0
    while barrier_count < num_barriers:
        x = random.randint(0, maze_width - 1)
        y = random.randint(0, maze_height - 1)
        if is_valid((x, y)) and (x, y) != starting_point and (x, y) != goal_point:
            maze[y][x] = 'X'
            barrier_count += 1

    return maze, starting_point, goal_point

# Function to draw the maze on the canvas
def draw_maze(maze, canvas, start, goal, cell_size, final_path=None, visited_nodes=None):
    canvas.delete("all")
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            cell = maze[y][x]
            if cell == 'S':
                canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, fill='Green')
            elif cell == 'G':
                canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, fill='Red')
            elif cell == 'X':
                canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, fill='black')

    # Draw lines to separate cells
    for y in range(1, len(maze)):
        canvas.create_line(0, y * cell_size, len(maze[0]) * cell_size, y * cell_size, fill='white')

    for x in range(1, len(maze[0])):
        canvas.create_line(x * cell_size, 0, x * cell_size, len(maze) * cell_size, fill='white')

    if final_path:
        for x, y in final_path:
            if (x, y) != start:
                canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, fill='blue', tags="path")

    if visited_nodes:
        for x, y in visited_nodes:
            if (x, y) != start and (x, y) != goal:
                canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, fill='orange', tags="visited")

# Update the movement directions to include diagonals
directions = [(1, 1), (1, 0), (1, -1), (0, 1), (0, -1), (-1, 1), (-1, 0), (-1, -1)]


def dfs(maze, start, goal, canvas, cell_size):
    stack = [(start, [])]
    visited = set()
    movements = 0  # Counter for movements

    while stack:
        (x, y), path = stack.pop()
        movements += 1  # Increment the movement counter
        print(f"DFS: Visiting node ({x}, {y})")

        if (x, y) == goal:
            print(f"DFS: Time taken to reach the goal: {movements} minutes.")
            return path

        if (x, y) not in visited:
            visited.add((x, y))
            draw_maze(maze, canvas, start, goal, cell_size, visited_nodes=visited)
            canvas.after(200)  # Introduce a delay of 100 milliseconds for visualization
            canvas.update()
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze) and maze[new_y][new_x] != 'X' and (new_x, new_y) not in visited:
                    stack.append(((new_x, new_y), path + [(x, y)]))

    return None

# Function for A* algorithm
def astar(maze, start, goal, canvas, cell_size):
    def heuristic(node, goal):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])

    open_list = [(0, start, [])]  # (cost, node, path)
    visited = set()
    movements = 0  # Counter for movements
    while open_list:
        open_list.sort()  # Sort based on cost
        _, (x, y), path = open_list.pop(0) # Pop the node with the lowest cost
        movements += 1  # Increment the movement counter
        h_value = heuristic((x, y), goal)
        print(f"A*: Visiting node ({x}, {y}) with heuristic value: {h_value}")
        if (x, y) == goal:
            total_cost = len(path)
            print(f"A*: Time taken to reach the goal: {movements} minutes.")
            print(f"A*: Total cost to reach the goal: {total_cost}")
            return path
        if (x, y) not in visited:
            visited.add((x, y))
            draw_maze(maze, canvas, start, goal, cell_size, visited_nodes=visited)
            canvas.after(200)
            canvas.update()
            for dx, dy in directions:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < len(maze[0]) and 0 <= new_y < len(maze) and maze[new_y][new_x] != 'X' and (new_x, new_y) not in visited:
                    new_path = path + [(x, y)]
                    cost = len(new_path)
                    priority = cost + heuristic((new_x, new_y), goal)
                    open_list.append((priority, (new_x, new_y), new_path))
    return None

# Create a Tkinter window
root = tk.Tk()
root.title("Maze Solver")

# Set the cell size
cell_size = 60

# Create a canvas to draw the maze
canvas = tk.Canvas(root, width=6 * cell_size, height=6 * cell_size)
canvas.pack()

# Generate and draw the maze
maze, start_point, goal_point = generate_maze()
draw_maze(maze, canvas, start_point, goal_point, cell_size)

# Function to solve the maze using DFS
def solve_dfs():
    # Clear previous path
    canvas.delete("path")
    canvas.delete("visited")
    # Solve the maze using DFS
    start = start_point
    goal = goal_point
    dfs_path = dfs(maze, start, goal, canvas, cell_size)

    # Display the path for DFS
    if dfs_path:
        for x, y in dfs_path:
            canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, fill='red', tags="path")

        # Highlight the start and goal points after solving
        draw_maze(maze, canvas, start_point, goal_point, cell_size, final_path=dfs_path)

# Function to solve the maze using A*
def solve_astar():
    canvas.delete("path")
    canvas.delete("visited")
    start = start_point
    goal = goal_point
    astar_path = astar(maze, start, goal, canvas, cell_size)

    if astar_path:
        for x, y in astar_path:
            canvas.create_rectangle(x * cell_size, y * cell_size, (x + 1) * cell_size, (y + 1) * cell_size, fill='yellow', tags="path")
        draw_maze(maze, canvas, start_point, goal_point, cell_size, final_path=astar_path)


# Create buttons for solving
dfs_button = tk.Button(root, text="DFS", command=solve_dfs, font=('Helvetica', 12), padx=10, pady=5, bg='cyan')
dfs_button.pack(side=tk.LEFT, padx=(50, 5), pady=10)

astar_button = tk.Button(root, text="A*", command=solve_astar, font=('Helvetica', 12), padx=10, pady=5, bg='lightgreen')
astar_button.pack(side=tk.LEFT, padx=5, pady=10)

# Run the Tkinter main loop
root.mainloop()

import tkinter as tk
from tkinter import ttk, messagebox
from collections import deque
import time

from graph import graph

pos = {
    "Campus Center": (400, 30),
    "Main Library": (180, 120),
    "Admin Office": (350, 120),
    "Learning Area": (550, 120),
    "Café": (750, 120),
    "Female Library": (130, 220),
    "Digital Library": (260, 220),
    "HR Office": (370, 220),
    "Freshman Office": (470, 220),
    "Staff Lounge": (560, 220),
    "LH01": (640, 220),
    "CL01": (720, 220),
    "Male Lounge": (810, 220),
    "LH02": (640, 320),
    "LH03": (640, 400),
    "LH04": (640, 480),
    "Physics Lab": (640, 560),
    "Chemistry Lab": (640, 620),
    "Biology Lab": (640, 680),
    "Sports Center": (640, 740),
    "CL02": (720, 320),
    "CL03": (720, 400),
    "CL04": (720, 480),
    "Female Lounge": (900, 220)
}

def get_predecessors(node):
    predecessors = []
    for n, neighbors in graph.items():
        for neighbor, cost in neighbors:
            if neighbor == node:
                predecessors.append(n)
    return predecessors

def bidirectional_search(start, goal, callback=None):
    if start == goal:
        return [start]
    
    forward_queue = deque([start])
    backward_queue = deque([goal])
    
    forward_visited = {start: None}
    backward_visited = {goal: None}
    
    while forward_queue and backward_queue:
        if forward_queue:
            node = forward_queue.popleft()
            
            if callback:
                callback(node, "explored")
                time.sleep(0.25)
            
            for neighbor, _ in graph[node]:
                if neighbor not in forward_visited:
                    forward_visited[neighbor] = node
                    forward_queue.append(neighbor)
                    
                    if neighbor in backward_visited:
                        path = build_path(forward_visited, backward_visited, neighbor)
                        return path
        
        if backward_queue:
            node = backward_queue.popleft()
            
            if callback:
                callback(node, "explored")
                time.sleep(0.25)
            
            for neighbor in get_predecessors(node):
                if neighbor not in backward_visited:
                    backward_visited[neighbor] = node
                    backward_queue.append(neighbor)
                    
                    if neighbor in forward_visited:
                        path = build_path(forward_visited, backward_visited, neighbor)
                        return path
    
    return None

def build_path(forward_visited, backward_visited, meeting_node):
    path = []
    
    node = meeting_node
    while node is not None:
        path.append(node)
        node = forward_visited[node]
    path.reverse()
    
    node = backward_visited[meeting_node]
    while node is not None:
        path.append(node)
        node = backward_visited[node]
    
    return path

class BidirectionalVisualization:
    def __init__(self, root):
        self.root = root
        self.root.title("BIDIRECTIONAL SEARCH - Campus Navigation")
        self.root.geometry("1200x800")
        self.root.configure(bg="#0a0a1a")
        
        main_frame = tk.Frame(root, bg="#0a0a1a")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.canvas = tk.Canvas(main_frame, width=900, height=780, bg="#0f0f1a", highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        control_frame = tk.Frame(main_frame, bg="#1a1a2e", width=280)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5, pady=10)
        control_frame.pack_propagate(False)
        
        title = tk.Label(control_frame, text="BIDIRECTIONAL SEARCH", font=("Arial", 14, "bold"), bg="#1a1a2e", fg="#e94560")
        title.pack(pady=15)
        
        desc = tk.Label(control_frame, text="Searches from both ends simultaneously", font=("Arial", 9), bg="#1a1a2e", fg="#aaaaaa")
        desc.pack(pady=5)
        
        start_frame = tk.Frame(control_frame, bg="#1a1a2e")
        start_frame.pack(pady=10, fill=tk.X, padx=20)
        
        tk.Label(start_frame, text="START:", font=("Arial", 11, "bold"), bg="#1a1a2e", fg="#00ff88").pack(anchor=tk.W)
        self.start_var = tk.StringVar(value="Campus Center")
        self.start_combo = ttk.Combobox(start_frame, textvariable=self.start_var, values=list(pos.keys()), font=("Arial", 10))
        self.start_combo.pack(fill=tk.X, pady=5)
        
        goal_frame = tk.Frame(control_frame, bg="#1a1a2e")
        goal_frame.pack(pady=10, fill=tk.X, padx=20)
        
        tk.Label(goal_frame, text="GOAL:", font=("Arial", 11, "bold"), bg="#1a1a2e", fg="#e94560").pack(anchor=tk.W)
        self.goal_var = tk.StringVar(value="Physics Lab")
        self.goal_combo = ttk.Combobox(goal_frame, textvariable=self.goal_var, values=list(pos.keys()), font=("Arial", 10))
        self.goal_combo.pack(fill=tk.X, pady=5)
        
        self.run_button = tk.Button(control_frame, text="RUN BIDIRECTIONAL SEARCH", font=("Arial", 11, "bold"), bg="#e94560", fg="white", command=self.run_search)
        self.run_button.pack(pady=15, padx=20, fill=tk.X)
        
        self.reset_button = tk.Button(control_frame, text="RESET", font=("Arial", 10), bg="#5c5c8a", fg="white", command=self.reset_canvas)
        self.reset_button.pack(pady=5, padx=20, fill=tk.X)
        
        info_frame = tk.Frame(control_frame, bg="#0f0f1a", relief=tk.RAISED, bd=2)
        info_frame.pack(pady=15, padx=20, fill=tk.X)
        
        self.steps_label = tk.Label(info_frame, text="STEPS: --", font=("Arial", 11), bg="#0f0f1a", fg="#ffffff")
        self.steps_label.pack(pady=5)
        
        self.meeting_label = tk.Label(info_frame, text="MEETING POINT: --", font=("Arial", 10, "bold"), bg="#0f0f1a", fg="#ffd700")
        self.meeting_label.pack(pady=5)
        
        path_frame = tk.Frame(control_frame, bg="#1a1a2e")
        path_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        tk.Label(path_frame, text="PATH FOUND:", font=("Arial", 10, "bold"), bg="#1a1a2e", fg="#00ff88").pack(anchor=tk.W)
        
        self.path_text = tk.Text(path_frame, height=20, width=30, bg="#0f0f1a", fg="#e0e0ff", font=("Arial", 9), wrap=tk.WORD)
        self.path_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.draw_graph()
    
    def draw_graph(self):
        self.canvas.delete("all")
        for node in graph:
            if node not in pos:
                continue
            x, y = pos[node]
            text_width = len(node) * 7
            rect_x1 = x - text_width//2 - 8
            rect_x2 = x + text_width//2 + 8
            rect_y1 = y - 10
            rect_y2 = y + 10
            
            self.canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, fill="#2d2d44", outline="#5c5c8a", width=2, tags=f"node_{node}")
            self.canvas.create_text(x, y, text=node, font=("Arial", 7, "bold"), fill="#e0e0ff", tags=f"text_{node}")
            
            for neighbor, weight in graph[node]:
                if neighbor in pos:
                    nx, ny = pos[neighbor]
                    self.canvas.create_line(x, y, nx, ny, fill="#3d3d5c", width=2)
    
    def reset_canvas(self):
        self.draw_graph()
        self.steps_label.config(text="STEPS: --")
        self.meeting_label.config(text="MEETING POINT: --")
        self.path_text.delete(1.0, tk.END)
        self.run_button.config(state=tk.NORMAL, text="RUN BIDIRECTIONAL SEARCH")
    
    def update_node_color(self, node, color):
        if node not in pos:
            return
        x, y = pos[node]
        text_width = len(node) * 7
        rect_x1 = x - text_width//2 - 8
        rect_x2 = x + text_width//2 + 8
        rect_y1 = y - 10
        rect_y2 = y + 10
        
        self.canvas.delete(f"node_{node}")
        self.canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, fill=color, outline="#7a7aaa", width=2, tags=f"node_{node}")
        self.canvas.create_text(x, y, text=node, font=("Arial", 7, "bold"), fill="#ffffff", tags=f"text_{node}")
        self.root.update()
    
    def animate_smooth_path(self, path):
        total_duration = 3.0
        steps = len(path)
        time_per_node = total_duration / steps
        
        for node in path:
            x, y = pos[node]
            text_width = len(node) * 7
            rect_x1 = x - text_width//2 - 8
            rect_x2 = x + text_width//2 + 8
            rect_y1 = y - 10
            rect_y2 = y + 10
            
            for i in range(20):
                alpha = i / 20
                if i < 10:
                    r, g, b = 50, 50, 100
                else:
                    r, g, b = 0, 255, 68
                
                color = f'#{int(r + (0 - r) * alpha):02x}{int(g + (255 - g) * alpha):02x}{int(b + (68 - b) * alpha):02x}'
                
                self.canvas.delete(f"node_{node}")
                self.canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, fill=color, outline="#7a7aaa", width=2, tags=f"node_{node}")
                self.canvas.create_text(x, y, text=node, font=("Arial", 7, "bold"), fill="#ffffff", tags=f"text_{node}")
                self.root.update()
                time.sleep(time_per_node / 20)
        
        for node in path:
            x, y = pos[node]
            text_width = len(node) * 7
            rect_x1 = x - text_width//2 - 8
            rect_x2 = x + text_width//2 + 8
            rect_y1 = y - 10
            rect_y2 = y + 10
            self.canvas.delete(f"node_{node}")
            self.canvas.create_rectangle(rect_x1, rect_y1, rect_x2, rect_y2, fill="#00ff44", outline="#7a7aaa", width=2, tags=f"node_{node}")
            self.canvas.create_text(x, y, text=node, font=("Arial", 7, "bold"), fill="#ffffff", tags=f"text_{node}")
            self.root.update()
            time.sleep(0.05)
    
    def display_path(self, path):
        self.path_text.delete(1.0, tk.END)
        for i, node in enumerate(path):
            if i == 0:
                self.path_text.insert(tk.END, f"START: {node}\n")
            elif i == len(path) - 1:
                self.path_text.insert(tk.END, f"GOAL: {node}\n")
            else:
                self.path_text.insert(tk.END, f"  {node}\n")
        
        self.steps_label.config(text=f"STEPS: {len(path) - 1}")
        
        meeting_idx = len(path) // 2
        self.meeting_label.config(text=f"MEETING POINT: {path[meeting_idx]}")
    
    def search_callback(self, node, status):
        if status == "explored":
            self.update_node_color(node, "#ffaa44")
            time.sleep(0.2)
    
    def run_search(self):
        self.reset_canvas()
        self.run_button.config(state=tk.DISABLED, text="SEARCHING...")
        
        start = self.start_var.get()
        goal = self.goal_var.get()
        
        if start not in graph or goal not in graph:
            messagebox.showerror("Error", "Invalid location!")
            self.run_button.config(state=tk.NORMAL, text="RUN BIDIRECTIONAL SEARCH")
            return
        
        self.root.update()
        
        path = bidirectional_search(start, goal, self.search_callback)
        
        if path:
            self.display_path(path)
            self.animate_smooth_path(path)
            self.run_button.config(state=tk.NORMAL, text="RUN BIDIRECTIONAL SEARCH")
        else:
            self.path_text.delete(1.0, tk.END)
            self.path_text.insert(tk.END, f"NO PATH FOUND\n")
            self.path_text.insert(tk.END, f"From '{start}' to '{goal}'")
            self.run_button.config(state=tk.NORMAL, text="RUN BIDIRECTIONAL SEARCH")

if __name__ == "__main__":
    root = tk.Tk()
    app = BidirectionalVisualization(root)
    root.mainloop()
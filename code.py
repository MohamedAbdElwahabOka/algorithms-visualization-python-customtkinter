import tkinter as tk
import customtkinter as ctk
import random
import time

class SortingVisualizer:
    """
        A class that creates a GUI that allows users to visualize the sorting algorithms bubble sort, selection sort, insertion sort, and quick sort.
    """
    def __init__(self, master):
        """
        Creates a new instance of the SortingVisualizer class.

        Args:
            master: The parent window.
        """
        self.master = master
        self.master.title("Sorting Visualizer")
        
        # Create the canvas.
        self.canvas = ctk.CTkCanvas(self.master, width=900, height=600, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=20, pady=20)
        
        # Create the button frame.
        self.button_frame = ctk.CTkFrame(self.master)
        self.button_frame.pack(side=tk.RIGHT, padx=20, pady=20)
        
        # Create the sort button.
        self.button = ctk.CTkButton(self.button_frame, text="Sort", command=self.sort)
        self.button.pack(side=tk.TOP, pady=10)
        
        # Create the stop button
        self.stop_button = ctk.CTkButton(self.button_frame, text="Stop", command=self.stop_sort, state=tk.DISABLED)
        self.stop_button.pack(side=tk.TOP, pady=10)
        
        # Create the reset button.
        self.reset_button = ctk.CTkButton(self.button_frame, text="Reset", command=self.reset)
        self.reset_button.pack(side=tk.TOP, pady=10)
        
        # Create the speed label.
        self.speed_label = ctk.CTkLabel(self.button_frame, text="Speed")
        self.speed_label.pack(side=tk.TOP, pady=10)
        
        # Create the speed slider.
        self.speed_slider = ctk.CTkSlider(self.button_frame, from_=1, to=10, width=200)
        self.speed_slider.pack(side=tk.TOP, pady=10)
        
        # Create the algorithm variable to be the main text in the beginning of the program.
        self.algorithm_var = tk.StringVar(value="Bubble Sort")
        
        # Create the algorithm menu.
        self.algorithm_menu = ctk.CTkOptionMenu(self.button_frame, values=["Bubble Sort", "Selection Sort", "Insertion Sort", "Quick Sort"], variable=self.algorithm_var,command=self.update_time_complexity)
        self.algorithm_menu.pack(side=tk.TOP, pady=10)
        
        # Create the data size label.
        self.data_size_label = ctk.CTkLabel(self.button_frame, text="Data Size")
        self.data_size_label.pack(side=tk.TOP, pady=10)
        
        # Create the data size slider
        self.size_slider = ctk.CTkSlider(self.button_frame, from_=10, to=100, width=200, command=self.reset)
        self.size_slider.pack(side=tk.TOP, pady=10)
        
        # Create the color variable to be the main text in the beginning of the program.
        self.color_var = tk.StringVar(value="Rainbow")
        
        # Create the color menu.
        self.color_menu= ctk.CTkOptionMenu(self.button_frame, values=["Rainbow", "Warm", "Cool"], variable=self.color_var)
        self.color_menu.pack(side=tk.TOP, pady=10)

        # Create the legend frame.
        self.legend_frame = ctk.CTkFrame(self.button_frame)
        self.legend_frame.pack(side=tk.TOP, pady=10)
        
        # Create the legend title label.
        self.legend_title = ctk.CTkLabel(self.legend_frame, text="Legend:")
        self.legend_title.pack(side=tk.TOP)
        
        # Create the legend items.
        self.legend_items = []
        self.legend_items.append(self.create_legend_item("#ff0000", "Unsorted"))
        self.legend_items.append(self.create_legend_item("#00ff00", "Sorted"))
        self.legend_items.append(self.create_legend_item("#0000ff", "Being Sorted"))
        self.data = self.generate_data()
        self.sorted_index = len(self.data)  # Define sorted_index attribute
        self.draw_data()
        self.sorting = False
        self.time_complexity_label = ctk.CTkLabel(self.button_frame, text="Time Complexity: O(n^2)")
        self.time_complexity_label.pack(side=tk.TOP, pady=10)
        
    def generate_data(self):
        """
            Generates a random list of numbers.

            Returns:
                A list of numbers.
        """
        return [random.randint(1, 100) for _ in range(int(self.size_slider.get()))]
        
    def draw_data(self, color="#0000ff"):
        """
            Draws the data on the canvas, with each number represented by a bar.

            Args:
                color: The color of the bars.
        """
        self.canvas.delete("all")
        bar_width = 900 // len(self.data)
        bar_gap = 2
        x0 = 0
        for i, value in enumerate(self.data):
            x1 = x0 + bar_width
            y1 = self.canvas.winfo_height()
            bar_height = value * 6
            y0 = y1 - bar_height
            if i < self.sorted_index:
                color = "#00ff00"
            elif i == self.sorted_index:
                color = "#0000ff"
            else:
                color = self.get_color(i)
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=color)
            x0 = x1 + bar_gap
        self.canvas.update()
        
    def get_color(self, index):
        """
            Gets the color of the bar at the specified index.

            Args:
                index: The index of the bar.

            Returns:
                The color of the bar.
        """
        color_scheme = self.color_var.get()
        if color_scheme == "Rainbow":
            return "#%02x%02x%02x" % (255 - self.data[index] * 2, self.data[index] * 2, 128)
        elif color_scheme == "Warm":
            return "#%02x%02x%02x" % (self.data[index] * 2, self.data[index] * 2, 255 - self.data[index] * 2)
        elif color_scheme == "Cool":
            return "#%02x%02x%02x" % (self.data[index] * 2, 255 - self.data[index] * 2, self.data[index] * 2)
        
    def create_legend_item(self, color, text):
        """
            Creates a legend item.

            Args:
                color: The color of the legend item.
                text: The text of the legend item.

            Returns:
                The legend item.
        """
        legend_item = ctk.CTkFrame(self.legend_frame)
        legend_item.pack(side=tk.TOP)
        legend_color = ctk.CTkCanvas(legend_item, width=20, height=20, bg=color, borderwidth=2, relief="sunken")
        legend_color.pack(side=tk.LEFT)
        legend_text = ctk.CTkLabel(legend_item, text=text)
        legend_text.pack(side=tk.LEFT)
        return legend_item
        
    def update_time_complexity(self, *args):
        """
            Updates the label that shows the time complexity of the selected algorithm.
        """
        algorithm = self.algorithm_var.get()
        if algorithm == "Bubble Sort":
            self.time_complexity_label.configure(text="Time Complexity: O(n^2)")
        elif algorithm == "Selection Sort":
            self.time_complexity_label.configure(text="Time Complexity: O(n^2)")
        elif algorithm == "Insertion Sort":
            self.time_complexity_label.configure(text="Time Complexity: O(n^2)")
        elif algorithm == "Quick Sort":
            self.time_complexity_label.configure(text="Time Complexity: O(n log n) avg, O(n^2) worst")
    def sort(self):
        """
            Sorts the data using the selected algorithm.
        """
        self.sorting = True
        self.button.configure(state=tk.DISABLED)
        self.stop_button.configure(state=tk.NORMAL)
        algorithm = self.algorithm_var.get()
        if algorithm == "Bubble Sort":
            self.bubble_sort()
        elif algorithm == "Selection Sort":
            self.selection_sort()
        elif algorithm == "Insertion Sort":
            self.insertion_sort()
        elif algorithm == "Quick Sort":
            self.quick_sort()
        self.sorted_index = len(self.data)
        self.draw_data()
        self.button.configure(state=tk.NORMAL)
        self.stop_button.configure(state=tk.DISABLED)
        self.sorting = False
        
    def stop_sort(self):
        """
            Stops the sorting process.
        """
        self.sorting = False
        
    def reset(self,size=None):
        """
            Clears the canvas and generates a new list of data.
        """
        self.data = self.generate_data()
        self.sorted_index = len(self.data)
        self.draw_data()
        
    def bubble_sort(self):
        """
            Sorts the data using the bubble sort algorithm.
        """
        n = len(self.data)
        for i in range(n):
            for j in range(n - i - 1):
                if not self.sorting:
                    return
                if self.data[j] > self.data[j + 1]:
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                    self.sorted_index = j
                    self.draw_data()
                    time.sleep(1 / self.speed_slider.get())
                    
    def selection_sort(self):
        """
            Sorts the data using the selection sort algorithm.
        """
        n = len(self.data)
        for i in range(n):
            min_index = i
            for j in range(i + 1, n):
                if not self.sorting:
                    return
                if self.data[j] < self.data[min_index]:
                    min_index = j
            self.data[i], self.data[min_index] = self.data[min_index], self.data[i]
            self.sorted_index = i
            self.draw_data()
            time.sleep(1 / self.speed_slider.get())
                    
    def insertion_sort(self):
        """
            Sorts the data using the insertion sort algorithm.
        """
        n = len(self.data)
        for i in range(1, n):
            key = self.data[i]
            j = i - 1
            while j >= 0 and self.data[j] > key:
                if not self.sorting:
                    return
                self.data[j + 1] = self.data[j]
                j -= 1
            self.data[j + 1] = key
            self.sorted_index = i
            self.draw_data()
            time.sleep(1 / self.speed_slider.get())
            
    
        
    def quick_sort(self):
        """
            Sorts the data using the quick sort algorithm.
        """
        stack = [(0, len(self.data) - 1)]
        while stack:
            low, high = stack.pop()
            if low < high:
                pivot = self.data[high]
                i = low - 1
                for j in range(low, high):
                    if self.data[j] < pivot:
                        i += 1
                        self.data[i], self.data[j] = self.data[j], self.data[i]
                        self.sorted_index = i
                        self.draw_data()
                        time.sleep(1 / self.speed_slider.get())
                self.data[i + 1], self.data[high] = self.data[high], self.data[i + 1]
                self.sorted_index = i + 1
                self.draw_data()
                time.sleep(1 / self.speed_slider.get())
                stack.append((low, i))
                stack.append((i + 2, high))
        self.sorted_index = len(self.data)
        self.draw_data()
        
# Make the root window for the program.   
root = ctk.CTk()
app = SortingVisualizer(root)
root.mainloop()

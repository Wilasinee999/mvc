import tkinter as tk
from view import JobFairView
from controller import JobFairController

if __name__ == "__main__":
    root = tk.Tk()
    view = JobFairView(root)
    controller = JobFairController(view)
    view.set_controller(controller)
    root.mainloop()
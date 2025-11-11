import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime
class ModernTodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskMaster - Modern To-Do List")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        self.root.resizable(True, True)
        try:
            self.root.iconbitmap("todo_icon.ico")
        except:
            pass
        self.filename = "todo_data.json"
        self.tasks = self.load_tasks()
        self.colors = {
            'primary': '#3498db',
            'secondary': '#2c3e50',
            'accent': '#e74c3c',
            'success': '#2ecc71',
            'warning': '#f39c12',
            'light': '#ecf0f1',
            'dark': '#34495e'
        }
        self.setup_styles()
        self.setup_ui()
        self.refresh_list()
    def setup_styles(self):
        """Configure custom styles for widgets"""
        style = ttk.Style()
        style.configure('Primary.TButton', 
                       background=self.colors['primary'],
                       foreground='white',
                       padding=(20, 10),
                       font=('Arial', 10, 'bold'))
        style.configure('Success.TButton',
                       background=self.colors['success'],
                       foreground='white',
                       padding=(15, 8),
                       font=('Arial', 9))
        style.configure('Warning.TButton',
                       background=self.colors['warning'],
                       foreground='white',
                       padding=(15, 8),
                       font=('Arial', 9))
        style.configure('Danger.TButton',
                       background=self.colors['accent'],
                       foreground='white',
                       padding=(15, 8),
                       font=('Arial', 9))
        style.configure('Header.TLabel',
                       background=self.colors['secondary'],
                       foreground='white',
                       font=('Arial', 18, 'bold'),
                       padding=10)
        style.configure('Stats.TLabel',
                       background=self.colors['dark'],
                       foreground='white',
                       font=('Arial', 10),
                       padding=5)
    def setup_ui(self):
        main_container = tk.Frame(self.root, bg=self.colors['secondary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        header_frame = tk.Frame(main_container, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))
        header_frame.pack_propagate(False)
        header_label = tk.Label(header_frame, 
                               text="🎯 TaskMaster", 
                               bg=self.colors['primary'],
                               fg='white',
                               font=('Arial', 24, 'bold'))
        header_label.pack(side=tk.LEFT, padx=20, pady=20)
        stats_frame = tk.Frame(header_frame, bg=self.colors['primary'])
        stats_frame.pack(side=tk.RIGHT, padx=20, pady=20) 
        self.stats_label = tk.Label(stats_frame,
                                   text="Tasks: 0 | Completed: 0 | Pending: 0",
                                   bg=self.colors['primary'],
                                   fg='white',
                                   font=('Arial', 10, 'bold'))
        self.stats_label.pack()
        content_frame = tk.Frame(main_container, bg=self.colors['light'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        left_panel = tk.Frame(content_frame, bg=self.colors['light'], width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        right_panel = tk.Frame(content_frame, bg='white')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        add_frame = tk.LabelFrame(left_panel, 
                                 text="➕ Add New Task", 
                                 bg=self.colors['light'],
                                 fg=self.colors['dark'],
                                 font=('Arial', 12, 'bold'),
                                 padx=15,
                                 pady=15)
        add_frame.pack(fill=tk.X, padx=10, pady=10)
        tk.Label(add_frame, 
                text="Task Description:", 
                bg=self.colors['light'],
                font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        self.task_entry = tk.Entry(add_frame, 
                                  font=('Arial', 11),
                                  bg='white',
                                  relief=tk.FLAT,
                                  width=25)
        self.task_entry.pack(fill=tk.X, pady=(0, 10))
        self.task_entry.bind('<Return>', lambda e: self.add_task())
        self.task_entry.focus()
        add_btn = tk.Button(add_frame,
                           text="Add Task",
                           command=self.add_task,
                           bg=self.colors['primary'],
                           fg='white',
                           font=('Arial', 10, 'bold'),
                           relief=tk.FLAT,
                           padx=20,
                           pady=8)
        add_btn.pack(pady=5)
        actions_frame = tk.LabelFrame(left_panel,
                                     text="⚡ Quick Actions",
                                     bg=self.colors['light'],
                                     fg=self.colors['dark'],
                                     font=('Arial', 12, 'bold'),
                                     padx=15,
                                     pady=15)
        actions_frame.pack(fill=tk.X, padx=10, pady=10)
        self.complete_btn = tk.Button(actions_frame,
                                     text="✅ Mark Complete",
                                     command=self.mark_complete,
                                     bg=self.colors['success'],
                                     fg='white',
                                     font=('Arial', 9),
                                     relief=tk.FLAT,
                                     width=20,
                                     pady=6)
        self.complete_btn.pack(fill=tk.X, pady=3)
        self.edit_btn = tk.Button(actions_frame,
                                 text="✏️ Edit Task",
                                 command=self.edit_task,
                                 bg=self.colors['warning'],
                                 fg='white',
                                 font=('Arial', 9),
                                 relief=tk.FLAT,
                                 width=20,
                                 pady=6)
        self.edit_btn.pack(fill=tk.X, pady=3)
        self.delete_btn = tk.Button(actions_frame,
                                   text="🗑️ Delete Task",
                                   command=self.delete_task,
                                   bg=self.colors['accent'],
                                   fg='white',
                                   font=('Arial', 9),
                                   relief=tk.FLAT,
                                   width=20,
                                   pady=6)
        self.delete_btn.pack(fill=tk.X, pady=3)
    
        bulk_frame = tk.Frame(actions_frame, bg=self.colors['light'])
        bulk_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.clear_completed_btn = tk.Button(bulk_frame,
                                           text="Clear Completed",
                                           command=self.clear_completed,
                                           bg=self.colors['dark'],
                                           fg='white',
                                           font=('Arial', 9),
                                           relief=tk.FLAT,
                                           pady=4)
        self.clear_completed_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.clear_all_btn = tk.Button(bulk_frame,
                                      text="Clear All",
                                      command=self.clear_all,
                                      bg='#c0392b',
                                      fg='white',
                                      font=('Arial', 9),
                                      relief=tk.FLAT,
                                      pady=4)
        self.clear_all_btn.pack(side=tk.RIGHT, fill=tk.X, expand=True, padx=(5, 0))
        
        list_header = tk.Frame(right_panel, bg=self.colors['dark'], height=40)
        list_header.pack(fill=tk.X)
        list_header.pack_propagate(False)
        
        tk.Label(list_header,
                text="📋 Your Tasks",
                bg=self.colors['dark'],
                fg='white',
                font=('Arial', 14, 'bold')).pack(side=tk.LEFT, padx=15, pady=10)
        tree_frame = tk.Frame(right_panel, bg='white')
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree = ttk.Treeview(tree_frame,
                                columns=('status', 'task', 'created', 'priority'),
                                show='headings',
                                height=15,
                                yscrollcommand=scrollbar.set)
        
        scrollbar.config(command=self.tree.yview)
        self.tree.heading('status', text='📊 Status')
        self.tree.heading('task', text='📝 Task Description')
        self.tree.heading('created', text='📅 Created')
        self.tree.heading('priority', text='🎯 Priority')
        self.tree.column('status', width=100, anchor='center')
        self.tree.column('task', width=300, anchor='w')
        self.tree.column('created', width=120, anchor='center')
        self.tree.column('priority', width=80, anchor='center')
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<Double-1>', self.on_double_click)
        self.tree.bind('<<TreeviewSelect>>', self.on_selection_change)
        footer_frame = tk.Frame(main_container, bg=self.colors['dark'], height=30)
        footer_frame.pack(fill=tk.X, padx=10, pady=(5, 10))
        footer_frame.pack_propagate(False)
        
        tk.Label(footer_frame,
                text="💡 Tip: Double-click a task to toggle its status | Created with ❤️",
                bg=self.colors['dark'],
                fg='white',
                font=('Arial', 8)).pack(pady=5)
    
    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as file:
                    return json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []
    
    def save_tasks(self):
        """Save tasks to JSON file"""
        with open(self.filename, 'w') as file:
            json.dump(self.tasks, file, indent=2)
    
    def add_task(self):
        """Add a new task"""
        task_description = self.task_entry.get().strip()
        if task_description:
            task = {
                'description': task_description,
                'completed': False,
                'created': datetime.now().strftime("%Y-%m-%d %H:%M"),
                'id': len(self.tasks) + 1,
                'priority': 'Medium'
            }
            self.tasks.append(task)
            self.save_tasks()
            self.task_entry.delete(0, tk.END)
            self.refresh_list()
            messagebox.showinfo("Success", "✅ Task added successfully!")
        else:
            messagebox.showwarning("Warning", "⚠️ Please enter a task description!")
    
    def refresh_list(self):
        """Refresh the task list display"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        for task in self.tasks:
            status = "✅ Completed" if task['completed'] else "⏳ Pending"
            priority = task.get('priority', 'Medium')
            item_id = self.tree.insert('', tk.END, values=(
                status,
                task['description'],
                task['created'],
                priority
            ))
            
            if task['completed']:
                self.tree.set(item_id, 'status', '✅ Completed')
        total_tasks = len(self.tasks)
        completed_tasks = sum(1 for task in self.tasks if task['completed'])
        pending_tasks = total_tasks - completed_tasks
        
        self.stats_label.config(
            text=f"Tasks: {total_tasks} | ✅ Completed: {completed_tasks} | ⏳ Pending: {pending_tasks}"
        )
    
    def get_selected_task(self):
        """Get the currently selected task"""
        selection = self.tree.selection()
        if selection:
            index = self.tree.index(selection[0])
            return index, self.tasks[index]
        return None, None
    
    def on_selection_change(self, event):
        """Update button states based on selection"""
        index, task = self.get_selected_task()
        if task:
            self.complete_btn.config(state=tk.NORMAL)
            self.edit_btn.config(state=tk.NORMAL)
            self.delete_btn.config(state=tk.NORMAL)
        else:
            self.complete_btn.config(state=tk.DISABLED)
            self.edit_btn.config(state=tk.DISABLED)
            self.delete_btn.config(state=tk.DISABLED)
    
    def mark_complete(self):
        """Mark selected task as complete"""
        index, task = self.get_selected_task()
        if task:
            if not task['completed']:
                task['completed'] = True
                self.save_tasks()
                self.refresh_list()
                messagebox.showinfo("Success", "🎉 Task marked as completed!")
            else:
                messagebox.showinfo("Info", "ℹ️ Task is already completed!")
        else:
            messagebox.showwarning("Warning", "⚠️ Please select a task!")
    
    def edit_task(self):
        """Edit selected task"""
        index, task = self.get_selected_task()
        if task:
            new_description = simpledialog.askstring(
                "Edit Task", 
                "Edit task description:", 
                initialvalue=task['description']
            )
            if new_description and new_description.strip():
                task['description'] = new_description.strip()
                self.save_tasks()
                self.refresh_list()
                messagebox.showinfo("Success", "✏️ Task updated successfully!")
        else:
            messagebox.showwarning("Warning", "⚠️ Please select a task to edit!")
    
    def delete_task(self):
        """Delete selected task"""
        index, task = self.get_selected_task()
        if task:
            result = messagebox.askyesno(
                "Confirm Delete", 
                f"🗑️ Are you sure you want to delete:\n\n\"{task['description']}\"?"
            )
            if result:
                del self.tasks[index]
                self.save_tasks()
                self.refresh_list()
                messagebox.showinfo("Success", "✅ Task deleted successfully!")
        else:
            messagebox.showwarning("Warning", "⚠️ Please select a task to delete!")
    
    def clear_completed(self):
        """Remove all completed tasks"""
        completed_tasks = [task for task in self.tasks if task['completed']]
        if not completed_tasks:
            messagebox.showinfo("Info", "ℹ️ No completed tasks to clear!")
            return
        
        result = messagebox.askyesno(
            "Confirm Clear", 
            f"🧹 Are you sure you want to remove {len(completed_tasks)} completed task(s)?"
        )
        
        if result:
            self.tasks = [task for task in self.tasks if not task['completed']]
            self.save_tasks()
            self.refresh_list()
            messagebox.showinfo("Success", f"✅ Removed {len(completed_tasks)} completed tasks!")
    
    def clear_all(self):
        """Remove all tasks"""
        if not self.tasks:
            messagebox.showinfo("Info", "ℹ️ No tasks to clear!")
            return
        
        result = messagebox.askyesno(
            "Confirm Clear All", 
            f"⚠️ DANGER: Are you sure you want to remove ALL {len(self.tasks)} tasks?\nThis action cannot be undone!"
        )
        
        if result:
            self.tasks = []
            self.save_tasks()
            self.refresh_list()
            messagebox.showinfo("Success", "✅ All tasks have been cleared!")
    
    def on_double_click(self, event):
        """Handle double-click on task (toggle complete status)"""
        index, task = self.get_selected_task()
        if task:
            task['completed'] = not task['completed']
            self.save_tasks()
            self.refresh_list()

def main():
    root = tk.Tk()
    root.update_idletasks()
    x = (root.winfo_screenwidth() // 2) - (800 // 2)
    y = (root.winfo_screenheight() // 2) - (600 // 2)
    root.geometry(f'800x600+{x}+{y}')
    app = ModernTodoApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
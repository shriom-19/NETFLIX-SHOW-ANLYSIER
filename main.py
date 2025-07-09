
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from subpart import all_genres, country_list, year, shows
from algo import country_fil, year_fil, genre_fil, top10_by_type, fdata
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class ToolTip:
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def show_tip(self, text):
        if self.tipwindow or not text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=text, justify=LEFT,
                      background="#2a2a2a", foreground="white",
                      relief=SOLID, borderwidth=1,
                      font=("Arial", "10", "normal"),
                      wraplength=400)
        label.pack(ipadx=1)

    def hide_tip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

# Ensure display is set for VNC
if 'DISPLAY' not in os.environ:
    os.environ['DISPLAY'] = ':0'

# Configure matplotlib to use a GUI backend
matplotlib.use('TkAgg')

# Create main window
root = Tk()
root.title('Netflix Shows Explorer')
root.configure(bg='#1a1a1a')

# Fullscreen
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry(f"{width}x{height}")

# Configure styles
style = ttk.Style()
style.theme_use('clam')

# Configure custom styles
style.configure('Title.TLabel', 
                background='#1a1a1a', 
                foreground='#e50914',
                font=('Arial', 24, 'bold'))

style.configure('Header.TLabel', 
                background='#1a1a1a', 
                foreground='#ffffff',
                font=('Arial', 14, 'bold'))

style.configure('Custom.TCombobox',
                fieldbackground='#333333',
                background='#333333',
                foreground='#ffffff',
                borderwidth=1,
                relief='solid')

style.configure('Custom.TFrame',
                background='#1a1a1a',
                relief='flat')

style.configure('Card.TFrame',
                background='#2a2a2a',
                relief='raised',
                borderwidth=2)

# Main container with padding
main_container = Frame(root, bg='#1a1a1a')
main_container.pack(fill=BOTH, expand=True, padx=20, pady=20)

# Title section
title_frame = Frame(main_container, bg='#1a1a1a')
title_frame.pack(fill=X, pady=(0, 30))

title_label = Label(title_frame,
                   text='🎬 NETFLIX SHOWS EXPLORER',
                   font=('Arial', 28, 'bold'),
                   fg='#e50914',
                   bg='#1a1a1a')
title_label.pack()

subtitle_label = Label(title_frame,
                      text='Discover and explore Netflix shows with interactive charts',
                      font=('Arial', 12),
                      fg='#cccccc',
                      bg='#1a1a1a')
subtitle_label.pack(pady=(5, 0))

# Controls section
controls_frame = Frame(main_container, bg='#2a2a2a', relief='raised', bd=2)
controls_frame.pack(fill=X, pady=(0, 20), padx=10, ipady=15, ipadx=15)

controls_title = Label(controls_frame,
                      text='📊 Filter Options',
                      font=('Arial', 16, 'bold'),
                      fg='#ffffff',
                      bg='#2a2a2a')
controls_title.pack(pady=(0, 15))

# Create a grid for controls
controls_grid = Frame(controls_frame, bg='#2a2a2a')
controls_grid.pack()

# Type selection
type_frame = Frame(controls_grid, bg='#2a2a2a')
type_frame.grid(row=0, column=0, padx=20, pady=10, sticky='w')

type_label = Label(type_frame,
                  text='Content Type:',
                  font=('Arial', 12, 'bold'),
                  fg='#ffffff',
                  bg='#2a2a2a')
type_label.pack(anchor='w')

typelist = ttk.Combobox(type_frame, 
                       values=shows, 
                       state="readonly",
                       font=('Arial', 10),
                       width=15)
typelist.pack(pady=(5, 0))
typelist.current(0)

# Country selection
country_frame = Frame(controls_grid, bg='#2a2a2a')
country_frame.grid(row=0, column=1, padx=20, pady=10, sticky='w')

country_label = Label(country_frame,
                     text='Country:',
                     font=('Arial', 12, 'bold'),
                     fg='#ffffff',
                     bg='#2a2a2a')
country_label.pack(anchor='w')

countrylist = ttk.Combobox(country_frame, 
                          values=country_list, 
                          state="readonly",
                          font=('Arial', 10),
                          width=20)
countrylist.pack(pady=(5, 0))
countrylist.current(0)

# Genre selection
genre_frame = Frame(controls_grid, bg='#2a2a2a')
genre_frame.grid(row=0, column=2, padx=20, pady=10, sticky='w')

genre_label = Label(genre_frame,
                   text='Genre:',
                   font=('Arial', 12, 'bold'),
                   fg='#ffffff',
                   bg='#2a2a2a')
genre_label.pack(anchor='w')

genrelist = ttk.Combobox(genre_frame, 
                        values=all_genres, 
                        state="readonly",
                        font=('Arial', 10),
                        width=20)
genrelist.pack(pady=(5, 0))
genrelist.current(0)

# Charts section with tabs
notebook = ttk.Notebook(main_container)
notebook.pack(fill=BOTH, expand=True, pady=(0, 10))

# Tab 1: Top 10 Chart
tab1 = Frame(notebook, bg='#1a1a1a')
notebook.add(tab1, text='📈 Top 10 Rankings')

# Chart title for tab 1
chart1_title = Label(tab1,
                    text="Top 10 Shows",
                    font=('Arial', 18, 'bold'),
                    fg='#e50914',
                    bg='#1a1a1a')
chart1_title.pack(pady=15)

# Graph frame for tab 1
graph_frame = Frame(tab1, bg='#1a1a1a')
graph_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

# Tab 2: Detailed List
tab2 = Frame(notebook, bg='#1a1a1a')
notebook.add(tab2, text='📋 Detailed View')

# Chart title for tab 2
chart2_title = Label(tab2,
                    text="Detailed Show Information",
                    font=('Arial', 18, 'bold'),
                    fg='#e50914',
                    bg='#1a1a1a')
chart2_title.pack(pady=15)

# Table frame for tab 2
table_frame = Frame(tab2, bg='#1a1a1a')
table_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

def show_graph():
    for widget in graph_frame.winfo_children():
        widget.destroy()

    # Filter data
    filtered = country_fil(fdata.copy(), countrylist.get())
    top10 = filtered[filtered['type'] == typelist.get()].sort_values(
        by='imdb_rating', ascending=False).head(10)

    if top10.empty:
        no_data_label = Label(graph_frame,
                             text="No data available for selected filters",
                             font=('Arial', 14),
                             fg='#cccccc',
                             bg='#1a1a1a')
        no_data_label.pack(expand=True)
        return

    # Plot setup with Netflix-style colors
    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor('#1a1a1a')
    ax.set_facecolor('#1a1a1a')

    # Create horizontal bar chart
    bars = ax.barh(range(len(top10)), top10['imdb_rating'], 
                   color='#e50914', alpha=0.8, height=0.7)

    # Customize the chart
    ax.set_yticks(range(len(top10)))
    ax.set_yticklabels(top10['title'], fontsize=10, color='white')
    ax.set_xlabel('IMDb Rating', fontsize=12, color='white')
    ax.set_title(f'Top 10 {typelist.get()}s in {countrylist.get()}', 
                fontsize=16, color='white', pad=20)

    # Add rating labels on bars
    for i, (bar, rating) in enumerate(zip(bars, top10['imdb_rating'])):
        ax.text(rating - 0.3, i, f'{rating:.1f}', 
               va='center', ha='right', color='white', fontweight='bold')

    # Style the axes
    ax.tick_params(colors='white')
    ax.tick_params(axis='x', which='both', bottom=False, labelbottom=False)
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()

    # Embed in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=BOTH, expand=True)

def show_table():
    for widget in table_frame.winfo_children():
        widget.destroy()

    # Filter data
    filtered = country_fil(fdata.copy(), countrylist.get())
    if genrelist.get() != all_genres[0]:  # If not "All Genres"
        filtered = genre_fil(filtered, genrelist.get())
    
    top30 = filtered[filtered['type'] == typelist.get()].sort_values(
        by='imdb_rating', ascending=False).head(30)

    if top30.empty:
        no_data_label = Label(table_frame,
                             text="No data available for selected filters",
                             font=('Arial', 14),
                             fg='#cccccc',
                             bg='#1a1a1a')
        no_data_label.pack(expand=True)
        return

    # Create table with scrollbars
    table_container = Frame(table_frame, bg='#1a1a1a')
    table_container.pack(fill=BOTH, expand=True)

    # Scrollbars
    v_scrollbar = Scrollbar(table_container, orient="vertical")
    v_scrollbar.pack(side='right', fill='y')

    h_scrollbar = Scrollbar(table_container, orient="horizontal")
    h_scrollbar.pack(side='bottom', fill='x')

    # Configure treeview style
    style.configure("Custom.Treeview",
                   background="#2a2a2a",
                   foreground="white",
                   rowheight=30,
                   fieldbackground="#2a2a2a",
                   font=('Arial', 10))
    style.configure("Custom.Treeview.Heading",
                   background="#e50914",
                   foreground="white",
                   font=('Arial', 11, 'bold'))

    # Create treeview
    columns = ['Title', 'Rating', 'Duration', 'Release Year']
    tree = ttk.Treeview(table_container,
                       columns=columns,
                       show='headings',
                       style="Custom.Treeview",
                       yscrollcommand=v_scrollbar.set,
                       xscrollcommand=h_scrollbar.set)

    # Configure columns
    tree.heading('Title', text='Title')
    tree.heading('Rating', text='IMDb Rating')
    tree.heading('Duration', text='Duration')
    tree.heading('Release Year', text='Year')

    tree.column('Title', width=300, anchor='w')
    tree.column('Rating', width=100, anchor='center')
    tree.column('Duration', width=100, anchor='center')
    tree.column('Release Year', width=100, anchor='center')

    # Store descriptions for tooltip
    descriptions = {}
    
    # Insert data
    for _, row in top30.iterrows():
        item_id = tree.insert('', 'end', values=[
            row['title'],
            f"{row['imdb_rating']:.1f}",
            row['duration'],
            row['release_year']
        ])
        # Store description for this item
        descriptions[item_id] = row['description'] if pd.notna(row['description']) else "No description available"

    # Create tooltip
    tooltip = ToolTip(tree)
    
    def on_motion(event):
        item = tree.identify_row(event.y)
        if item and item in descriptions:
            tooltip.show_tip(f"{descriptions[item][:300]}{'...' if len(descriptions[item]) > 300 else ''}")
        else:
            tooltip.hide_tip()
    
    def on_leave(event):
        tooltip.hide_tip()
    
    # Bind events for tooltip
    tree.bind('<Motion>', on_motion)
    tree.bind('<Leave>', on_leave)

    tree.pack(side='left', fill='both', expand=True)
    v_scrollbar.config(command=tree.yview)
    h_scrollbar.config(command=tree.xview)

def update_displays():
    show_graph()
    show_table()
    
    # Update chart titles
    selected_country = countrylist.get()
    selected_type = typelist.get()
    selected_genre = genrelist.get()
    
    title1 = f"Top 10 {selected_type}s"
    if selected_country != country_list[0]:
        title1 += f" in {selected_country}"
    chart1_title.config(text=title1)
    
    title2 = f"Detailed {selected_type} Information"
    if selected_genre != all_genres[0]:
        title2 += f" - {selected_genre}"
    chart2_title.config(text=title2)

# Bind events
typelist.bind("<<ComboboxSelected>>", lambda e: update_displays())
countrylist.bind("<<ComboboxSelected>>", lambda e: update_displays())
genrelist.bind("<<ComboboxSelected>>", lambda e: update_displays())

# Status bar
status_frame = Frame(main_container, bg='#333333', height=30)
status_frame.pack(fill=X, side=BOTTOM)

status_label = Label(status_frame,
                    text="Ready | Use the filters above to explore Netflix content",
                    font=('Arial', 10),
                    fg='#cccccc',
                    bg='#333333')
status_label.pack(side=LEFT, padx=10, pady=5)

# Initialize displays
update_displays()

# Start the GUI
root.mainloop()

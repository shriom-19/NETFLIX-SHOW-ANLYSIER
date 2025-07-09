import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas._config import display
from pandas.core.methods import describe
import seaborn as sns
from subpart import all_genres, country_list, year, shows
from algo import country_fil, year_fil, genre_fil, top10_by_type, fdata
from tkinter import *
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

root = Tk()
root.title('NETFLIX SHOWS')

# Fullscreen
width = root.winfo_screenwidth()
height = root.winfo_screenheight()
root.geometry(f"{width}x{height}")

# -------------------------------
# Scrollable Canvas + Frame Setup
canvas = Canvas(root, bg='#141414')
container = Frame(root, bg="#141414")
container.pack(expand=True, fill=BOTH)

canvas = Canvas(container, bg='#141414')
canvas.pack(side=LEFT, fill=BOTH, expand=True)

v_scrollbar = Scrollbar(container, orient='vertical', command=canvas.yview)
v_scrollbar.pack(side=RIGHT, fill=Y)

canvas.configure(yscrollcommand=v_scrollbar.set)

# --- Main Frame inside canvas ---
main_frame = Frame(canvas,
                   bg="#141414",
                   borderwidth=0,
                   relief='flat',
                   highlightbackground='#000000',
                   highlightthickness=0)
canvas_window = canvas.create_window((width // 2, 0), window=main_frame, anchor='n')

# Center main_frame horizontally on resize
def center_main_frame(event):
    canvas.coords(canvas_window, event.width // 2, 0)

canvas.bind("<Configure>", center_main_frame)


sub_frame = Frame(main_frame, bg='#141414')
sub_frame.grid(row=1, column=0, sticky='NSEW', columnspan= 5)


# --- Scrollregion Update ---
def update_scrollregion(event):
    canvas.configure(scrollregion=canvas.bbox("all"))


main_frame.bind("<Configure>", update_scrollregion)




# -------------------------------
# GUI Content
label1 = Label(main_frame,
               text='NETFLIX SHOWS',
               font=("Helvetica", 28, "italic bold"),
               fg='#e30913',
               bg='#141414')
label1.grid(sticky='NSEW', row=0, columnspan=5, pady=10)

# type Dropdown
sublabel1 = Label(sub_frame,
                  text='Type:',
                  font='Arial 12 bold',
                  fg='grey',
                  bg='#141414')
sublabel1.grid(row=1, column=0, sticky='NSWE', padx=(10, 0))

typelist = ttk.Combobox(sub_frame, values=shows, state="readonly")
typelist.grid(row=1, column=2, sticky='NSWE', padx=10, pady=10)
typelist.current(0)

#country dropdown
sublabel2 = Label(sub_frame,
                  text='country:',
                  font='Arial 12 bold',
                  fg='grey',
                  bg='#141414')
sublabel2.grid(row=1, column=3, sticky='nswE', padx=(10, 0))

countrylist = ttk.Combobox(sub_frame, values=country_list, state="readonly")
countrylist.grid(row=1, column=4, sticky='nswE', padx=10, pady=10)

countrylist.current(0)

# Bind combobox selection to update function

label2 = Label(sub_frame,
               text=f"TOP 10 {typelist.get()} ",
               font=("Helvetica", 15, "italic bold"),
               fg='#ae0610',
               bg='#141414')

filtered_data = country_fil(fdata, '0')
# top10_by_type(fdata, typelist.get())

graph_frame = Frame(sub_frame, bg='#141414')
graph_frame.grid(sticky='n', row=2, column=0, columnspan=5, pady=(0, 10))


def show_graph():
    for widget in graph_frame.winfo_children():
        widget.destroy()

    # Filter data
    filtered = country_fil(fdata.copy(), countrylist.get())
    top10 = filtered[filtered['type'] == typelist.get()].sort_values(
        by='imdb_rating', ascending=False).head(10)

    # Plot setup
    fig, ax = plt.subplots(figsize=(6, 4))
    fig.patch.set_facecolor('#141414')  # Full figure background
    ax.set_facecolor('#141414')  # Plot area background
    sns.set_style("dark")  # Optional dark mode style

    # Barplot
    bars = sns.barplot(
        x='imdb_rating',
        y='title',
        data=top10,
        ax=ax,
        color='#e90000',
        linewidth=0,  # no border width
        edgecolor='none')

    # Add white rating text on bars
    for bar in bars.patches:
        rating = bar.get_width()
        y = bar.get_y() + bar.get_height() / 2
        ax.text(rating - 0.5,
                y,
                f'{rating:.1f}',
                color='white',
                va='center',
                ha='right',
                fontsize=9)

    # Title styling
    ax.set_title(f"Top 10 {typelist.get()}s in {countrylist.get()}",
                 color='white',
                 fontsize=14)

    # Remove x-axis and y-axis labels & ticks
    ax.set_xlabel("")
    ax.set_xticks([])
    ax.tick_params(axis='x', bottom=False, colors='white')
    ax.tick_params(axis='y', colors='white')

    # Remove outer spines (borders)
    for spine in ax.spines.values():
        spine.set_visible(False)

    fig.tight_layout()

    # Embed in Tkinter
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()


def update_graph_label(event=None):
    selected_type = typelist.get()
    selected_country = countrylist.get()

    # Update top title label
    label2.config(
        text=
        f"TOP 10 {selected_type.upper()} SHOWS IN {selected_country.upper()}")

    # Show updated graph
    show_graph()


typelist.bind("<<ComboboxSelected>>", update_graph_label)
countrylist.bind("<<ComboboxSelected>>", update_graph_label)

update_graph_label()
label2.grid(sticky='EW', row=0, column=0, columnspan=5, pady=10)
#genreframe
genre_frame = Frame(main_frame, bg='#595959')
genre_frame.grid(row=2,
                 column=0,
                 sticky='EW',
                 columnspan=5,
                 ipady=10,
                 ipadx=20)

glabel1 = Label(genre_frame,
                text=f"Best {typelist.get()} of your genre ",
                font=("Helvetica", 15, "italic bold"),
                fg='#ffffff',
                bg='#595959',
                bd=3,
                highlightbackground='#000000')
update_graph_label()
glabel1.grid(sticky='nsEW', row=0, column=0, columnspan=5, pady=20)

# gene drop down

# Add more widgets (e.g., genre, year, plots) below

#display graph
glabel2 = Label(genre_frame,
                text='Genre:',
                font='Arial 14 italic',
                fg='white',
                bg='#595959')
glabel2.grid(row=1, column=0, sticky='snwE', padx=(10, 0))

genrelist = ttk.Combobox(genre_frame, values=all_genres, state="readonly")
genrelist.grid(row=1, column=1, sticky='wsnE', padx=10, pady=10)
genrelist.current(0)

genrelist.bind("<<ComboboxSelected>>", update_graph_label)

table_frame = Frame(genre_frame, bg='#595959')
table_frame.grid(row=3, column=1, columnspan=5, sticky='nEW')

def show_table():
    for widget in table_frame.winfo_children():
        widget.destroy()

    # Filter data
    filtered = country_fil(fdata.copy(), countrylist.get())
    filtered = genre_fil(filtered, genrelist.get())
    top10 = filtered[filtered['type'] == typelist.get()].sort_values(
        by='imdb_rating', ascending=False).head(30)

    # Only keep desired columns
    selected_cols = ['title', 'imdb_rating', 'duration', 'description']
    top10 = top10[selected_cols].copy()

    if top10.empty:
        Label(table_frame,
              text="No data available for selected filters.",
              fg='white',
              bg='#595959',
              font=("Arial", 12, "italic")).pack()
        return  # Properly indented

    # Scrollbars
    vsb = Scrollbar(table_frame, orient="vertical")
    vsb.pack(side='right', fill='y')

    hsb = Scrollbar(table_frame, orient="horizontal")
    hsb.pack(side='bottom', fill='x')

    # Create Treeview
    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background="#1e1e1e",
                    foreground="white",
                    rowheight=40,
                    fieldbackground="#1e1e1e",
                    font=('Helvetica', 10))
    style.configure("Treeview.Heading",
                    background="#e30913",
                    foreground="white",
                    font=('Helvetica', 11, 'bold'))

    tree = ttk.Treeview(table_frame,
                        columns=selected_cols,
                        show='headings',
                        yscrollcommand=vsb.set,
                        xscrollcommand=hsb.set)

    for col in selected_cols:
        width = 250 if col == 'title' else 300 if col == 'description' else 120
        tree.heading(col, text=col.capitalize())
        tree.column(col, width=width, anchor='w')

    for _, row in top10.iterrows():
        tree.insert('', 'end', values=list(row))

    tree.pack(side='left', fill='both', expand=True)
    vsb.config(command=tree.yview)
    hsb.config(command=tree.xview)

    # ----------- Tooltip Logic for Description Hover -----------
    tooltip = Label(table_frame,
                    text="",
                    bg="grey",
                    fg="white",
                    wraplength=400,
                    font=('Helvetica', 10),
                    relief='solid',
                    borderwidth=1)
    tooltip.place_forget()

    def on_motion(event):
        region = tree.identify_region(event.x, event.y)
        col = tree.identify_column(event.x)
        row_id = tree.identify_row(event.y)

        if region == "cell" and col == "#4":  # Description is the 4th column
            item = tree.item(row_id)
            if item and item["values"]:
                desc = item["values"][3]  # Description
                tooltip.config(text=desc)
                tooltip.place(x=event.x_root - tree.winfo_rootx() - 300,
                              y=event.y_root - tree.winfo_rooty() + 20)
        else:
            tooltip.place_forget()

    def on_leave(event):
        tooltip.place_forget()

    tree.bind("<Motion>", on_motion)
    tree.bind("<Leave>", on_leave)



def update_table_label(event=None):
    selected_type = typelist.get()
    selected_genre = genrelist.get()

    # Update genre header label
    glabel1.config(
        text=f"Best {selected_type} of your genre: {selected_genre}"
        if selected_genre != '0' else f"Best {selected_type} of your genre")

    # Show updated table
    show_table()


# display table from row 3 to 13,23,33
genrelist.bind("<<ComboboxSelected>>", update_table_label)

update_graph_label()
update_table_label()

root.mainloop()

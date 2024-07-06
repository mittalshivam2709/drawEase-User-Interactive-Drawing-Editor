import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
import xml.etree.ElementTree as ET
from PIL import Image, ImageTk
from tkinter import messagebox
from tkinter import colorchooser

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 800
list_of_objects = []
list_of_groups = []
list_of_selected = []
first=0
second=0
third=0
fourth=0



color_option='red'
corner_option='green'


# selected_color='red'
# selected_corner='square'



def show_color_dialog():
    global color_option,corner_option
    color_dialog = tk.Toplevel(dialog)
    color_dialog.title("Edit Color")
    
    def close_color_dialog(color):
        # print(color)
        global color_option
        # selected_color.set(color)
        # print(selected_color)
        color_option=color
        editor.change_line_color(color_option)
        color_dialog.destroy()
    
    colors = ["Black", "Red", "Green", "Blue"]
    for color in colors:
        tk.Button(color_dialog, text=color, command=lambda c=color: close_color_dialog(c)).pack(pady=5)


def show_corner_dialog():
    corner_dialog = tk.Toplevel(dialog)
    corner_dialog.title("Edit Corner Style")
    
    def close_corner_dialog(corner_style):
        global corner_option
        selected_corner.set(corner_style)
        corner_option=corner_style
        editor.change_corner(corner_style)        
        corner_dialog.destroy()
    
    corner_styles = ["Rounded", "Square"]
    for style in corner_styles:
        tk.Button(corner_dialog, text=style, command=lambda s=style: close_corner_dialog(s)).pack(pady=5)


def show_edit_dialog_line(obj):
    global dialog
    dialog = tk.Toplevel(root)
    dialog.title("Edit Options")
    
    current_color_label = tk.Label(dialog, text="Line Color: " + obj.color)
    current_color_label.pack(pady=5)
    
    
    
    tk.Button(dialog, text="Edit Color", command=show_color_dialog).pack(pady=5)



def show_edit_dialog_rect(obj):
    global dialog
    dialog = tk.Toplevel(root)
    dialog.title("Edit Options")
    
    current_color_label = tk.Label(dialog, text="Line Color: " + obj.color)
    current_color_label.pack(pady=5)
    
    current_corner_label = tk.Label(dialog, text="Corner Style: " + obj.corner_style)
    current_corner_label.pack(pady=5)
    
    
    tk.Button(dialog, text="Edit Color", command=show_color_dialog).pack(pady=5)
    tk.Button(dialog, text="Edit Corner Style", command=show_corner_dialog).pack(pady=5)





def draw_rounded_rectangle(canvas, x1, y1, x2, y2, radius, color,**kwargs):
    points = [x1 + radius, y1,
              x1 + radius, y1,
              x2 - radius, y1,
              x2 - radius, y1,
              x2, y1,
              x2, y1 + radius,
              x2, y1 + radius,
              x2, y2 - radius,
              x2, y2 - radius,
              x2, y2,
              x2 - radius, y2,
              x2 - radius, y2,
              x1 + radius, y2,
              x1 + radius, y2,
              x1, y2,
              x1, y2 - radius,
              x1, y2 - radius,
              x1, y1 + radius,
              x1, y1 + radius,
              x1, y1]
    return canvas.create_polygon(points, outline=kwargs.get('outline', 'black'), width=kwargs.get('width', 1), smooth=True,fill=color)





def show_color_options():
    # Create a color chooser dialog
    color_choice = colorchooser.askcolor(title="Select Line Color")
    if color_choice:
        selected_color = color_choice[1]  # Get the selected color
        print("Selected color:", selected_color)
        # Perform further actions with the selected color





def destroy_button_by_text(root, button_text):
    for widget in root.winfo_children():
        if isinstance(widget, tk.Button) and widget.cget("text") == button_text:
            widget.destroy()
            break

        
class DrawingObject:
    def __init__(self):
        self.selected = False
    def is_clicked(self, x, y):
        pass
    def delete(self):
        pass
    def copy(self):
        pass
    def move(self, dx, dy):
        pass
    def show_on_select(self):
        pass
    def show_properly(self):
        pass
    def delete(self):
        pass
    def check_in_area(self,start_x,start_y, x, y,):
        pass
    def get_code(self):
        pass
    def show_edit_menu(self):
        pass
    
    
class Line(DrawingObject):
    def __init__(self, x1, y1, x2, y2, color,id):
        super().__init__()
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.dash_offset = 0

        self.id = id
    def draw(self, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill=self.color)
    def set_id(self, id):
        self.id = id
    def is_clicked(self, x, y):
        pass
    def move(self, dx, dy):
        editor.canvas.coords(self.id, self.x1 + dx, self.y1 + dy, self.x2 + dx, self.y2 + dy)
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy
        
    def edit(self):
        editor.edit_line()

    def set_color(self, color):
        print(color)
        self.color=color
        editor.canvas.itemconfig(self.id,fill=color)
    

    def show_on_select(self):
        editor.canvas.itemconfig(self.id, dash=(10, 10))
        self.move_dash()
        pass
    
    def show_properly(self):
        editor.canvas.itemconfig(self.id, dash=())
        # editor.canvas.itemconfig(self.id, dash=(5, 5))
        pass
    def ungroup(self):
        global list_of_objects
        list_of_objects.append(Line(self.x1, self.y1, self.x2, self.y2, self.color, id=self.id))
        pass
    def delete(self):
        # return super().delete()
        editor.canvas.delete(self.id)
        pass
    def move_dash(self):
        self.dash_offset += 2
        editor.canvas.itemconfig(self.id, dashoffset=self.dash_offset)
        if self.dash_offset >= 10:
            self.dash_offset = 0
        editor.canvas.after(50, self.move_dash)
    def check_in_area(self,start_x,start_y, x, y,):
        if self.x1 >= start_x and self.y1 >= start_y and self.x2 <= x and self.y2 <= y:
            return True
    def get_code(self):
        return 'line '+ str(self.x1)+' '+ str(self.y1)+' '+ str(self.x2)+' '+ str(self.y2)+' '+ self.color+'\n'

class Rectangle(DrawingObject):
    def __init__(self, x1, y1, x2, y2, color, corner_style,id):
        super().__init__()
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
        self.corner_style = corner_style
        self.id = id
        self.dash_offset = 0
    
    def draw(self, canvas):
        canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, outline=self.color)
    def set_id(self, id):
        self.id = id
    def is_clicked(self, x, y):
        # Check if (x, y) is inside the rectangle
        pass
    def move(self, dx, dy):
        editor.canvas.coords(self.id, self.x1 + dx, self.y1 + dy, self.x2 + dx, self.y2 + dy)
        self.x1 += dx
        self.y1 += dy
        self.x2 += dx
        self.y2 += dy
        
    def edit(self):
        print("yes,gussing")
        editor.edit_rect()
        # editor.edit_rect_corner()

    def set_color(self, color):
        self.color=color
        editor.canvas.itemconfig(self.id,outline=color)
    
    def set_corner(self,corner):
        self.corner_style = corner
        # Delete the existing rectangle
        editor.canvas.delete(self.id)
        # Create a new rectangle with updated corner style
        self.id = draw_rounded_rectangle(editor.canvas, 100, 100, 200, 200, 20, fill="blue", outline="")

    def show_on_select(self):
        editor.canvas.itemconfig(self.id, dash=(10, 10))
        self.move_dash()
        pass
    def show_properly(self):
        editor.canvas.itemconfig(self.id, dash=())
        pass
    def ungroup(self):
        global list_of_objects
        list_of_objects.append(Rectangle(self.x1, self.y1, self.x2, self.y2, self.color, self.corner_style, id=self.id))

        pass
    def delete(self):
        # return super().delete()
        editor.canvas.delete(self.id)
        pass
    def move_dash(self):
        self.dash_offset += 2
        editor.canvas.itemconfig(self.id, dashoffset=self.dash_offset)
        if self.dash_offset >= 10:
            self.dash_offset = 0
        editor.canvas.after(50, self.move_dash)
    def check_in_area(self,start_x,start_y, x, y,):
        if self.x1 >= start_x and self.y1 >= start_y and self.x2 <= x and self.y2 <= y:
            return True
    def get_code(self):
        return 'rectangle '+ str(self.x1)+' '+ str(self.y1)+' '+ str(self.x2)+' '+ str(self.y2)+' '+ self.color+' '+ self.corner_style+'\n'
class Group(DrawingObject):
    def __init__(self):
        super().__init__()
        self.objects = []
    
    def add_object(self, obj):
        self.objects.append(obj)
    def draw(self, canvas):
        for obj in self.objects:
            obj.draw(canvas)
    
    def is_clicked(self, x, y):
        # Check if (x, y) is inside any object in the group
        pass
    
    def delete(self):
        # Delete all objects in the group
        pass
    
    def copy(self):
        # Copy all objects in the group
        pass
    
    def move(self, dx, dy):
        # Move all objects in the group by (dx, dy)
        for obj in self.objects:
            obj.move(dx, dy)
        pass
    def show_on_select(self):
        for obj in self.objects:
            obj.show_on_select()
        pass
    def show_properly(self):
        for obj in self.objects:
            obj.show_properly()
        pass
    def ungroup(self):
        for obj in self.objects:
            if isinstance(obj,Group):
                list_of_groups.append(obj)
            else:
                obj.ungroup()
    def ungroupall(self):
        for obj in self.objects:
            if isinstance(obj,Group):
                for obj2 in obj.objects:
                    self.objects.append(obj2)                
                # obj.ungroupall()
                if obj in list_of_groups:
                    list_of_groups.__delitem__(list_of_groups.index(obj))
                # list_of_groups.append(obj)
            else:
                obj.ungroup()
            # obj.ungroupall()
        # Remove the group and add its objects to the canvas
        pass
    def delete(self):
        # return super().delete()
        for obj in self.objects:
            obj.delete()
        pass
    def check_in_area(self, start_x, start_y, x, y):
        for obj in self.objects:
            if obj.check_in_area(start_x, start_y, x, y):
                return True
    def get_code(self):
        ascii_code = 'begin\n'
        for obj in self.objects:
           ascii_code+= obj.get_code()
        ascii_code+= 'end\n'
        return ascii_code
current_rectangle = None
current_line = None
choice = 'draw'
start_x, start_y = 0, 0 

    
class DrawingEditor:
    global canvas
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="white")
        self.canvas.pack()
        self.objects = []
        self.selected_object = False
        self.code = ''
        self.asciicode = ''
        
        # Add toolbar buttons and menu items for drawing operations
        self.create_menu()
        self.create_toolbar()
        # Bind mouse events
        # self.canvas.bind("<Button-1>", self.on_click)

            # Bind the canvas to respond to mouse events
        image33 = Image.open("s2.png")
        image33 = image33.resize((30, 30))
        self.imag1 = ImageTk.PhotoImage(image33)
        self.canvas.button = tk.Button(root, text="draw rectangle",image=self.imag1, command=self.create_rectangle)
        self.canvas.button.pack(side=tk.LEFT, padx=10, pady=10)
        image333 = Image.open("s3.png")
        image333 = image333.resize((30, 30))
        self.imag2 = ImageTk.PhotoImage(image333)
        self.canvas.button = tk.Button(root, text="draw line", image=self.imag2, command=self.create_line)
        self.canvas.button.pack(side=tk.LEFT, padx=10, pady=10)
        image = Image.open("s1.png")
        image = image.resize((30, 30))
        self.image = ImageTk.PhotoImage(image)
        self.canvas.button = tk.Button(root, text="select", image=self.image, command=self.select_object)
        self.canvas.button.pack(side=tk.LEFT, padx=10, pady=10)
        # self.canvas.bind("<Button-1>", self.on_click)

    
    def create_menu(self):
        # Create menu for file operations
        self.menu = tk.Menu(self.root)
        self.root.config(menu=self.menu)
        
        file_menu = tk.Menu(self.menu, tearoff=0)
        file_menu.add_command(label="Open", command=self.open_file)
        file_menu.add_command(label="Save", command=self.save_file)
        self.menu.add_cascade(label="File", menu=file_menu)
    
    def create_toolbar(self):
        # Create toolbar with drawing tools
        pass
    def create_line(self):
        self.canvas.bind("<Button-1>", start_line)
        self.canvas.bind("<B1-Motion>", draw_line)
        self.canvas.bind("<ButtonRelease-1>", end_line)
    def create_rectangle(self):
        self.canvas.bind("<Button-1>", start_rectangle)
        self.canvas.bind("<B1-Motion>", draw_rectangle)
        self.canvas.bind("<ButtonRelease-1>", end_rectangle)
    def open_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Drawing Files", "*.txt")])
        if filename:
            self.load_drawing(filename)
    
    def save_file(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Drawing Files", "*.txt")])
        if filename:
            self.save_drawing(filename)
    
    def load_drawing(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                # Parse each line and create corresponding drawing objects
                pass
    def generate_code(self):
        self.asciicode = ''
        for line in list_of_objects:
            self.asciicode+=line.get_code()
        for group in list_of_groups:
            self.asciicode+=group.get_code()
        print(self.asciicode)
    def save_drawing(self, filename):
        self.generate_code()
        with open(filename, 'w') as file:
            file.write(self.asciicode)
    
    def on_click(self, event):
        # Handle mouse click events
        x, y = event.x, event.y
        
        # Check if an object is clicked
        for obj in reversed(self.objects):
            if obj.is_clicked(x, y):
                self.select_object(obj)
                break
    
    def select_object(self):
        global choice
        global list_of_selected

        # Deselect the currently selected object
        if self.selected_object:
            for obj in list_of_selected:
                obj.show_properly()
            self.selected_object = False
            choice = 'draw'
            destroy_button_by_text(self.root, "group")
            destroy_button_by_text(self.root, "move")
            destroy_button_by_text(self.root, "ungroup")
            destroy_button_by_text(self.root, "ungroup-all")
            destroy_button_by_text(self.root, "delete")
            destroy_button_by_text(self.root, "line_edit_button")
            destroy_button_by_text(self.root, "Corner_style_change")
            destroy_button_by_text(self.root, "Edit")            
            list_of_selected.clear()
            return 
        
        # Select the new object
        self.selected_object = True
        self.create_rectangle()
        choice = 'select'
        self.canvas.button = tk.Button(root, text="group", command=self.remove_rectangle)
        self.canvas.button.pack(side=tk.LEFT, padx=10, pady=10)
        self.canvas.button = tk.Button(root, text="move", command=self.move_object)
        self.canvas.button.pack(side=tk.LEFT, padx=10, pady=10)
        self.canvas.button = tk.Button(root, text="ungroup", command=self.ungroup)
        self.canvas.button.pack(side=tk.LEFT, padx=10, pady=10)
        self.canvas.button = tk.Button(root, text="ungroup-all", command=self.ungroupall)
        self.canvas.button.pack(side=tk.LEFT, padx=10, pady=10)
        self.canvas.button = tk.Button(root, text="delete", command=self.delete)
        self.canvas.button.pack(side=tk.LEFT, padx=10, pady=10)
        



    def edit_line(self):
    # Create a button for selecting line color
        # print("efone")
        global color_option
        selected_color = tk.StringVar()
        selected_color.set("")

        our_object=None
        # selected_corner = tk.StringVar()
        # selected_corner.set("")
        global list_of_selected
        for obj in list_of_selected:
            if isinstance(obj, Line):
                our_object=obj

        self.edit_button = tk.Button(root, text="Edit", command=lambda obj=our_object: show_edit_dialog_line(obj))
        self.edit_button.pack(pady=20)
        # print(color_option)
        # self.change_line_color(color_option)


    
    def edit_rect(self):
    # Create a button for selecting line color
        # print("efone")
        global color_option
        selected_color = tk.StringVar()
        selected_color.set("")

        global list_of_selected
        for obj in list_of_selected:
            if isinstance(obj, Rectangle):
                our_object=obj

        self.edit_button = tk.Button(root, text="Edit", command=lambda obj=our_object: show_edit_dialog_rect(obj))
        self.edit_button.pack(pady=20)
        # print(color_option)
        # self.change_line_color(color_option)
    
    


    def change_line_color(self, color):
        # Change the color of the selected line(s)
        global list_of_selected
        for obj in list_of_selected:
            if isinstance(obj, Line):
                obj.set_color(color)
            if isinstance(obj,Rectangle):
                obj.set_color(color)
                
                
                
    
    
    
    # def edit_line(self):
    # # Create a button for selecting line color
    #     # print("efone")
    #     self.color_button = tk.Button(self.root, text="Edit", command=show_color_options)
    #     self.color_button.pack(padx=20, pady=10)
            


    # def show_color_options(self):
    #     # Create a popup menu for selecting line color
    #     self.color_menu = tk.Menu(self.root, tearoff=0)
    #     self.color_menu.add_command(label="Black", command=lambda: self.change_line_color("black"))
    #     self.color_menu.add_command(label="Red", command=lambda: self.change_line_color("red"))
    #     self.color_menu.add_command(label="Green", command=lambda: self.change_line_color("green"))
    #     self.color_menu.add_command(label="Blue", command=lambda: self.change_line_color("blue"))
        
    #     # Display the color options menu
    #     self.color_menu.post(self.color_button.winfo_rootx(), self.color_button.winfo_rooty() + self.color_button.winfo_height())

    # def change_line_color(self, color):
    #     # Change the color of the selected line(s)
    #     global list_of_selected
    #     for obj in list_of_selected:
    #         if isinstance(obj, Line):
    #             obj.set_color(color)
    #         if isinstance(obj,Rectangle):
    #             obj.set_color(color)

    
    

        # Redraw the canvas to reflect the color changes
        # self.redraw_canvas()

    
    # def edit_rect_corner(self):
    #     self.corner_button = tk.Button(self.root, text="Corner_style_change", command=self.show_corner_options)
    #     self.corner_button.pack()
    
    
    
    
    def change_corner(self, corner):
        # Change the color of the selected line(s)
        global list_of_selected,first,second,third,fourth
        for obj in list_of_selected:
            if isinstance(obj,Rectangle):
                # obj.set_corner(corner)
                print("ha")
                if corner=="Rounded":
                    self.canvas.delete(obj.id)
                    # self.canvas.create_rectangle(obj.x1, obj.y1, obj.x2, obj.y2, outline="grey")
                    obj.id=draw_rounded_rectangle(editor.canvas, obj.x1, obj.y1, obj.x2, obj.y2, 20,obj.color ,outline='black', width=1)
                    obj.corner_style='Rounded'
                    obj.show_on_select()
                    
                else:
                    self.canvas.delete(obj.id)
                    obj.id=self.canvas.create_rectangle(obj.x1, obj.y1, obj.x2, obj.y2, outline="grey",fill=obj.color)
                    obj.corner_style='Square'
                    obj.show_on_select()
                    # self.canvas.delete(first)
                    # self.canvas.delete(second)
                    # self.canvas.delete(third)
                    # self.canvas.delete(fourth)
                    


                # Redraw the canvas to reflect the color changes
                # self.redraw_canvas()
    
        
    def ungroup(self):
        for obj in list_of_selected:
            if isinstance(obj,Group):
                # list_of_groups.append(obj)
                obj.ungroup()
                list_of_groups.__delitem__(list_of_groups.index(obj))
                
    def delete(self):
        for obj in list_of_selected:
            obj.delete()
           
            if isinstance(obj,Group):
                list_of_groups.__delitem__(list_of_groups.index(obj))
            else:
                list_of_objects.__delitem__(list_of_objects.index(obj))
        list_of_selected.clear()
    def ungroupall(self):
        # global list_of_groups
        for group in list_of_selected:
            if isinstance(group,Group):
                group.ungroupall()
                list_of_groups.__delitem__(list_of_groups.index(group))
    def move_object(self):
        self.canvas.bind("<Button-1>",  self.start_move)
        self.canvas.bind("<B1-Motion>", self.move_object1)
        self.canvas.bind("<ButtonRelease-1>", self.end_move1)
        
    def start_move(self, event):
        global start_x, start_y
        start_x, start_y = event.x, event.y
    def move_object1(self, event):
        global start_x, start_y
        global list_of_selected
        
        x, y = event.x, event.y
        dx, dy = x - start_x, y - start_y
        for obj in list_of_selected:
            print('on time of moving check ', obj)
            obj.move(dx, dy)
        for obj in list_of_groups:
            print('object', obj)
            # obj.move(dx, dy)
        start_x, start_y = x, y
    def end_move1(self, event):
        global choice
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")
        choice = 'draw'
        pass
    def remove_rectangle(self):
        # self.canvas.bind("<Button-1>", remove_rectangle)
        new_group = Group()
        global list_of_selected
        global list_of_groups
        global list_of_objects
        for obj in list_of_selected:
            if isinstance(obj,Group):
                list_of_groups.__delitem__(list_of_groups.index(obj))
            else:
                list_of_objects.__delitem__(list_of_objects.index(obj))
            new_group.add_object(obj)
            
        list_of_groups.append(new_group)
    def redraw_canvas(self):
        self.canvas.delete("all")
        for obj in self.objects:
            obj.draw(self.canvas)
            
    

def start_rectangle(event):
    global start_x, start_y, current_rectangle
    start_x, start_y = event.x, event.y
    if choice == 'select':
        current_rectangle = editor.canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="grey", dash=(5, 5))
    else:
        current_rectangle = editor.canvas.create_rectangle(start_x, start_y, start_x, start_y, outline="grey",width=2)

        
def draw_rectangle(event):
    if current_rectangle:
        x, y = event.x, event.y
        editor.canvas.coords(current_rectangle, start_x, start_y, x, y)
    # print(start_x, start_y, x, y)
def end_rectangle(event):
    global start_x, start_y, current_rectangle, choice, list_of_selected
    
    if current_rectangle:
        x, y = event.x, event.y
        editor.canvas.coords(current_rectangle, start_x, start_y, x, y)
        if choice == 'select':
           
            for line in list_of_objects:
                if line.check_in_area(start_x, start_y, x, y):
                    list_of_selected.append(line)
            for group in list_of_groups:
                if group.check_in_area(start_x, start_y, x, y):
                    list_of_selected.append(group)
                   
            for obj in list_of_selected:
                obj.show_on_select()
                if(len(list_of_selected)==1):
                    if(isinstance(obj,Line)):
                        obj.edit()
                    if(isinstance(obj,Rectangle)):
                        obj.edit()
            editor.canvas.delete(current_rectangle)
            
            return
        list_of_objects.append(Rectangle(start_x, start_y, x, y, "Black", "sharp", id=current_rectangle))
def start_line(event):
    global start_x, start_y, current_line
    start_x, start_y = event.x, event.y
    current_line = editor.canvas.create_line(start_x, start_y, start_x, start_y, tags="line")

def draw_line(event):
    if current_line:
        x, y = event.x, event.y
        editor.canvas.coords(current_line, start_x, start_y, x, y)
def end_line(event):
    global start_x, start_y, current_line
    if current_line:
        x, y = event.x, event.y
        editor.canvas.coords(current_line, start_x, start_y, x, y)
        list_of_objects.append(Line(start_x, start_y, x, y, "black", id=current_line))
        

# Example usage
root = tk.Tk()
root.title("Drawing Editor")
editor = DrawingEditor(root)

selected_color = tk.StringVar()
selected_color.set("")

selected_corner = tk.StringVar()
selected_corner.set("")


# tk.Label(root, text="Selected Color:").pack()
# tk.Label(root, textvariable=selected_color).pack()

# tk.Label(root, text="Selected Corner Style:").pack()
# tk.Label(root, textvariable=selected_corner).pack()

# edit_button = tk.Button(root, text="Edit", command=show_edit_dialog)
# edit_button.pack(pady=20)
# app= App()
# app.mainloop()
root.mainloop()



print('gopal')
print(list_of_objects)
print('list of rectangles')
print(list_of_objects)
print('list of groups')
for group in list_of_groups:
    print('new_group')
    print(group)
    for obj in group.objects:
        print(obj, end='')  # print all objects in the group
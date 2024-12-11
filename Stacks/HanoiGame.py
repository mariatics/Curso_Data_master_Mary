import tkinter as tk
from tkinter import messagebox
import logging

# Configuración del logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Aquí es donde se crean los discos
class Node:
    def __init__(self, value):
        self.value = value
        self.next_node = None

    def get_value(self):
        return self.value

    def set_next_node(self, next_node):
        self.next_node = next_node

# Aquí es donde se van a ir apilando los discos
class Stack:
    def __init__(self, limit=1000): 
        self.top_item = None
        self.size = 0
        self.limit = limit

    def has_space(self):
        return self.limit > self.size

    def is_empty(self):
        return self.size == 0

    def push(self, value):
        if not self.has_space():
            logger.warning("La pila está llena ¡No queda espacio!")
            messagebox.showwarning("Advertencia", "La pila está llena ¡No queda espacio!")
            return

        item = Node(value)
        item.set_next_node(self.top_item)
        self.top_item = item
        self.size += 1

    def pop(self):
        if self.is_empty():
            logger.warning("La pila está totalmente vacía!")
            messagebox.showwarning("Advertencia", "La pila está totalmente vacía!")
            return None

        item_to_remove = self.top_item
        self.top_item = self.top_item.next_node
        self.size -= 1
        return item_to_remove.get_value()

    def peek(self):
        if self.is_empty():
            logger.warning("La pila está totalmente vacía!")
            messagebox.showwarning("Advertencia", "La pila está totalmente vacía!")
            return None
        
        return self.top_item.get_value()

    def get_disks(self):
        disks = []
        current = self.top_item
        while current:
            disks.append(current.get_value())
            current = current.next_node
        return disks[::-1]  # Devuelve en orden de abajo hacia arriba

# Aquí es donde comienza lo bueno (bueno, apenas la ventana)
class HanoiGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Torres de Hanoi")
        
        self.stacks = [Stack(limit=1000) for _ in range(3)]  # Tres pilas
        self.move_count = 0
        self.optimal_moves = 0
        self.create_widgets()

    # Aquí se crean los widgets de la interfaz
    def create_widgets(self):
        self.disk_label = tk.Label(self.root, text="Número de discos (máx 1000):")
        self.disk_label.pack()

        self.disk_entry = tk.Entry(self.root)
        self.disk_entry.pack()

        self.start_button = tk.Button(self.root, text="Iniciar Juego", command=self.start_game)
        self.start_button.pack()

        self.canvas = tk.Canvas(self.root, width=600, height=400, bg="white")
        self.canvas.pack()

        self.from_label = tk.Label(self.root, text="Mover desde la pila:")
        self.from_label.pack()

        self.from_stack_var = tk.IntVar(value=0)
        self.from_stack_dropdown = tk.OptionMenu(self.root, self.from_stack_var, 1, 2, 3)
        self.from_stack_dropdown.pack()

        self.to_label = tk.Label(self.root, text="Mover a la pila:")
        self.to_label.pack()

        self.to_stack_var = tk.IntVar(value=1)
        self.to_stack_dropdown = tk.OptionMenu(self.root, self.to_stack_var, 1, 2, 3)
        self.to_stack_dropdown.pack()

        self.move_button = tk.Button(self.root, text="Mover Disco", command=self.move_disk)
        self.move_button.pack()

        self.reset_button = tk.Button(self.root, text="Reiniciar Juego", command=self.reset_game)
        self.reset_button.pack()

        self.result = tk.Label(self.root, text="")
        self.result.pack()

        self.moves_label = tk.Label(self.root, text="")
        self.moves_label.pack()

        self.optimal_moves_label = tk.Label(self.root, text="")
        self.optimal_moves_label.pack()

    # Comienza el juego y prepara las pilas
    def start_game(self):
        try:
            num_disks = int(self.disk_entry.get())
            if num_disks < 1 or num_disks > 1000:
                raise ValueError("El número de discos debe estar entre 1 y 1000.")
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        # Reiniciar las pilas
        self.stacks = [Stack(limit=num_disks) for _ in range(3)]
        self.move_count = 0
        self.optimal_moves = (2 ** num_disks) - 1 
        self.moves_label.config(text=f"Movimientos realizados: {self.move_count}")
        self.optimal_moves_label.config(text=f"Movimientos óptimos: {self.optimal_moves}")

        # Apilar los discos en la primera pila
        for i in range(num_disks, 0, -1):
            self.stacks[0].push(i)
        self.draw_stacks()

    # Dibuja las pilas y discos en el lienzo
    def draw_stacks(self):
        self.canvas.delete("all")  
        positions = [100, 300, 500]  # Posiciones de las torres
        for i, stack in enumerate(self.stacks):
            x = positions[i]
            for j, disk in enumerate(stack.get_disks()):
                width = disk * 20  # Ancho del disco
                self.canvas.create_rectangle(x - width // 2, 300 - j * 20, 
                                               x + width // 2, 300 - (j + 1) * 20, 
                                               fill="blue")

    # Mueve un disco de una pila a otra
    def move_disk(self):
        from_stack_idx = self.from_stack_var.get() - 1 
        to_stack_idx = self.to_stack_var.get() - 1 
        if self.stacks[from_stack_idx].is_empty():
            self.result.config(text="No hay discos para mover.")
            return

        disk = self.stacks[from_stack_idx].peek()
        if (self.stacks[to_stack_idx].is_empty() or
                disk < self.stacks[to_stack_idx].peek()):
            self.stacks[to_stack_idx].push(self.stacks[from_stack_idx].pop())
            self.move_count += 1
            self.moves_label.config(text=f"Movimientos realizados: {self.move_count}")
            self.result.config(text=f"Moviendo disco {disk} de Pila {from_stack_idx + 1} a Pila {to_stack_idx + 1}")
            self.draw_stacks()
        else:
            self.result.config(text="Movimiento inválido.")

    # Reinicia el juego
    def reset_game(self):
        self.stacks = [Stack(limit=1000) for _ in range(3)]  
        self.move_count = 0
        self.moves_label.config(text=f"Movimientos realizados: {self.move_count}")
        self.result.config(text="")
        self.disk_entry.delete(0, tk.END)  # Limpiar entrada de discos
        self.canvas.delete("all")  # Limpiar el lienzo

# Este bloque inicia la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    game = HanoiGame(root)
    root.mainloop()
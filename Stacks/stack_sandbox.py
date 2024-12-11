from Node import Node

import logging
# Configuración del módulo logging

class Stack:
    def __init__(self):
        # Inicializa la pila vacía
        self.top_item = None
        logging.warning("Inicializando la pila.")

    def peek(self):
        # Verifica si el elemento superior existe
        if self.top_item:
            logging.warning("Obteniendo el valor del elemento superior.")
            return self.top_item.get_value()
        else:
            logging.warning("La pila está vacía. Lanzando AttributeError.")
            raise AttributeError("No se puede hacer peek en una pila vacía.")

    def push(self, value):
        # Crea un nuevo nodo con el valor proporcionado
        logging.warning(f"Agregando valor {value} a la pila.")
        item = Node(value)  # Crea un nodo con el valor dado
        item.set_next_node(self.top_item)  # Conecta el nuevo nodo con el nodo superior actual
        self.top_item = item  # Establece el nuevo nodo como el nodo superior

    def pop(self):
        # Elimina el nodo superior y devuelve su valor
        if self.top_item is None:
            logging.warning("Intentando eliminar de una pila vacía. Lanzando AttributeError.")
            raise AttributeError("No se puede hacer pop en una pila vacía.")
        item_to_remove = self.top_item  # Guarda el nodo superior
        self.top_item = item_to_remove.get_next_node()  # Actualiza el nodo superior
        logging.warning(f"Eliminando el valor {item_to_remove.get_value()} de la pila.")
        return item_to_remove.get_value()  # Devuelve el valor del nodo eliminado

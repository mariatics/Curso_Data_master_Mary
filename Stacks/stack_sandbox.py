from Node import Node

import logging


class Stack:
    def __init__(self, limit=1000):
        self.top_item = None
        self.size = 0
        self.limit = limit
        logging.warning("Inicializando la pila con límite de {} elementos.".format(limit))

    def peek(self):
        if not self.is_empty():
            logging.warning("Obteniendo el valor del elemento superior.")
            return self.top_item.get_value()
        else:
            logging.warning("La pila esta totalmente vacia!")
            return None

    def push(self, value):
        if self.has_space():
            logging.warning(f"Agregando valor {value} a la pila.")
            item = Node(value)
            item.set_next_node(self.top_item)
            self.top_item = item
            self.size += 1
        else:
            logging.warning("La pila esta llena ¡No queda espacio!")

    def pop(self):
        if not self.is_empty():
            item_to_remove = self.top_item
            self.top_item = item_to_remove.get_next_node()
            self.size -= 1
            logging.warning(f"Eliminando el valor {item_to_remove.get_value()} de la pila.")
            return item_to_remove.get_value()
        else:
            logging.warning("La pila esta totalmente vacia!")
            return None

    def has_space(self):
        return self.size < self.limit

    def is_empty(self):
        return self.size == 0

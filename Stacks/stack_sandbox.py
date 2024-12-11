from Node import Node

import logging

# Configuración del módulo logging
logging.basicConfig(level=logging.WARNING, format='%(levelname)s: %(message)s')

class Stack:
    def __init__(self):
        # Inicializa la pila con un elemento superior vacío
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

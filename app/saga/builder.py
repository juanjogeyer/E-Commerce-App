from typing import Callable, List
from .exceptions import SagaError

class SagaStep:
    """Representa un paso en la saga con su acción principal y su compensación."""
    def __init__(self, action: Callable, compensation: Callable):
        self.action = action
        self.compensation = compensation

class SagaBuilder:
    """Orquestador para gestionar la ejecución de una saga con pasos de acción y compensación."""
    
    def __init__(self):
        self.steps: List[SagaStep] = []
        self.compensations: List[Callable] = []

    @staticmethod
    def create():
        """Inicializa un nuevo SagaBuilder."""
        return SagaBuilder()

    def action(self, action: Callable, compensation: Callable):
        """Agrega una acción y su compensación como un paso de la saga."""
        self.steps.append(SagaStep(action, compensation))
        return self

    def build(self):
        """Construye la saga lista para ser ejecutada."""
        return self

    def execute(self):
        """Ejecuta cada paso de la saga; si falla, revierte las acciones previas."""
        try:
            for step in self.steps:
                step.action()  # Ejecuta la acción principal
                self.compensations.append(step.compensation)  # Guarda la compensación en caso de fallo
            print("Saga ejecutada exitosamente.")
        except Exception as e:
            print(f"Error en la saga: {e}. Iniciando compensación...")
            self._compensate()
            raise SagaError("Saga fallida, se ejecutó la compensación.") from e

    def _compensate(self):
        """Ejecuta las compensaciones en orden inverso para deshacer acciones."""
        for compensation in reversed(self.compensations):
            try:
                compensation()  # Ejecuta la compensación
            except Exception as e:
                print(f"Error en la compensación: {e}")
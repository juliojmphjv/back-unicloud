from abc import ABC, abstractmethod

class DashboardInterface(ABC):

    @abstractmethod
    def get_dashboard(self) -> str:
        pass
from typing import Type
from unicloud_dashboard.interfaces.dashboard import DashboardInterface

class DashboardFactory:

    def __init__(self, name: str) -> None:
        self.pod_name = name


    def get_dasboard(self, dashboard: Type[DashboardInterface]):
        dashboard = dashboard.get_dashboard()
        return dashboard


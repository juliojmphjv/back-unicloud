from dashboards.zadara_dash import ZadaraDashboard
from factory.factory import DashboardFactory
from unicloud_pods.models import ZadaraPods

pods = ZadaraPods.objects.all()
for pod in pods:
    engenheiro = DashboardFactory(pod)
    zad = ZadaraDashboard('teste')
    engenheiro.get_token(zad)

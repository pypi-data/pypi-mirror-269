from netbox.api.routers import NetBoxRouter
from . import views


app_name = "netbox_device_support_plugin"

router = NetBoxRouter()
# Cisco Support
router.register(r"cisco-device", views.CiscoDeviceSupportViewSet)
router.register(r"cisco-device-type", views.CiscoDeviceTypeSupportViewSet)
# Fortnet Support
router.register(r"fortinet-device", views.FortinetDeviceSupportViewSet)
# PureStorage Support
router.register(r"purestorage-device", views.PureStorageDeviceSupportViewSet)

urlpatterns = router.urls

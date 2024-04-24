from extras.plugins import PluginMenuItem

menu_items = (
    # Cisco Support
    PluginMenuItem(
        link="plugins:netbox_device_support_plugin:ciscodevicesupport_list",
        link_text="Cisco Device Support",
    ),
    PluginMenuItem(
        link="plugins:netbox_device_support_plugin:ciscodevicetypesupport_list",
        link_text="Cisco Device Type Support",
    ),
    # Fortnet Support
    PluginMenuItem(
        link="plugins:netbox_device_support_plugin:fortinetdevicesupport_list",
        link_text="Fortinet Device Support",
    ),
    # PureStorage Support
    PluginMenuItem(
        link="plugins:netbox_device_support_plugin:purestoragedevicesupport_list",
        link_text="PureStorage Device Support",
    ),
)

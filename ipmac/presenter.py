"""Presenter class"""
from ipmac.gui import Gui
from ipmac.dataModel import SqlData


class Presenter:
    """Presenter class """

    def __init__(self):
        self.view = Gui()
        self.data = SqlData()

    def handle_update_all_data(self):
        """Returns all data from model"""
        self.data.update_data()

    def handle_get_list_data(self):
        """Returns list data from model"""
        return self.data.get_devices()

    def handle_update_active_device(self, idx):
        """Trigger model to set active device based on idx"""
        self.data.update_active_device(idx)

    def handle_get_active_device(self):
        """Returns active DeviceData obj from model"""
        return self.data.get_active_device()

    def handle_get_device_id(self, dev_name):
        """Calls data method to retrieve device id
        for a specified dev_name
        """
        return self.data.get_device_id(dev_name)

    def handle_save_device_data(self, data):
        """Triger save device data obj into model obj """
        self.data.add_device_data(data)

    def handle_delete_device(self, data_obj):
        """Triger delete device data obj into model obj """
        self.data.delete_device_data(data_obj)

    def handle_delete_if(self):
        """Trigger delete selected interfaces """
        self.data.delete_if_data(self.data.get_selected_if_list())

    def handle_update_device(self, data_obj):
        """Triger update device data obj into model obj """
        self.data.update_device_data(data_obj)

    def handle_trigger_update_dev_list(self):
        """Triger update device device list in gui """
        self.handle_update_all_data()
        self.view.update_device_list()

    def handle_check_device(self, dev_name):
        """Calls model to verify if device_name already exists"""
        return self.data.is_device_present(dev_name)

    def handle_get_if_for_device(self, device_obj):
        """Returns formated interface list of active device"""
        return self.data.get_if_data(device_obj)

    def handle_get_all_if(self):
        """Returns formated interface list for all devices"""
        return self.data.get_all_if_data()

    def handle_save_if_data(self, if_data):
        """Triger save interface data to db"""
        self.data.add_if_data(if_data)

    def handle_trigger_update_if_list(self):
        """Triger update if list in gui """
        self.handle_update_all_data()
        active_dev = self.handle_get_active_device()
        self.handle_update_active_device(active_dev.device_id)
        active_dev = self.handle_get_active_device()
        self.view.fill_if_table(active_dev)

    def handle_update_selected_if_list(self, if_data_list):
        """Trigger update selected interface list"""
        self.data.update_selected_if_list(if_data_list)

    def run(self):
        """Run method of Presenter"""
        self.view.create_main_gui(self)
        self.view.mainloop()

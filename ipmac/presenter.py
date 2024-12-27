from ipmac.gui import Gui
from ipmac.dataModel import SqlData


class Presenter:
    """Presenter class """

    def __init__(self):
        self.view = Gui()
        self.data = SqlData()

    def handle_get_list_data(self):
        """Returns list data from model"""
        self.data.create_device_struct()
        return self.data.get_devices()

    def handle_update_active_device(self, idx):
        """Trigger model to set active device based on idx"""
        self.data.update_active_device(idx)

    def handle_get_active_device(self):
        """Returns active device obj from model"""
        return self.data.get_active_device()

    def handle_save_device_data(self, data):
        """Triger save device data obj into model obj """
        self.data.add_device_data(data)

    def handle_delete_device(self, data_obj):
        """Triger delete device data obj into model obj """
        self.data.delete_device_data(data_obj)

    def handle_update_device(self, data_obj):
        """Triger update device data obj into model obj """
        self.data.update_device_data(data_obj)

    def handle_trigger_update_dev_list(self):
        """Triger update device device list in gui """
        self.view.update_device_list()

    def handle_check_device(self, dev_name):
        """Calls model to verify if device_name already exists"""
        return self.data.is_device_present(dev_name)

    def run(self):
        """Run method of Presenter"""
        self.view.create_main_gui(self)
        self.view.mainloop()

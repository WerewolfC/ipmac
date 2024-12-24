""" GUI class"""
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
import re

import ipmac.types as data_types

# window params
WINDOW_MAIN_SIZE = "800x450"
WINDOW_MAIN_TITLE = "IPMac utility"
WINDOW_ADD_DEVICE_SIZE = "350x240"
WINDOW_ADD_DEVICE_TITLE = "Add new device"
WINDOW_ADD_INTERFACE_SIZE = "350x220"
WINDOW_ADD_INTERFACE_TITLE = "Add new device"


class Gui(ttk.Window):
    """Class implements main window"""

    def __init__(self):
        """Create entire GUI frame """
        super().__init__(themename=data_types.GUI_STYLE_NAME)
        self.title(WINDOW_MAIN_TITLE)
        self.geometry(WINDOW_MAIN_SIZE)
        self.resizable(False, False)

    def create_main_gui(self):
        """Create main window"""

        self.add_top_frame()
        self.add_left_frame()
        self.add_rigth_frame()

    def add_top_frame(self):
        """Create search bar"""

        search_frame = ttk.Frame(self)
        # add input field
        search_text = tk.StringVar()
        textbox = ttk.Entry(search_frame, textvariable=search_text, width=50)
        textbox.focus()
        textbox.pack(side="left", expand=True, fill="x", padx=5, pady=5)

        # add search button
        btn_search = ttk.Button(master=search_frame,
                                text="Search",
                                width=10,
                                bootstyle="secondary")
        btn_search.pack(side="right", padx=5, pady=5, anchor="w")
        search_frame.pack(side="top", expand=False, fill="both", padx=5, pady=5)

    def add_left_frame(self):
        """Create listbox frame"""
        device_frame = ttk.Frame(self)
        lst_device = tk.Listbox(device_frame)
        lst_device.pack(side="top", expand=True, fill="both", padx=5, pady=5)
        btn_add_device = ttk.Button(master=device_frame,
                                    text="+",
                                    width=5,
                                    command=self._cb_add_device,
                                    bootstyle="secondary")
        btn_rem_device = ttk.Button(master=device_frame,
                                    text="-",
                                    width=5,
                                    command=self._cb_rem_device,
                                    bootstyle="secondary")
        btn_edit_device = ttk.Button(master=device_frame,
                                     text="...",
                                     width=5,
                                     command=self._cb_edit_device,
                                     bootstyle="secondary")
        btn_add_device.pack(side="left", padx=5, pady=5, anchor="w")
        btn_rem_device.pack(side="left", padx=5, pady=5, anchor="w")
        btn_edit_device.pack(side="left", padx=5, pady=5, anchor="w")
        device_frame.pack(side="left", expand=True, fill="both", padx=5, pady=5)

    def add_rigth_frame(self):
        """Create details frame"""
        info_frame = ttk.Frame(self)

        txt_device_desc = tk.Text(info_frame, height=3, width=95)
        txt_device_desc.pack(side="bottom", expand=True, padx=5, pady=5)

        tbl_list_if = Tableview(
            master=info_frame,
            coldata=data_types.COLDATA,
            stripecolor=(self.style.colors.light, None),
        )
        tbl_list_if.pack(side="bottom", expand=True, fill="both")

        btn_add_if = ttk.Button(master=info_frame,
                                text="+",
                                width=5,
                                command=self._cb_add_if,
                                bootstyle="secondary")
        btn_rem_if = ttk.Button(master=info_frame,
                                text="-",
                                width=5,
                                bootstyle="secondary")
        btn_edit_if = ttk.Button(master=info_frame,
                                 text="...",
                                 width=5,
                                 command=self._cb_edit_if,
                                 bootstyle="secondary")
        btn_copy_mac = ttk.Button(master=info_frame,
                                  text="cp MAC",
                                  width=5,
                                  bootstyle="secondary")
        btn_copy_ip = ttk.Button(master=info_frame,
                                 text="cp IP",
                                 width=5,
                                 bootstyle="secondary")
        btn_add_if.pack(side="left", padx=5, pady=5, anchor="w")
        btn_rem_if.pack(side="left", padx=5, pady=5, anchor="w")
        btn_edit_if.pack(side="left", padx=5, pady=5, anchor="w")
        btn_copy_mac.pack(side="right", padx=5, pady=5, anchor="w")
        btn_copy_ip.pack(side="right", padx=5, pady=5, anchor="w")

        info_frame.pack(side="left", expand=True, fill="both", padx=5, pady=5)

    def _cb_add_device(self):
        """Add device callback method"""
        self.device_win = DeviceWinManager.get_device_window(data_types.default_device_data)
        self.device_win.focus()

    def _cb_rem_device(self):
        """Remove device callback method"""
        pass

    def _cb_edit_device(self):
        """Edit device callback method"""
        # TODO : replace stub with actual data from DB
        self.device_win = DeviceWinManager.get_device_window(data_types.stub_device_data)
        self.device_win.focus()

    def _cb_edit_if(self):
        """Add if callback method"""
        # TODO : replace stub with actual data from DB
        self.if_win = IfWinManager.get_if_window(data_types.stub_if_data)
        self.if_win.focus()

    def _cb_add_if(self):
        """Add if callback method"""
        self.if_win = IfWinManager.get_if_window(data_types.default_if_data)
        self.if_win.focus()

    def _cb_rem_if(self):
        """Remove if callback method"""
        pass


class WindowAddDevice(ttk.Toplevel):
    """Class implements add device window"""

    def __init__(self, win_title=WINDOW_ADD_DEVICE_TITLE, device_data=data_types.default_device_data):
        """Create add device GUI frame

        win_tytle   = window title
        device_data = optional object containing Device name + device description
                      is used only for editing existing device

        """
        super().__init__()
        self.title(win_title)
        self.geometry(WINDOW_ADD_DEVICE_SIZE)
        self.resizable(False, False)
        self._device_data = device_data
        self.create_add_device_gui()

    def create_add_device_gui(self):
        """Create add device window"""
        frm_device_name = ttk.Frame(self)
        lbl_device_name = ttk.Label(frm_device_name, text="Device name:", width=20)
        lbl_device_name.pack(side="left", expand=True, fill="x", anchor="w")

        validate_device_name = self.register(self.check_device_name)
        self._device_name = tk.StringVar(value=self._device_data.device_name)
        print(self._device_name.get())
        ent_device_name = ttk.Entry(frm_device_name,
                                    textvariable=self._device_name,
                                    validatecommand=(validate_device_name, '%P'),
                                    width=20)
        # ent_device_name.focus()
        ent_device_name.pack(side="top", expand=True, fill="x")

        frm_device_desc = ttk.Frame(self)
        lbl_device_desc = ttk.Label(frm_device_desc, text="Description:", width=20)
        lbl_device_desc.pack(side="top", expand=True, fill="x")
        self._txt_device_desc = ttk.Text(frm_device_desc, height=5)
        self._txt_device_desc.insert("1.0", self._device_data.device_desc)
        self._txt_device_desc.pack()

        frm_buttons = ttk.Frame(self)
        btn_save = ttk.Button(master=frm_buttons,
                              text="Save",
                              command=self._callback_save,
                              bootstyle="secondary")
        btn_clear = ttk.Button(master=frm_buttons,
                               text="Clear",
                               width=5,
                               command=self._callback_clear,
                               bootstyle="secondary")
        btn_close = ttk.Button(master=frm_buttons,
                               text="Close",
                               width=5,
                               command=self._callback_close,
                               bootstyle="secondary")
        btn_save.pack(side="left", padx=5, pady=5, anchor="w")
        btn_clear.pack(side="left", padx=5, pady=5, anchor="w")
        btn_close.pack(side="left", padx=5, pady=5, anchor="w")

        frm_device_name.pack(padx=5, pady=5)
        frm_device_desc.pack(padx=5, pady=5)
        frm_buttons.pack(padx=5, pady=5)

    def _callback_save(self):
        """Callback method to save"""
        # TODO
        pass

    def _callback_close(self):
        """Callback method to close window"""
        DeviceWinManager.destroy_device_edit_window()

    def _callback_clear(self):
        """Callback method to clear IO fields"""

        self._device_name.set("")
        self._device_desc = ""
        self._txt_device_desc.delete("1.0", tk.END)

    @staticmethod
    def check_device_name(dev_name):
        """Validate device name"""
        print(dev_name)
        return True
        # return bool(re.match(valid_pattern, ip_name))


class WindowAddInterface(ttk.Toplevel):
    """Class implements add interface window"""

    def __init__(self, win_title=WINDOW_ADD_INTERFACE_TITLE, if_data=data_types.default_if_data):
        """Create entire GUI frame

        win_tytle   = window title
        if_data     = optional obj containing IP, MAC, type
                      is used only for editing existing if

        """
        super().__init__()
        self.title(win_title)
        self.geometry(WINDOW_ADD_INTERFACE_SIZE)
        self.resizable(False, False)
        self._if_data = if_data
        self.create_add_interface_gui()

    def create_add_interface_gui(self):
        """Create add interface window"""
        print(self._if_data)
        # register validation _callback
        validate_ip_address = self.register(self.check_ip_address)
        validate_mac_address = self.register(self.check_mac_address)

        lbl_device_name = ttk.Label(self, text=f"Device name: {self._if_data.device_name}")
        lbl_device_name.pack()

        frm_ip = ttk.Frame(self)
        lbl_ip = ttk.Label(frm_ip, width=15, text="IP address:", anchor="w")
        self._ip_name = tk.StringVar(value=self._if_data.ip)
        ent_ip_name = ttk.Entry(frm_ip,
                                validate="focus",
                                validatecommand=(validate_ip_address, '%P'),
                                textvariable=self._ip_name,
                                width=20)
        ent_ip_name.focus()
        lbl_ip.pack(side="left", expand=True, fill="x")
        ent_ip_name.pack(side="left", expand=True, fill="x")

        frm_mac = ttk.Frame(self)
        lbl_mac = ttk.Label(frm_mac, width=15, text="MAC address:", anchor="w")
        self._mac_name = tk.StringVar(value=self._if_data.mac)
        ent_mac_name = ttk.Entry(frm_mac,
                                 validate="focus",
                                 validatecommand=(validate_mac_address, '%P'),
                                 textvariable=self._mac_name,
                                 width=20)
        lbl_mac.pack(side="left", expand="True", fill="x")
        ent_mac_name.pack(side="left", expand=True, fill="x")

        frm_type = ttk.Frame(self)
        lbl_type = ttk.Label(frm_type, width=15, text="Interface type:", anchor="w")
        lbl_type.pack(side="left", expand="True", fill="x")
        self._type_name = tk.IntVar()
        self.combo_type = ttk.Combobox(frm_type, state="readonly", values=list(data_types.IF_TYPE.values()))
        found_key = [idx for idx, val in data_types.IF_TYPE.items() if val == self._if_data.if_type]
        self.combo_type.current(found_key if found_key else 0)
        self.combo_type.pack(side="left", expand=True, fill="x")

        frm_buttons = ttk.Frame(self)
        btn_save = ttk.Button(master=frm_buttons,
                              text="Save",
                              command=self._callback_save,
                              bootstyle="secondary")
        btn_clear = ttk.Button(master=frm_buttons,
                               text="Clear",
                               width=5,
                               command=self._callback_clear,
                               bootstyle="secondary")
        btn_close = ttk.Button(master=frm_buttons,
                               text="Close",
                               width=5,
                               command=self._callback_close,
                               bootstyle="secondary")
        btn_save.pack(side="left", padx=5, pady=5, anchor="w")
        btn_clear.pack(side="left", padx=5, pady=5, anchor="w")
        btn_close.pack(side="left", padx=5, pady=5, anchor="w")

        frm_ip.pack(padx=5, pady=5)
        frm_mac.pack(padx=5, pady=5)
        frm_type.pack(padx=5, pady=5)
        frm_buttons.pack(padx=5, pady=5)

    def _callback_save(self):
        """Callback method to save"""
        # TODO
        pass

    def _callback_close(self):
        """Callback method to close window"""
        IfWinManager.destroy_if_edit_window()

    def _callback_clear(self):
        """Callback method to clear IO fields"""

        self._ip_name.set("")
        self._mac_name.set("")
        self._type_name = 0
        self.combo_type.current(0)

    @staticmethod
    def check_ip_address(ip_name):
        """Validate IP address
        Rules:
            - max len 15
            - digits only
            - 3 dots
        """
        valid_pattern = r"^(\d{1,3}[.]){3}(\d{1,3})$"
        return bool(re.match(valid_pattern, ip_name))

    @staticmethod
    def check_mac_address(mac_name):
        """Validate MAC address
        Rules:
            - max len 17
            - HEXA only
            - 5 column char
        """
        valid_pattern = r"^([0-9A-F]{2}[:]){5}([0-9A-F]{2})$"
        return bool(re.match(valid_pattern, mac_name.upper()))


class DeviceWinManager:
    """Window manager that returns the existing object """
    _device_edit_window = None

    @staticmethod
    def get_device_window(dev_data):
        """Returns a device edit window """
        if not DeviceWinManager._device_edit_window:
            DeviceWinManager._device_edit_window = WindowAddDevice(device_data=dev_data)
        return DeviceWinManager._device_edit_window

    @staticmethod
    def destroy_device_edit_window():
        """Destroys the window object """
        if DeviceWinManager._device_edit_window:
            DeviceWinManager._device_edit_window.destroy()
        DeviceWinManager._device_edit_window = None


class IfWinManager:
    """Window manager that returns the existing object """
    _if_edit_window = None

    @staticmethod
    def get_if_window(if_data):
        """Returns a device edit window """
        if not IfWinManager._if_edit_window:
            IfWinManager._if_edit_window = WindowAddInterface(if_data=if_data)
        return IfWinManager._if_edit_window

    @staticmethod
    def destroy_if_edit_window():
        """Destroys the window object """
        if IfWinManager._if_edit_window:
            IfWinManager._if_edit_window.destroy()
        IfWinManager._if_edit_window = None


if __name__ == "__main__":
    # window = Gui("flatly")
    # window.create_main_gui()
    # window.mainloop()
    # demo_device_data = {
    #     "device_name": "Wolverine",
    #     "device_desc": "some really reallty longlonglonglonglonglonglonglonglonglonglonglonglongllongong text text text text text text text text text text "
    # }
    add_window = WindowAddDevice(device_data=data_types.stub_device_data)
    add_window.create_add_device_gui()
    add_window.mainloop()
    demo_if_data = {
        "device_name": "Wolverine",
        "ip": "192.168.0.100",
        "mac": "AA:BB:CC:DD:EE:FF",
        "type": "Wireless"
    }
    # demo_if_data = {
    #     "device_name": "",
    #     "ip": "",
    #     "mac": "",
    #     "type": "Wired"
    # }
    # print(demo_if_data)
    # add_window = WindowAddInterface("flatly", win_title="Edit interface", if_data=demo_if_data)
    # add_window.create_add_interface_gui()
    # add_window.mainloop()

""" GUI class"""
import re

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.tableview import Tableview
from ttkbootstrap.scrolled import ScrolledText

import ipmac.types as data_types

# window params
WINDOW_MAIN_SIZE = "800x450"
WINDOW_MAIN_TITLE = "IPMac utility"
WINDOW_ADD_DEVICE_SIZE = "350x210"
WINDOW_ADD_DEVICE_TITLE = "Add new device"
WINDOW_ADD_INTERFACE_SIZE = "350x180"
WINDOW_ADD_INTERFACE_TITLE = "Add new interface"

# message dialogs
REMOVE_DEVICE_TITLE = "Are you sure you want to remove device {0}?"
REMOVE_DEVICE_TEXT = "Remove {0}"
DEVICE_EXISTS_TITLE = "Cannot remove {0}"
DEVICE_EXISTS_TEXT = """There are interfaces defined for this device.\nDelete existing interfaces first"""
WRONG_DEVICE_TITLE = "Cannot add interface for {0}"
WRONG_DEVICE_TEXT = "{0} is not a valid device.\nPlease select a valid device"

BANNED_DEVICE_LIST = [0]


def disable_event():
    """Empty function used to disable windows close x button"""
    pass


class Gui(ttk.Window):
    """Class implements main window"""

    def __init__(self):
        """Create entire GUI frame """
        super().__init__(themename=data_types.GUI_STYLE_NAME)
        self.title(WINDOW_MAIN_TITLE)
        self.geometry(WINDOW_MAIN_SIZE)
        self.resizable(False, False)
        self.presenter = None
        # disable x close main window button
        self.protocol("WM_DELETE_WINDOW", disable_event)

    def create_main_gui(self, presenter):
        """Create main window"""
        self.presenter = presenter
        self.presenter.handle_update_all_data()
        self.add_top_frame()
        self.add_left_frame()
        self.add_rigth_frame()
        self.presenter.handle_update_active_device(0)
        self.update_device_list()

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
                                bootstyle="primary")
        btn_search.pack(side="right", padx=5, pady=5, anchor="w")
        search_frame.pack(side="top", expand=False, fill="both", padx=5, pady=5)

    def add_left_frame(self):
        """Create listbox frame"""
        device_frame = ttk.Frame(self)

        dev_list_frame = ttk.Frame(device_frame)
        lst_device_scroll = tk.Scrollbar(dev_list_frame, orient="vertical")
        self.lst_device = tk.Listbox(dev_list_frame,
                                     yscrollcommand=lst_device_scroll.set)
        self.lst_device.bind("<<ListboxSelect>>", self._cb_dev_lst_select)
        self.lst_device.pack(side="left", expand=True, fill="both", pady=5)

        lst_device_scroll.config(command=self.lst_device.yview)
        lst_device_scroll.pack(side="left", fill="y")
        dev_list_frame.pack(side="top", expand=True, fill="both", padx=5, pady=5)

        device_actions_frame = ttk.Frame(device_frame)
        btn_add_device = ttk.Button(master=device_actions_frame,
                                    text="+",
                                    width=3,
                                    command=self._cb_add_device,
                                    bootstyle="primary")
        btn_rem_device = ttk.Button(master=device_actions_frame,
                                    text="-",
                                    width=3,
                                    command=self._cb_rem_device,
                                    bootstyle="primary")
        # TODO:
        # btn_edit_device = ttk.Button(master=device_actions_frame,
        #                              text="...",
        #                              width=3,
        #                              command=self._cb_edit_device,
        #                              bootstyle="primary")
        btn_add_device.pack(side="left", padx=2, pady=2, anchor="w")
        btn_rem_device.pack(side="left", padx=2, pady=2, anchor="w")
        #btn_edit_device.pack(side="left", padx=5, pady=5, anchor="w")
        device_actions_frame.pack(side="top", expand=False, fill="both", padx=5, pady=5)

        export_frame = ttk.Frame(device_frame)
        btn_export_csv = ttk.Button(master=export_frame,
                                    text="Export CSV",
                                    width=10,
                                    command=self._cb_export_csv,
                                    bootstyle="primary")
        btn_import_csv = ttk.Button(master=export_frame,
                            text="Import CSV",
                            width=10,
                            command=self._cb_import_csv,
                            bootstyle="primary")
        btn_export_csv.pack(side="left", padx=2, pady=2, anchor="w")
        btn_import_csv.pack(side="left", padx=2, pady=2, anchor="w")
        export_frame.pack(side="bottom", expand=False, fill="both", padx=5, pady=5)


        device_frame.pack(side="left", expand=False, fill="both", padx=5, pady=5)

    def add_rigth_frame(self):
        """Create details frame"""
        info_frame = ttk.Frame(self)

        if_list = self.presenter.handle_get_all_if()
        self.tbl_list_if = Tableview(
            height=15,
            master=info_frame,
            coldata=data_types.COLDATA,
            rowdata=if_list,
            searchable=False,
            autofit=True,
            autoalign=True
        )
        self.tbl_list_if.pack(side="bottom", expand=True, fill="both")
        self.tbl_list_if.view.bind('<<TreeviewSelect>>', self.cb_tableview_if_select)

        btn_add_if = ttk.Button(master=info_frame,
                                text="+",
                                width=3,
                                command=self._cb_add_if,
                                bootstyle="primary")
        btn_rem_if = ttk.Button(master=info_frame,
                                text="-",
                                width=3,
                                command=self._cb_rem_if,
                                bootstyle="primary")
        # TODO:
        # btn_edit_if = ttk.Button(master=info_frame,
        #                          text="...",
        #                          width=3,
        #                          command=self._cb_edit_if,
        #                          bootstyle="primary")
        btn_copy_mac = ttk.Button(master=info_frame,
                                  text="cp MAC",
                                  width=5,
                                  bootstyle="primary")
        btn_copy_ip = ttk.Button(master=info_frame,
                                 text="cp IP",
                                 width=5,
                                 bootstyle="primary")
        btn_add_if.pack(side="left", padx=5, pady=5, anchor="w")
        btn_rem_if.pack(side="left", padx=5, pady=5, anchor="w")
        #btn_edit_if.pack(side="left", padx=5, pady=5, anchor="w")
        btn_copy_mac.pack(side="right", padx=5, pady=5, anchor="w")
        btn_copy_ip.pack(side="right", padx=5, pady=5, anchor="w")
        info_frame.pack(side="top", expand=True, fill="both", padx=5, pady=5) #  info data frame

        desc_frame = ttk.Frame(self) #  description frame
        self.txt_device_desc = ScrolledText(desc_frame, autohide=True, height=3, width=80)
        self.txt_device_desc.pack(side="left", expand=False, padx=5, pady=5)
        btn_exit_app = ttk.Button(master=desc_frame,
                                  text="Exit",
                                  command=self._cb_exit,
                                  width=5,
                                  bootstyle="primary")
        btn_exit_app.pack(side="left", expand=True, fill="both", padx=5, pady=5)
        desc_frame.pack(side="top", expand=True, fill="both", padx=5, pady=5)

    def _cb_add_device(self):
        """Add device callback method"""
        self.device_win = DeviceWinManager.get_device_window(self.presenter,
                                                             data_types.default_device_data)
        self.device_win.focus()

    def _cb_rem_device(self):
        """Remove device callback method"""
        selected_device = self.presenter.handle_get_active_device()

        if not selected_device.if_list:
            # device has no if assigned
            remove = ttk.dialogs.dialogs.Messagebox.yesno(
                message=REMOVE_DEVICE_TITLE.format(selected_device.device_name),
                title=REMOVE_DEVICE_TEXT.format(selected_device.device_name),
                parent=self,
                alert=True
            )
            if remove == "Yes":
                self.presenter.handle_delete_device(selected_device)
                self.presenter.handle_trigger_update_dev_list()
        else:
            # there are no if for device
            can_not_remove_dialog = ttk.dialogs.dialogs.Messagebox.show_warning(
                message=DEVICE_EXISTS_TEXT.format(selected_device.device_name),
                title=DEVICE_EXISTS_TITLE.format(selected_device.device_name),
                parent=self,
                alert=True
            )

    def _cb_export_csv(self):
        """Callback for export to csv procedure"""
        self.presenter.handle_export_csv()

    def _cb_import_csv(self):
        """Callback for import from csv procedure"""
        self.presenter.handle_import_csv()


    def _cb_edit_device(self):
        """Edit device callback method"""
        self.device_win = DeviceWinManager.get_device_window(self.presenter,
                                                             self.presenter.handle_get_active_device())
        self.device_win.focus()

    def _cb_edit_if(self):
        """Add if callback method"""
        # TODO : replace stub with actual data from DB
        self.if_win = IfWinManager.get_if_window(data_types.stub_if_data)
        self.if_win.focus()

    def _cb_add_if(self):
        """Add if callback method"""
        selected_device = self.presenter.handle_get_active_device()
        if_data = data_types.default_if_data
        # inherit device_id from the selected device
        if_data.device_id = selected_device.device_id
        if selected_device.device_id not in BANNED_DEVICE_LIST:
            self.if_win = IfWinManager.get_if_window(self.presenter, if_data)
            self.if_win.focus()
        else:
            # cannot add if for selected device
            can_not_add_if_dialog = ttk.dialogs.dialogs.Messagebox.show_warning(
                message=WRONG_DEVICE_TEXT.format(selected_device.device_name),
                title=WRONG_DEVICE_TITLE.format(selected_device.device_name),
                parent=self,
                alert=True
                )

    def _cb_rem_if(self):
        """Remove if callback method"""
        # check if selected_list is not empty
        self.presenter.handle_delete_if()
        self.presenter.handle_trigger_update_if_list()
        # TODO: else display message - IF deleted ?

    def _cb_exit(self):
        """Exit app callback method"""
        self.destroy()

    def update_device_list(self):
        """Callback the presenter handle and update the list widget"""
        device_data = self.presenter.handle_get_list_data()
        self.lst_device.delete(0, tk.END)
        for data in device_data:
            self.lst_device.insert(*data)
        self.lst_device.selection_set(0)

    def _cb_dev_lst_select(self, event):
        """"Callback method for element selection in device list

        when device is selected from device list, calls presenter to update the
        coresponding if list and DeviceData obj for Delete / Edit Device window
        """

        selection = event.widget.curselection()
        if selection:
            # callback presenter to update active device in model
            selected_dev_id = self.presenter.handle_get_device_id(self.lst_device.get(selection[0]))
            self.presenter.handle_update_active_device(selected_dev_id)
            active_device = self.presenter.handle_get_active_device()
            self.txt_device_desc.delete(1.0, tk.END)
            self.txt_device_desc.insert(tk.END, active_device.device_desc)

            # update interface list
            self.fill_if_table(active_device)

    def fill_if_table(self, active_device):
        """ Update if list object with new data

        Update is done based on active device selected in Device list
        and is filtered for All devices option
        """

        if active_device.device_id in BANNED_DEVICE_LIST:
            # All devices option selected in gui
            if_list = self.presenter.handle_get_all_if()
        else:
            # callback presenter to get if list for curently selected device
            if_list = self.presenter.handle_get_if_for_device(active_device)
        self.tbl_list_if.build_table_data(coldata=data_types.COLDATA, rowdata=if_list)

    def cb_tableview_if_select(self, event):
        """Callback method when one or multiple elements are selected in tableview"""

        selected_rows = self.tbl_list_if.get_rows(selected=True)
        selected_if_list = []
        for row in selected_rows:
            try:
                dev_id= self.presenter.handle_get_device_id(row.values[0])
            except data_types.DeviceNameNotFoundError as error:
                # TODO:show message dialog
                pass
            else:
                rev_lookup = {v: k for k, v in data_types.IF_TYPE.items()}
                if_type_id = rev_lookup.get(row.values[3])
                selected_if = data_types.InterfaceData(
                        device_id=dev_id,
                        ip=row.values[1],
                        mac=row.values[2],
                        if_type=if_type_id
                    )
                selected_if_list.append(selected_if)
        self.presenter.handle_update_selected_if_list(selected_if_list)


class WindowAddDevice(ttk.Toplevel):
    """Class implements add device window"""

    def __init__(self,
                 presenter=None,
                 win_title=WINDOW_ADD_DEVICE_TITLE,
                 device_data=data_types.default_device_data):
        """Create add device GUI frame

        win_title   = window title
        device_data = optional object containing Device name + device description
                      is used only for editing existing device

        """
        super().__init__()
        self.title(win_title)
        self.geometry(WINDOW_ADD_DEVICE_SIZE)
        # disable x close main window button
        self.protocol("WM_DELETE_WINDOW", disable_event)
        self.resizable(False, False)
        self.presenter = presenter
        self._device_data = device_data
        self.create_add_device_gui()

    def create_add_device_gui(self):
        """Create add device window"""
        frm_device_name = ttk.Frame(self)
        lbl_device_name = ttk.Label(frm_device_name, text="Device name:", width=20)
        lbl_device_name.pack(side="left", expand=True, fill="x", anchor="w")

        validate_device_name = self.register(self.check_device_name)
        self._device_name = tk.StringVar(value=self._device_data.device_name)
        ent_device_name = ttk.Entry(frm_device_name,
                                    validate="focus",
                                    validatecommand=(validate_device_name, '%P'),
                                    textvariable=self._device_name,
                                    width=20)
        ent_device_name.focus()
        ent_device_name.pack(side="top", expand=True, fill="x")

        frm_device_desc = ttk.Frame(self)
        lbl_device_desc = ttk.Label(frm_device_desc, text="Description:", width=20)
        lbl_device_desc.pack(side="top", expand=True, fill="x")
        self._txt_device_desc = ScrolledText(frm_device_desc, autohide=True, height=5)
        self._txt_device_desc.insert("1.0", self._device_data.device_desc)
        self._txt_device_desc.pack()

        frm_buttons = ttk.Frame(self)
        btn_save_dev = ttk.Button(master=frm_buttons,
                                  text="Save",
                                  command=self._cb_device_save,
                                  bootstyle="primary")
        btn_clear_dev = ttk.Button(master=frm_buttons,
                                   text="Clear",
                                   width=5,
                                   command=self._cb_device_clear,
                                   bootstyle="primary")
        btn_close_dev = ttk.Button(master=frm_buttons,
                                   text="Close",
                                   width=5,
                                   command=self._cb_device_close,
                                   bootstyle="primary")
        btn_save_dev.pack(side="left", padx=5, pady=5, anchor="w")
        btn_clear_dev.pack(side="left", padx=5, pady=5, anchor="w")
        btn_close_dev.pack(side="left", padx=5, pady=5, anchor="w")

        frm_device_name.pack(padx=5, pady=5)
        frm_device_desc.pack(padx=5, pady=5)
        frm_buttons.pack(padx=5, pady=5)

    def _cb_device_save(self):
        """Callback method to save device data

        Check if device_name already exist, if not add new device...
        otherwise update existing device
        """
        target_name = self._device_name.get().capitalize()
        dev_present = self.presenter.handle_check_device(target_name)
        dev_data = data_types.DeviceData(self._device_data.device_id,
                                         target_name,
                                         self._txt_device_desc.get("1.0", tk.END))
        # TODO: save when device already present
        # if dev_present and self.check_device_name:
        #     # dev is present, proceed with update data
        #     self.presenter.handle_update_device(dev_data)
        # else:
        #     # add new device
        #     self.presenter.handle_save_device_data(dev_data)
        #     self._cb_device_close()
        if self.check_device_name(self._device_name.get()):
            #  add new device
            self.presenter.handle_save_device_data(dev_data)
            self._cb_device_close()

    def _cb_device_close(self):
        """Callback method to close window"""
        DeviceWinManager.destroy_device_edit_window()
        self.presenter.handle_trigger_update_dev_list()

    def _cb_device_clear(self):
        """Callback method to clear IO fields"""

        self._device_name.set("")
        self._device_desc = ""
        self._txt_device_desc.delete("1.0", tk.END)

    @staticmethod
    def check_device_name(dev_name):
        """Validate device name
        Rules:
            -not empty
            -alphanumeric [0..9][aA..ZA]
        """
        valid_pattern = r"^[a-zA-Z0-9]+$"
        return bool(re.match(valid_pattern, dev_name))


class WindowAddInterface(ttk.Toplevel):
    """Class implements add interface window"""

    def __init__(self,
                 presenter=None,
                 win_title=WINDOW_ADD_INTERFACE_TITLE,
                 if_data=data_types.default_if_data):
        """Create entire GUI frame

        win_tytle   = window title
        if_data     = optional obj containing IP, MAC, type
                      is used only for editing existing if

        """
        super().__init__()
        self.title(win_title)
        self.geometry(WINDOW_ADD_INTERFACE_SIZE)
        self.resizable(False, False)
        # disable x close main window button
        self.protocol("WM_DELETE_WINDOW", disable_event)
        self.presenter = presenter
        self._if_data = if_data
        self.create_add_interface_gui()

    def create_add_interface_gui(self):
        """Create add interface window"""
        # register validation _callback
        validate_ip_address = self.register(self.check_ip_address)
        validate_mac_address = self.register(self.check_mac_address)

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
        btn_save_if = ttk.Button(master=frm_buttons,
                                 text="Save",
                                 command=self._cb_if_save,
                                 bootstyle="primary")
        btn_clear_if = ttk.Button(master=frm_buttons,
                                  text="Clear",
                                  width=5,
                                  command=self._cb_if_clear,
                                  bootstyle="primary")
        btn_close_if = ttk.Button(master=frm_buttons,
                                  text="Close",
                                  width=5,
                                  command=self._cb_if_close,
                                  bootstyle="primary")
        btn_save_if.pack(side="left", padx=5, pady=5, anchor="w")
        btn_clear_if.pack(side="left", padx=5, pady=5, anchor="w")
        btn_close_if.pack(side="left", padx=5, pady=5, anchor="w")

        frm_ip.pack(padx=5, pady=5)
        frm_mac.pack(padx=5, pady=5)
        frm_type.pack(padx=5, pady=5)
        frm_buttons.pack(padx=5, pady=5)

    def _cb_if_save(self):
        """Callback method to save interface"""
        input_valid = self.check_ip_address(self._ip_name.get()) \
            and self.check_mac_address(self._mac_name.get())
        if_data = data_types.InterfaceData(if_id=0,
                                           device_id=self._if_data.device_id,
                                           ip=self._ip_name.get(),
                                           mac=self._mac_name.get(),
                                           if_type=self._type_name.get())
        if input_valid:
            self.presenter.handle_save_if_data(if_data)
            self.presenter.handle_trigger_update_if_list()
            self._cb_if_close()

    def _cb_if_close(self):
        """Callback method to close window"""
        IfWinManager.destroy_if_edit_window()
        self.presenter.handle_trigger_update_if_list()

    def _cb_if_clear(self):
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
    def get_device_window(presenter, dev_data):
        """Returns a device edit window """
        if not DeviceWinManager._device_edit_window:
            DeviceWinManager._device_edit_window = WindowAddDevice(presenter=presenter,
                                                                   device_data=dev_data)
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
    def get_if_window(presenter, if_data):
        """Returns a device edit window """
        if not IfWinManager._if_edit_window:
            IfWinManager._if_edit_window = WindowAddInterface(presenter=presenter,
                                                              if_data=if_data)
        return IfWinManager._if_edit_window

    @staticmethod
    def destroy_if_edit_window():
        """Destroys the window object """
        if IfWinManager._if_edit_window:
            IfWinManager._if_edit_window.destroy()
        IfWinManager._if_edit_window = None

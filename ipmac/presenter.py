class Presenter:
    """Presenter class """

    def __init__(self, view):
        self.view = view

    def run(self):
        """Run method of Presenter"""
        self.view.create_main_gui()
        self.view.mainloop()

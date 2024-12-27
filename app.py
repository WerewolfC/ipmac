"""IPMac app - IP/MAC binding app"""
# from ipmac.gui import Gui
from ipmac.presenter import Presenter


def main():
    """Main app function"""
    # model = Model()
    # view = Gui()
    presenter = Presenter()
    presenter.run()


if __name__ == '__main__':
    main()

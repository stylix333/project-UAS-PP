from gui import KizunaGUI
from logic import KizunaLogic

def main():
    logic = KizunaLogic()
    app = KizunaGUI(logic)
    app.run()

if __name__ == "__main__":
    main()

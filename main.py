from logic import KizunaApp
from gui import KizunaGUI


def main():
    # Menginisialisasi data & logika bisnis (tanpa tkinter)
    app = KizunaApp()

    # Menginisialisasi GUI, menyambungkannya dengan data/logika di atas
    gui = KizunaGUI(app)

    # Menjalankan tampilan login lalu loop utama Tkinter agar jendela tetap terbuka
    gui.run()


if __name__ == "__main__":
    main()

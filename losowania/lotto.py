import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtGui import QFont
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Lotto - kupony")
        self.setFixedHeight(200)
        self.setFixedWidth(500)

        button = QPushButton("Zapisz kupon z ostatniego losowania")
        button.setFont(QFont('Times', 18))
        button.setStyleSheet("QPushButton"
                             "{"
                             "background-color : lightgray;"
                             "}"
                             "QPushButton::pressed"
                             "{"
                             "background-color : gray;"
                             "}"
                             )
        button.setFixedHeight(100)
        button.setFixedWidth(500)
        button.clicked.connect(save_ticket)
        self.setCentralWidget(button)


def get_ticket() -> dict:  # zwraca ostatnie losowanie lotto w postaci slownika gdzie:
    # key - dzien losowania
    # value  - wynik losowania
    req = requests.request("GET", "http://serwis.mobilotto.pl/mapi_v6/index.php?json=getGames")
    res = req.json()

    ticket = res['Lotto']['numerki']
    full_date = res['Lotto']['data_losowania']
    day = full_date.split(" ")[0].split("-")  # wydobycie samej daty bez godziny i rozdzielenie po myslnikach
    day_rev = ''.join(i + "." for i in day[::-1]).rstrip(
        ".")  # przekonwertowanie daty z listy do formatu ddmmyyyy i separacja po kropce
    list_of_numbers = ticket.split(",")
    list_of_numbers_int = [int(i) for i in list_of_numbers]  # zamiana numerkow losowania ze stringow na int
    list_of_numbers_int.sort()
    draw_dict = {day_rev: list_of_numbers_int}
    return draw_dict


def save_ticket():  # zamienia slownik z wynikami losowania na stringa i zapisuje do pliku wyniki.txt
    with open("wyniki.txt", 'r+', encoding='utf-8') as file:
        data = str(get_ticket())
        lines = file.readlines()

        if len(lines) == 0:  # zabezpieczenie przed odczytem linii z pustego pliku
            file.write(data + "\n")
            file.close()
            print(f"Kupon {get_ticket()} został zapisany")
        else:
            if lines[-1].strip() == str(data):  # sprawdzenie czy dzisiejsze losowanie zostalo juz zapisane
                print(f"Kupon {get_ticket()} już istnieje w ewidencji")
            else:
                file.write(data + "\n")
                file.close()
                print(f"Kupon {get_ticket()} został zapisany")


def main():

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()

    # save_ticket()


if __name__ == '__main__':
    main()

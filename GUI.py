import sys
import json
from server import Server
from client import Client


from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QApplication, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel


class Button(QPushButton):
    def __init__(self, text):
        super().__init__(text)




class RegistrationStateWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.__registration_state_init()

    def __registration_state_init(self):
        self.__registration_state_layout = QVBoxLayout()

        self.__login_field = QLineEdit()
        self.__pass_field = QLineEdit()

        self.__register_button = Button('Зарегистрироваться')
        self.__already_have_accout_button = Button('Уже есть аккаунт?')

        self.__register_button.setFixedWidth(150)


        self.__registration_state_layout.addWidget(self.__login_field)
        self.__registration_state_layout.addWidget(self.__pass_field)

        self.__registration_state_layout.addWidget(self.__register_button)
        self.__registration_state_layout.addWidget(self.__already_have_accout_button)

        self.setLayout(self.__registration_state_layout)

    def get_buttons(self):
        return self.__register_button, self.__already_have_accout_button

    def get_fields(self):
        return self.__login_field, self.__pass_field


class AuthorizationStateWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.__authorizahion_state_init()


    def __authorizahion_state_init(self):
        self.__authorizahion_state_layout = QVBoxLayout()

        self.__login_field = QLineEdit()
        self.__pass_field = QLineEdit()

        self.__enter_button = Button('Войти')
        self.__no_accout_button = Button('Нет аккаунта?')

        self.__authorizahion_state_layout.addWidget(self.__login_field)
        self.__authorizahion_state_layout.addWidget(self.__pass_field)

        self.__authorizahion_state_layout.addWidget(self.__enter_button)
        self.__authorizahion_state_layout.addWidget(self.__no_accout_button)

        self.setLayout(self.__authorizahion_state_layout)

    def get_buttons(self):
        return self.__enter_button, self.__no_accout_button

    def get_fields(self):
        return self.__login_field, self.__pass_field


class MainWindow(QMainWindow):
    """
    MACHINE_STATES = {
        0: 'registration',
        1: 'authorizahion',
        2: 'registration error',
        3: 'authorizahion error',
        4: 'entered'
    }
    """

    def __init__(self):
        """
        Конструктор класса
        """
        super().__init__()
        self.setFixedSize(600, 600)


        self.__client = Client('127.0.0.1', 12345)
        self.__client.connect()

        # Инициализация виджетов для каждой машины состояния
        self.__registration_state = self.__get_registration_state()
        self.__authorizahion_state = self.__get_registration_state()

        self.setWindowTitle('Регистрация')
        self.setCentralWidget(self.__registration_state)


    def __register(self):
        login_field, password_field = self.__registration_state.get_fields()

        login = login_field.text()
        password = password_field.text()

        message = f'REGISTER:{login}:{password}'
        self.__client.send_message(message)
        received_message = self.__client.recv_message

        print(received_message)

    def __login(self):
        login_field, password_field = self.__authorizahion_state.get_fields()

        login = login_field.text()
        password = password_field.text()

        message = f'LOGIN:{login}:{password}'
        self.__client.send_message(message)
        received_message = self.__client.recv_message
        print(received_message)

    def __get_registration_state(self):
        registration_state = RegistrationStateWidget()
        register_button, already_have_accout_button = registration_state.get_buttons()

        register_button.clicked.connect(self.__register)
        already_have_accout_button.clicked.connect(self.__change_machine_state_to_authorization)
        return registration_state

    def __get_authorization_state(self):
        authorizahion_state = AuthorizationStateWidget()
        enter_button, no_accout_button = authorizahion_state.get_buttons()

        enter_button.clicked.connect(self.__login)
        no_accout_button.clicked.connect(self.__change_machine_state_to_registration)
        return authorizahion_state

    def __change_machine_state_to_registration(self):
        self.__registration_state = self.__get_registration_state()
        self.setWindowTitle('Регистрация')
        self.setCentralWidget(self.__registration_state)

    def __change_machine_state_to_authorization(self):
        self.__authorizahion_state = self.__get_authorization_state()
        self.setWindowTitle('Авторизация')
        self.setCentralWidget(self.__authorizahion_state)

    def closeEvent(self, event):
        self.__client.disconnect()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
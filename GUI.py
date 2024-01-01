import sys
import json
from server import Server
from client import Client

from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow, QWidget, QPushButton, QApplication, QVBoxLayout, QHBoxLayout, QLineEdit, QLabel, QLayout


class Label(QLabel):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            color: #fff;
            font-size: 22px;
            font-weight: bold;
        """)


class Button(QPushButton):
    def __init__(self, text):
        super().__init__(text)
        self.setStyleSheet("""
            width: 145px;
            margin: 20px auto;
            padding: 20px 40px;
            color: #dbdbdb;
            background-color: #0b141e;
            border-radius: 28px;
            font-size: 14px;
            font-weight: bold;
        """)


class TextField(QLineEdit):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            border: 2px solid gray;
            width: 145px;
            margin: 20px 66px;
            padding: 20px 40px;
            color: #dbdbdb;
            border-radius: 28px;
            font-size: 20px;
            font-weight: bold;
        """)


class RegistrationStateWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.__registration_state_init()

    def __registration_state_init(self):
        self.__registration_state_layout = QVBoxLayout()

        self.login_field = TextField()
        self.login_field.setPlaceholderText('Login')
        self.login_field.setAlignment(QtCore.Qt.AlignCenter)
        self.pass_field = TextField()
        self.pass_field.setPlaceholderText('Password')
        self.pass_field.setAlignment(QtCore.Qt.AlignCenter)

        self.register_button = Button('Sign up')
        self.already_have_accout_button = Button('Enter account')

        self.error_text = Label()

        self.__registration_state_layout.addWidget(self.login_field)
        self.__registration_state_layout.addWidget(self.pass_field)

        self.__registration_state_layout.addWidget(self.error_text, alignment=QtCore.Qt.AlignCenter)
        self.__registration_state_layout.addWidget(self.register_button, alignment=QtCore.Qt.AlignCenter)
        self.__registration_state_layout.addWidget(self.already_have_accout_button, alignment=QtCore.Qt.AlignCenter)

        self.setLayout(self.__registration_state_layout)



class AuthorizationStateWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.__authorizahion_state_init()


    def __authorizahion_state_init(self):
        self.__authorizahion_state_layout = QVBoxLayout()

        self.login_field = TextField()
        self.login_field.setPlaceholderText('Login')
        self.login_field.setAlignment(QtCore.Qt.AlignCenter)
        self.pass_field = TextField()
        self.pass_field.setPlaceholderText('Password')
        self.pass_field.setAlignment(QtCore.Qt.AlignCenter)

        self.enter_button = Button('Sign in')
        self.no_accout_button = Button('Create Accout')

        self.error_text = Label()

        self.__authorizahion_state_layout.addWidget(self.login_field)
        self.__authorizahion_state_layout.addWidget(self.pass_field)

        self.__authorizahion_state_layout.addWidget(self.error_text, alignment=QtCore.Qt.AlignCenter)
        self.__authorizahion_state_layout.addWidget(self.enter_button, alignment=QtCore.Qt.AlignCenter)
        self.__authorizahion_state_layout.addWidget(self.no_accout_button, alignment=QtCore.Qt.AlignCenter)

        self.setLayout(self.__authorizahion_state_layout)


class UsingStateWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__using_state_init()

    def __using_state_init(self):
        pass


class MainWindow(QMainWindow):
    def __init__(self):
        """
        Конструктор класса
        """
        super().__init__()

        self.setBaseSize(500, 450)
        self.setStyleSheet("""
            background-color: #06090d;
        """)

        self.__client = Client('127.0.0.1', 12345)
        self.__client.connect()

        # Инициализация виджетов для каждой машины состояния
        self.__registration_state = self.__get_registration_state()
        self.__authorizahion_state = self.__get_registration_state()
        self.__using_state = self.__get_using_state()

        self.setWindowTitle('Sign up')

        self.setCentralWidget(self.__registration_state)

        if not self.__client.is_connected():
            self.__registration_state.error_text.setText(self.__client.recv_message)

    def __register(self):
        login = self.__registration_state.login_field.text()
        password = self.__registration_state.pass_field.text()

        if len(login) == 0 or len(password) == 0:
            self.__registration_state.login_field.setPlaceholderText('Заполните поле')
            self.__registration_state.pass_field.setPlaceholderText('Заполните поле')
        else:
            message = f'REGISTER\t{login}\t{password}'
            self.__client.send_message(message)
            received_message = self.__client.recv_message

            self.__registration_state.error_text.setText(received_message)

    def __login(self):
        login = self.__authorizahion_state.login_field.text()
        password = self.__authorizahion_state.pass_field.text()

        if len(login) == 0 or len(password) == 0:
            self.__authorizahion_state.login_field.setPlaceholderText('Заполните поле')
            self.__authorizahion_state.pass_field.setPlaceholderText('Заполните поле')
        else:
            message = f'LOGIN\t{login}\t{password}'
            self.__client.send_message(message)
            received_message = self.__client.recv_message

            self.__authorizahion_state.error_text.setText(received_message)

    def __get_registration_state(self):
        registration_state = RegistrationStateWidget()
        registration_state.register_button.clicked.connect(self.__register)
        registration_state.already_have_accout_button.clicked.connect(self.__change_machine_state_to_authorization)

        return registration_state

    def __get_authorization_state(self):
        authorizahion_state = AuthorizationStateWidget()
        authorizahion_state.enter_button.clicked.connect(self.__login)
        authorizahion_state.no_accout_button.clicked.connect(self.__change_machine_state_to_registration)
        return authorizahion_state

    def __get_using_state(self):
        using_state = UsingStateWidget()
        return using_state

    def __change_machine_state_to_registration(self):
        self.__registration_state = self.__get_registration_state()
        self.setWindowTitle('Sign up')
        self.setCentralWidget(self.__registration_state)

    def __change_machine_state_to_authorization(self):
        self.__authorizahion_state = self.__get_authorization_state()
        self.setWindowTitle('Sign in')
        self.setCentralWidget(self.__authorizahion_state)

    def __change_machine_state_to_using(self):
        self.__using_state = self.__get_using_state()
        self.setWindowTitle('Messenger')
        self.setCentralWidget(self.__using_state)

    def closeEvent(self, event):
        if self.__client.is_connected():
            self.__client.disconnect()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())
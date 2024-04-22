# !/usr/bin/python3
# -*- coding:utf-8 -*-
"""
@author: JHC000abc@gmail.com
@file: demo2.py
@time: 2023/11/22 16:59
@desc:

"""
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLineEdit, QPushButton, \
    QHBoxLayout
from PyQt5.QtGui import QColor


class ChatWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chat Window")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        self.chat_list = QListWidget()
        self.chat_list.setWordWrap(True)
        layout.addWidget(self.chat_list)

        self.input_box = QLineEdit()
        self.send_button = QPushButton("Send")
        self.send_button.clicked.connect(self.send_message)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.input_box)
        input_layout.addWidget(self.send_button)

        layout.addLayout(input_layout)

        self.setLayout(layout)

    def add_message(self, sender, message):
        item = QListWidgetItem(f"{sender}: {message}")
        item.setTextAlignment(0 if sender == 'Me' else 2)
        item.setBackground(QColor("#DCF8C6") if sender == 'Me' else QColor("#FFFFFF"))

        self.chat_list.addItem(item)

    def send_message(self):
        message = self.input_box.text()
        if message:
            self.add_message("Me", message)
            self.input_box.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()

    window.add_message("Friend", "Hello!")
    window.add_message("Me", "Hi there!")

    sys.exit(app.exec_())

import sys
import requests
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, \
    QMessageBox, QComboBox
from PyQt5.QtCore import Qt


class CurrencyConverter(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Currency Converter")
        self.setGeometry(100, 100, 300, 100)

        # Creating and styling the title label
        self.app_title = QLabel("Currency Converter")
        self.app_title.setAlignment(Qt.AlignCenter)
        font = QFont("arial", 14)
        self.app_title.setFont(font)

        # Creating widgets for user input
        self.amount_entry = QLineEdit()
        self.amount_entry.setPlaceholderText("Enter The Amount to Convert")

        self.from_currency_combo = QComboBox()
        self.to_currency_combo = QComboBox()

        # Label to display the conversion result
        self.result_label = QLabel("Result: ")
        self.result_label.setFont(QFont("Arial", 11))

        # Button to trigger the conversion
        self.convert_button = QPushButton("Convert")
        self.convert_button.setFont(QFont("Arial", 11))

        # Fetching currency data from API
        response = requests.get('https://v6.exchangerate-api.com/v6/97bf863157633c0d1bf81027/latest/USD')
        data = response.json()

        # Populating the currency comboboxes with fetched data
        for currency in data['conversion_rates']:
            self.from_currency_combo.addItem(currency)
            self.to_currency_combo.addItem(currency)

        # Creating layouts to organize widgets
        layout = QVBoxLayout()
        combos_layout = QHBoxLayout()
        result_layout = QHBoxLayout()
        convert_button_layout = QHBoxLayout()

        # Adding widgets to layouts
        layout.addWidget(self.app_title)
        layout.addWidget(self.amount_entry)

        combos_layout.addWidget(self.from_currency_combo)
        combos_layout.addWidget(self.to_currency_combo)

        result_layout.addWidget(self.result_label)

        convert_button_layout.addWidget(self.convert_button)

        layout.addLayout(combos_layout)
        layout.addLayout(result_layout)
        layout.addLayout(convert_button_layout)

        # Connecting the convert button to the conversion function
        self.convert_button.clicked.connect(self.convert)

        self.setLayout(layout)

    def convert(self):
        # Getting user input
        from_text = self.from_currency_combo.currentText().upper()
        to_text = self.to_currency_combo.currentText().upper()
        amount = self.amount_entry.text()

        # Handling empty fields
        if not amount or not from_text or not to_text:
            QMessageBox.warning(self, "Error", "Please fill all fields")
            return

        try:
            amount = float(amount)  # Converting amount to float
        except ValueError:
            QMessageBox.warning(self, "Error", "Please enter a valid number for the amount")
            return
        try:
            # Fetching exchange rate data
            response = requests.get(f'https://v6.exchangerate-api.com/v6/97bf863157633c0d1bf81027/latest/{from_text}')
            data = response.json()
            exchange_rate = data['conversion_rates'][to_text]
            result = exchange_rate * amount
            self.result_label.setText(f"{result:.2f} {to_text}")  # Displaying the result
        except Exception as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {str(e)}")


def main():
    app = QApplication(sys.argv)
    currency_converter = CurrencyConverter()
    currency_converter.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

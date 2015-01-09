#! usr/bin/env/ python 3.4

__version__ = '1.0.0'

import sys

from os import urandom
from string import ascii_lowercase, ascii_uppercase, digits, punctuation
from threading import Timer

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


def generate_password(pass_length):
    """Generate your random password based on pass_length
    
    pass_length -> str
    """
    
    phrase = ""  # this object must be a str before being returned
    DIGITS = list(digits)
    LOWER_CASE = list(ascii_lowercase)
    UPPER_CASE = list(ascii_uppercase)
    SPECIAL_CHARACTERS = list(punctuation)

    random_bytes = list(urandom(pass_length))           # convert bytes to decimal equivalent
    character_list = [chr(i) for i in random_bytes]     # convert decimal equivalent to character

    for i in character_list: phrase += i
    print(random_bytes)

    return phrase

def test_generate(pass_length):
    """TEST: Generate random characters from a-z, A-Z, 0-9, and special characters

    pass_length -> tuple
    This will return test_phrase, test_lowercase, test_uppercase, test_punctuation and test_numbers
    """
    test_phrase = ""
    test_numbers = 0
    test_lowercase = 0
    test_uppercase = 0
    test_punctuation = 0
    characterSet = digits + ascii_lowercase + ascii_uppercase + punctuation
    while pass_length:                          # number of loops based on user input
        singleCHAR = list(urandom(1))           # generate 1 byte of random char and convert to its decimal equivalent
        candidateCHAR = chr(singleCHAR[0])
        if candidateCHAR in characterSet:       # let python find a random character in characterSet
            test_phrase += candidateCHAR        # append the valid character in the new given container
            pass_length -= 1                    # decrease the loop by 1 for a valid match
            if candidateCHAR in digits:
                test_numbers += 1
            elif candidateCHAR in ascii_lowercase:
                test_lowercase += 1
            elif candidateCHAR in ascii_uppercase:
                test_uppercase += 1
            elif candidateCHAR in punctuation:
                test_punctuation += 1
            else:
                print("For an unknown reason, no character was counted.")

    return test_phrase, test_lowercase, test_uppercase, test_punctuation, test_numbers


class RiddlerGUI(QDialog):
    """Main class that will create the GUI for Riddler app"""
    
    def __init__(self, parent=None):
        """create the form"""
        
        super(RiddlerGUI, self).__init__(parent)
        #self.clear_timer = None
        self._widgets()
        self._layout()
        self._properties()
        self._connections()

    def _properties(self):
        """Set properties for all QWidgets"""
        
        self.setWindowTitle('Riddler {} | Password Generator'.format(__version__))
        # self.resize(600, 250)  # width, height
        self.lenSBox.setValue(25)   # set the default value for the self.lenSBox widget
        self.resultLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)  # make resultLabel selectable my mouse
        self.setLayout(self.layout_wrapper)
    
    def _layout(self):
        """Set layout for all QWidgets and layouts"""
        
        self.vertical_left = QVBoxLayout()
        self.vertical_left.addWidget(self.riddlerLabel)
        self.statsGBoxV = QVBoxLayout()
        self.statsGBoxV.addWidget(self.lengthLabel)
        self.statsGBoxV.addWidget(self.brutalityLabel)
        self.statsGBoxV.addWidget(self.lowerLabel)
        self.statsGBoxV.addWidget(self.upperLabel)
        self.statsGBoxV.addWidget(self.specialLabel)
        self.statsGBoxV.addWidget(self.numbersLabel)
        self.statsGBoxV.addWidget(self.dateLabel)
        self.statsGBoxV.addWidget(self.remarksLabel)
        self.statsGBox.setLayout(self.statsGBoxV)
        self.vertical_left.addWidget(self.statsGBox)
        
        self.vertical_right = QVBoxLayout()
        self.h_lenspin = QHBoxLayout()
        self.h_lenspin.addWidget(self.lengthSpinLabel)
        self.h_lenspin.addWidget(self.lenSBox)
        self.h_lenspin.addWidget(self.cipherComboBox)
        self.vertical_right.addLayout(self.h_lenspin)
        self.vertical_right.addWidget(self.generateButton)
        self.vertical_right.addWidget(self.closeButton)
        self.vertical_right.addStretch(1)
        
        self.horizontal = QHBoxLayout()
        self.horizontal.addLayout(self.vertical_left)
        self.horizontal.addWidget(self.v_separator)
        self.horizontal.addLayout(self.vertical_right)
                
        self.horizontal_bottom = QHBoxLayout()
        self.horizontal_bottom.addWidget(self.resultLabel)
        self.horizontal_bottom.addStretch(1)
        
        self.layout_wrapper = QVBoxLayout()
        self.layout_wrapper.addLayout(self.horizontal)
        self.layout_wrapper.addLayout(self.horizontal_bottom)
    
    def _connections(self):
        """Signals and slots here"""

        self.generateButton.clicked.connect(self.on_generateButton_clicked)
        self.closeButton.clicked.connect(self.on_closeButton_clicked)

    def _widgets(self):
        """Add new QWidgets inside this method"""
        
        self.riddlerLabel = QLabel("Riddler - January 2014")
        self.statsGBox = QGroupBox("Password Statistics")
        self.lengthLabel = QLabel("Length\t\t: -")
        self.brutalityLabel = QLabel("Brutality\t\t: -")
        self.lowerLabel = QLabel("Lowercase\t: -")
        self.upperLabel = QLabel("Uppercase\t: -")
        self.specialLabel = QLabel("Special Characters\t: -")
        self.numbersLabel = QLabel("Numbers\t\t: -")
        self.dateLabel = QLabel("Date/Time\t: -")
        self.remarksLabel = QLabel("Remarks\t\t: None")
        self.v_separator = QFrame()
        self.v_separator.setFrameShape(self.v_separator.VLine)
        self.v_separator.setFrameShadow(self.v_separator.Sunken)
        self.lengthSpinLabel = QLabel("Length:")
        self.lenSBox = QSpinBox()
        self.spacer = QSpacerItem(1, 1, QSizePolicy.Fixed, QSizePolicy.Preferred)
        self.generateButton = QPushButton("G&enerate")
        self.closeButton = QPushButton("&Close")
        self.resultLabel = QLabel("Ready")
        self.clear_timer = Timer(5, self.clear_resultLabel)
        self.clear_timer.start()
        self.cipherComboBox = QComboBox()
        self.cipherComboBox.insertItem(0, "Ceasar")
        self.cipherComboBox.insertItem(1, "One-Time Pad")
        self.cipherComboBox.insertItem(2, "Vigenere")


    def clear_resultLabel(self):

        self.resultLabel.clear()

    def on_generateButton_clicked(self):
        """handle clicked event for Generate button"""

        self.clear_timer.cancel()
        raw_len = self.lenSBox.value()
        worth = test_generate(raw_len)  # get length and generate password here
        self.lengthLabel.setText("Length\t\t: %s" % raw_len)
        self.brutalityLabel.setText("Brutality\t\t: %s" % "Weakling")
        self.lowerLabel.setText("Lowercase\t: %s" % worth[1])
        self.upperLabel.setText("Uppercase\t: %s" % worth[2])
        self.specialLabel.setText("Special Characters\t: %s" % worth[3])
        self.numbersLabel.setText("Numbers\t\t: %s" % worth[4])

        self.resultLabel.setText(worth[0])

    def on_closeButton_clicked(self):
        """Handle clicked event for Close button"""

        self.clear_timer.cancel()   # stop timer if the user eventually clicked the close button
        sys.exit(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    riddler_gui = RiddlerGUI()
    riddler_gui.show()
    app.exec_()

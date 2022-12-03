#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Validator Editor """

__author__     = 'Lars Schneckenburger'
__copyright__  = 'Copyright 2022 Storm Hamsters'
__credits__    = 'Anja Edelmann, Ricky Raths, Lars Schneckenburger, Salah Xaaji'
__license__    = 'GPL'
__version__    = '1.0'
__created__    = '19.11.2022'
__maintainer__ = 'Lars Schneckenburger'
__email__      = 'schnela@students.zhaw.ch'
__status__     = 'done'

import string
from Editor import Editor


class Validator:

    def __init__(self, commands, commands_with_parameter, commands_adding_text):
        self.valid_commands = commands
        self.valid_commands_with_parameter = commands_with_parameter
        self.valid_commands_adding_text = commands_adding_text

    def input_is_valid(self, command, text_length):
        """
        Checks if the input is valid for further use

        Parameters
        ----------
        command : tuple
            preformatted command from the user
        text_length : int
            Number of paragraphs in the editor

        Returns
        -------
        check : tuple
            Tuple with a boolean result and a result message

        """
        check = (True, "")
        # validate command
        if not self.command_is_valid(command[0]):
            text = "Not a valid command. Please try again."
            check = (False, text)

        elif self.command_needs_parameter(command[0]):
            if not self.paragraph_number_is_valid(command, text_length) \
                and command[1] != False:
                text = "Not a valid parameter. Please try again."
                check = (False, text)
        
            elif not self.format_fix_has_parameter(command):
                text = "Format fix needs parameter bigger than 0"
                check = (False, text)

        return check

    def command_is_valid(self, command):
        """
        Checks if the command is a valid command for the editor

        Parameters
        ----------
        command : str
            preformatted command from the user

        Returns
        -------
        validator : bool
            Result from the validation
        """
        validator = False
        if command in self.valid_commands:
            validator = True
        return validator
    
    def command_needs_parameter(self, command):
        """
        Checks if the command needs a parameter to run

        Parameters
        ----------
        command : str
            preformatted command from the user

        Returns
        -------
        validator : bool
            Result from the validation
        """
        validator = False
        if command in self.valid_commands_with_parameter:
            validator = True
        return validator

    def paragraph_number_is_valid(self, command, text_length):
        """
        Checks if the paragraph number is valid to use

        Parameters
        ----------
        command : tuple
            preformatted command from the user
        text_length : int
            Number of paragraphs in the editor

        Returns
        -------
        check : bool
            Result from the index check
        """
        check = True #by default check is True, unless it's proven False
        commando = command[0]
        parameter = command[1]
        if commando == "FORMAT FIX":
            pass
        elif ((commando not in self.valid_commands_adding_text 
                and parameter > text_length) 
            or (commando in self.valid_commands_adding_text 
                and parameter > text_length + 1) 
            or parameter < 1):
            check = False
        return check
    
    def format_fix_has_parameter(self, command):
        check = True  # by default check is True, unless it's proven False
        if command[0] == "FORMAT FIX" and not command[1]:
            check = False
        return check

    def validate_new_paragraph(self, new_paragraph):
        """
        Validates the input.
        Paragraph can only contain alphanumeric values and specific characters.
        Allowed characters: alphabets, umlaut, digits and the following
        characters: .,:;-!?’()"%@+*[]{}/\&#$

        Parameters
        ----------
        new_paragraph : str
            paragraph to validate

        Returns
        -------
        filtered_paragraph : str
            filtered paragraph

        """
        alphabet      = list(string.ascii_letters)
        numbers       = [str(i) for i in range(0, 10)]
        umlauts       = ["ä", "ö", "ü", "Ä", "Ö", "Ü"]
        character_set = list('.,:;-!?’()"%@+*[]{}/\&#$ ')
        valid_inputs  = alphabet + numbers + umlauts + character_set

        filtered_paragraph = ""
        for character in new_paragraph:
            if character in valid_inputs:
                filtered_paragraph += character

        return filtered_paragraph
    
    def text_is_given(self, text):
        """
        Checks if the text is given with commands that are needing text

        Parameters
        ----------
        text : str
            preformatted command from the user

        Returns
        -------
        validator : bool
            Result from the check if text is given
        """
        validator = True
        if len(text) <= 0:
            validator = False
        return validator


if __name__ == "__main__":
    editor = Editor()
    validator = Validator(editor.commands,
                          editor.commands_with_parameter,
                          editor.commands_adding_text)

    # test valid cases from command_is_valid
    print("\nTest: command_is_valid (valid cases)")
    print(validator.command_is_valid("ADD"))
    print(validator.command_is_valid("DEL"))
    print(validator.command_is_valid("DUMMY"))
    print(validator.command_is_valid("EXIT"))
    print(validator.command_is_valid("FORMAT RAW"))
    print(validator.command_is_valid("FORMAT FIX"))
    print(validator.command_is_valid("INDEX"))
    print(validator.command_is_valid("PRINT"))
    print(validator.command_is_valid("REPLACE"))

    # test invalid cases from command_is_valid
    print("\nTest: command_is_valid (invalid cases)")
    print(validator.command_is_valid("ADDING"))
    print(validator.command_is_valid("DELETE"))
    print(validator.command_is_valid("DUMMIES"))
    print(validator.command_is_valid("EXITT"))
    print(validator.command_is_valid("FORMAT WOW"))
    print(validator.command_is_valid("FORMAT FIX 30"))
    print(validator.command_is_valid("INDICE"))
    print(validator.command_is_valid("PRINTS"))
    print(validator.command_is_valid("REPLACED"))
    print(validator.command_is_valid("adD 3 3 3"))
    print(validator.command_is_valid("add3 2"))
    print(validator.command_is_valid("Delet 3"))
    print(validator.command_is_valid("  del 3   "))
    print(validator.command_is_valid("DUMMY D 3"))
    print(validator.command_is_valid(""))
    print(validator.command_is_valid("e xit 5"))
    print(validator.command_is_valid("format RAW 20"))
    print(validator.command_is_valid("Format_fix 30"))
    print(validator.command_is_valid("iNDEx 5"))

    # test valid cases from input_is_valid
    print("\nTest: input_is_valid (valid cases)")
    print(validator.input_is_valid(("DUMMY", 1), 2))

    # test invalid cases from input_is_valid
    print("\nTest: input_is_valid (invalid cases)")
    print(validator.input_is_valid(("ADD", 5), 2))
    print(validator.input_is_valid(("DUMMY", -1), 2))
    print(validator.input_is_valid(("DEL", 7), 3))
    print(validator.input_is_valid(("DELETE", 1), 3))

    # test valid cases from command_needs_parameter
    print("\nTest: command_needs_parameter (valid cases)")
    print(validator.command_needs_parameter("ADD"))
    print(validator.command_needs_parameter("DUMMY"))
    print(validator.command_needs_parameter("DEL"))
    print(validator.command_needs_parameter("REPLACE"))
    print(validator.command_needs_parameter("FORMAT FIX"))

    # test invalid cases from command_needs_parameter
    print("\nTest: command_needs_parameter (invalid cases)")
    print(validator.command_needs_parameter("EXIT"))
    print(validator.command_needs_parameter("FORMAT RAW"))

    # test valid cases from paragraph_number_is_valid
    print("\nTest: paragraph_number_is_valid (valid cases)")
    print(validator.paragraph_number_is_valid(("ADD", 1), 3))
    print(validator.paragraph_number_is_valid(("ADD", 2), 1))

    # test invalid cases from paragraph_number_is_valid
    print("\nTest: paragraph_number_is_valid (invalid cases)")
    print(validator.paragraph_number_is_valid(("ADD", 74), 30))

    # test valid cases from format_fix_has_parameter
    print("\nTest: format_fix_has_parameter (valid cases)")
    print(validator.format_fix_has_parameter("FORMAT FIX 20"))

    # test invalid cases from format_fix_has_parameter
    print("\nTest: format_fix_has_parameter (invalid cases)")
    print(validator.format_fix_has_parameter("FORMAT FIX"))

    # test valid cases from validate_new_paragraph
    print("\nTest: validate_new_paragraph (valid cases)")
    print(validator.validate_new_paragraph("These are valid symbols:;-!?’()"))

    # test invalid cases from validate_new_paragraph
    print("\nTest: validate_new_paragraph (invalid cases)")
    print(validator.validate_new_paragraph("£"))

    # test valid cases from text_is_given
    print("\nTest: text_is_given (valid cases)")
    print(validator.text_is_given("Test-Text"))
    print(validator.text_is_given("T?’()"))

    # test invalid cases from text_is_given
    print("\nTest: text_is_given (invalid cases)")
    print(validator.text_is_given(""))


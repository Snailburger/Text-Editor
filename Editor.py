#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Editor """

__author__     = 'Lars Schneckenburger'
__copyright__  = 'Copyright 2022 Storm Hamsters'
__credits__    = 'Anja Edelmann, Ricky Raths, Lars Schneckenburger, Salah Xaaji'
__license__    = 'GPL'
__version__    = '1.0'
__created__    = '31.10.2022'
__maintainer__ = 'Lars Schneckenburger'
__email__      = 'schnela@students.zhaw.ch'
__status__     = 'done'

import string


class Editor:

    def __init__(self):
        self.text = []
        # the input text is saved in a list. 
        # each element represents a paragraph.
        self.text_in_format = []
        # second list for the text, where the rules of the format is applied
        self.current_format = ("raw", 0)
        self.dummy = "Lorem ipsum dolor sit amet, consectetur adipiscing " \
                     "elit, sed do eiusmod tempor incididunt ut labore et " \
                     "dolore magna aliqua. Ut enim ad minim veniam, quis " \
                     "nostrud exercitation ullamco laboris nisi ut aliquip " \
                     "ex ea commodo consequat. Duis aute irure dolor in " \
                     "reprehenderit in voluptate velit esse cillum dolore eu " \
                     "fugiat nulla pariatur. Excepteur sint occaecat " \
                     "cupidatat non proident, sunt in culpa qui officia " \
                     "deserunt mollit anim id est laborum."  # dummy text

        self.commands = ["ADD", "DEL", "DUMMY", "EXIT", "FORMAT RAW",
                         "FORMAT FIX", "INDEX", "PRINT", "REPLACE"]
        # list with possible and valid commands for user
        self.commands_with_parameter = ["ADD", "DEL", "DUMMY",
                                        "FORMAT FIX", "REPLACE"]
        
        self.commands_adding_text = ["ADD", "DUMMY"]


    def get_commands(self):
        """
        Get list with valid/possible commands.
        
        Parameters
        ----------
        None.
    
        Returns
        -------
        self.commands : list
            list with valid/possible commands
        """
        return self.commands

    def add_n(self, paragraph, n):
        """
        Method adds a new paragraph. The paragraph is inserted at position n.
        
        Parameters
        ----------
        paragraph : str
        n : int
            position for new paragraph as int
    
        Returns
        -------
        None.
    
        """
        self.text.insert(n-1, paragraph)

    def del_n(self, n):
        """
        Deletes a paragraph. 
    
        Parameters
        ----------
        n : int 
            position of paragraph to be deleted as int
    
        Returns
        -------
        None.
    
        """
        self.text.pop(n-1)

    def dummy_n(self, n):
        """
        Inserts a permanently programmed dummy text.

        Parameters
        ----------
        n : int
            position for new paragraph as int

        Returns
        -------
        None.

        """
        self.text.insert(n-1, self.dummy)

    def format_raw(self):
        """
        Sets the output format to output paragraphs preceded by paragraph
        numbers. This is the default behavior.

        Parameters
        ----------
        None.
    
        Returns
        -------
        None.
    
        """
        self.text_in_format = []
        counter = 1
        for paragraph in self.text:
            self.text_in_format.append((str(counter) + " : " + paragraph))
            counter += 1

    def format_fix(self):
        """
        Sets the output format to output with a maximum column width of b
        characters. The wrapping behavior is as follows:
            - Wrapping is only allowed after a space character.
            - The space after which a break is made does not count towards the
            line length. It will still be printed on the current line, even if
            it may no longer fit on it.
            - If there is no break within the column width after a break, you
            can use the column width, it is allowed to wrap after the column
            width.
    
        Parameters
        ----------
        None.
    
        Returns
        -------
        None.
    
        """
        self.text_in_format = []
        b = self.current_format[1]  # maximum column width
        for paragraph in self.text:
            split_paragraph = paragraph.split()  # get list with all words
            new_word = ""
            column = ""  # is necessary for empty paragraph
            while split_paragraph:
                column = new_word

                while len(column) <= b:
                    if not split_paragraph:
                        break
                    else:
                        new_word = split_paragraph.pop(0)

                    if len(column) == 0:  # first word in column
                        column += new_word
                    else:
                        column += " " + new_word

                if len(new_word) > b:  # word longer than b
                    self.text_in_format.append(new_word[:-(len(new_word) - b)])
                    new_word = new_word[b:]  # rest of the word
                else:
                    self.text_in_format.append(column[:-len(new_word)])
            # handling last word in paragraph
            if column == "":
                self.text_in_format.append(column + "\n")
            elif (len(self.text_in_format[len(self.text_in_format) - 1]) +
                  len(new_word)) > b:
                self.text_in_format.append(new_word+ "\n")
            else:
                self.text_in_format.pop()  # is necessary for empty paragraph
                self.text_in_format.append(column + "\n")

    def change_format(self, new_format, b=0):
        """
        Defines current format.
    
        Parameters
        ----------
        new_format : str
            raw or fix
        b : int
            maximum column width format fix
    
        Returns
        -------
        None.
    
        """
        if new_format == "raw":
            self.current_format = ("raw", b)
        else:
            self.current_format = ("fix", b)

    def index(self):
        """
        Outputs an index (word index) of all terms that occur more than three
        times across all paragraphs. A term starts with a capital letter. The
        index lists the paragraphs where the respective term occurs as a
        comma-separated number sequence.
    
        Parameters
        ----------
        None.
    
        Returns
        -------
        None.
    
        """
        word_index = {}
        alphabet = list(string.ascii_letters)
        # make word index
        counter_paragraph = 1
        for paragraph in self.text:
            split_paragraph = paragraph.split()  # get single words
            for term in split_paragraph:
                if term[0].isupper():  # term starts with a capital letter
                    if term[-1] not in alphabet:
                        # cuts last character if it is a symbol/punctuation
                        term = term[:-1]
                    if term not in word_index:
                        word_index[term] = [counter_paragraph]
                    else:
                        if counter_paragraph in word_index[term]:
                            None
                        else:
                            word_index[term].append(counter_paragraph)
            counter_paragraph += 1
        return word_index

    def get_text_in_format(self):
        """
        Return the text according to the currently set output format.

        Parameters
        ----------
        None.

        Returns
        -------
        self.text_in_format : list
            The list with the paragraphs in the current format

        """
        if len(self.text) <= 0:
            return self.text
        if self.current_format[0] == "raw":
            self.format_raw()
        else:
            self.format_fix()
        return self.text_in_format

    def replace(self, search, replace, n):
        """
        Method replaces a word or text in paragraph n with a new word or text.
        Searching and replacing is done within paragraph n and not across
        paragraph boundaries. 
    
        Parameters
        ----------
        search : str
            "Old" string to be searched and replaced in the paragraph

        replace : str
            "New" string that replaces the "Old" string in the paragraph

        n : int
            Paragraph number of the paragraph that is being searched

        Returns
        -------
        None.
    
        """
        paragraph = self.text.pop(n-1)
        new_paragraph = paragraph.replace(search, replace)
        self.text.insert(n-1, new_paragraph)


if __name__ == "__main__":
    print("\nTest: Init")
    editor = Editor()

    print("\nTest: get_commands")
    editor.get_commands()

    print("\nTest: add")
    editor.change_format("raw")
    editor.add_n("First paragraph", 1)
    editor.add_n("Second paragraph", 2)
    editor.add_n("Third paragraph", 3)
    editor.add_n("Last paragraph", False)
    editor.add_n("Fourth paragraph", 4)

    editor.change_format("fix", 20)

    print("\nTest: Delete")
    editor.del_n(2)
    editor.del_n(False)

    print("\nTest: Dummy")
    editor.change_format("raw")
    editor.dummy_n(2)

    print("\nTest: Format Raw")
    editor.change_format("raw")

    print("\nTest: Format Fix")
    editor.change_format("fix", 20)

    print("\nTest: Index")
    editor.add_n("Hund Katze", 1)
    editor.add_n("Hund Katze", 1)
    editor.add_n("Hund", 1)
    editor.change_format("raw")
    editor.index()

    print("\nTest: Index")
    editor.add_n("Hund Katze", 1)
    editor.add_n("katze", 1)
    editor.index()

    print("\nTest: Empty Paragraph")
    editor.add_n("", 1)
    editor.add_n("", 4)
    editor.change_format("fix", 20)

    print("\nTest: Validate Input")
    print("Input: Mathematik 3 + 2 = 5")
    editor.change_format("raw")
    editor.add_n("Mathematik 3 + 2 = 5", False)

    print("\nTest: Search/replace")
    editor.add_n("ich suche dich", False)
    editor.replace("suche dich", "habe dich gefunden", False)
    editor.replace("k", "K", 2)


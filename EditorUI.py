""" EditorUI  """

__author__     = 'Salah Xaaji'
__copyright__  = 'Copyright 2022 Storm Hamsters'
__credits__    = 'Anja Edelmann, Ricky Raths, Lars Schneckenburger, Salah Xaaji'
__license__    = 'GPL'
__version__    = '1.0'
__created__    = '12.11.2022'
__maintainer__ = 'Salah Xaaji'
__email__      = 'xaajisal@students.zhaw.ch'
__status__     = 'done'


from Editor import Editor
from EditorValidator import Validator


class EditorUI:

    def __init__(self):
        self.running = False
        self.editor = Editor()
        self.validator = Validator(self.editor.commands,
                                   self.editor.commands_with_parameter,
                                   self.editor.commands_adding_text)
        self.commands_map = {
            "ADD": self.add, "DEL": self.delete,
            "DUMMY": self.dummy, "FORMAT RAW": self.change_format_to_raw,
            "FORMAT FIX": self.change_format_to_fix, "INDEX": self.index,
            "PRINT": self.print_text, "REPLACE": self.replace,
            "EXIT": self.exit}
        # dictionary of all the editor commands
        # keys: name of the commands in the class 'Editor'
        # values: corresponding method of the class 'Editor'

    def run(self):
        """
        Method runs the editor. To quit the method the function exit() must be
        called.
        
        Parameters
        ----------
        None.

        Returns
        -------
        None.
        
        """
        self.start()
        while self.running:
            user_command = self.get_user_command()
            
            formatted_command = self.split_command(user_command)

            validated_input = self.validator.input_is_valid(
                                    formatted_command,len(self.editor.text)
                                )
            if not validated_input[0]:
                print(validated_input[1])

            else:
                command, parameter = formatted_command
                if parameter and command in self.editor.commands_with_parameter:
                    self.commands_map[command](parameter)
                else:                    
                    self.commands_map[command]()

    def get_user_command(self):
        """
        Method gets the desired command from the user through the input in the 
        console
    
        Parameters
        ----------
        None.

        Returns
        -------
        command : str
            The raw input from the user
    
        """
        print("************************************************\n")
        self.print_commands()
        command = input("Enter command: ")
        return command

    def dummy(self, parameter= False):
        """
        Method calls the dummy_n method from Editor and prints a message for the 
        user
    
        Parameters
        ----------
         parameter : bool / int
            False if no parameter is given, else index of paragraph

        Returns
        -------
        None.
    
        """
        if parameter == False:
            parameter = self.define_n(add = True)
        self.editor.dummy_n(parameter)
        print("Successfully added dummy")

    def add(self, parameter= False):
        """
        Method calls the add_n method from Editor and prints a message for the 
        user
    
        Parameters
        ----------
        parameter : bool / int
            False if no parameter is given, else index of paragraph

        Returns
        -------
        None.
    
        """
        # define parameter if not given
        if parameter == False:
            parameter = self.define_n(add = True)
        # user input
        new_paragraph = str(input("Add Paragraph: "))
        # validate input
        validated_paragraph = \
            self.validator.validate_new_paragraph(new_paragraph)
        self.editor.add_n(validated_paragraph, parameter)
        print("Successfully added paragraph")

    def delete(self, parameter= False):
        """
        Method calls the del_n method from Editor and prints a message for the 
        user
    
        Parameters
        ----------
        parameter : bool / int
            False if no parameter is given, else index of paragraph

        Returns
        -------
        None.
    
        """
        # check if there is a text to be deleted
        if self.validator.text_is_given(self.editor.text):
            # define parameter if not given
            if parameter == False:
                parameter = self.define_n(add = False)
            self.editor.del_n(parameter)
            print("Successfully deleted paragraph")
        else:
            print("The paragraph could not be deleted")

    def replace(self, parameter=False):
        """
        Method gets replace parameter from user, calls the replace_n method from
        Editor and prints a message for the user
    
        Parameters
        ----------
        parameter : bool / int
            False if no parameter is given, else index of paragraph

        Returns
        -------
        None.
    
        """
        if parameter == False:
            parameter = self.define_n(add = False)
        search = str(input("What do you want to replace: "))
        replace = str(input("With what do you want to replace it: "))
        self.editor.replace(search, replace, parameter)
        print("Successfully replaced paragraph")

    def change_format_to_raw(self):
        """
        Method changes the current format to raw
    
        Parameters
        ----------
        None.

        Returns
        -------
        None.
    
        """
        self.editor.change_format("raw")
        print("Successfully used format raw")

    def change_format_to_fix(self, parameter):
        """
        Method changes the current format to fix with a certain number of
        characters per line.
    
        Parameters
        ----------
        parameter : bool / int
            False if no parameter is given, else index of paragraph

        Returns
        -------
        None.
    
        """
        self.editor.change_format("fix", parameter)
        print("Successfully used format fix")

    def index(self):
        """
        Method runs the index method from the editor and prints the result
    
        Parameters
        ----------
        None.

        Returns
        -------
        None.
    
        """
        word_index = self.editor.index()
        # output
        for term in word_index:
            if len(word_index[term]) >= 3:  # occur more than three times
                term_paragraphs = [
                    str(paragraph) for paragraph in word_index[term]
                ]
                print(term, " ", ', '.join(term_paragraphs))

    def print_text(self):
        """
        Method prints the content of the editor
    
        Parameters
        ----------
        None.

        Returns
        -------
        None.
    
        """
        text = self.editor.get_text_in_format()
        if len(text) == 0:
            print("Your editor does not have any text in it yet...")
        else:
            for column in text:
                print(column)

    def exit(self):
        """
        Method stops the editor
    
        Parameters
        ----------
        None.

        Returns
        -------
        None.
    
        """
        self.running = False

    def start(self):
        """
        Method sets the editor to ready for running
    
        Parameters
        ----------
        None.

        Returns
        -------
        None.
    
        """
        self.running = True

    def print_commands(self):
        """
        Method prints the possible commands for the user
    
        Parameters
        ----------
        None.

        Returns
        -------
        None.
    
        """
        print("You can choose from the following commands:")
        print(self.editor.get_commands())

    def define_n(self, add=False):
        """
        If n is not entered, n is defined as the last paragraph number.
        Distinction between methods that add paragraph or not.
    
        Parameters
        ----------
        None.
    
        Returns
        -------
        n : int
            The last paragraph number

        """
        if add:
            n = self.get_last_n() + 1
            # if a paragraph is being added, the last paragraph is 1 plus 
            # the highest paragraph number in the text. 
        else:
            n = self.get_last_n()
        return n

    def get_last_n(self):
        """
        Method returns the last paragraph number.
    
        Parameters
        ----------
        None.
    
        Returns
        -------
        The last paragraph number.
    
        """
        return len(self.editor.text)
    
    def split_command(self, command):
        """
        Splits the raw command from user in command and parameter
    
        Parameters
        ----------
        command :  str

        Returns
        -------
        (command, parameter) : tuple
            Tuple with command and parameter. If command or parameter is not given
            it returns False for its value
    
        """
        command_split = command.split(" ")
        if len(command_split) <= 0:
            return (False, False)
        else:
            parameter = command_split[-1]
            # Some commands have the option to define the parameter n,
            # which indicates the paragraph n
            # if a parameter has been entered, it would be the last element
            if parameter.isnumeric():
                # check if the last element is numeric and therefore parameter n
                command = " ".join(command_split[:-1])
            command = command.upper()
            if parameter.isnumeric():
            # returns a tuple if there is a numeric parameter n
                return (command, int(parameter))
            elif not parameter.isnumeric():
            # returns only the command if there is no numeric parameter n
                return (command, False)


if __name__ == "__main__":

    my_editor_ui = EditorUI()
    my_editor_ui.editor.text = ["ABCD", "EFGH", "IJKL","1234"]  # sample text

    # test: Start and Exit Editor
    print("\nTest: Start and Exit Editor")
    print("Before starting: ", my_editor_ui.running)  # expected output: False
    my_editor_ui.start()
    print("After starting:", my_editor_ui.running)  # expected output: True
    my_editor_ui.exit()
    print("After exiting: ", my_editor_ui.running)  # expected output: False

    # test: getting command and splitting the command
    print("\nTest: getting command and splitting the command")
    test_command = my_editor_ui.get_user_command()  # e.g. 'format fix 20'
    print("Test command: "+test_command)  # expected output: 'format fix 20'

    test_command_split = my_editor_ui.split_command(test_command)
    print("Test command split: ", test_command_split)
    # expected output: ('FORMAT FIX', 20), type: tuple

    # test: Text manipulations and print
    print("\nTest: Test manipulations and print")
    my_editor_ui.add(False)
    # expected result: Program should ask for new paragraph and add it
    # example: 'Test'
    print("New Text after adding: ")
    my_editor_ui.print_text()
    # expected result: Text with the new paragraph 'Test'

    my_editor_ui.delete(False)
    print("New Text after deleting: ")
    my_editor_ui.print_text()
    # expected result: Text without the new paragraph 'Test'

    print("Get the last possible paragraph if no paragraph number is given: ")
    my_editor_ui.define_n(False)
    # expected output: 4, because the last paragraph number is 4, and add = False
    print(my_editor_ui.get_last_n())
    # expected output: 4, because that's the last paragraph number

    # test: Format setting and changing 
    print("\nTest: Format setting and changing")
    print(my_editor_ui.editor.current_format)  # expected result: ('raw',0)
    my_editor_ui.change_format_to_fix(20)
    print(my_editor_ui.editor.current_format)  # expected result: ('fix',20)

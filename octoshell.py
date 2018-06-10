import argparse
from prompt_toolkit.application import Application
from prompt_toolkit.document import Document
from prompt_toolkit.filters import has_focus
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout.containers import HSplit, Window
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import TextArea
from lib.messages import WELCOME_MSG
from lib.command_parser import CommandParser
from lib.api_manager import ApiManager

class Octoshell():
    cmd_history = []
    cmd_history_cursor = 0

    def __init__(self, host, apikey):
        self.host = host
        self.apikey = apikey
        self.output_field = TextArea(style='class:output-field', text=WELCOME_MSG)
        self.input_field = TextArea(height=1, prompt=' # ', style='class:input-field')
        self.api_manager = ApiManager(self.host, self.apikey)
        self.cmd_parser = CommandParser(self.api_manager)
        self.define_keybindings()
        self.main()

    def main(self):
        self.container = HSplit([
            self.output_field,
            Window(height=1, char='-', style='class:line'),
            self.input_field
        ])

        style = Style([
                ('input-field', 'bg:#cccccc #000000'),
            ])
        
        # Run application.
        application = Application(
            layout=Layout(self.container, focused_element=self.input_field),
            key_bindings=self.kb,
            style=style,
            mouse_support=True,
            full_screen=True)

        application.run()
            
    def define_keybindings(self):
        """
            handles general key events, eg. quitting the application
        """
        self.kb = KeyBindings()
        @self.kb.add('c-c')
        @self.kb.add('c-q')
        def _(event):
            ''' Pressing Ctrl-Q or Ctrl-C will exit the user interface. '''
            event.app.exit()
        @self.kb.add('enter', filter=has_focus(self.input_field))
        def _(event):
            self.add_line(event)
    
    def add_line(self, event):
        """
            Append a line to the terminal output screen and clears the input line
        """
        new_text = (self.output_field.text 
            + '> ' + self.input_field.text + '\n'
            + self.cmd_parser.parse_cmd(self.input_field.text) 
            + '\n')
        self.output_field.buffer.document = Document(
            text=new_text, cursor_position=len(new_text))

        if len(self.input_field.text) > 0:
            self.cmd_history.append(self.input_field.text)
            self.cmd_history_cursor = len(self.cmd_history)
        self.input_field.text = '' # reset input field   

    
        
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('host', help="Octoprint host")
    parser.add_argument('apikey', help="Octoprint API key")
    parser.parse_args()
    args = parser.parse_args()
    Octoshell(args.host, args.apikey)
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
from prompt_toolkit.shortcuts import PromptSession


class Octoshell:
    cmd_history = []
    cmd_history_cursor = 0

    def __init__(self, host, apikey):
        self.host = host
        self.apikey = apikey
        self.api_manager = ApiManager(self.host, self.apikey)
        self.cmd_parser = CommandParser(self.api_manager)
        self.main()

    def main(self):
        session = PromptSession(message="> ", enable_history_search=True)
        app = session.app
        textarea = TextArea(
            text=WELCOME_MSG,
            read_only=False,
            scrollbar=True,
        )
        app.layout.container.height = 1
        mainlayout = HSplit([textarea, app.layout.container])
        app.layout = Layout(mainlayout, app.layout.current_control)

        # monkey patch fullscreen mode
        app.full_screen = True
        app.renderer.full_screen = True

        def accept(buf):
            if buf.text == "exit":
                app.exit(result="")
            else:
                newtext = self.cmd_parser.parse(buf.text)
                textarea.text = textarea.text + "\n" + newtext
                textarea.buffer.cursor_position = len(textarea.text)
                import time; time.sleep(5)
                buf.reset(append_to_history=True)

        session.default_buffer.accept_handler = accept
        try:
            app.run()
        except (KeyboardInterrupt, EOFError):  # ctrl+c or ctrl+d
            pass
        # self.container = HSplit([
        #     self.output_field,
        #     Window(height=1, char='-', style='class:line'),
        #     self.input_field
        # ])

        # style = Style([
        #         ('input-field', 'bg:#cccccc #000000'),
        #     ])

        # # Run application.
        # application = Application(
        #     layout=Layout(self.container, focused_element=self.input_field),
        #     key_bindings=self.kb,
        #     style=style,
        #     mouse_support=True,
        #     full_screen=True)

        # application.run()





if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("host", help="Octoprint host")
    parser.add_argument("apikey", help="Octoprint API key")
    parser.parse_args()
    args = parser.parse_args()
    Octoshell(args.host, args.apikey)

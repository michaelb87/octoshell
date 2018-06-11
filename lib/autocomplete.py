from prompt_toolkit.auto_suggest import AutoSuggest, Suggestion

class AutoCompleter(AutoSuggest):
    commands = ['h', 'status', 'ls']
    def get_suggestion(self, buffer, document):
        for c in self.commands:
            if c.startswith(document.text):
                return Suggestion(c.replace(document.text,''))
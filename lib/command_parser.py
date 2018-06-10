class CommandParser():
    def __init__(self, api_manager):
        self.api_manager = api_manager

    def parse_cmd(self,cmd):
        cleaned = cmd.strip()
        if cleaned == 'h' or cleaned == 'help':
            return 'I cannot help you now'
        return cmd
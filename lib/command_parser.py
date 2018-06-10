class CommandParser():
    def __init__(self, host, apikey):
        pass

    def parse_cmd(self,cmd):
        cleaned = cmd.strip()
        if cleaned == 'h' or cleaned == 'help':
            return 'I cannot help you now'
        return cmd
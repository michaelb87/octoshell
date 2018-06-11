from textwrap import dedent
class CommandParser():
    def __init__(self, api_manager):
        self.api_manager = api_manager

    def parse_cmd(self,cmd):
        cleaned = cmd.strip()
        if cleaned == 'h' or cleaned == 'help':
            return self.help_text()
        if cleaned == 'ls' or cleaned == 'list':
            return self.api_manager.list_files()
        if cleaned == 'status':
            return self.api_manager.get_status()
        return cmd
    
    def help_text(self):
        return dedent(
            '''
            Help:
            
            ls - list all files
            status - printer status
            ''')
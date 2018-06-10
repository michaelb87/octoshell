
    
def parse_cmd(cmd):
    cleaned = cmd.strip()
    if cleaned == 'h' or cleaned == 'help':
        return 'I cannot help you now'
    return cmd
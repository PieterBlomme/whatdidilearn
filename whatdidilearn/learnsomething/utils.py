def get_arxiv_sanity_array(script_content):
    capture = False
    text = ''
    for line in script_content.splitlines():
        if line.startswith('var papers'):
            line = line.replace('var papers', 'var arxiv_sanity_similar')
            capture = True
        if line.startswith('var pid_to_users'):
            capture = False

        if capture:
            text += line
    return text
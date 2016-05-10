import os.path
import dl7, dljson

formats = {
    'JSON': dljson,
    'DL7': dl7
    }

extensions = {
    'json': 'JSON',
    'zxu': 'DL7'
}

def get_module(filename):
    pair = os.path.splitext(filename)
    if pair[1] and pair[1][0] == '.':
        extension = pair[1][1:].lower()
        if extension in extensions:
            return formats[extensions[extension]]
    return None

mapping = {
    ' ': '%20',
    '/': '%2F',
    '?': '%3F',
    '\\':'%5C',
    '|': '%7C',
}

def strip_filename( str ):
    for src in mapping.keys():
        str = str.replace(src, mapping[src])

    return str
__author__ = 'michiel'


def load_shader(fileName, type='vertex'):
    try:
        file = open('../res/shaders/{type}/{fileName}'.format(type=type, fileName=fileName), 'r', 1)
        shader = ''
        for line in file:
            shader += line + '\n'

        file.close()
    except Exception as err:
        print(err.with_traceback(None))
        exit(1)

    return shader
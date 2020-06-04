#parse('header.py')

#set( $CLASS_NAME = ${StringUtils.removeAndHump(${NAME}, "_.")} )

class $CLASS_NAME(object):
    def __init__(self, *args, **kwargs):
        pass


__all__ = [
    '$CLASS_NAME'
]
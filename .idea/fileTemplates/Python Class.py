#set( $CAMEL_NAME = ${StringUtils.removeAndHump(${NAME}, "_.")} )

#parse ("DefaultVariables.py")
__author__ = "${FULLNAME}"
__email__ = "${FULLEMAIL}"
__copyright__ = "${COPYRIGHT}"
__license__ = "${LICENSE}"

class ${CAMEL_NAME}(object):
    pass


__all__ = [
    '${CAMEL_NAME}',
]
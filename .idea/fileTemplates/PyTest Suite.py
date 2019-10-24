#set( $CAMEL_NAME = ${StringUtils.removeAndHump(${NAME}, "_.")} )

import pytest

#parse ("DefaultVariables.py")
__author__ = "${FULLNAME}"
__email__ = "${FULLEMAIL}"
__copyright__ = "${COPYRIGHT}"
__license__ = "${LICENSE}"

class ${CAMEL_NAME}(object):
    pass


if __name__ == "__main__":
    pytest.main()
#set( $SUITE_NAME = ${StringUtils.sub(${NAME}, 'test_', '')} )
#set( $CAMEL_NAME = ${StringUtils.removeAndHump(${SUITE_NAME})} )

import pytest

#parse ("DefaultVariables.py")
__author__ = "${FULLNAME}"
__email__ = "${FULLEMAIL}"
__copyright__ = "${COPYRIGHT}"
__license__ = "${LICENSE}"

class ${CAMEL_NAME}TestSuite(object):
    pass


if __name__ == "__main__":
    pytest.main()
import pytest

#parse('header.py')

#set( $CLASS_NAME = ${StringUtils.removeAndHump(${NAME}, "_.")} )

class $CLASS_NAMETestSuite(object):
    def test_something(self):
        assert False


if __name__ == "__main__":
    pytest.main()

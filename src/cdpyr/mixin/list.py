from collections import UserList


class ObjectList(UserList):

    @property
    def __wraps__(self):
        return None

    def __getattr__(self, name):
        res = []

        for data in self.data:
            attr = getattr(data, name)

            if not callable(attr) or isinstance(attr, ObjectList):
                res.append(attr)

                continue

            def wrapper(*args, **kwargs):
                return attr(*args, **kwargs)

            res.append(wrapper)

        # if a custom class is wrapped and the current result contains only
        # these objects, we will return the original ObjectList with the results
        if self.__wraps__ is not None and \
            all(isinstance(o, self.__wraps__) for o in res):
            return self.__class__(res)

        return ObjectList(res)

    def __call__(self, *args, **kwargs):
        res = []

        for data in self.data:
            res.append(data(*args, **kwargs))

        # if a custom class is wrapped and the current result contains only
        # these objects, we will return the original ObjectList with the results
        if self.__wraps__ is not None and all(
            isinstance(o, self.__wraps__) for o in res):
            return self.__class__(res)

        return ObjectList(res)

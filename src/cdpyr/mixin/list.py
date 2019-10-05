from collections import UserList


class DispatcherList(UserList):

    def __getattr__(self, name):
        res = self.__class__()

        for data in self.data:
            attr = getattr(data, name)

            if not callable(attr) or isinstance(attr, DispatcherList):
                res.append(attr)

                continue

            def wrapper(*args, **kwargs):
                return attr(*args, **kwargs)

            res.append(wrapper)

        return res

    def __call__(self, *args, **kwargs):
        res = self.__class__()

        for data in self.data:
            res.append(data(*args, **kwargs))

        return res

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func

    return decorate
class Singleton(type):
    _instances = {}

    def has_instance(cls):
        return cls in cls._instances.keys()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
            # print(f"inited a {cls.__name__} object")
            # print(f"dict: {cls.__dict__}")
        else:
            if args:
                # if len(args)>2:
                #     raise ValueError("Singleton setting should")
                # setattr(cls._instances[cls], 'floors', args[0])
                # setattr(cls._instances[cls], 'mode', args[1])
                raise ValueError("Modify a Singleton object should only use keyword arguments!")
            elif kwargs:
                for k, v in kwargs.items():
                    if k in tuple(i for i in tuple(i for i in dir(super()) if i.islower())):
                        setattr(cls._instances[cls], k, v)
            # else:
            #     print(f"WARNING: Instance already exist!{args}{kwargs}")
        # print(f"returned a {cls.__name__} object")
        return cls._instances[cls]

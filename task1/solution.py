def strict(func):
    def wrapper(*args, **kwargs):
        annotations = func.__annotations__
        
        for arg_name, arg_value in zip(annotations.keys(), args):
            expected_type = annotations[arg_name]
            if not isinstance(arg_value, expected_type):
                raise TypeError(f"Argument '{arg_name}' must be of type {expected_type.__name__}, not {type(arg_value).__name__}")
        
        for arg_name, arg_value in kwargs.items():
            if arg_name in annotations:
                expected_type = annotations[arg_name]
                if not isinstance(arg_value, expected_type):
                    raise TypeError(f"Argument '{arg_name}' must be of type {expected_type.__name__}, not {type(arg_value).__name__}")
        
        return func(*args, **kwargs)
    return wrapper
import traceback


def print_function_name(func):
    def wrapper(*args, **kwargs):
        print("--->", func.__name__, ": function call:")
        try:
            nb = func(*args, **kwargs)
            print("--->", func.__name__, ": Done with output", nb)
            return nb
        except ValueError as e:
            print(f"--->", func.__name__, f": Error: {str(e)}")
        except Exception as e:
            print("--->", func.__name__, ": Failed with exception:")
            traceback.print_exc()
            raise e

    return wrapper


def log_on_value_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            print(f"Error: {str(e)}")
        # except git.exc.InvalidGitRepositoryError

    return wrapper

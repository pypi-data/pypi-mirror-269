import threading

def debounce(wait):
    """ Decorator that will postpone a function's
        execution until after `wait` seconds
        have elapsed since the last time it was invoked. """
    def decorator(fn):
        def debounced(*args, **kwargs):
            def call_it():
                fn(*args, **kwargs)
            
            if hasattr(debounced, '_timer'):
                debounced._timer.cancel()
            
            debounced._timer = threading.Timer(wait, call_it)
            debounced._timer.start()
        
        return debounced
    return decorator
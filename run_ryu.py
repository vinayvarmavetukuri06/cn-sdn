import collections
import collections.abc
import sys

# 1. Fix the MutableMapping error
collections.MutableMapping = collections.abc.MutableMapping
collections.Iterable = collections.abc.Iterable
collections.MutableSet = collections.abc.MutableSet
collections.Callable = collections.abc.Callable

# 2. Fix the ALREADY_HANDLED error for eventlet 0.33.3
import eventlet
import eventlet.wsgi
if not hasattr(eventlet.wsgi, 'ALREADY_HANDLED'):
    eventlet.wsgi.ALREADY_HANDLED = None

# 3. Start Ryu
from ryu.cmd.manager import main

if __name__ == '__main__':
    # Add your controller file to the arguments
    if 'my_controller.py' not in sys.argv:
        sys.argv.append('my_controller.py')
    main()

# from Testi.Requesti import Requesti as Requesti
# from Testi.Responsi import Responsi as Responsi
#from testirequesti.Requesti import Requesti
from .Responsi import Responsi
from .Requesti import Requesti
import copy
import requests


def patch_requests(capture_file):
    """ Patch requests.get and requests.post """
    # Keep a copy of the original method
    original_requests_get = copy.copy(requests.get)
    requesti = Requesti(capture_file)

    def decor(func):
        def wrapper(*args,  **kwargs):
            requests.get = requesti.mock_get
            func()
            # Restore original method
            requests.get = original_requests_get
        return wrapper
    return decor

import requests
import re
import copy
import logging
import json
from . import Responsi


class Requesti():
    def __init__(self, capture_file, exact_urls=True):
        """ New Requesti instance using a packet capture file

        Arguments:
            capture_file: A path to a .har file
            exact_urls:
                @TODO
                If False, preform some preprocesing of URLs to match against
                remove http[s]://www and trailing /, lowercase.
        """
        self.exact_urls = exact_urls
        if capture_file.endswith(".har"):
            with open(capture_file, "r") as fp:
                self.capture = json.load(fp)['log']['entries']
        elif capture_file.endswith(".cap"):
            raise NotImplementedError(".cap files not implemented yet")
        else:
            raise ValueError("Unknown filetype {}".format(capture_file))

    def find_packets(self, url_regex, params=None):
        """ Searches capture for a packet matching url, and optionally params

        Arguments:
            url_regex: match only packets with url matching this regex statement
            params:
                @TODO
                an optional dictionary of additional http request header filters
        Returns:
            A list of matching request/response pairs from capture file
        """
        if params:
            raise NotImplementedError("Parameter limiting is not Implmented")
        matched = [
            e for e in self.capture
            if re.match(url_regex, e['request']['url'])
        ]
        return matched

    def mock_get(self, url, params=None, **kwargs):
        """ Mock requests.get calls by replying matched responses from capture.

        Arguments:
            url: match against this url
            params:
                optional, containing these params
                Not implemented
        Returns:
            A requests.Response object from capture
        Raise:
            ResourceWarning: If no matching packets found in capture.
            NotImplementedError: Anything other than exact matching of URLs
        """
        if self.exact_urls and not params:
            matched = [e for e in self.capture if e['request']['url'] == url]
            if len(matched) == 1:
                return Responsi(matched[0])
            if len(matched) == 0:
                raise Warning("No packets matched url {}".format(url))
            if len(matched) > 1:
                logging.debug(
                    "request for {} matched multiple entries in the "
                    "capture file, using first entry".format(url)
                )
                return Responsi(matched[0])
        else:
            raise NotImplementedError(
                "Matching against parameters and non-exact urls not yet implemented"
            )
        pass

    def inject_get_request(self, func):
        """ Method override for requests.get to reply from capture instead of
        shooting real http requests.
        """
        # Keep a copy of the original method
        original_requests_get = copy.copy(requests.get)

        def wrapper(*args,  **kwargs):
            requests.get = self.mock_get
            func()
            # Restore original method
            requests.get = original_requests_get
        return wrapper


def patch_requests(func, capture_file):
    """ Patch requests.get and requests.post
    """
    # Keep a copy of the original method
    original_requests_get = copy.copy(requests.get)
    requesti = Requesti(capture_file)

    def wrapper(*args,  **kwargs):
        requests.get = requesti.mock_get
        func()
        # Restore original method
        requests.get = original_requests_get
    return wrapper

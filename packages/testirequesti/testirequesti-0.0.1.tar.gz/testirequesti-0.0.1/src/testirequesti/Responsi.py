import requests


class Responsi():
    """ Try and behave like requests.Response object """

    def __init__(self, har_entry):

        print(har_entry)
        self.text = har_entry['response']['content']['text']
        headers = har_entry['response']['headers']
        # name/value list into key:value dict
        # Note: I might be dropping entries with duplicate names here???
        # TODO This puts an extra {} !!!
        self.headers = {h['name']: h['value'] for h in headers}
        self.status_code = har_entry['response']['status']

        # Should be of type RequestCookieJar!!!
        self.cookies = har_entry['response']['cookies']
        # TODO
        # self.request - a requests.models.PreparedRequest
        # self.raw - a urllib3 HTTPResponse
        # self.url - The final url after redirection
        # ...

    def json():
        raise NotImplementedError("not decoding JSON just yet...")
    # TODO all the rest of requests.Response methods

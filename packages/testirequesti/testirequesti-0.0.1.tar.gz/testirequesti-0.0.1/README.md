# Testi Requesti - Mocking utils for pytest.
Mock HTTP Responses by replying Responses from a capture file.
patch python's `requests.get()`, to search in the capture instead of sending an http request.
Currently only supports .har files, and patching requests.get

# requests
Requests mocked by replying packet captures in .har file format.
I plan to implement .pcap files in the future if i find those necessary, 
and possibly also scripts to craft responses. 

**currently only the GET verb is implemented** and only match by the URL (headers are ignored) and returns the first packet matched.

## To generate a HAR file

### Firefox
To generate a .har file in Firefox, open the network console (Ctrl + Shift + E) and start browsing.
When done, right click on ths capture window and "Save All As HAR".


## Examples

inject mocked requests onto requests.get 
```python
from testirequesti import Requesti, patch_requests

URL = "https://some-url.com/"

@patch_requests("project_root/tests/data/session.har")
def test_something():
    mocked_response = requests.get(URL)
```

To find all captured packets to url
```python
requesti = Requesti(HAR_FILE)
url_regex = "^http.*.parliament\.uk"
matched = requesti.find_packets(url_regex)
```

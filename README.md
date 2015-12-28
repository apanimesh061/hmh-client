# hmh-client

This is a Python wrapper of the [HMH developer portal APIs][hmhco].

There are a total of [5 APIs][guide]:

  - Identity API
  - Assignment API
  - Documents API
  - Tags API
  - Content API

The Identity and Tags API are fully functional right now. 

There are two version of this API: 
  - V1 (version 1)
  - V2 (version 2)

All the wrappers are currently dealing with the V1 API.

I used `urllib2` library for this project but I am planning to shift to `requests` as I have founf it more developer friendly.

### Version
0.0.1

### Tech

This wrapper uses the following packages:

* [urllib2] - Library for opening URLs
* [urllib] - Used for encoding URLs
* [json] - Encoding/Decoding URLs
* [cPickle] - Persistence of objects

### Todos

 - Transition from urllib2 to [requests][tran]
 - Add Code Comments
 - Complete other APIs
 - Write Tests

License
----

GPL 2.0

   [hmhco]: <https://developer.hmhco.com/>
   [tran]: <http://docs.python-requests.org/en/latest/>
   [guide]: <https://developer.hmhco.com/api-guide>
   [urllib2]: <https://docs.python.org/2/library/urllib2.htmlr>
   [urllib]: <https://docs.python.org/2/library/urllib.html>
   [json]: <https://docs.python.org/2/library/json.html>
   [cPickle]: <https://wiki.python.org/moin/UsingPickle>



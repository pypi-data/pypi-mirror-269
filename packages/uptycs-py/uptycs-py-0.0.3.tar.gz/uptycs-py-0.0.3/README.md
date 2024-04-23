# uptycs_py
Uptycs API helper library (for Python 3)

## Installation

If you already know how to install python packages, then you can install it via pip:

You might need sudo on linux. if you want to install using pip, you can use following command:
```
$ sudo pip install uptycs-py
```

## Usage

This modules contains classes to interact with the Uptycs API using Python.
```
Some commonly used classes include:
  UptApiAuth()     - Read an Uptycs API key file and create authorization header
  UptApiCall()     - Call an Uptycs API method
  UptAlertRule()   - Get or Create an alert rule
  UptAssets()      - Show/update assets registered in Uptycs, add/remove tags from assets
  UptEventRule()   - Get or Create an event rule
  UptLkpTable()    - Get or Create a lookup table (typically for whitelists/blacklists)
  UptQueryGlobal() - Run a query against global (flight recorder)
  UptQueryRt()     - Run a query against realtime
```

Test sample:

```
import sys
import uptycs_py

keyfile = sys.argv[1]
myauth = uptycs_py.UptApiAuth(keyfile)
myasset = uptycs_py.UptAssets(myauth)
print("Total number of assets %s " % len(myasset.items))
print(myasset.get_id_from_hostname('test_host_name'))
```

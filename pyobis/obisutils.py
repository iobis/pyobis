import requests

obis_baseurl = "http://api.iobis.org/"

class NoResultException(Exception):
    pass

def obis_search_GET(url, args, **kwargs):
  out = requests.get(url, params=args, **kwargs)
  out.raise_for_status()
  stopifnot(out.headers['content-type'])
  return out.json()

def obis_GET(url, args, **kwargs):
  out = requests.get(url, params=args, **kwargs)
  out.raise_for_status()
  stopifnot(out.headers['content-type'])
  return out.json()

def stopifnot(x):
  if x != 'application/json;charset=UTF-8':
    raise NoResultException("content-type did not = application/json")

def stop(x):
  raise ValueError(x)

def handle_arrstr(x):
  if x.__class__.__name__ == 'NoneType':
    pass
  else:
    if x.__class__.__name__ == 'str':
      return x
    else:
      return ','.join(x)


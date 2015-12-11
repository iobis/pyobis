import requests

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
  if x != 'application/json':
    raise NoResultException("content-type did not = application/json")

def stop(x):
  raise ValueError(x)

obis_baseurl = "http://api.iobis.org/"

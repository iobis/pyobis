import requests

obis_baseurl = "http://api.iobis.org/"

class NoResultException(Exception):
    pass

def obis_GET(url, args, ctype, **kwargs):
  out = requests.get(url, params=args, **kwargs)
  out.raise_for_status()
  stopifnot(out.headers['content-type'], ctype)
  return out.json()

def obis_write_disk(url, path, ctype, **kwargs):
  out = requests.get(url, stream=True, **kwargs)
  out.raise_for_status()
  with open(path, 'wb') as f:
    for chunk in out.iter_content(chunk_size = 1024):
      if chunk:
        f.write(chunk)
  return path

def stopifnot(x, ctype):
  if x != ctype:
    raise NoResultException("content-type did not equal " + str(ctype))

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


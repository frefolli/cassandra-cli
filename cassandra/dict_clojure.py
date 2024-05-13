from cassandra.regex_utils import is_reference
from cassandra.env import get_from_env

def closure_for_skel(skel, env):
  if isinstance(skel, list):
    return [closure_for_skel(_, env) for _ in skel]
  elif isinstance(skel, dict):
    return {key:closure_for_skel(skel[key], env) for key in skel}
  elif isinstance(skel, str):
    if is_reference(skel):
      value = get_from_env(env, skel[2:-1].split('.'))
      if value is None:
        raise Exception("unknown reference to '%s'" % skel[2:-1])
      return value
    else:
      return skel
  else:
    return skel

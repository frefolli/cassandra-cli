from lib.regex_utils import identify_next_jinja_reference
from lib.env import get_from_env

def closure_for_jinja(text: str, env: dict) -> str:
  next_reference = identify_next_jinja_reference(text)
  while next_reference is not None:
    (ref, span) = next_reference
    value = get_from_env(env, ref.split('.'))
    if value is None:
      raise Exception("unknown reference to '%s'" % ref)
    text = "%s\"%s\"%s" % (text[:span[0]], value, text[span[1]:])
    next_reference = identify_next_jinja_reference(text)
  return text

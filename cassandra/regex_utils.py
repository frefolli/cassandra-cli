#!/usr/bin/python3
import re

def is_ip_address(text: str) -> bool:
  # Match only IPv4
  return re.match("^[0-9]+(\\.[0-9]+)+$", text) is not None

def is_domain(text: str) -> bool:
  return re.match("^[a-zA-Z_][a-zA-Z0-9_]*(\\.[a-zA-Z_][a-zA-Z0-9_]*)+$", text) is not None

def is_nodeID(text: str) -> bool:
  return re.match("^[a-zA-Z_][a-zA-Z0-9_]*$", text) is not None

def is_reference(text: str) -> bool:
  return re.match("^\\$\\([a-zA-Z0-9_.]+\\)$", text) is not None

def identify_next_jinja_reference(text: str):
  result = re.search("\\{\\{\\s*[a-zA-Z0-9_.]+\\s*\\}\\}", text)
  if result is None:
    return None
  span = result.span()
  return (text[span[0]+2:span[1]-2], span)

from cassandra.regex_utils import is_ip_address, is_nodeID, is_domain

def find_ip_from_domain(config: dict, domain: str) -> str:
  for nodeID in config['nodes']:
    if config['nodes'][nodeID]['domain'] == domain:
      return config['nodes'][nodeID]['ip']
  raise Exception("unknown domain '%s'" % domain)

def find_ip_from_nodeID(config: dict, nodeID: str) -> str:
  if (nodeID in config['nodes']):
    return config['nodes'][nodeID]['ip']
  raise Exception("unknown nodeID '%s'" % nodeID)

def preprocess_config(config: dict) -> dict:
  nodes = {}
  for node in config['nodes']:
    nodes[node['name']] = node
  config['nodes'] = nodes
  
  seeds = []
  for seed in config['options']['seeds']:
    if is_ip_address(seed):
      seeds.append(seed)
    elif is_nodeID(seed):
      seeds.append(find_ip_from_nodeID(config, seed))
    elif is_domain(seed):
      seeds.append(find_ip_from_domain(config, seed))
    else:
      raise Exception("unknown piece of junk: '%s'" % seed)
  config['options']['resolved_seeds'] = ",".join(seeds)
  return config

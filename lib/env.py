from lib.regex_utils import is_ip_address, is_nodeID, is_domain

def build_env_for_node(config: dict, nodeID: str):
  env = {}
  env['node'] = config['nodes'][nodeID].copy()
  env['options'] = config['options']
  env['options']['seeds'] = config['options']['resolved_seeds']
  env['node']['other_node_ips'] = []
  for otherNodeID in config['nodes']:
      if otherNodeID != nodeID:
        env['node']['other_node_ips'].append(config['nodes'][otherNodeID]['ip'])
  env['node']['other_node_ips'] = " ".join(env['node']['other_node_ips'])
  return env

def get_from_env(env: dict|None, keys: list[str]):
  if env is None:
    return None
  if len(keys) == 0:
    return env
  else:
    return get_from_env(env.get(keys[0]), keys[1:])

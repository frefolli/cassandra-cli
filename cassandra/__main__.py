#!/usr/bin/python3
import tempfile
import os
import sys
import argparse
import logging

from cassandra.yaml_utils import read_yaml_file, write_yaml_file
from cassandra.properties_utils import write_properties_file
from cassandra.bash_utils import read_bash_file, write_bash_file
from cassandra.config import preprocess_config
from cassandra.env import build_env_for_node
from cassandra.dict_clojure import closure_for_skel
from cassandra.jinja_clojure import closure_for_jinja
from cassandra.ssh import ssh_execute_command, ssh_send_file, _system_command

CASSANDRA_HOME="/home/cassandra24/apache-cassandra-5.0-beta1"
CASSANDRA=f"{CASSANDRA_HOME}/bin/cassandra"
NODETOOL=f"{CASSANDRA_HOME}/bin/nodetool"

def FallbackIfNotThere(local_path, fallback):
  if not os.path.exists(local_path):
    _system_command(f"mkdir -p {os.path.dirname(local_path)}")
    _system_command(f"cp {fallback} {local_path}")

def ConfigYamlPath():
  local_path = "~/.config/python-cassandra/config.yaml"
  fallback = "/usr/share/python-cassandra/config.yaml"
  FallbackIfNotThere(local_path, fallback)
  return local_path

def CassandraSetupPath():
  local_path = "~/.config/python-cassandra/skel/cassandra-setup.sh"
  fallback = "/usr/share/python-cassandra/skel/cassandra-setup.sh"
  FallbackIfNotThere(local_path, fallback)
  return local_path

def CassandraYamlPath():
  local_path = "~/.config/python-cassandra/skel/cassandra.yaml"
  fallback = "/usr/share/python-cassandra/skel/cassandra.yaml"
  FallbackIfNotThere(local_path, fallback)
  return local_path

def CassandraRackDcYamlPath():
  local_path = "~/.config/python-cassandra/skel/cassandra-rackdc.yaml"
  fallback = "/usr/share/python-cassandra/skel/cassandra-rackdc.yaml"
  FallbackIfNotThere(local_path, fallback)
  return local_path

def DoSetup():
  config = preprocess_config(read_yaml_file("config.yaml"))
  skel_cassandra_setup = read_bash_file("skel/cassandra-setup.sh")
  with tempfile.TemporaryDirectory() as tmpdir:
    for nodeID in config['nodes']:
      env = build_env_for_node(config, nodeID)
      cassandra_setup = closure_for_jinja(skel_cassandra_setup, env)
      cassandra_setup_path = os.path.join(tmpdir, "cassandra-setup.sh")
      write_bash_file(cassandra_setup_path, cassandra_setup)
      # Send Cassandra Setup
      # Execute Cassandra Setup
      ssh_send_file(nodeID, cassandra_setup_path, "/home/cassandra24")
      ssh_execute_command(nodeID, "bash cassandra-setup.sh")

def DoConfigure():
  config = preprocess_config(read_yaml_file(ConfigYamlPath()))
  skel_cassandra_yaml = read_yaml_file(CassandraYamlPath())
  skel_cassandra_rackdc_yaml = read_yaml_file(CassandraRackDcYamlPath())
  with tempfile.TemporaryDirectory() as tmpdir:
    for nodeID in config['nodes']:
      env = build_env_for_node(config, nodeID)
      cassandra_yaml = closure_for_skel(skel_cassandra_yaml.copy(), env)
      cassandra_yaml_path = os.path.join(tmpdir, "cassandra.yaml")
      write_yaml_file(cassandra_yaml_path, cassandra_yaml)
      cassandra_rackdc_yaml = closure_for_skel(skel_cassandra_rackdc_yaml.copy(), env)
      cassandra_rackdc_yaml_path = os.path.join(tmpdir, "cassandra-rackdc.properties")
      write_properties_file(cassandra_rackdc_yaml_path, cassandra_rackdc_yaml)
      ssh_send_file(nodeID, cassandra_yaml_path, f"{CASSANDRA_HOME}/conf")
      ssh_send_file(nodeID, cassandra_rackdc_yaml_path, f"{CASSANDRA_HOME}/conf")

def DoStart():
  config = preprocess_config(read_yaml_file(ConfigYamlPath()))
  for nodeID in config['nodes']:
    ssh_execute_command(nodeID, f"\"nohup {CASSANDRA} &\"")

def DoStop():
  config = preprocess_config(read_yaml_file(ConfigYamlPath()))
  for nodeID in config['nodes']:
    ssh_execute_command(nodeID, f"{NODETOOL} stopdaemon")

def DoReset():
  config = preprocess_config(read_yaml_file(ConfigYamlPath()))
  for nodeID in config['nodes']:
    ssh_execute_command(nodeID, f"rm -rf {CASSANDRA_HOME}/data/*")

def DoStatus():
  config = preprocess_config(read_yaml_file(ConfigYamlPath()))
  nodeID = list(config['nodes'].keys())[0]
  ssh_execute_command(nodeID, f"{NODETOOL} status")

def main_cli():
  argument_parser = argparse.ArgumentParser()
  argument_parser.add_argument('action', choices=['setup', 'configure', 'start', 'stop', 'reset', 'status'])
  argument_parser.add_argument('-v','--verbose', action='store_true', default=False)
  cli_config = argument_parser.parse_args(sys.argv[1:])

  if cli_config.verbose:
    logging.getLogger().setLevel(logging.DEBUG)

  match cli_config.action:
    case 'setup':
      DoSetup()
    case 'configure':
      DoConfigure()
    case 'start':
      DoStart()
    case 'stop':
      DoStop()
    case 'reset':
      DoReset()
    case 'status':
      DoStatus()

if __name__ == "__main__":
  main_cli()

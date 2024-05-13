import os
import logging

def _system_command(cmd):
  logging.debug("Executing: '%s'" % cmd)
  os.system(cmd)

def ssh_execute_command(host: str, cmd: str):
  _system_command(f"ssh {host} {cmd}")

def ssh_send_file(host: str, file: str, dest: str):
  _system_command(f"scp {file} {host}:{dest}")

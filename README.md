# SNMP-bandwidth-collector

Example use: get_info.py domains.txt or threaded.py domains.txt

Line 17 of get_info.py or line 31 in threaded.py needs to have community set from public to appropriate community string.

The threaded version cuts time approximately in half.

threaded.py will output a log file in the working dir with data single lined per domain.

Appropriate permissions are needed for logging to work properly.


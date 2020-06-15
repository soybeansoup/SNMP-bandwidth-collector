# SNMP-bandwidth-collector

Example use: Python3 get_info.py domains.txt or Python3 threaded.py domains.txt

Line 17 of get_info.py or line 31 in threaded.py needs to have community set from public to appropriate community string.

The threaded version cuts time approximately in half although it is not as optimized as it could be.

threaded.py will output a log file in the working dir with data single lined per domain.
It will need appropriate permissions enabled for logging to work properly


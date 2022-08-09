# EncryptedATMBankServer
Implementation (using client-server protocol) to mimic transactions/ e-banking between an ATM (client) and a bank (server) which allows for secure deposits, withdrawals, and current balance checks.

#USAGE
Important: PLEASE READ INSTRUCTIONS to ensure understanding of how everything works.
These 2 files must be run in a certain order to ensure no timeouts occur.
Please run, in this order:
Server.py (bank process)
Client.py (ATM process)
Processes should be run on the same machine, on SEPERATE TERMINALS.
Ensure BOTH PROCESSES ARE KILLED before running again, or the port will show up as in-use. Again, SEPERATE TERMINALS for server/client

Additionally, run config.py to generate new public/private keypairs for server and client (should be done every run).
Private keys should not be accessed by anyone but the process they are generated for- Public keys,
inversely, are considered public knowledge and can be accessed by anyone.

Use 'pip install bitstring' before running any code, if bitstring is not already installed on your environment.

Thank you! Good luck + Have fun
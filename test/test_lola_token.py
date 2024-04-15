import os
from dotenv import dotenv_values

import sys
import os
# Get the parent directory of the current script
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Add the parent directory to the Python module search path
sys.path.append(parent_dir)
sys.path.append(parent_dir + '/lolapy')
from lolapy import decode_lola_token



config = {
    **dotenv_values("example/.env"),    # load development variables
    **os.environ,               # override loaded values with environment variables
}

lola_token = decode_lola_token(config["ASSISTANT_TOKEN"])
tenantId = lola_token.tenantId
assistantId = lola_token.assistantId

print(f"tenantId: {tenantId}")
print(f"assistantId: {assistantId}")

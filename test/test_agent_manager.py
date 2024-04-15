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
from lolapy import LolaAgentManager


config = {
    **dotenv_values("example/.env"),    # load development variables
    **os.environ,               # override loaded values with environment variables
}


if __name__ == "__main__":
    token = config["ASSISTANT_TOKEN"]
    prompter_url = "http://localhost:4000"

    agent_manager = LolaAgentManager(token, prompter_url)
    agent_manager.completion("12345", "Hello Bartosz")

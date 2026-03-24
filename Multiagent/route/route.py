from Multiagent.find_files.find_files import workspace_scanner_agent
from Multiagent.log_filter.log_filter import log_filter_agent
from Multiagent.find_files.find_files import find_all_files
from Multiagent.sub_agent.file_not_found.file_not_found import found_error
from groq import Groq


state = {}

state.update(workspace_scanner_agent(state))
state.update(log_filter_agent(state))
state.update(found_error(state))

record = state["errors"]
error = record[0]["content"]
main_error = state["main_error"]




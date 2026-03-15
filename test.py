from Multiagent.find_files.find_files import workspace_scanner_agent
from Multiagent.log_filter.log_filter import log_filter_agent
from Multiagent.error_analyzer.error_analyzer import find_main_files

state = {}

state.update(workspace_scanner_agent(state))
state.update(log_filter_agent(state))


print(state["errors"])

from prompt import Prompt
from memory import Memory
from reactengineer import ReactEngineer
from autostartup import AutoStartup

if __name__ == "__main__":
	prompt = Prompt()
	memory = Memory()
	react_engineer = ReactEngineer(prompt)
	auto_startup = AutoStartup(react_engineer, prompt, memory)
	auto_startup.run()
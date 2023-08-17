# AutoStartup
Coding was livestreamed here -> https://youtube.com/live/ZCyxDRSw0wE

# What is this?
AutoStartup is a Llama 2 autonomous agent built around the https://github.com/jawerty/10x-react-engineer project. It divises a startup idea, business plans and generates React codebases all based on a simple user input "intuition".

# How it works
First, AutoStartup takes in an "intuition" from the user. An example being "I think a website for dogsitters would be cool". Then the Agent divises a business idea from this as well as a business plan. It will iterate on the business plan with "Criticisms" (similar to [AutoGPT](https://github.com/Significant-Gravitas/Auto-GPT)). After each criticism it'll adjust the business plan and "pitch" to an investor prompt. The investor will either approve or disapprove of the final plan. After this final approval it will generate the code base and perform "pivots" based on user feedback

1) User intutiton (e.g. "I think a website for dogsitters would be cool")
2) Idea Loop
	- Develops initial business idea
	- Writes business plan
	- Criticize loop
		- Criticizes business plan and generates new plan
		- Uses new plan to ask "investor" for approval
		- Upon approval continue
			- Else: restart loop with new plan
	- Generate a product idea from finalized business plan
3) Generates React Codebase
	- Utilize [10x-React-Engineer](https://github.com/jawerty/10x-react-engineer) (a project I built on a stream a couple days before this one) to generate the codebase
4) (optional) Make a pivot based on the user's feedback

## Features
- 100% Llama 2 Inference
	- No OpenAI keys necessary
- React Codebase Generation
- Memory
	- Vector search for historically successful ideas paired with intuitions.
	- Previous criticisms are utilized for investor approvals
- Lean Startup concepts
	- Utilizes lean startup methodologies (pivot, tight mvp build loop)

# How to use it
Please understand you need to have a quality GPU that can load the LLama 2 13b parameter chat model. Hpwever, I built this all on Google Colab and think this is a great way to get around the costs of AI Agents + GPT-4.


### Run from source
If you want to run from source run these commands. (*After getting access to llama 2 and logging into huggingface-cli*)

Install
```
$ pip3 install -r requirements.txt
```

Run the main loop
```
$ python3 main.py
```

### Better option for quick testing
Here's a Google [Colab](https://colab.research.google.com/drive/1Piw69Bs6aQUj55jTdBHQcCHdM9ZSDpLa?usp=sharing) with the code for you to play with

# TODO
- Fine-tune a llama 2 chat model to be better at coding react. So far it's ok but needs some bug fixing more often than not
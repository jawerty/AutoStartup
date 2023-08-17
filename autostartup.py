from agent import Agent

class AutoStartup(Agent):
  def __init__(self, react_engineer, prompt, memory):
    super().__init__()
    self.react_engineer = react_engineer
    self.prompt = prompt
    self.memory = memory

  def parse_pivot_result(self, result):
    pivot_result = result[result.index("[/INST]"):]
    print("pivot_result", pivot_result)
    new_idea = None
    new_idea_tag = "New Business Idea:"

    for line_item in pivot_result.split("\n"):
      if new_idea_tag in line_item:
        new_idea = line_item[line_item.index(new_idea_tag) + len(new_idea_tag):].strip()
        break

    return new_idea

  def parse_mvp_idea_result(self, result):
    mvp_idea_result = result[result.index("[/INST]"):]
    print("mvp_idea_result", mvp_idea_result)
    product_idea = None
    product_idea_tag = "PRODUCT:"

    for line_item in mvp_idea_result.split("\n"):
      if product_idea_tag in line_item:
        product_idea = line_item[line_item.index(product_idea_tag) + len(product_idea_tag):].strip()
        break

    return product_idea

  def parse_business_plan_approval_result(self, result):
    business_plan_approval_result = result[result.index("[/INST]"):]
    print("business_plan_approval_result", business_plan_approval_result)
    answer = None
    answer_tag = "ANSWER:"

    for line_item in business_plan_approval_result.split("\n"):
      if answer_tag in line_item:
        answer = line_item[line_item.index(answer_tag) + len(answer_tag):].strip()
        break

    return answer

  def parse_criticisms_result(self, result):
    criticisms_result = result[result.index("[/INST]"):]

    line_item_sep = "- "

    criticisms_block = criticisms_result[criticisms_result.index('Criticisms:'):criticisms_result.index('New Business Plan:')]
    criticisms = []
    for line_item in criticisms_block.split("\n"):
      line_item = line_item.strip()
      if line_item_sep in line_item:
        criticisms.append(line_item[line_item.index(line_item_sep) + len(line_item_sep):])

    business_block = criticisms_result[criticisms_result.index('New Business Plan:'):]
    business_plan = []
    for line_item in business_block.split("\n"):
      line_item = line_item.strip()
      if line_item_sep in line_item:
        business_plan.append(line_item[line_item.index(line_item_sep) + len(line_item_sep):])

    print("Criticisms:")
    for item in criticisms:
      print("- ", item)

    print("New Business Plan:")
    for item in business_plan:
      print("- ", item)

    return business_plan, criticisms

  def parse_business_plan_result(self, result):
    business_plan_result = result[result.index("[/INST]"):]
    business_plan_items = []

    line_item_sep = "- "
    for line_item in business_plan_result.split("\n"):
      line_item = line_item.strip()
      if line_item_sep in line_item:
        business_plan_items.append(line_item[line_item.index(line_item_sep) + len(line_item_sep):])

    return business_plan_items

  def parse_idea_result(self, result):
    # print(result)
    idea_result = result[result.index("[/INST]"):]
    name = None
    branding = None
    idea = None
    for line_item in result.split("\n"):
      line_item = line_item.strip()
      name_tag = "NAME:"
      branding_tag = "BRANDING_COLORS:"
      idea_tag = "IDEA:"
      if name_tag in line_item:
        name = line_item[line_item.index(name_tag) + len(name_tag):].strip()
      elif branding_tag in line_item:
        branding = line_item[line_item.index(branding_tag) + len(branding_tag):].strip()
      elif idea_tag in line_item:
        idea = line_item[line_item.index(idea_tag) + len(idea_tag):].strip()

    return {
        "idea": idea,
        "branding": branding,
        "name": name
    }

  def pivot(self, business_plan, idea):
    pivot_prompt = self.prompt.get_pivot_prompt(business_plan, idea)
    pivot_result = self.generate(pivot_prompt)
    return self.parse_pivot_result(pivot_result)

  def criticism_loop(self, business_plan, limit=5, i=1):
      if limit == i:
        print("Criticism loop hit it's limit. Your business is approved anyway...")
        return business_plan

      print("\n\nCriticizing your business plan...\n")
      criticism_prompt = self.prompt.get_criticisms_prompt(business_plan)
      criticism_result = self.generate(criticism_prompt)
      new_business_plan, criticisms = self.parse_criticisms_result(criticism_result)
       # original business plan and criticisms
      self.memory.add_business_plan_history(new_business_plan, criticisms)

      print("\n\nSubmitting your new business plan for approval...")
      business_plan_approval_prompt = self.prompt.get_business_plan_approval_prompt(new_business_plan, history=self.memory.get_business_plan_history())
      business_plan_approval_result = self.generate(business_plan_approval_prompt)

      answer = self.parse_business_plan_approval_result(business_plan_approval_result)
      if answer is None:
        return False

      if answer.lower() == "yes":
        return new_business_plan
      else:
        print("Business plan did not pass approval. Criticizing again...")
        return self.criticism_loop(new_business_plan, limit=limit, i=i+1)

  def generate_code(self, product_idea, name, branding):
    self.react_engineer.run(idea=product_idea, name=name, branding=branding)

  def idea_loop(self, intuition, pivot_idea=None):
    def reiterate(message):
      print(message)
      x = input("$ Try again? [y/n]")
      if x == "y":
        return self.idea_loop(intuition)
      else:
        return False

    if pivot_idea:
      idea_response = pivot_idea
      idea = pivot_idea['idea']
    else:
      idea_prompt = self.prompt.get_idea_prompt(intuition, self.memory)
      idea_result = self.generate(idea_prompt)
      idea_response = self.parse_idea_result(idea_result)
      idea = idea_response["idea"]

    if idea is None:
      return reiterate("Couldn't think of an idea...")

    print("Here's the new idea")
    print("Idea:", idea)
    print("Name:", idea_response["name"])
    print("Branding:", idea_response["branding"])
    print('\n')
    print("Scheming a business plan...")
    business_plan_prompt = self.prompt.get_business_plan_prompt(idea)
    business_plan_result = self.generate(business_plan_prompt)
    business_plan_items = self.parse_business_plan_result(business_plan_result)
    if len(business_plan_items) == 0:
      return reiterate("Couldn't think of a business plan...")
    print("Your business plan:")
    for item in business_plan_items:
      print("- ", item)

    # try:
    criticism_result  = self.criticism_loop(business_plan_items, limit=1)
    # except:
    #   criticism_result = False

    if criticism_result == False:
      return reiterate("Business plan could not be properly criticized.")

    print("\nYour business idea passed my investors approval!\n")
    business_plan = criticism_result
    print("Developing the MVP idea...")

    mvp_idea_prompt = self.prompt.get_mvp_idea_prompt(business_plan)
    mvp_idea_result = self.generate(mvp_idea_prompt)
    product_idea = self.parse_mvp_idea_result(mvp_idea_result)

    # storing and encoding for further use

    memory.store_intution_idea(intuition, product_idea)
    print("Product idea:", product_idea)
    self.generate_code(product_idea, idea_response["name"], idea_response["branding"])

    # do pivot
    print("Check out your code in the react-output/ folder\n\n")
    x = input("$ Do you want to pivot? [y/n]")
    if x == "y":
      print("Figuring out new product idea...")
      new_idea = self.pivot(business_plan, product_idea)
      return self.idea_loop(intuition, pivot_idea=idea_response)
    else:
      return True

    print("AutoStartup has built you a project! Go on and crush!")

  def run(self):
    print("$ I am AutoStartup. Your personal startup creator. I will think of an idea for a startup based on your intutions.\n\nTell me your intution starting with \"I think\"")
    initial_intutition = input("$ ")
    self.idea_loop(initial_intutition)
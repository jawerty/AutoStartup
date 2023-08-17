from sentence_transformers import SentenceTransformer, util

class Memory():
  def __init__(self):
    self.model = SentenceTransformer('all-MiniLM-L6-v2')
    self.business_plan_history = []

    # get the most similar intuition and return the idea to use as an example in the input
    self.intuition_store = []

  def store_intution_idea(self, intution, idea):
    embeddings = self.model.encode(intution)
    self.intuition_store.append({
        "embeddings": embeddings,
        "intution": intution,
        "idea": idea
    })

  def search_intutions(self, intutiton):
    if len(self.intuition_store) == 0:
      return None

    new_intutiton_embedding = self.model.encode(intutiton)

    for stored_intutiton, i in enumerate(self.intuition_store):
      self.intuition_store[i]['score'] = util.dot_score(new_intutiton_embedding, stored_intutiton["embedding"]).item()

    return list(sorted(self.intuition_store, lambda x: x['score'], reverse=True))[0]

  def add_business_plan_history(self, business_plans, criticisms):
    history_item = ""
    history_item += "Business Plan:"
    for item in business_plans:
      history_item += "- " + item + "\n"

    if criticisms:
      history_item += "Criticisms:"
      for item in criticisms:
        history_item += "- " + item + "\n"

    self.business_plan_history.append(history_item)

  def get_business_plan_history(self):
    return self.business_plan_history[:3]

  def clear_business_plan_history(self):
    self.business_plan_history = []
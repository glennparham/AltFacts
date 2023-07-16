
from paperqa import Docs

# get a list of paths

docs = Docs()
for d in my_docs:
    docs.add(d)

answer = docs.query("What manufacturing challenges are unique to bispecific antibodies?")
print(answer.formatted_answer)
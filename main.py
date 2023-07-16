from typing import List 

import os

os.environ['OPENAI_API_KEY'] = open('.env').read().strip()

class Claim:

    def __init__(self, claim_text:str):
        from paperqa import Answer
        self.claim_text = claim_text
        self.claim_id = self.generate_claim_id()
        self.answer: Answer
    
    def generate_claim_id(self) -> str:
        # generate a uuid
        import uuid
        return str(uuid.uuid4())
    
    def verify_claim(self):
        from paperqa import Docs
        import pickle

        with open("my_docs.pkl", "rb") as f:
            docs = pickle.load(f)
        
        answer = docs.query(self.claim_text)
        # print(answer.answer)
        self.answer = answer
        return answer

    

class AltFacts:

    def __init__(self, generated_text:str, source_documents:List[str]):
        self.generated_text = generated_text
        self.source_documents= source_documents
        self.extracted_claims: List[Claim] = []


    def extract_claims(self) -> List[Claim]:
        import openai
        prompt = "Context: " + self.generated_text + "\nWhat are a list of claims that could be fact checked?:"
        openai.api_key = "***"

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150,
            n=1,  # Specify the number of claims you want to generate
            stop=None,
            temperature=0.8
        )
        raw_claims = response['choices'][0]['text'].strip()
        
        claims = raw_claims.split("\n")
        extracated_claims = []
        for claim in claims:
            extracated_claims.append(Claim(claim))
        self.extracted_claims=extracated_claims
        return extracated_claims

    def get_extracted_claims(self) -> List[Claim]:
        return self.extracted_claims
    
    def get_extracted_claims_str(self) -> List[str]:
        return list(map(lambda x: x.claim_text+"\n", self.extracted_claims))

    def get_source_documents_filenames(self) -> List[str]:
        # iterate over source_documents and append "/sample_pdfs/" to each and return array
        return list(map( lambda x: "/sample_pdfs/"+x,self.source_documents))
    
    def generate_pandas_dataframe(self) -> str:
        import pandas as pd
        
        # Create a Pandas dataframe with the following columns: claim_id (uuid), claim_text, source_text, source_location
        # df = pd.DataFrame([])
        dics = []
        # Iterate over each claim, and append a row to the dataframe
        for claim in self.extracted_claims:
            # print(claim.claim_id, claim.claim_text)
            
            if(claim.answer.contexts):
                for context in claim.answer.contexts:
                    dics.append( {'claim_id':claim.claim_id,'claim_text':claim.claim_text, "justification": context.context,"source_text":context.text.text,"source_text_location":context.text.name,"credibility_score":context.score})
            else:
                dics.append( {'claim_id':claim.claim_id,'claim_text':claim.claim_text, "justification": "No justification found","source_text":"No source text found","source_text_location":"No source text location found","credibility_score":"No credibility score found"})
        df = pd.DataFrame(dics) 
            
        df.to_csv('claims.csv', index=False)
        return "Generated"



    def answer_claims(self):

        from paperqa import Docs
        import pickle

        with open("my_docs.pkl", "rb") as f:
            docs = pickle.load(f)
        
        claim_answers = []
        for claim in self.extracted_claims:
            claim_answers.append(claim.verify_claim())
        return claim_answers
    
if __name__ == '__main__':

    ### To run this, run `python3 main.py` in the interpreter
    print("\n✅ Initializing AltFacts...\n")
    generated_text = "On September 7, 2016 said '[O]ne of the first things we must do is to enforce all classification rules and to enforce all laws relating to the handling of classified information. In January 2024, former President Trump said 'please don't hate on me.'"
    source_documents = ["trump_indictment.pdf"]
  
    altfacts_instance = AltFacts(generated_text=generated_text,source_documents=source_documents)

    print("Here are the underlying source documents: ", altfacts_instance.get_source_documents_filenames())

    ## Extract the claims from the original generated text.
    print("\n⌛ Now extracting the claims of the generated text...\n")
    altfacts_instance.extract_claims()
    print("✅ Extracted Claims:\n", altfacts_instance.get_extracted_claims_str())

    ## Iterate over the claims and pass through paperqa
    print("\n\n⌛ Now verifying the claims...")
    answers = altfacts_instance.answer_claims()

    print("\n\n✅ Claims have been verified!")

    print("\n⌛Now writing verifications to CSV...\n")
    altfacts_instance.generate_pandas_dataframe()

    print("\n\n✅ CSV has been generated!\n")


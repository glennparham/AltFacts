from typing import List 

import os
import sys
# import from .env file

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

    # Should return a list of claims (strings). for now filler text. make sure it's strongly typed
    def extract_claims(self) -> List[Claim]:
        # Sample: Trump Indictment
        # Sample Claim 1 [True]: On September 7, 2016 said "“[O]ne of the first things we must do is to enforce all classification rules and to enforce all laws relating to the handling of classified information."
        # Sample Claim 2 [False]: In January 2024, former President Trump said 'please don't hate on me.'
        extracted_claims =  [Claim("On September 7, 2016 said '[O]ne of the first things we must do is to enforce all classification rules and to enforce all laws relating to the handling of classified information."),Claim("In January 2024, former President Trump said 'please don't hate on me.'")]
        self.extracted_claims = extracted_claims
        return self.extracted_claims

    def get_extracted_claims(self) -> List[Claim]:
        return self.extracted_claims
    
    def get_extracted_claims_str(self) -> List[str]:
        return list(map(lambda x: x.claim_text, self.extracted_claims))

    def get_source_documents_filenames(self) -> List[str]:
        # iterate over source_documents and append "/sample_pdfs/" to each and return array
        return list(map( lambda x: "/sample_pdfs/"+x,self.source_documents))
    
    def generate_pandas_dataframe(self) -> str:
        import pandas as pd
        
        # Create a Pandas dataframe with the following columns: claim_id (uuid), claim_text, source_text, source_location
        df = pd.DataFrame()
        
        # Iterate over each claim, and append a row to the dataframe
        for claim in self.extracted_claims:
            print(claim.claim_id, claim.claim_text)
            temp_dic = {'claim_id':claim.claim_id,'claim_text':claim.claim_text}    
            df = df.append(temp_dic, ignore_index=True)
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
    print("\nInitializing AltFacts...\n")
    generated_text = "HERE ARE SOME FALSE CLAIMS!!!!"
    source_documents = ["trump_indictment.pdf"]
    altfacts_instance = AltFacts(generated_text=generated_text,source_documents=source_documents)

    print("Here are the underlying source documents: ", altfacts_instance.get_source_documents_filenames())

    ## Extract the claims from the original generated text.
    print("\nNow extracting the claims of the generated text...")
    altfacts_instance.extract_claims()
    print("Extracted Claims:\n", altfacts_instance.get_extracted_claims_str())

    ## Iterate over the claims and pass through paperqa
    print("\n\nNow answering the claims...")
    answers = altfacts_instance.answer_claims()

    print("\nNow generating a Pandas dataframe...")
    altfacts_instance.generate_pandas_dataframe()


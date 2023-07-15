from typing import List 

class AltFacts:

    def __init__(self, generated_text:str, source_documents:List[str]):
        self.generated_text = generated_text
        self.source_documents= source_documents
        self.extracted_claims = None

    # Should return a list of claims (strings). for now filler text. make sure it's strongly typed
    def extract_claims(self) -> List[str]:
        # Sample: Trump Indictment
        # Sample Claim 1 [True]: On September 7, 2016 said "“[O]ne of the first things we must do is to enforce all classification rules and to enforce all laws relating to the handling of classified information."
        # Sample Claim 2 [False]: In January 2024, former President Trump said 'please don't hate on me.'
        extracted_claims =  ["On September 7, 2016 said '[O]ne of the first things we must do is to enforce all classification rules and to enforce all laws relating to the handling of classified information.',In January 2024, former President Trump said 'please don't hate on me.'"]
        self.extracted_claims = extracted_claims
        return self.extracted_claims

    def get_extracted_claims(self) -> List[str]:
        return self.extracted_claims

    def get_source_documents_filenames(self) -> List[str]:
        # iterate over source_documents and append "/sample_pdfs/" to each and return array
        return list(map( lambda x: "/sample_pdfs/"+x,self.source_documents))
    



if __name__ == '__main__':
    print("\nInitializing AltFacts...\n")
    generated_text = "HERE ARE SOME FALSE CLAIMS!!!!"
    source_documents = ["trump_indictment.pdf"]
    altfacts_instance = AltFacts(generated_text=generated_text,source_documents=source_documents)

    print("Here are the underlying source documents: ", altfacts_instance.get_source_documents_filenames())

    ## Extract the claims from the original generated text.
    print("\nNow extracting the claims of the generated text...")
    altfacts_instance.extract_claims()
    print("Extracted Claims:\n", altfacts_instance.get_extracted_claims())



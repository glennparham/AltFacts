from typing import List 

class AltFacts:

    def __init__(self, generated_text:str, source_documents:List[str]):
        self.generated_text = generated_text
        self.source_documents= source_documents

    # Should return a list of claims (strings). for now filler text. make sure it's strongly typed
    def extract_claims(self) -> List[str]:
        return ["This is a false claim", "This is another false claim"]


    def get_source_documents_names(self) -> List[str]:
        # iterate over source_documents and append "/sample_pdfs/" to each and return array

        return list(map( lambda x: "/sample_pdfs/"+x,self.source_documents))


if __name__ == '__main__':
    print("Initializing AltFacts...")
    generated_text = "HERE ARE SOME FALSE CLAIMS!!!!"
    source_documents = ["trump_indictment.pdf"]
    altfacts_instance = AltFacts(generated_text=generated_text,source_documents=source_documents)

    print("Here are the underlying source documents...", altfacts_instance.get_source_documents_names())


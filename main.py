from typing import List 

class AltFacts:

    def __init__(self, generated_text:str):
        self.generated_text = ""

    # Shoule return a list of claims (strings). for now filler text. make sure it's strongly typed
    def extract_claims(self) -> List[str]:
        return ["This is a false claim", "This is another false claim"]

    

if __name__ == '__main__':
    print("Initializing AltFacts...")
    AltFacts("HERE ARE SOME FALSE CLAIMS!!!!")


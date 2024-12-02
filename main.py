from fastapi import FastAPI
import uvicorn
import random
import pyiwn
from pyiwn import Language
from typing import Optional
from fastapi import FastAPI, Query
# Initialize FastAPI app
app = FastAPI()

# Initialize IndoWordNet
iwn = pyiwn.IndoWordNet(lang=Language.HINDI)

# Your get_random_hindi_word function (assuming it's working)
def get_random_hindi_word(length=5):
    all_synsets = iwn.all_synsets()
    words = []
    for synset in all_synsets:
        for lemma in synset.lemmas():
            if len(lemma.name()) == length:
                words.append(lemma.name())
    if words:
        return random.choice(words)
    else:
        return None
def get_definition(word):
    synsets = iwn.synsets(word)
    if synsets:
        # Try to get gloss, if not available, get examples
        description = synsets[0].gloss() or synsets[0].examples()
        
        # If both are missing, get hypernyms (broader categories)
        if not description:
            hypernyms = synsets[0].hypernyms()
            if hypernyms:
                description = [h.lemmas()[0].name() for h in hypernyms]  # Get hypernym names

        # If everything else is missing, just return the word itself
        if not description:
            description = word

        return description
    else:
        return None
    
# Create an endpoint
@app.get("/random_hindi_word/")
async def random_word(length: Optional[int] = Query(5, description="Length of the word (default is 5)")):
    word = get_random_hindi_word(length)
    if word:
        definition = get_definition(word)
        return {"random_hindi_word": word, "description": definition}
    else:
        return {"message": f"No Hindi words of length {length} found."}

# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Run on port 8000

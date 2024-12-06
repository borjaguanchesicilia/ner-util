import re
from spacy.language import Language
from spacy.tokens import Doc

@Language.component("normalize_text")
def normalize_text(doc):
    texto = re.sub(f"={4,}", "=", doc.text)
    return Doc(doc.vocab, words=texto.split(), spaces=[True] * len(texto.split()))
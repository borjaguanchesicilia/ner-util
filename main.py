from ner_project.ner_util import NerUtil
from ner_project.common import MODELS

if __name__ == "__main__":
    ner_util = NerUtil("./data/inputs/esp.testb")
    ner_util.remove_named_entities()

    for model_id in list(MODELS.keys()):
        ner_util.load_spacy_model(model_id)
        ner_util.tokenize_text()
        ner_util.save_annotated_results(f"./data/outputs/{MODELS[model_id]}_spacy.txt")
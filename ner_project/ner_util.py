import spacy
import re
from .common import ENTITIES, MODELS
from .utils.common_utils import read_file
from .utils.normalizer import normalize_text

class NerUtil():
    """
    Clase para procesar y etiquetar entidades en un texto utilizando Spacy.
    """

    def __init__(self, file_path):
        """
        Inicializa la clase NerUtil.
        
        Argumentos:
        file_path (str): Ruta del archivo de entrada que contiene el texto a procesar.
        
        La función lee el archivo, elimina las líneas vacías y prepara el texto para su procesamiento.
        """

        self._found_entities = []
        self._plain_text = ""
        self._text = [line for line in read_file(file_path) if line != "\n"]


    def load_spacy_model(self, model):
        """
        Carga el modelo de Spacy especificado.
        
        Argumentos:
        model (int): Número que representa el modelo de Spacy a cargar:
            1. Modelo es_core_news_sm
            2. Modelo es_core_news_md
            3. Modelo es_core_news_lg
        
        Este método carga el modelo de Spacy indicado y añade el componente de normalización.
        """

        self._model = MODELS[model]
        self._model_loaded = spacy.load(self._model)
        self._model_loaded.add_pipe("normalize_text", first=True)


    def tokenize_text(self):
        """
        Tokeniza el texto utilizando el modelo cargado de Spacy.
        
        Este método convierte el texto plano en tokens utilizando el modelo de Spacy previamente cargado.
        Los tokens generados se almacenan en el atributo _spacy_doc_loaded, que es un objeto de tipo
        spacy.tokens.Doc, que contiene información sobre los tokens, sus etiquetas y las entidades asociadas.
        """

        self._spacy_doc_loaded = self._model_loaded(self._plain_text)
    

    def remove_named_entities(self):
        """
        Elimina las entidades nombradas del texto.
        
        Este método identifica y elimina las entidades nombradas del texto, basándose en las entidades
        definidas en ENTITIES. El texto modificado sin las entidades nombradas se guarda como texto
        plano y las entidades encontradas son almacenadas en una lista.
        """

        entity_pattern = re.compile(rf"(?:^|\s)({'|'.join(map(re.escape, ENTITIES))})\b")

        for line in self._text:
            found_in_line = entity_pattern.findall(line)
            if len(found_in_line) != 0:
                self._found_entities.append(found_in_line[0])
                line = entity_pattern.sub("", line)

            self._plain_text += line
            
        self._plain_text = " ".join(self._plain_text.split())
        print(f"El fichero tiene {len(self._plain_text)} tokens.")
        print(f"Se han encontrado {len(self._found_entities)} entidades.")


    def save_annotated_results(self, file_name):
        """
        Guarda los resultados anotados en un archivo.
        
        Argumentos:
        file_name (str): Ruta del archivo donde se guardarán los resultados anotados.
        
        Este método recorre los tokens generados por Spacy, asigna las etiquetas de las entidades
        (si las hay) y guarda el texto del token junto con su etiqueta (entidad) en el archivo especificado.
        """

        i = 0
        with open(file_name, "w", encoding="UTF-8") as resultado:
            for token in self._spacy_doc_loaded:
                if token.ent_iob_ != "O":
                    etiqueta = f"{token.ent_iob_}-{token.ent_type_}"
                else:
                    etiqueta = token.ent_iob_

                resultado.write(f"{token.text} {self._found_entities[i]} {etiqueta}\n")
                i += 1
__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

import argparse
from src.rag.ragCLFaiss import ragCLFaiss
import utils.CONST as C
import utils.FUNCTIONS as F 

"""
    Manages Meta FAISS Interactions (search & store)
    usage: RagFaiss [-h] 
                    [-action {memsearch,indexsearch,store}] 
                    [-embprompt {JSON with the prompt embeddings}] 
                    [-embchunks {JSON with the chunks embeddings}]
                    [-nearest {Number of nearest chunks}] 
                    [-faissname {Name of the FAISS index}] 
                    [-faisspath {Where to store the FAISS index and data}] 
                    [-nfile {list of the nearest chunks / json}] 

    3 Usages :
        * store -> Index/Store a PDF content : Mandatory parameters: -embchunks / -faissname / -faisspath
        * indexsearch -> Search on an existing index: Mandatory parameters: -embprompt / -faissname / -faisspath
        * memsearch -> Similarity search with PDF content (no index): -embchunks / -embchunks
"""

def main():
    myRag = ragCLFaiss()
    parser = argparse.ArgumentParser()
    try:
        parser.add_argument("-" + C.ARG_FAISSACTION[0], help=C.ARG_FAISSACTION[1], required=False, 
                            choices=[C.ARG_FAISSACTION_VALMSEARCH, C.ARG_FAISSACTION_VALISEARCH, C.ARG_FAISSACTION_VALSTORE])
        parser.add_argument("-" + C.ARG_EMBEDDINGS_PT[0], help=C.ARG_EMBEDDINGS_PT[1], required=False)
        parser.add_argument("-" + C.ARG_EMBEDDINGS_CK[0], help=C.ARG_EMBEDDINGS_CK[1], required=False)
        parser.add_argument("-" + C.ARG_NEAREST[0], help=C.ARG_NEAREST[1], required=False, type=int, default=C.SM_DEFAULT_NEAREST)
        parser.add_argument("-" + C.ARG_FAISSNAME[0], help=C.ARG_FAISSNAME[1], required=False, default=C.FAISS_DEFAULT_NAME)
        parser.add_argument("-" + C.ARG_FAISSPATH[0], help=C.ARG_FAISSPATH[1], required=False, default=C.FAISS_DEFAULT_STORE)
        parser.add_argument("-" + C.ARG_NEARESTFILE[0], help=C.ARG_NEARESTFILE[1], required=False)
        args = vars(parser.parse_args())
        myRag.setCLIArgs(args)

        if (args[C.ARG_FAISSACTION[0]] == C.ARG_FAISSACTION_VALMSEARCH):
            # Memory search / need -> ARG_EMBEDDINGS_CK / ARG_EMBEDDINGS_PT
            vChunks = F.readJsonFromFile(args[C.ARG_EMBEDDINGS_CK[0]])
            vPrompt = F.readJsonFromFile(args[C.ARG_EMBEDDINGS_PT[0]])
            myRag.add(vChunks)
            similars = myRag.search(args[C.ARG_NEAREST[0]], vPrompt)
            F.writeToFile(args[C.ARG_NEARESTFILE[0]], similars[C.JST_TEXT].to_json())

        elif (args[C.ARG_FAISSACTION[0]] == C.ARG_FAISSACTION_VALISEARCH):
            # Index search / need -> ARG_EMBEDDINGS_PT / ARG_FAISSNAME / ARG_FAISSPATH
            vPrompt = F.readJsonFromFile(args[C.ARG_EMBEDDINGS_PT[0]])
            myRag.indexName = args[C.ARG_FAISSNAME[0]]
            myRag.load(args[C.ARG_FAISSPATH[0]])
            similars = myRag.search(args[C.ARG_NEAREST[0]], vPrompt)
            F.writeToFile(args[C.ARG_NEARESTFILE[0]], similars[C.JST_TEXT].to_json())

        elif (args[C.ARG_FAISSACTION[0]] == C.ARG_FAISSACTION_VALSTORE):
            # Calculate and Store index / need -> ARG_EMBEDDINGS_CK / ARG_FAISSNAME / ARG_FAISSPATH
            myRag.indexName = args[C.ARG_FAISSNAME[0]]
            vChunks = F.readJsonFromFile(args[C.ARG_EMBEDDINGS_CK[0]])
            myRag.add(vChunks)
            myRag.save(args[C.ARG_FAISSPATH[0]])
        else:
            raise Exception("No action selected, please select search or store")

        myRag.CLI_output(C.OUT_SUCCESS)

    except Exception as e:
        parser.print_help()
        myRag.CLI_output(C.OUT_ERROR, True, str(e))
        
if __name__ == "__main__":
    main()
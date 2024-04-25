__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

import argparse
from src.rag.ragCLChromadb import ragCLChromadb
import utils.CONST as C
import utils.FUNCTIONS as F 

"""
    Manages Chroma DB Interactions (search & store)
    Launch Chroma DB server via:
        $ chroma run --host localhost --port 8000 --path D:/chromadb
        
    usage: RagChromaDB  -h, --help            show this help message and exit
                        -action {store,search} Action to execute on the Chroma DB Engine (store/search)
                        -nearest NEAREST      Faiss Number of nearest chunks to gather for prompting
                        -collection COLLECTION Chroma DB collection name
                        -nfile NFILE          JSON file path which contains the nearest chunks/texts
                        -embprompt EMBPROMPT  JSON file path which contains the data and embeddings for the prompt
                        -embchunks EMBCHUNKS  JSON file path which contains the data and embeddings for the chunks
    2 Usages :
        * store -> Index/Store a PDF content : Mandatory parameters: -embchunks / -collection / -path
        * search -> Search on an existing index: Mandatory parameters: -embprompt / -collection / -path
"""

def main():
    myRag = ragCLChromadb()
    parser = argparse.ArgumentParser()
    try:
        parser.add_argument("-" + C.ARG_CDB_ACTION[0], help=C.ARG_CDB_ACTION[1], required=False, 
                            choices=[C.ARG_CDB_VALSTORE, C.ARG_CDB_VALSEARCH])
        parser.add_argument("-" + C.ARG_NEAREST[0], help=C.ARG_NEAREST[1], required=False, type=int, default=C.SM_DEFAULT_NEAREST)
        parser.add_argument("-" + C.ARG_CDB_COLLECTION[0], help=C.ARG_CDB_COLLECTION[1], required=False, default=C.CDB_DEFAULT_COLLECTION)
        parser.add_argument("-" + C.ARG_NEARESTFILE[0], help=C.ARG_NEARESTFILE[1], required=False)
        parser.add_argument("-" + C.ARG_EMBEDDINGS_PT[0], help=C.ARG_EMBEDDINGS_PT[1], required=False)
        parser.add_argument("-" + C.ARG_EMBEDDINGS_CK[0], help=C.ARG_EMBEDDINGS_CK[1], required=False)
        parser.add_argument("-" + C.ARG_CDB_HOST[0], help=C.ARG_CDB_HOST[1], required=False, default=C.CDB_DEFAULT_HOST)
        parser.add_argument("-" + C.ARG_CDB_PORT[0], help=C.ARG_CDB_PORT[1], required=False, default=C.CDB_DEFAULT_PORT, type=int)
        args = vars(parser.parse_args())
        myRag.setCLIArgs(args)

        # Initialize the Chroma DB server
        myRag.initServer(args[C.ARG_CDB_HOST[0]], args[C.ARG_CDB_PORT[0]])
        myRag.collectionName = args[C.ARG_CDB_COLLECTION[0]]

        if (args[C.ARG_CDB_ACTION[0]] == C.ARG_CDB_VALSEARCH):
            # Chroma DB search / need -> ARG_EMBEDDINGS_PT / ARG_FAISSNAME / ARG_FAISSPATH
            vPrompt = F.readJsonFromFile(args[C.ARG_EMBEDDINGS_PT[0]])
            similars = myRag.search(args[C.ARG_NEAREST[0]], vPrompt)
            F.writeToFile(args[C.ARG_NEARESTFILE[0]], similars[C.JST_TEXT].to_json())

        elif (args[C.ARG_CDB_ACTION[0]] == C.ARG_CDB_VALSTORE):
            # Calculate and Store index / need -> ARG_EMBEDDINGS_CK / ARG_FAISSNAME / ARG_FAISSPATH
            vChunks = F.readJsonFromFile(args[C.ARG_EMBEDDINGS_CK[0]])
            myRag.add(vChunks)
        else:
            raise Exception("No action selected, please select search or store")

        myRag.CLI_output(C.OUT_SUCCESS)

    except Exception as e:
        parser.print_help()
        myRag.CLI_output(C.OUT_ERROR, True, str(e))
        
if __name__ == "__main__":
    main()
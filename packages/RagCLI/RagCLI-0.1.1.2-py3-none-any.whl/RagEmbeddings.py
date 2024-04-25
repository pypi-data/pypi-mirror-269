__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

import argparse
from rag.ragCLFaiss import ragCL
import utils.CONST as C
import utils.FUNCTIONS as F 

"""
    Create embeddings:
        1) from a single string (prompt)
        2) from a list of chunks (JSON)
            Format -> {'chunks': ['Transcript of ...', ...] }
    usage: RagEmbeddings [-h] 
                         -embeddings {File and path for the embeddings / JSON}
                         [-chunks {List of chunks in a JSON format}] 
                         [-prompt {prompt}] 
"""



def main():
    parser = argparse.ArgumentParser()
    myRag = ragCL()
    try:
        parser.add_argument("-" + C.ARG_CHUNKS[0], help=C.ARG_CHUNKS[1], required=False, default=C.NULLSTRING)
        parser.add_argument("-" + C.ARG_PROMPT[0], help=C.ARG_PROMPT[1], required=False, default=C.NULLSTRING)
        parser.add_argument("-" + C.ARG_EMBEDDINGS[0], help=C.ARG_EMBEDDINGS[1], required=True)
        args = vars(parser.parse_args())
        myRag.setCLIArgs(args)

        # We must have a bit of chunks or a prompt, otherwise -> Exception
        chunks = F.getCLIArgurment(args, C.ARG_CHUNKS[0])
        prompt = F.getCLIArgurment(args, C.ARG_PROMPT[0])
        if (chunks == C.NULLSTRING and prompt == C.NULLSTRING or 
            chunks != C.NULLSTRING and prompt != C.NULLSTRING):
            raise Exception("A prompt or a list of chunks must be provided, but not both!")

        if (prompt != C.NULLSTRING):
            embeddings = myRag.textEmbeddings(args[C.ARG_PROMPT[0]])
        else:
            # Get the chunks first as list
            chunks = F.readJsonFromFile(args[C.ARG_CHUNKS[0]])
            embeddings = myRag.chunkEmbeddings(chunks)

        # Write the json in a file 
        if (not F.writeJsonToFile(args[C.ARG_EMBEDDINGS[0]],  embeddings)):
            raise Exception("Impossible to write the embeddings in a file")
        
        myRag.CLI_output(C.OUT_SUCCESS)

    except Exception as e:
        parser.print_help()
        myRag.CLI_output(C.OUT_ERROR, True, str(e))
        
if __name__ == "__main__":
    main()
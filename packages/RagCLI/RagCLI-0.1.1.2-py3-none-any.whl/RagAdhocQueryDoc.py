__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

import argparse
from rag.ragCLFaiss import ragCLFaiss
import utils.CONST as C

"""
    usage: RagAdhocQueryDoc [-h] 
                            -prompt {question to the LLM} 
                            -pdf {PDF file and path} 
                            [-temperature {LLM temperature}] 
                            [-chunk_size {Chunk size for char chunking, def 500}]
                            [-chunk_overlap {Chunk overlap for char chunking, def 50}] 
                            [-sep {Chunk separator}] 
                            [-nearest {Number of nearest chunks}] 
                            [-model {Ollama LLM Model}]
                            [-urlbase {Ollama URL}]
"""

def main():
    parser = argparse.ArgumentParser()
    myRag = ragCLFaiss()
    try:
        parser.add_argument("-" + C.ARG_PROMPT[0], help=C.ARG_PROMPT[1], required=True)
        parser.add_argument("-" + C.ARG_PDFFILE[0], help=C.ARG_PDFFILE[1], required=True)
        parser.add_argument("-" + C.ARG_TEMP[0], help=C.ARG_TEMP[1], required=False, type=float, default=C.LLM_DEFAULT_TEMPERATURE) # float(self.temperature.replace(",", "."))
        parser.add_argument("-" + C.ARG_CHUNKSIZE[0], help=C.ARG_CHUNKSIZE[1], required=False, type=int, default=C.CHKS_DEFAULT_SIZE)
        parser.add_argument("-" + C.ARG_CHUNKOVAP[0], help=C.ARG_CHUNKOVAP[1], required=False, type=int, default=C.CHKS_DEFAULT_OVERLAP)
        parser.add_argument("-" + C.ARG_SEP[0], help=C.ARG_SEP[1], required=False, default=C.CHKS_DEFAULT_SEP)
        parser.add_argument("-" + C.ARG_NEAREST[0], help=C.ARG_NEAREST[1], required=False, type=int, default=C.SM_DEFAULT_NEAREST)
        parser.add_argument("-" + C.ARG_MODEL[0], help=C.ARG_MODEL[1], required=False, default=C.OLLAMA_DEFAULT_LLM)
        parser.add_argument("-" + C.ARG_URL[0], help=C.ARG_URL[1], required=False, default=C.OLLAMA_LOCAL_URL)
        args = vars(parser.parse_args())
        myRag.setCLIArgs(args)

        # 1 - Read the pdf content
        pdf = myRag.readPDF(args[C.ARG_PDFFILE[0]], C.ARG_READER_VALPYPDF)
        # 2 - Chunk document
        nb, chunks = myRag.chunk(pdf, C.CHUNK_METHOD.CHARACTER, args[C.ARG_SEP[0]], args[C.ARG_CHUNKSIZE[0]], args[C.ARG_CHUNKOVAP[0]])
        # 3 - Text embeddings
        vPrompt = myRag.textEmbeddings(args[C.ARG_PROMPT[0]])
        # 4 - Chunks embeddings
        vChunks = myRag.chunkEmbeddings(chunks)
        # 5 - Index the chunks
        myRag.add(vChunks)
        # 6 - Similarity Search
        similars = myRag.search(args[C.ARG_NEAREST[0]], vPrompt)
        # 7 - Build prompt
        customPrompt = myRag.buildPrompt(args[C.ARG_PROMPT[0]], similars[C.JST_TEXT])
        # 8 - Ask to the LLM ...
        resp = myRag.promptLLM(customPrompt, args[C.ARG_URL[0]], args[C.ARG_MODEL[0]], args[C.ARG_TEMP[0]])
    
        myRag.CLI_output(resp)

    except Exception as e:
        parser.print_help()
        myRag.CLI_output(C.OUT_ERROR, True, str(e))
        
if __name__ == "__main__":
    main()
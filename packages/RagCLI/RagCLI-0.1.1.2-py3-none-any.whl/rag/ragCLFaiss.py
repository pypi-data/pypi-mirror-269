__author__ = "Benoit CAYLA"
__email__ = "benoit@datacorner.fr"
__license__ = "MIT"

from elements.faiss.FAISSWrapper import FAISSWrapper
from rag.ragCL import ragCL

"""
    This FAISS implementation uses by default the sentence_transformer model (cf. C.EMBEDDING_MODEL) to create and manage embeddings
"""

class ragCLFaiss(ragCL):
    def __init__(self):
        self.__myfaiss = FAISSWrapper()
        self.__indexName = "memory"
        super().__init__()

    @property
    def indexName(self):
        return self.__indexName
    @indexName.setter
    def indexName(self, value):
        self.__indexName = value
        
    def add(self, vChunks):
        """ Add text chunks (embeddings) in the FAISS index
            Format:
            {0: {'text': 'How many jobs Joe Biden wants to create ?', 
                'embedding': array([-6.65125623e-02,  4.26685601e-01, -1.22626998e-01, -1.14275487e-02,
                                    -1.76032424e-01, -2.55425069e-02,  3.19633447e-02,  1.10126780e-02,
                                    -1.75059751e-01,  2.00320985e-02,  3.28031659e-01,  1.18581623e-01,
                                    -9.89666581e-02,  1.68430805e-01,  1.19766712e-01, -7.14423656e-02, ...] 
                },
            1: {'text': '...', 
                'embedding': array([...]
                },
            ...
            }
        Args:
            vChunks (json): chunks with embeddings
        """
        self.__myfaiss.add(vChunks)
        self.addMilestone("ADDTOINDEX", "Add chunks to the FAISS Index")

    def search(self, k, vPrompt):
        """ Makes a search in the FAISS index and returns the k mearest datasets from the prompt

        Args:
            k (int): most k nearest chunks
            vPrompt (json): data and embeddings for the prompt
        Returns:
            DataFrame: List of the most nearest neighbors
        """
        similars = self.__myfaiss.getNearest(vPrompt, k)
        self.addMilestone("SIMILARSEARCH", "Similarity Search executed successfully")
        return similars

    def save(self, path):
        """ Store the FAISS index on the disk
        Args:
            path (str): index path
        Returns:
            _type_: False if error
        """
        try:
            self.addMilestone("FAISSSTORE", "Chunks embeddings indexed and stored successfully")
            self.__myfaiss.save(path, self.__indexName)
            return True
        except Exception as e:
            self.log.error("Error while storing FAISS index: {}".format(e))
            return False
            
    def load(self, path):
        """ Load the FAISS index on the disk
        Args:
            path (str): index path
        Returns:
            _type_: False if error
        """
        try:
            self.addMilestone("FAISSLOAD", "Chunks embeddings loaded successfully")
            self.__myfaiss.load(path, self.__indexName)
            return True
        except Exception as e:
            self.log.error("Error while loading FAISS index: {}".format(e))
            return False


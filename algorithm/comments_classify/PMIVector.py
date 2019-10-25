from collections import Counter
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from sklearn.preprocessing import normalize
from scipy.sparse import linalg

class PMIVector:
    def __init__(self,sentences,back_window=2,front_window=2):
        self.wv = None
        self.nwv = None
        self.tok2indx = dict()
        self.indx2tok = None
        self.sentences = sentences
        self.unigram_counts = Counter()
        self.back_window = back_window
        self.front_window = front_window
        self.skipgram_counts = Counter()

    def train(self,embedding_size=32):
        self._unigram_()
        self._skipgram_()
        self._generate_mat_()
        self._generate_pmi_()

        uu, ss, vv = linalg.svds(self.sppmi_mat, embedding_size)
        unorm = uu / np.sqrt(np.sum(uu*uu, axis=1, keepdims=True))
        vnorm = vv / np.sqrt(np.sum(vv*vv, axis=0, keepdims=True))
        #word_vecs = unorm
        #word_vecs = vnorm.T
        self.wv = uu + vv.T
        self.nwv = self.wv / np.sqrt(np.sum(self.wv*self.wv, axis=1, keepdims=True))
    
    def _unigram_(self):
        for ii, headline in enumerate(self.sentences):
            if ii % 500000 == 0:
                print(f'finished {ii/len(self.sentences):.2%} of lines')
            for token in headline.split():
                unigram_counts[token] += 1
                if token not in self.tok2indx:
                    self.tok2indx[token] = len(self.tok2indx)
        self.indx2tok = {indx:tok for tok,indx in self.tok2indx.items()}

    def _skipgram_(self):
        for iline,line in enumerate(self.sentences):
            sentence = line.split()
            for iword,word in enumerate(sentence):
                ifw = max(0,iword-self.back_window)
                ibw = min(len(sentence),iword+self.front_window)
                indexes = [i for i in range(ifw,ibw) if i!=iword]
                for idx in indexes:
                    try:
                        skipgram = (word,sentence[idx])
                        self.skipgram_counts[skipgram] += 1
                    except Exception as e:
                        print(f'error: {len(sentence)},{idx}',skipgram,e.message)
                        break

    def _generate_mat_(self):
        row_indxs = []
        col_indxs = []
        dat_values = []

        for (tok1, tok2), sg_count in self.skipgram_counts.items():
        #     print(tok1,tok2,sg_count)
            tok1_indx = self.tok2indx[tok1]
            tok2_indx = self.tok2indx[tok2]
                
            row_indxs.append(tok1_indx)
            col_indxs.append(tok2_indx)
            dat_values.append(sg_count)
            
        self.wwcnt_mat = sparse.csr_matrix((dat_values, (row_indxs, col_indxs)))
        self.wwcnt_norm_mat = normalize(self.wwcnt_mat, norm='l2', axis=1)

    def _generate_pmi_(self):
        num_skipgrams = self.wwcnt_mat.sum()
        # for creating sparce matrices
        row_indxs = []
        col_indxs = []

        pmi_dat_values = []
        ppmi_dat_values = []
        spmi_dat_values = []
        sppmi_dat_values = []

        # smoothing
        alpha = 0.75
        nca_denom = np.sum(np.array(self.wwcnt_mat.sum(axis=0)).flatten()**alpha)
        sum_over_words = np.array(self.wwcnt_mat.sum(axis=0)).flatten()
        sum_over_words_alpha = sum_over_words**alpha
        sum_over_contexts = np.array(self.wwcnt_mat.sum(axis=1)).flatten()

        ii = 0
        for (tok1, tok2), sg_count in self.skipgram_counts.items():
            ii += 1
            if ii % 1000000 == 0:
                print(f'finished {ii/len(self.skipgram_counts):.2%} of skipgrams')
            tok1_indx = self.tok2indx[tok1]
            tok2_indx = self.tok2indx[tok2]
            
            nwc = sg_count
            Pwc = nwc / num_skipgrams
            nw = sum_over_contexts[tok1_indx]
            Pw = nw / num_skipgrams
            nc = sum_over_words[tok2_indx]
            Pc = nc / num_skipgrams
            
            nca = sum_over_words_alpha[tok2_indx]
            Pca = nca / nca_denom
            
            pmi = np.log2(Pwc/(Pw*Pc))
            ppmi = max(pmi, 0)
            
            spmi = np.log2(Pwc/(Pw*Pca))
            sppmi = max(spmi, 0)
            
            row_indxs.append(tok1_indx)
            col_indxs.append(tok2_indx)
            pmi_dat_values.append(pmi)
            ppmi_dat_values.append(ppmi)
            spmi_dat_values.append(spmi)
            sppmi_dat_values.append(sppmi)
                
        # pmi_mat = sparse.csr_matrix((pmi_dat_values, (row_indxs, col_indxs)))
        # ppmi_mat = sparse.csr_matrix((ppmi_dat_values, (row_indxs, col_indxs)))
        # spmi_mat = sparse.csr_matrix((spmi_dat_values, (row_indxs, col_indxs)))
        self.sppmi_mat = sparse.csr_matrix((sppmi_dat_values, (row_indxs, col_indxs)))

    def get_vector(self,word):
        indx = self.tok2indx[word]
        return self.nwv.getrow(indx)

    def save(self,filename):
        pass

    def load(self,filename):
        pass
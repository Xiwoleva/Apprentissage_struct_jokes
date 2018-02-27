import numpy as np
import glob
def _clean_words(words, split_possesive=True):
    out = []
    punctuation = None
    
    for word in words:
        word = word.strip()
        word = word.strip("\"“”") # remove quotations, as it is out of the scope of the project

        if (word != "") and word[-1] in ['.',',','!','?',':',';']:
            punctuation = word[-1]
            word = word[:-1]
                
        if (word != ""):
            
            #if start:
            #    word = word.lower()
            
            if word[-1] == "—": # some of the words have this at the end, not sure why...
                out.append(word[:-1])
            
            # fixing contractions
            if word[-3:] == "'re" or word[-3:] == "’re":
                out.append(word[:-3])
                out.append("are")
            elif word[-3:] == "'ve" or word[-3:] == "’ve":
                out.append(word[:-3])
                out.append("have")
            elif word[-2:] == "'s" or word[-2:] == "’s":
                if word[:-2].lower() == "it":
                    out.append(word[:-2])
                    out.append("is")
                elif split_possesive:
                    out.append(word[:-2])
                    out.append("'s")
            elif word[-3:] == "'ll" or word[-3:] == "’ll":
                out.append(word[:-3])
                out.append("will")
            elif word[-2:] == "'m" or word[-2:] == "’m":
                out.append(word[:-2])
                out.append("am")
            elif word[-3:] == "n't" or word[-3:] == "n’t":
                if word.lower() == "ain't":
                    out.append("am")
                    out.append("not")
                else:
                    out.append(word[:-3])
                    out.append("not")
            else :
                out.append(word)

        # split the word from the punctuation. Helps with sentence stucture
        if punctuation is not None:
            out.append(punctuation)
            punctuation = None
            
    return out
    

def load_jokes(file="./conan-jokes-data/output/jokes-all-clean.txt", split_possesive=True):
    X = []
    sub_x = []
    for line in open(file):
        if line.strip() == "":
            if len(sub_x) != 0:
                X.append(np.array(sub_x))
                sub_x = []
        else:
            sub_x = _clean_words(line.strip().split(), split_possesive=split_possesive)
            
    return X


def load_bbc(split_possesive=True):
    files = np.array(glob.glob("./bbc/*/*.txt"))
    idx = np.arange(len(files))
    np.random.shuffle(idx)
    files = files[idx]
    X = []
    for i in idx:
        sub_x = []
        try:
            for line in open(files[i]):
                if line.strip() == "":
                    if len(sub_x) != 0:
                        X.append(np.array(sub_x))
                        sub_x = []
                else:
                    sub_x = _clean_words(line.strip().split(), split_possesive=split_possesive)
        except:
            pass
                
    return X

def load_random(nb_scentences, mu=15, sigma=10):
    words = np.unique(np.hstack([np.unique(np.hstack(load_bbc())), np.unique(np.hstack(load_jokes()))]))
    
    out = []
    for i in range(nb_scentences):
        out.append(words[np.random.randint(words.shape[0], size=max(int(np.random.normal(mu,sigma)),1))])
    return out
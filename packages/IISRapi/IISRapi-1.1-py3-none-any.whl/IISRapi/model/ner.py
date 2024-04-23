import os
import sys
import torch
import re
import flair
import subprocess
from flair.models import SequenceTagger
from flair.data import Sentence
from .data import Data
class IISRner:
    def __init__(self,dev):
        self.pos=[]
        self.model_path=self.get_path()
        if(dev>=0 and torch.cuda.is_available()):
             flair.device = torch.device('cuda:' + str(dev))
        else:
            flair.device = torch.device('cpu')
       
        self.model = self.load_model()
        
    def get_path(self):
        try:
            import IISRner
            path=os.path.join(os.path.dirname(IISRner.__file__),"best-model-ner.pt")
        except ModuleNotFoundError:
            print("Model file not found. Downloading model...")
            model_url="https://github.com/DH-code-space/punctuation-and-named-entity-recognition-for-Ming-Shilu/releases/download/IISRmodel/IISRner-1.0-py3-none-any.whl"
            subprocess.call(["pip", "install", model_url])
            import IISRner
            path=os.path.join(os.path.dirname(IISRner.__file__),"best-model-ner.pt")
        return path

    def load_model(self):
        return SequenceTagger.load(self.model_path)
        
    def __call__(self,texts):
        if isinstance(texts,str):
            result=Data(ori_txt=texts, ret_txt=self.ner(texts),ner_tags=self.pos)
            return result
        elif isinstance(texts,Data):
            result=texts._replace(ori_txt=texts.ori_txt,ret_txt=self.ner(texts.ori_txt),ner_tags=self.pos)
            return result
     
    def ner(self,text):
        seg = text.strip().replace(' ', '　')  # replace whitespace with special symbol
        sent = Sentence(' '.join([i for i in seg.strip()]), use_tokenizer=False)
        self.model.predict(sent)
        temp = []
        for ne in sent.get_labels():
            se = re.search("(?P<s>[0-9]+):(?P<e>[0-9]+)", str(ne))
            la = re.search("(?P<l> ? [A-Z]+)", str(ne))
            start = int(se.group("s"))
            end = int(se.group("e"))
            label = la.group("l")
            texttemp=text[start:end]
            temp.append((start, end, label.strip(),texttemp))
        temp.reverse()
        self.pos=temp
        temp.sort(key=lambda a: a[0], reverse=True)
        for start, end, label, texttemp in temp:
            if len(text[start:end].replace('　', ' ').strip()) != 0:
                text = text[:start] + "<" + label + ">" + text[start:end] + "</" + label + ">" + text[end:]
        result=self.post_processing(text)
        self.pos.reverse()
        return result.strip().replace('　', ' ')
    
    def post_processing(self,word):
        whole = word.split('\n')
        for line in whole:
            for match in reversed(list(re.finditer("<LOC>(.?)</LOC><WEI>(.?)</WEI>", line))):
                start, end = match.start(), match.end()
                line = line[:start] + line[start:end].replace("</LOC><WEI>", "").replace("</WEI>", "</LOC>") + line[end:]
            for match in reversed(list(re.finditer("<WEI>(.?)</WEI><LOC>(.?)</LOC>", line))):
                start, end = match.start(), match.end()
                line = line[:start] + line[start:end].replace("</WEI><LOC>", "").replace("<WEI>", "<LOC>") + line[end:]
            for match in reversed(list(re.finditer("<ORG>(.?)</ORG><(LOC|WEI)>(.?)</(LOC|WEI)><ORG>", line))):
                start, end = match.start(), match.end()
                line = line[:start] + "<ORG>" + re.sub("<[A-Z/]+>", "", line[start:end]) + line[end:]
            for match in reversed(list(re.finditer("<(LOC|WEI|ORG)>(.?)</(LOC|WEI|ORG)><", line))):
                start, end = match.start(), match.end()
                line = line[:start] + line[end - 1:end + 4] + re.sub("<[A-Z/]+>", "", line[start:end - 1]) + line[end + 4:]
            for match in re.finditer("王</PER>", line):
                start, end = match.start(), match.end()
                while line[start] != "<":
                    start -= 1
                line = line[:start] + "<OFF>" + re.sub("<[A-Z/]+>", "", line[start:end]) + "</OFF>" + line[end:]
            for match in re.finditer("[王侯公伯]</(LOC|WEI|ORG)>", line):
                start, end = match.start(), match.end()
                while line[start] != "<":
                    start -= 1
                line = line[:start] + "<OFF>" + re.sub("<[A-Z/]+>", "", line[start:end]) + "</OFF>" + line[end:]
            for match in re.finditer("[王侯公伯]</(LOC|WEI|ORG)>", line):
                start, end = match.start(), match.end()
                while line[start] != "<":
                    start -= 1
                line = line[:start] + "<OFF>" + re.sub("<[A-Z/]+>", "", line[start:end]) + "</OFF>" + line[end:]
            for match in re.finditer("殿</(WEI|ORG)>", line):
                start, end = match.start(), match.end()
                while line[start] != "<":
                    start -= 1
                line = line[:start] + "<LOC>" + re.sub("<[A-Z/]+>", "", line[start:end]) + "</LOC>" + line[end:]
            for match in reversed(list(re.finditer("<(WEI|ORG)>(等|各)", line))):
                start, end = match.start(), match.end()
                while line[end] != ">":
                    end += 1
                line = line[:start] + re.sub("<[A-Z/]+>", "", line[start:end]) + line[end:]
            for match in re.finditer("司</OFF>", line):
                start, end = match.start(), match.end()
                while line[start] != "<":
                    start -= 1
                line = line[:start] + "<ORG>" + re.sub("<[A-Z/]+>", "", line[start:end]) + "</ORG>" + line[end:]
            line = line.replace("<ORG>司</ORG>", "司")
            return line + '\n'
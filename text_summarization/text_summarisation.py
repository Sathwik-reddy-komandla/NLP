import sys


import spacy
from spacy.lang.en.stop_words import STOP_WORDS

from string import punctuation
from heapq import nlargest


text="""
Samsung Group,[3] or simply Samsung (Korean: 삼성; RR: samseong [samsʌŋ]) (stylized as SΛMSUNG), is a South Korean multinational manufacturing conglomerate headquartered in Samsung Digital City, Suwon, South Korea.[1] It comprises numerous affiliated businesses,[1] most of them united under the Samsung brand, and is the largest South Korean chaebol (business conglomerate). As of 2020, Samsung has the eighth highest global brand value.[4]

Samsung was founded by Lee Byung-chul in 1938 as a trading company. Over the next three decades, the group diversified into areas including food processing, textiles, insurance, securities, and retail. Samsung entered the electronics industry in the late 1960s and the construction and shipbuilding industries in the mid-1970s; these areas would drive its subsequent growth. Following Lee's death in 1987, Samsung was separated into five business groups – Samsung Group, Shinsegae Group, CJ Group and Hansol Group, and JoongAng Group.

Notable Samsung industrial affiliates include Samsung Electronics (the world's largest information technology company, consumer electronics maker and chipmaker measured by 2017 revenues),[5][6] Samsung Heavy Industries (the world's second largest shipbuilder measured by 2010 revenues),[7] and Samsung Engineering and Samsung C&T Corporation (respectively the world's 13th and 36th largest construction companies).[8] Other notable subsidiaries include Samsung Life Insurance (the world's 14th largest life insurance company),[9] Samsung Everland (operator of Everland Resort, the oldest theme park in South Korea)[10] and Cheil Worldwide (the world's 15th largest advertising agency, as measured by 2012 revenues).[11][12]

Etymology
According to Samsung's founder, the meaning of the Korean hanja word Samsung (三星) is "three stars". The word "three" represents something "big, numerous and powerful",[13] while "stars" means "everlasting" or "eternal", like stars in the sky.[14][15]

"""
import string
import re
text=re.sub(r'\[.*?\]','',text)
text=re.sub(r'\(.*?\)','',text)
text=re.sub(r'[^\x00-\x7F]+','',text)
text=re.sub(f"[{re.escape(string.punctuation)}]",'',text)

stopwords=list(STOP_WORDS)

nlp=spacy.load('en_core_web_sm')

doc=nlp(text)

tokens=[token.text for token in doc]

word_freq={}

for word in doc:
    if word.text.lower() not in stopwords and word.text.lower() not in punctuation:
        if word.text not in word_freq.keys():
            word_freq[word.text]=1
        else:
            word_freq[word.text]+=1

max_freq=max(word_freq.values())


for word in word_freq.keys():
    word_freq[word]=word_freq[word]/max_freq

sent_tokens=[sent for sent in doc.sents]


sent_scores={}
for sent in sent_tokens:
    for word in sent:
        if word.text in word_freq.keys():
            if sent not in sent_scores.keys():

                sent_scores[sent]=word_freq[word.text]
            else:
                sent_scores[sent]+=word_freq[word.text]


select_len=int(len(sent_tokens)*0.3) if int(len(sent_tokens)*0.3)>0 else 1
print(sent_tokens)


summary=nlargest(select_len,sent_scores,key=sent_scores.get)

final_summary=[word.text for word in summary]
summary=' '.join(final_summary)
print(select_len)

print("length of text :",len(text))
print("length of sumary :",len(summary))



import difflib
import requests
def compare(pg1c,pg2c):
    sim_ratio=difflib.SequenceMatcher(None, pg1c, pg2c).ratio()
    return sim_ratio
url1="https://en.wikipedia.org/Computer_Science"
url2="https://en.wikipedia.org/Information_Retrieval"
pg1=requests.get(url1)
pg1c=pg1.text
pg2=requests.get(url2)
pg2c=pg2.text
score=compare(pg1c,pg2c)
print(score)
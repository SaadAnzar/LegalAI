# from gpt_index import GPTSimpleVectorIndex, SimpleDirectoryReader, GPTListIndex, GPTTreeIndex
# import os

# # Loads all the data from the txts folder
# documents = SimpleDirectoryReader('txts').load_data()

# # builds an index over the documents in the data folder
# index = GPTSimpleVectorIndex(documents)

# index.save_to_disk("/Users/arshad/Desktop/Projects/Legal/api/index/index.json")
# # load from disk
# index = GPTSimpleVectorIndex.load_from_disk('/Users/arshad/Desktop/Projects/Legal/api/index/index.json')

# response = index.query("What type of document it is?", verbose=True, response_mode="default")

# print(response)


# import ai21

# ai21.api_key = "9y72PNOvg2dnqoZsF1d7UGtTGUHlaRG5"

# prompt = "Following is a legal document, summarize it to get a very easy explanation:\n\nLast Will and Testament of Harry James PotterI, Harry James Potter, of 4 Privet Drive, Little Whinging, Surrey, being of sound mind and body, dohereby make, publish, and declare this to be my last will and testament, hereby revoking any and allother wills and codicils made by me.1. Payment of Debts and Expenses. I direct that my executor shall pay all of my just debts,funeral expenses, and the expenses of administration of my estate as soon as possible aftermy death.2. Speciﬁc Bequests. I give, devise and bequeath the following speciﬁc gifts to the followingpersons:● I leave my Invisibility Cloak to my son, Albus Severus Potter● I leave my Firebolt broomstick to my daughter, Lily Luna Potter● I leave my Tales of Beedle the Bard to Hermione Granger● I leave my Snitch to my godson, James Sirius Potter3. Residuary Estate. I give, devise and bequeath all the rest, residue, and remainder of myestate, both real and personal, to my wife, Ginny Weasley Potter4. Executor. I nominate Ron Weasley to serve as executor of this my last will and testament. IfRon Weasley is unable or unwilling to serve, I nominate Hermione Granger to serve asexecutor.5. Governing Law. This will shall be governed by and construed in accordance with the laws ofthe State of Wizarding Britain.IN WITNESS WHEREOF, I have hereunto set my hand and seal on the date and year ﬁrst abovewritten.Harry James PotterSigned, sealed, published and declared by the above-named Harry James Potter, as and for his lastwill and testament, in the presence of us, who at his request, and in his presence, and in thepresence of each other, have subscribed our names as witnesses.Neville LongbottomLuna Lovegood"
# response = ai21.Completion.execute(model='j1-grande', prompt=prompt, maxTokens=1024, temperature=0.5)
# print(response["completions"][0]["data"]["text"].lstrip())

import requests
import json

url = "https://api.ai21.com/studio/v1/experimental/summarize"

payload = {
    "text": "Last Will and Testament of Harry James PotterI, Harry James Potter, of 4 Privet Drive, Little Whinging, Surrey, being of sound mind and body, dohereby make, publish, and declare this to be my last will and testament, hereby revoking any and allother wills and codicils made by me.1. Payment of Debts and Expenses. I direct that my executor shall pay all of my just debts,funeral expenses, and the expenses of administration of my estate as soon as possible aftermy death.2. Speciﬁc Bequests. I give, devise and bequeath the following speciﬁc gifts to the followingpersons:● I leave my Invisibility Cloak to my son, Albus Severus Potter● I leave my Firebolt broomstick to my daughter, Lily Luna Potter● I leave my Tales of Beedle the Bard to Hermione Granger● I leave my Snitch to my godson, James Sirius Potter3. Residuary Estate. I give, devise and bequeath all the rest, residue, and remainder of myestate, both real and personal, to my wife, Ginny Weasley Potter4. Executor. I nominate Ron Weasley to serve as executor of this my last will and testament. IfRon Weasley is unable or unwilling to serve, I nominate Hermione Granger to serve asexecutor.5. Governing Law. This will shall be governed by and construed in accordance with the laws ofthe State of Wizarding Britain.IN WITNESS WHEREOF, I have hereunto set my hand and seal on the date and year ﬁrst abovewritten.Harry James PotterSigned, sealed, published and declared by the above-named Harry James Potter, as and for his lastwill and testament, in the presence of us, who at his request, and in his presence, and in thepresence of each other, have subscribed our names as witnesses.Neville LongbottomLuna Lovegood",
    "documentType": "TEXT",
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "Authorization": "Bearer 9y72PNOvg2dnqoZsF1d7UGtTGUHlaRG5"
}

response = requests.post(url, json=payload, headers=headers)

json_string = response.text
data = json.loads(json_string)
print(data["summaries"][0]["text"])



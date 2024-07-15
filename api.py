####################################################################################


# THIS FILE IS JUST FOR API TESTING !!!!
# THIS FILE IS NOT REQUIRED FOR WORKING OF THE BOT !!! 


#####################################################################################



from googleapiclient import discovery
import json
import os

API_KEY=os.getenv("API_KEY")

while True:

  
   text = input('> ')

   client = discovery.build(
     "commentanalyzer",
     "v1alpha1",
     developerKey=API_KEY,
     discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
     static_discovery=False,
   )

   analyze_request = {
     'comment': { 'text': text },
     'requestedAttributes': {'TOXICITY': {}},
     'languages': ['en', 'hi', 'hi-Latn']
   }

   response = client.comments().analyze(body=analyze_request).execute()
   toxicity = response['attributeScores']['TOXICITY']['summaryScore']['value']
   lan_detected = response['detectedLanguages'][0]
   print( f"Toxicity: {toxicity*100:.2f}%")
   print(f"lang: {lan_detected}")

   if text == "exit":
    break 
    exit()

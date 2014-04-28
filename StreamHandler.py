"""StreamHandler.py

Handler for the Twitter streaming

"""
from tweepy import StreamListener
import json, time, sys, csv, os

class StreamHandler(StreamListener):
	"""
	StreamHandler for Twitter streaming
	
	"""
	
	def __init__(self, confData):
		"""
		Initialize the local variables
		
		Args:
			confData(json): Json object with all the configuration values
		
		"""
		
		self.counter = 0		
		self.outputFolder= confData["Output Folder"]
		self.chunkSize=confData["Tweets"]
        
		
        
        
	def on_data(self, data):
		"""
		When receiving data, split on Warning and Data, rest will be skip.
		Warnings will be shown in command line, data will be written to the csv
		file.
		
		Args:
			data(str): Json received by Twitter Streaming.
		
		"""
        
		if  'in_reply_to_status' in data:
			self.on_status(data)
		elif 'warning' in data:
			warning = json.loads(data)['warnings']
			print warning['message']
			return false




	def on_status(self, status):
		"""
		Handles the tweet received.
		Transforms information received to a JSON object, extract the information
		from the fields and write to a file.
		
		When the number of tweets downloaded is higher than the limit in the configuration,
		the program exits.
	
		Args:
			status(str): Tweet received by Twitter Streaming.
	
		"""
    
		tweetJson = json.loads(status)
    	
		
		tweet_id=tweetJson["id_str"]
		tweet=tweetJson["text"].encode('UTF-8')
		user_language = tweetJson["user"]["lang"]
		
		
		#Write the tweet to a single file with the name as the tweetId and the content as the tweet
		self.singleOutput  = open(self.outputFolder+'//'+tweet_id, 'wb+')
		self.singleOutput.write(tweet)
		self.singleOutput.close()
		
    	  
		self.counter += 1

		#If the number of tweets is reached we finish the program
		if self.counter >= self.chunkSize:
			exit(0)
			

		return

	def on_error(self, status_code):
		"""
		On error, the error is shown in the command line
	
		"""
		sys.stderr.write('Error: ' + str(status_code) + "\n")
		return False
        
        

	def on_timeout(self):
		"""
		On timeout sleeps for 60 seconds and try again.
	
		"""
		sys.stderr.write("Timeout, sleeping for 60 seconds...\n")
		time.sleep(60)
		return 
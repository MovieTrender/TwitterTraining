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
		self.outputFile= confData["Output File"]
		self.outputCommonFolder= confData["Output Common Folder"]
		self.outputSingleFolder= confData["Output Single Folder"]
		self.outputSingleTimeStamp=time.strftime('%Y%m%d-%H%M%S')
		self.chunkSize=confData["Tweets per file"]
        
		#Create the file (with timestamp) for all the Tweets downloaded. 
		self.commonOutput  = csv.writer(open(self.outputCommonFolder+'//'+time.strftime('%Y%m%d-%H%M%S')+'-'+self.outputFile+'.csv', 'wb+'))

		#We dont need headers in the files generated
		#self.output.writerow(["user_id","user_name","user_followers_count","user_friends_count","user_timezone","created_at","tweet"])
		
		#Create the first timeStamp folder for the singles tweets
		os.makedirs(self.outputSingleFolder+'//'+self.outputSingleTimeStamp)
		
        
        
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
		from the fields and write a new row to the CSV file.
		
		When the number of rows in the CSV is higher than the limit in the configuration,
		closes the file and create a new one with the timestamp.
	
		Args:
			status(str): Tweet received by Twitter Streaming.
	
		"""
    
		tweet = json.loads(status)
    	
		user_id=tweet["user"]['id']
		user_name=tweet["user"]['name'].encode('UTF-8')
		user_followers=tweet["user"]['followers_count']
		user_friends=tweet["user"]['friends_count']
		user_timezone=tweet["user"]['time_zone']
		created_at=tweet["created_at"]
		tweet_id=tweet["id_str"]
		tweet=tweet["text"].encode('UTF-8')
		
		#Write the fields extracted to the common file
		self.commonOutput.writerow([tweet_id,user_id,user_name,user_followers,user_friends,user_timezone,created_at,tweet])
		
		#Write the tweet to a single file with the name as the tweetId and the content as the tweet
		self.singleOutput  = open(self.outputSingleFolder+'//'+self.outputSingleTimeStamp+'//'+tweet_id, 'wb+')
		self.singleOutput.write(tweet)
		self.singleOutput.close()
		
    	  
		self.counter += 1

		#If the limit for the file is reached, the file is closed and a new one is opened.
		if self.counter >= self.chunkSize:
			#Create a new common file
			self.commonOutput.close()
			self.commonOutput  = csv.writer(open(self.outputCommonFolder+'//'+time.strftime('%Y%m%d-%H%M%S')+'-'+self.outputFile+'.csv', 'wb+'))
			self.counter = 0
			#Create a new timeStamp folder, and setup the new path
			self.outputSingleTimeStamp=time.strftime('%Y%m%d-%H%M%S')
			os.makedirs(self.outputSingleFolder+'//'+self.outputSingleTimeStamp)
			

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
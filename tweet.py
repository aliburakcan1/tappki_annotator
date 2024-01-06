import requests
import streamlit.components.v1 as components
import random

class Tweet(object):
	def __init__(self, url):
		api = "https://publish.twitter.com/oembed?url={}".format(url)
		response = requests.get(api)
		self.text =response.json()['html']

	def _repr_html_(self):
		return self.text
	
	def get_tweet_id(self):
		return self.tweet_id

	def component(self):
		return components.html(self.text, height=800, scrolling=True)
	

	
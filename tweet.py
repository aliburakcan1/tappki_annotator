import requests
import streamlit.components.v1 as components

class Tweet(object):
	def __init__(self, url):
		try:
			api = "https://publish.twitter.com/oembed?url={}".format(url)
			response = requests.get(api)
			self.text = response.json()['html']
		except:
			self.text =  f"<blockquote class='missing'>This tweet {url} is no longer available.</blockquote>"

	def _repr_html_(self):
		return self.text

	def component(self):
		return components.html(self.text, height=800, scrolling=True)
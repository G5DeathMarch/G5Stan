# G5Stan
G5 Groupme chatbot!

Stan is a chatbot hosted on Heroku. 
He is currently capable of the following commands:

/gif {searchterm}
	-This sends a search term to the giphy API and responds
	to the specified chat with a random gif from the
	API
	
/cheerup
	-This selects a random inspiring line from a local file 
	and sends it to the chat

/helpmestan [command]
	-This will give details about what I can do. The search
	term is used to give more detailed information about a
	certain command. If you don't give me anything to search,
	I'll just tell you all the commands I know.

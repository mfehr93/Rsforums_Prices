# Rsforums_Prices
Contains a web scraper (written in Python 3) that uses regular expressions to find prices of the format &lt;float/int>/&lt;float/int>/.../&lt;float/int>

-Example of a "baseUrl" required for gather(...) and makeGraphs(...): 
	"http://forum.runescape.com/forums.ws?17,18,177,65864498,goto,"
	--The "goto," at the end of the url is necessary at the moment.
	--Future changes may make this requirement unnecessary.

-Of primary importance is modifying the sortLines function to allow for
	steeper price fluctuations that go beyond the ranges currently set.
	--Achieving this may allow other price checking forum threads to be parsed as well.

-Not supported: updates that do not contain all prices in the thread.
	That is, the post with text "Bookmarked - INS WAND 206s" does not update wand price to 206M
	--Part of the problem, here, is that timeLst is a 1-D list.
		Updating the time for the example wand update above would result in an extra time in the list.
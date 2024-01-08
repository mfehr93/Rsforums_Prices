# Rsforums_Prices
Contains a web scraper (written in Python 3) that uses regular expressions to find prices of the format &lt;float/int>/&lt;float/int>/.../&lt;float/int>

-Unfortunately, Runescape forum price reporting is somewhat dead, rendering
	this project somewhat dead as well.

-Example of a "baseUrl" required for gather(...) and makeGraphs(...): 
	"http://forum.runescape.com/forums.ws?17,18,177,65864498,goto,"
	--Future changes may make this requirement unnecessary.

-Of primary importance is modifying the sortLines function to allow for
	steeper price fluctuations that go beyond the ranges currently set.
	--The project in its current form depends on the user defining price ranges

-Not supported: updates that do not contain all prices in the thread.
	That is, the post with text "Bookmarked - INS WAND 206s" does not update wand price to 206M
	--As the code is currently structured, only full price reports of all items 
		are able to be plotted.
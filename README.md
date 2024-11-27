# Rsforums_Prices
Contains a web scraper (written in Python 3) that uses regular expressions to find prices of the format &lt;float/int>/&lt;float/int>/.../&lt;float/int>

-Unfortunately, the Runescape forums have permanently been deleted, so this tool is useless. 

-For historical purposes, here is what the old forums looked like:

![Screenshot 2024-11-27 145446](https://github.com/user-attachments/assets/6e0e98fd-2386-44d7-8455-9bfc4a3b715c)

-When the forums were alive, this is what it used to output as a result of parsing price reporting on the forums:

![Noxious_Longbow](https://github.com/user-attachments/assets/fe80dcb8-d961-46bb-b0d0-5b4a68a61db2)

-Example of a "baseUrl" required for gather(...) and makeGraphs(...): 
	"http://forum.runescape.com/forums.ws?17,18,177,65864498,goto,"

-Of primary importance is modifying the sortLines function to allow for
	steeper price fluctuations that go beyond the ranges currently set.
	--The project in its current form depends on the user defining price ranges

-Not supported: updates that do not contain all prices in the thread.
	That is, the post with text "Bookmarked - INS WAND 206s" does not update wand price to 206M
	--As the code is currently structured, only full price reports of all items 
		are able to be plotted.

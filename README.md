# couplearchive
A program to download/save history from the Couple web app (couple.me)
It will download all your "moments" files (or as many as you want). It will also download your chat history, subject to possible limitations of the browser (if you have a long chat history, Chrome may crash before it can load the whole thing).

This script has only been tested on Windows 10, but might work on other systems.

To run this program, you will need to install the following:

Chrome browser (https://www.google.com/chrome/)

Chromedriver (http://chromedriver.chromium.org/downloads)

Python 3.x (I recommend Anaconda3) (https://www.anaconda.com/download/)

Some python packages:

  <blockquote>Selenium</blockquote>
  
  <blockquote>BeautifulSoup4</blockquote>
  
In Anaconda, you would install those packages by doing the following:

  <blockquote>Open the Anaconda Navigator</blockquote>
  
  <blockquote>Click "Environments" on the left side</blockquote>
  
  <blockquote>Select the "base (root)" environment</blockquote>
  
  <blockquote>Click the drop-down box at the top that says "Installed" and change it to "All"</blockquote>
  
  <blockquote>Search for the name of the package</blockquote>
  
  <blockquote>Click the checkbox next to the package (if it is not already checked)</blockquote>
  
  <blockquote>Click "Apply"</blockquote>
  
Once everything is installed, save CoupleDownloader.py somewhere on your computer and run it by double-clicking. If for whatever reason it is not set up to run by double-clicking, you can run the Anaconda Prompt and run it by typing "python" and the full path to the script, e.g.

python c:/users/ejb/downloads/coupledownloader.py

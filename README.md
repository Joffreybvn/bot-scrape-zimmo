# Challenge: Collecting data
by [Jean-Christophe Meunier](https://github.com/jcmeunier77), [Noah Alvarez Gonzalez](https://github.com/NoahAlvarezGonzalez) & [Joffrey Bienvenu](https://github.com/Joffreybvn).

## Challenge's summary
**The mission is**: To collect as much data as possible about the market price of real estate in Belgium, in order to build a dataset that can be used later to create an AI.

### Constraints:
 - Get data from all over Belgium.
 - Deliver a *.CSV* file with a minimum of 10 000 entries.
 - No empty fields.
 - No duplicates.
 - Always record numerical values if possible.

### Objective:
Create a program capable of scraping one (or more ?) real estate websites while respecting all constraints.

## The target: Zimmo.be - Why ?
We have chosen to scrapp [zimmo.be](https://www.zimmo.be/fr/) for the following reasons:
 - It contains more than 100,000 real estate's advertisements in Belgium.<br>
 <img src="https://raw.githubusercontent.com/Joffreybvn/challenge-collecting-data/master/docs/arrow.svg" width="12"> So, we can get data for all over Belgium without having to scrapp multiples local agencies' website.
 
 
 - This website is *easy* to scrapp:
   - **No Javascript**: All the data is available in the HTML code of the site as soon as the page is loaded. There is no Javascript that delays the loading of these data. There is no button we have to click on to access these data.<br>
 <img src="https://raw.githubusercontent.com/Joffreybvn/challenge-collecting-data/master/docs/arrow.svg" width="12"> So, it is possible to scrapp this website **without Selenium (no web browser)**, simply with WebRequests; this can increase the speed of our program !
 
 
   - **A well structured HTML**: The data is encapsulated in clear html tags, with identical tags and attributes each time the page loads.<br>
 <img src="https://raw.githubusercontent.com/Joffreybvn/challenge-collecting-data/master/docs/arrow.svg" width="12"> So we can just use the **simplests recovery methods** of BeautifulSoup.
 
 
   - **A well structured website**: The entry point for our scrapper is this page: [https://www.zimmo.be/fr/province/](https://www.zimmo.be/fr/province/). By reading the URL, you can guess what it may contain. And this page regroups all the real estate selling offers of the website, classified by regions.<br>The offers' links are very clear too: [https://www.zimmo.be/fr/borgerhout-2140/a-vendre/maison/JP4OF/](https://www.zimmo.be/fr/borgerhout-2140/a-vendre/maison/JP4OF/), they contain the city, the postal code, the type of offer (for sale/to rent), the type of property (house/apartment), and a unique identification code.<br>
<img src="https://raw.githubusercontent.com/Joffreybvn/challenge-collecting-data/master/docs/arrow.svg" width="12"> It is therefore possible to **apply a filter directly on URLs**, thus preventing our program from browsing unnecessary pages.

   - **Bot compliant**: The site is poorly protected against bots, and responds well to the huge amount of requests send by our program. For the 20,000 + pages we scrapped, we had to complete a total of 4 captchas.<br>
<img src="https://raw.githubusercontent.com/Joffreybvn/challenge-collecting-data/master/docs/arrow.svg" width="12"> We didn't had to implement a strong anti-banning strategy.

## The program: A Scrapping Bot

### What does our program do ?
Based on the [challenge's constraints](https://github.com/Joffreybvn/challenge-collecting-data#constraints), we wanted a program capable of:
 - Scrapp zimmo.be.
 - Able to scrapp other websites later.
 - Work with captchas.
 - Clean up data and complete missing data.
 - Deliver a CSV that meets the customer's specifications.
 - Backup data in case of a crash.
 
### Integrated concepts:
In order to practice, we tried to integrate the concepts seen during the last two weeks into the program, such as:

 - Object-oriented programming.
 - Threading.
 - Scrapping with WebRequest/Selenium and BeautifulSoup.
 - Regular Expressions.
 - Typing.
 - Data manipulation with Pandas' Dataframes.
 - File creation and crash recovery.
 - Decorators (*This goal was not achieved*).

### A picture is worth a thousand words:
Here is the architecture of our program:

 - <img src="https://raw.githubusercontent.com/Joffreybvn/challenge-collecting-data/master/docs/module.svg" height="15"> Module
 - <img src="https://raw.githubusercontent.com/Joffreybvn/challenge-collecting-data/master/docs/object.svg" height="15"> Object
 - <img src="https://raw.githubusercontent.com/Joffreybvn/challenge-collecting-data/master/docs/threaded_object.svg" height="15"> Threaded Object
![program architecture](https://raw.githubusercontent.com/Joffreybvn/challenge-collecting-data/master/docs/architecture.svg)

### How does it works ?
Our program is divided into three modules:
- A **Scrapper** (for Zinno.be), in charge of scrapping the data.
- A **Cleaner**, which cleans the data and makes backups.
- A **Merger**, which transforms all backup files into a *.CSV*.

The Object **Data Collector** coordinates the instantiation of the modules and the transmission of data between them.

### Why this architecture ?
The two strong points of this architecture are:
 - Being able to **scrapp all the sites** we want: The Zinno.be scrapper is an interchangeable module.<br><br>
<img src="https://raw.githubusercontent.com/Joffreybvn/challenge-collecting-data/master/docs/arrow.svg" width="12"> To scrap another website, we just need to implement another module (example: An Immoweb scrap module), and connect it to the rest of the program. No need to write a new program from 0, nor to modify the Cleaner or Merger.

 - Being able to deliver **one *.CSV* in the desired format** to the customer: Some customers want numeric values everywhere, others prefer True/False with strings, ... Our program can do that easily !<br><br>
<img src="https://raw.githubusercontent.com/Joffreybvn/challenge-collecting-data/master/docs/arrow.svg" width="12"> To be able to deliver a *.CSV* formatted on demand without having to scrapp the whole website again, our program saves the scrapping data in a "backup" folder with [pickles files](https://docs.python.org/3/library/pickle.html). **It backs them up as it retrieves them from the site**. Once all the data is recovered, it transforms it into *.CSV* via the Merger.<br><br>
<img src="https://raw.githubusercontent.com/Joffreybvn/challenge-collecting-data/master/docs/arrow.svg" width="12"> **Advantage**: This architecture also avoids us to have to start to scrapp from the beginning if the program crashed (internet connection down ? Ban ?). As all data is saved in files, we can simply resume from where the program stopped before.
 
 ### All Objects definitions:
 - **Data Collector**: Instantiate the Manager. Collect the raw data from the Manager and send it to the cleaner. When the scrapp is complete, is instantiate a Merger.
 
 - **Manager**: It connects the UrlGrabber and the Scrapper to the Collector.
 - **UrlGrabber**: It retrieve all real estate advertisements' URL from zimmo.be
 - **Scrapper**: Once the job of the UrlGrabber is complete, it scrapp the data of each given URLs.
 
 - **WebDriver**: It initialize a custom version of Selenium Webdriver, with proxy, Javascript and images disables, AdBlock activated.
 - **Requester**: It initialize a custom version of Request. *Currently, this class is not used*.
 
 - **Cleaner**: It cleans and normalizes the raw data send by the Collector. The data is then put in a Dataframe and send to the Saver.
 - **Saver**: It save a given dataframe to a pickle file, in the *./backup/* folder.
 
 - **Merger**: It retrieve all pickles files from the *./backup/* folder. Then, depending on client's needs, it apply some filter and save everything in a *.CSV* file.
 
 ### How to deal with Captchas ?
 Currently, Captchas are the reason why we are not scrapping zimmo.be through Request. Here is how we deal with them:
 1. The Webdriver is set to 
 
 ## TO DO - Future improvements:
 
  - **Scrapping Zimmo.be through Request only** (No more Selenium): To speed up the scrapping, we need to reimplace Selenium by Request. But we need to implement something to detect when the Request face a Captach, and open a Selenium webpage of the website for us to solve the captcha.

## Variables definition
 - locality : str
 - type_of_property : house/appartment
 - subtype of property :
 - price : int (euros)
 - sale_type : by agency/notarial
 - Num_rooms : int
 - area : int (squared meters)
 - kitchen_equipment : none, equipped, fully equipped
 - furnished : yes/no
 - open_fire : yes/no
 - terrace : yes/no
   - If yes, surface : int (squared meters)
 - garden
   - if yes, surface : int (squared meters)
 - surface_land : int (squared meters)
 - surface_plot_land : int (squared meters)
 - number_of_facades : int
 - swimming_pool : yes/no
 - state_building : new/to be renovated 


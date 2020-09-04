# Challenge: Collecting data
by [Jean-Christophe Meunier](https://github.com/jcmeunier77), [Noah Alvarez Gonzalez](https://github.com/NoahAlvarezGonzalez) & [Joffrey Bienvenu](https://github.com/Joffreybvn).

## Program architecture
![program architecture](https://raw.githubusercontent.com/Joffreybvn/challenge-collecting-data/master/docs/architecture.svg)

- The **Data Collector** is the core of our program: It manage the scrappers to retrieve content, and send it to the Cleaner to be saved into CSV files.

- The Manager, UrlGrabber and Scrapper are the three object that handle the scrapping:
  - The **Manager** retrieve the list of all webpages to fetch thanks to the **UrlGrabber**.
  - Then, the Manager call the **Scrapper** to retrieve the data of the house's advertisement.
UrlGrabber and Scrapper are threaded to allow concurrent execution and optimize execution speed.

- The **Cleaner** clean, complete and normalize our raw data. Then it pass the data to the **Saver**, which save it to a CSV file.
Both are threaded to optimize allow concurrent execution and optimize execution speed.

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


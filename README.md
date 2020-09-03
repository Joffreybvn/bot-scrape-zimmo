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
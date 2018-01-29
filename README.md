# Trabalho Final Curso Python FGV #

This repository is intended to keep the final assessment of FGV's Python Summer Course (Jan/2018).

----

* Student: Artur Chiaperini Grover
* Course: FGV's Python Summer Course (Jan/2018)
* Professors: [Flávio Cordeço Coelho](https://github.com/fccoelho) and [Renato Rocha Souza](https://github.com/rsouza)
* Assessment Task: [here](https://github.com/fccoelho/crypto_algo_trading/blob/master/CryptoMarketAnalysis.md) 

----

# What you will find here #

1. The project [TrabalhoFinalCursoPython_FGV](https://github.com/3dhardgamer/TrabalhoFinalCursoPython_FGV/blob/master/TrabalhoFinalCursoDeVerao_Python_FGV.ipynb).
2. ```capturer.py``` = script with class and functions that conects to exchange API and retrieves the data.
3. ```create_db.py``` = script that creates the SQLite database.

A few comments regarding the project:
- The jupyter-notebook file runs ```create_db.py``` just follow the instruction and you should be fine to retrieve data from the exchange and create the database.
- ```create_db.py``` this does not hold an option to append data only (either the db is overwritten or created from scratch).
- required python modules to run the above notebook:
  * bokeh = 0.12.13
  * holoviews = 1.9.2
  * numpy = 1.14.0
  * pandas = 0.22.0
  * pytz = 2017.3
  * requests = 2.18.4
  * sqlachemy = 1.2.1

# The Project #

The exchange selected was [CEX.IO](https://cex.io). From this exchange data of the following pair (crypto/currency) are automatically  retrieved for the period given (start / end dates *YYYY-MM-DD*):
- Bitcoin / Euro (BTC/EUR)
- Bitcoin / US Dollar (BTC/USD)
- Etherium / Euro (ETH/EUR)
- Etherium / US Dollar (ETH/USD)
- Zcash / Euro (ZEC/EUR)
- Zcash / US Dollar (ZEC/USD)

The data is stored in a SQLite database, where each table corresponds to a different pair.
Once data is in the db, it is possible to fetch the data from there.

There is a quick data inspection to verify data range, followed by the data visualisation.





  






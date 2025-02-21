# python_PyQt5_BLE_Client
Client per collegare morse decoder ESP32 BLE Server
Il presente programma python ha, come dice il titolo, lo scopo di gestire il collegamento con il server per decodifica e trasmissione del codice morse in QSO radioamatoriali in via di realizzazione da parte del sottoscritto IU2RPO.

Il progetto è sulla scia di quello realizzato nel 2021 di cui at https://github.com/vinloren/morse_decoder, basato su ESP12, rivisto e aggiornato alla luce dell'evoluzione tecnologica maturata a distanza di quattro anni. Al posto del ESP12 questa versione aggiornata fà affidamento su scheda ESP32 Lilygo T-Display con display oled TFT a colori da 1.14" e controller ST7789. Il collegamento fra client e server avverrà via bluetooth ble anziché WiFi che questa scheda è pure in grado di gestire.

Vedremo più avanti i dettagli relativi al BLE sever sopra accennato non prima di esporre una descrizione sulle particolarità che caratterizzano quasta applicazione client in python PyQt5.


# python_PyQt5_BLE_Client
Il presente programma python ha, come dice il titolo, lo scopo di gestire il collegamento con il server per decodifica e trasmissione del codice morse in QSO radioamatoriali in via di realizzazione da parte del sottoscritto IU2RPO.

Il progetto è sulla scia di quello realizzato nel 2021 di cui at https://github.com/vinloren/morse_decoder, basato su ESP32, rivisto e aggiornato alla luce dell'evoluzione tecnologica maturata a distanza di quattro anni. Al posto del crudo ESP32 questa versione aggiornata fà affidamento a scheda ESP32 Lilygo T-Display con display oled TFT a colori da 1.14" e controller ST7789. Il collegamento fra client e server avverrà via bluetooth ble anziché WiFi che questa scheda è pure in grado di gestire.

Vedremo più avanti i dettagli relativi al BLE sever sopra accennato non prima di esporre una descrizione sulle particolarità che caratterizzano questa applicazione client in python PyQt5.

## Descrizione funzionalità
Osservando l'immagine .jpg della finestra PyQt5 qui allegata notiamo:
1) tasto SCAN: per collegare il server ble dobbiamo conoscerne nome pubblicato, MAC address bluetooth e "Characteristic". Per acquisire queste informazioni, l'applicazione fà uno scan di tutti i dispositivi bluetooth raggiungibili nelle vicinenze per riportare poi nella combo box accanto i nomi dei dispositivi trovati che hanno accessibili "Service" e "Characteristic". Lo scan dura tre minuti per garantire un'acquisizione completa.
2) Allo scadere dei tre minuti, dopo qualche secondo di ritardo, troveremo la combo box riempita con gli identificativi dei devices trovati. Scorrendo la lista ci posizioneremo cliccando sul nome che ci interessa per poi battere "CONNECT" ed entrare in collegamento col server BLE prescelto.
3) Possiamo collegarci a qualunque BLE device ma poi lo scambio dei dati sarà condizionato dal protocollo specifico disegnato sul server in oggetto, del quale il presente client è ignaro, quindi difficilemnete potremo andare al di là della semplice connessione se non in collegamento col server ESP32 Lyligo T-Display Morse decoder che descriverò in seguito.
4) La progress bar verde ai piedi della finestra window intrattiene l'utente in attesa del termine dello scan.
5) Il tasto "INVIO" alla sinistra del campo di input a fondo finestra provvederà a inviare interrogazioni / cmandi al server le cui risposte appariranno nella text box di destra, mentre nella text box di sinistra troveremo tutti i riferimenti ai dispositivi BLE intercettati nelle vicinanze dallo scan.

## Requisiti python
1) Python 3.11.x
2) pip install PyQt5
3) pip install bleak



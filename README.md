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

# Lilygo T-Display BLE Server / Morse Decoder
Questo progetto fà seguito ad altri fatti in passato gestendo in input, su uno degli adc del ESP32, il segnale audio discriminato con algoritmi FFT (Fast Fourier Transformatiion) onde rilevare il dit e il dah (punti e linee) per produrre la corretta decodifica. "Roba" pesante questa che poi dava risultati sempre in bilico fra successo e fallimento. Tutto questo mi faceva venire la nostalgia dei primi anni 80 quando decodificavo segnali morse e RTTY con un modem autocosruito con ekementi discreti collegato fra uscita audio dell'indimentiabile Yesu FRG7 e microprocessore National SC/Mp con 2kb di ram e 1kb di rom e schermo CRT da 7". Andva tutto alla perfezione.

L'approccio del progetto attuale, per ciò che riguarda l'input e le sua discriminazione, è cambiato e per certi versi ritorna a quello degli anni 80 dove il segnale audio a 600-800hz veniva trasformato il 0 / 1 (logica digitale alto - basso) prima di darlo in pasto all'elaborazione del processore. Di fatto oggi abbiamo a disposizione al prezzo di 1€ (un €uro) dei rivelatori di suoni che forniscono uscita "alta" quando il microfono rileva un suono che supera il livello di soglia prefissato. Chi fosse interessato dia uno sguardo a: https://it.aliexpress.com/item/1005006827749945.html?spm=a2g0o.order_list.order_list_main.22.1ab03696cNpjQg&gatewayAdapt=glo2ita

La soluzione per trasformare il segnale analogico della nota cw in input digitale è stata quella di collegare l'uscita del rivelatore audio a un input PIO del ESP32 sotto forma di 0 - 1 che poi l'applicazione Arduino C++ provvede ad elaborare. Un semplice schema del collegamento rivelatore - Lilygo T-Display è allegato nella directory Lilygo_T-Display_morse-decoder.

## Sketch Arduino Lilygo_T-Display_BLE_Morse_Decoder
Ho scelto di operare sul morse decoder attraverso il colegamneto con l'applicazione python PyQt5 perima descritta per agevolare la scelta delle variabili di configurazione oltre che per fare in modo che quanto decodificato dal server e messo a display sul suo oled 1.14" a colori venisse anche inviato al client che lo controlla.


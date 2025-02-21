import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, \
        QPushButton, QTextEdit, QLineEdit, QLabel, QProgressBar,QComboBox
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
import asyncio
from bleak import BleakScanner , BleakClient
from time import sleep

class BLEScanThread(QThread):
    actionDone = pyqtSignal(object)  # Segnale per inviare i risultati alla GUI

    def __init__(self, loop):
        super().__init__()
        self.loop = loop

    def run(self):
        # Esegui la scansione BLE nel loop asyncio
        result = asyncio.run(BLE_scan_service.scan_ble_devices())  # Attendi il risultato della scansione asincrona
        self.actionDone.emit(result)  # Invia il risultato alla GUI


class BLEClient(QThread):
    actionDone = pyqtSignal(str)
    rcvd = False
    xmtd = False

    def __init__(self,loop,address,characteristic,xmtdata):
        super().__init__()
        self.loop = loop
        self.address = address
        self.characteristic = characteristic
        self.xmtdata = xmtdata

    def run(self):
        print("Run cnnect")
        asyncio.run(self.connect_and_echo())
        #self.connect_and_echo("64:b7:08:ad:09:72")
        
    async def connect_and_echo(self):
        print("Entrato con address")
        print(self.address)
        async with BleakClient(self.address) as client:
            print(f"Connessione a {self.address}...")
            while(1):            
                # Controlla se la connessione è avvenuta correttamente
                sleep(0.1)
                if client.is_connected:
                    if not self.rcvd:
                        response = await client.read_gatt_char(self.characteristic)
                        self.rcvd = True
                        self.actionDone.emit(response.decode('latin-1', errors='ignore'))
                    elif self.xmtdata != "":
                        await client.write_gatt_char(self.characteristic, self.xmtdata.encode('latin-1'))
                        self.xmtdata = ""
                        self.rcvd = False
                else:
                    print("Connessione fallita.")
                    break

    # Esegui l'operazione di connessione e echo
    loop = asyncio.get_event_loop()
    

class BLE_scan_service:
    # Funzione per la scansione dei dispositivi BLE e la raccolta delle informazioni
    @staticmethod
    async def scan_ble_devices():
        recs = []    
        devices = await BleakScanner.discover(timeout=180)  # Scansione asincrona
        for device in devices:
            dvc = {}
            print(f"Dispositivo trovato:")
            print(f"  Nome: {device.name}")
            if device.name is not None:    
                # Proviamo a connetterci al dispositivo per ottenere i servizi e le caratteristiche
                try:
                    async with BleakClient(device.address) as client:
                        dvc["Nome"] = device.name
                        print(f"  Connesso a {device.address}")
                        dvc["MAC"] = device.address
                        # Recuperiamo i servizi (service UUID) del dispositivo
                        services = await client.get_services()
                        for service in services:
                            print(f"  Servizio trovato: {service.uuid}")
                            dvc["Service"] = service.uuid
                            dvc["Characteristic"] = None 
                            # Recuperiamo le caratteristiche (characteristic UUID)
                            for characteristic in service.characteristics:
                                print(f"    Caratteristica trovata: {characteristic.uuid}")
                                try:
                                    dvc["Characteristic"] = characteristic.uuid
                                except Exception as x:
                                    print("Errore accesso a characteristic: {x}")
                        recs.append(dvc)
                except Exception as e:
                    print(f"  Errore nel recuperare servizi/caratteristiche: {e}")   
            print("-" * 40)
        return recs


class MyWindow(QWidget):
    scanned = {}
    def __init__(self):
        super().__init__()

        self.setWindowTitle('BLE_Client')
        self.setGeometry(100, 100, 560, 380)  # Impostiamo la dimensione della finestra a 800x600

        # Creiamo il layout verticale
        self.layout = QVBoxLayout()
        # top layout orizzontale
        self.hhome = QHBoxLayout()
        self.scanb = QPushButton('SCAN', self)
        self.targetlbl = QLabel("Target dvc")
        self.scanb.clicked.connect(self.on_scanb_click)
        self.target = QComboBox(self)
        self.target.activated.connect(self.select_target)
        self.target.setMinimumWidth(120)
        self.filler = QLabel("    ")
        self.filler.setMinimumWidth(250)
        self.hhome.addWidget(self.scanb)
        self.hhome.addWidget(self.targetlbl)
        self.hhome.addWidget(self.target)
        self.connectb = QPushButton('CONNECT', self)
        self.connectb.clicked.connect(self.on_connectb_click)
        self.hhome.addWidget(self.connectb)
        self.hhome.addWidget(self.filler)
        self.layout.addLayout(self.hhome) 
        self.hh2 = QHBoxLayout()
        self.scanlbl = QLabel("Scan output")
        self.rcvdatlbl = QLabel("Dati ricevuti")
        self.hh2.addWidget(self.scanlbl)
        self.hh2.addWidget(self.rcvdatlbl)
        self.hh1 = QHBoxLayout()
        self.text_area1 = QTextEdit(self)
        self.hh1.addWidget(self.text_area1)
        self.text_area2 = QTextEdit(self)
        self.hh1.addWidget(self.text_area2)   
        self.layout.addLayout(self.hh2) 
        self.layout.addLayout(self.hh1) 
        self.hh3 = QHBoxLayout()
        self.button1 = QPushButton('Clear', self)
        self.button1.clicked.connect(self.on_button1_click)
        self.hh3.addWidget(self.button1)
        self.button2 = QPushButton('Clear', self)
        self.button2.clicked.connect(self.on_button2_click)
        self.hh3.addWidget(self.button2)
        self.layout.addLayout(self.hh3)
        self.hh4 = QHBoxLayout()
        self.inviob = QPushButton('INVIO', self)
        self.inviob.clicked.connect(self.on_inviob_click)
        self.input_text = QLineEdit(self)
        self.input_text.setPlaceholderText('Inserisci del testo...')
        self.hh4.addWidget(self.inviob)
        self.hh4.addWidget(self.input_text)
        self.hh5 = QHBoxLayout()
        self.progress = QProgressBar(self)
        self.progress.setRange(0, 180)  # 180 secondi = 3 minuti
        self.progress.setValue(0)
        self.progress.setTextVisible(True)
        self.progress.setStyleSheet("QProgressBar { background-color: #e0e0e0; border: 1px solid #8c8c8c; border-radius: 5px;height: 10px }"
                                       "QProgressBar::chunk { background-color: green; }")
        
        self.hh5.addWidget(self.progress)
        self.layout.addLayout(self.hh4)
        self.layout.addLayout(self.hh5)
        # Timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.time_left = 180  # 3 minuti in secondi
        self.setLayout(self.layout)

    def start_timer(self):
        self.time_left = 180  # Reset del timer
        self.progress.setValue(0)
        self.timer.start(1000)  # Aggiorna ogni secondo

    def update_progress(self):
        self.time_left -= 1
        self.progress.setValue(180 - self.time_left)
        if self.time_left <= 0:
            self.timer.stop()
            #self.start_button.setText("Timer Finito")

    def select_target(self):
        print(self.target.currentText())
        i = self.target.currentIndex()
        print(self.scanned[i])
        

    def on_button1_click(self):
        text = self.input_text.text()
        self.text_area1.clear()

    def on_button2_click(self):
        self.text_area2.clear()

    def on_scanb_click(self):
        print("Inizio scan")
        self.text_area2.append("Aspetta 3 minuti per termine scan, poi seleziona target in combo box prima di premere connect.")
        loop = asyncio.new_event_loop()  # Crea un nuovo loop
        asyncio.set_event_loop(loop)  # Imposta questo loop come quello corrente
        self.BLEscan = BLEScanThread(loop)  # Passa il loop al thread
        self.BLEscan.actionDone.connect(self.onFound)
        self.BLEscan.start()
        self.start_timer()

    def on_connectb_click(self):
        print("CONNECT clicked")
        if not self.scanned:
            return
        # Prendi l'indirizzo MAC e la caratteristica dal target index selezionato  
        i = self.target.currentIndex()
        address = self.scanned[i]["MAC"] 
        characteristic =  self.scanned[i]["Characteristic"]
        xmtdata = ""
        # Crea un nuovo loop asincrono per il thread BLEClient
        loop = asyncio.new_event_loop()  
        asyncio.set_event_loop(loop)  # Imposta questo loop come quello corrente
        # Crea il thread BLEClient e passa i parametri necessari
        self.BLEconnect = BLEClient(loop, address, characteristic,xmtdata)
        # Collega il segnale per ottenere i dati dal server
        self.BLEconnect.actionDone.connect(self.onData)
        # Avvia il thread
        self.BLEconnect.start()
        print("Rientro da connect_and_echo")

    def on_inviob_click(self):
         print("INVIO clicked")
         self.BLEconnect.xmtdata = self.input_text.text()

    def onFound(self, value):
        print("Risultato scan")
        print(value)
        self.scanned = value
        # Aggiungi i risultati della scansione nel text_area e add nome dei device 
        # nella combobox target
        for device in value:
            self.target.addItem(device["Nome"])
            self.text_area1.append(f"Dispositivo trovato: {device['Nome']}, MAC: {device['MAC']}, Service: {device['Service']},Characteristic: {device['Characteristic']}")

    def onData(self,value):
        print("Dati da server")
        print(value)
        self.text_area2.append(value)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())

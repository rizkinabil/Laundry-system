"""
    Di sisi Penyedia jasa laundry, pertama laundry menunggu request/subscription dari client
    ketika sudah ada subscription, laundry akan mengirim pesan terima kasih ke client
    pada waktu yang bersamaan, laundry juga melakukan subscribe terhadap topik pesanan yang akan dibuat oleh client
    sehingga ketika client tinggal mengirim/publish pesan ke laundry

"""

# import library
import random
import time
import os
from IPython.core.display import clear_output
from paho import mqtt
from tabulate import tabulate

from paho.mqtt import client as mqtt_client

# deklarasi broker dan port yang sama dengan client
broker = 'broker.emqx.io'
port = 1883

# deklarasi topik berlangganan laundry bojong
topic_cl2bj = "berlangganan bojong"
    
# function utama dari proses yang dijalankan di sisi laundry
def auto_sub(client):
    # deklarasi list untuk menyimpan pesanan dari client laundry bojong
    listBojong = []

    # on_connect function
    def on_connect_autosub(client, userdata, flags, rc):
        if rc == 0:
            print('connected')
        else:
            print('error')
    
    # on_message function untuk message apabila client telah melakukan placement order
    def on_mess_autosub(client, userdata, msg):
        print('')
        data_pesanan = str(msg.payload.decode('utf-8'))
        listBojong.append(data_pesanan)
        clear_output(wait=True)
        # os.system('cls')
        print('+----------------------------------------------+')
        print('|         Pesanan Untuk Laundry Bojong         |')
        print('+----------------------------------------------+')
        print(data_pesanan)

    # deklarasi topik yang sama dengan publish di client bojong
    topic_auto = 'autosub'
    client.on_connect = on_connect_autosub
    client.on_message = on_mess_autosub

    try:
        # template pesan terima kasih yang akan dipublish ke client bojong
        msg = 'Terima kasih sudah memilih Laundry Bojong'
        client.connect(broker, port)

        client.loop_start()
        print('')
        print(f'<> kirim pesan data ke client </> \n')
        time.sleep(2)

        """
            Pada proses ini, laundry bojong mengirim pesan terima kasih kepada client bojong yang telah berlangganan
            setelah itu laundry bojong akan menerima informasi placement order dari client bojong
        """

        # proses pengiriman feedback terima kasih dan penerimaan informasi placement order
        client.publish(topic_cl2bj, msg)
        client.subscribe(topic_auto, qos=1)
        while True:
            time.sleep(1)
        client.loop_stop()
    # handle error
    except:
        print('gagal melakukan auto subscribe')



# running function
def run():
    # deklarasi client
    client = mqtt_client.Client('laundry bojong', clean_session=False)
    
    # proses dijalankan
    auto_sub(client)

    # handle proses apabila ingin dilanjut atau tidak
    pil = input('lanjutkan proses pesanan? (y/n)')
    if pil == 'y' or pil == 'Y':
        print('lanjut proses')
    else:
        print('stop')
        os.system('cls')
    while True:
        time.sleep(1)


# main program
if __name__ == '__main__':
    status = True
    while status:
        cek = input('nyalakan fitur (y) : ')
        if cek =="y":
            run()
        else:
            os._exit

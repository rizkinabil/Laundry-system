# python 3.6

import random
import time
import os
from IPython.core.display import clear_output
from paho import mqtt
from tabulate import tabulate

from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "Laundry Bojong"

topic_cl2bj = "berlangganan bojong"
    

def auto_sub(client):
    listBojong = []

    def on_connect_autosub(client, userdata, flags, rc):
        if rc == 0:
            print('connected')
        else:
            print('error')

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


    topic_auto = 'autosub'
    client.on_connect = on_connect_autosub
    client.on_message = on_mess_autosub

    try:
        msg = 'Terima kasih sudah memilih Laundry Bojong'
        client.connect(broker, port)

        client.loop_start()
        print('')
        print(f'<> kirim pesan data ke client </> \n')
        time.sleep(2)

        client.publish(topic_cl2bj, msg)
        client.subscribe(topic_auto, qos=1)
        while True:
            time.sleep(1)
        client.loop_stop()
    except:
        print('gagal melakukan auto subscribe')




def run():
    
    client = mqtt_client.Client('laundry bojong', clean_session=False)
    
    auto_sub(client)
    pil = input('lanjutkan proses pesanan? (y/n)')
    if pil == 'y' or pil == 'Y':
        print('lanjut proses')
    else:
        print('stop')
        os.system('cls')
    while True:
        time.sleep(1)



if __name__ == '__main__':
    status = True
    while status:
        cek = input('nyalakan fitur (y) : ')
        if cek =="y":
            run()
        else:
            os._exit

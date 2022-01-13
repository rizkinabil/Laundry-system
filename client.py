# python3.6

import datetime
from logging import NullHandler
import time
import os
from paho import mqtt
from tabulate import tabulate


from IPython.core.display import clear_output

from prettytable import PrettyTable

from paho.mqtt import client as mqtt_client



broker = 'broker.emqx.io'
port = 1883
topic = "Laundry Bojong"

topic_cl2bj = "berlangganan bojong"
topic_cl2sn = "berlangganan soang"



# on_message func untuk pesan telah berlangganan
def sub_pesan() :

    client = mqtt_client.Client('pesan')
    def message_langgananBojong(client, userdata, msg):
        print('')
        pesan = str(msg.payload.decode('utf-8'))
        print(f'Pesan dari Laundry Bojong : ',pesan)
        # client.loop_stop()

    client.connect(broker, port)
    client.loop_start()
    client.subscribe(topic_cl2bj, qos=1)

    client.on_message = message_langgananBojong



    

def langganan_bojong(nama, berat, no_kategori):
    
    # on_connect func untuk berlangganan
    def connect_laundryBojong(client, userdata, flags, rc):
        time.sleep(1.5)
        print('')
        if rc == 0:
            print('Pesanan berhasil terkirim...')
        else:
            print('gagal terhubung!')
    
    

    def publish_reverse(nama, berat, no_kategori):
        if no_kategori == '1':
            kategori = 'Ekonomis'
        elif no_kategori == '2':
            kategori = 'Standar'
        elif no_kategori == '3':
            kategori = 'Premium'

        topic_auto = 'autosub'
        client_reverse = mqtt_client.Client(topic_auto)
        # data_pesanan = ''+nama+'|'+berat+ 'Kg''|'+kategori+''
        data_pesanan = nama+' membuat pesanan : \n -> laundry = '+berat+' Kg \n -> Kategori = '+kategori
        client_reverse.connect(broker, port)
        client_reverse.loop_start()
        print('')
        print('------ membuat pesanan ke laundry bojong ------')
        time.sleep(2)
        print('')

        client_reverse.publish(topic_auto, data_pesanan, qos=1, retain=False)
        client_reverse.loop_stop()

    client = mqtt_client.Client('bojong', clean_session=True)
    client.on_connect = connect_laundryBojong
    client.connect(broker, port)

    client.loop_start()
    publish_reverse(nama, berat, no_kategori)

    client.loop_stop()

    


def langganan_soang(nama, berat, no_kategori):
    
    # on_connect func untuk berlangganan
    def connect_laundrySoang(client, userdata, flags, rc):
        time.sleep(1.5)
        print('')
        if rc == 0:
            print('Pesanan berhasil terkirim...')
        else:
            print('gagal terhubung!')
    
    # on_message func untuk pesan telah berlangganan
    def message_langgananSoang(client_mes, userdata, msg):
        
        print('')
        pesan = str(msg.payload.decode('utf-8'))
        print(f'Pesan dari Laundry Soang : ',pesan)
        




    def publish_reverse(nama, berat, no_kategori):
        if no_kategori == '1':
            kategori = 'Ekonomis'
        elif no_kategori == '2':
            kategori = 'Standar'
        elif no_kategori == '3':
            kategori = 'Premium'

        topic_auto = 'autosub soang'
        client_reverse = mqtt_client.Client(topic_auto)
        # data_pesanan = ''+nama+'|'+berat+ 'Kg''|'+kategori+''
        data_pesanan = nama+' membuat pesanan : \n -> laundry = '+berat+' Kg \n -> Kategori = '+kategori
        client_reverse.connect(broker, port)
        client_reverse.loop_start()
        print('')
        print('------ membuat pesanan ke Laundry Soang ------')
        time.sleep(2)
        print('')

        client_reverse.publish(topic_auto, data_pesanan, qos=1, retain=False)
        client_reverse.loop_stop()

    client = mqtt_client.Client('soang', clean_session=True)
    client.on_connect = connect_laundrySoang
    client.connect(broker, port)

    client_mes = mqtt_client.Client('pesan')
    client_mes.connect(broker, port)
    client_mes.loop_start()
    client_mes.subscribe(topic_cl2sn, qos=1)
    client_mes.on_message = message_langgananSoang


    client.loop_start()
    publish_reverse(nama, berat, no_kategori)

    client.loop_stop()


def menu():
    table = PrettyTable(['No', 'Menu'])
    table.add_row(['1', 'Langganan ke Laundry Bojong'])
    table.add_row(['2', 'Langganan ke Laundry Soang'])
    table.add_row(['3', 'Exit'])
    table.align = 'l'
    print(table)

def banding_waktu(nama, berat, jenis_paket):
    # waktu pengajuan laundry bojong dan soang
    today = datetime.datetime.now()
    waktu_pengajuan = str(today.strftime('%d-%m-%y')) + \
        ' ('+str(today.strftime('%H:%M:%S'))+') '

    # waktu cucian dimasukkan ke antrean Bojong
    selisih_waktu = today + datetime.timedelta(minutes = 5)
    antrean_bojong = str(selisih_waktu.strftime(
        '%d-%m-%y')) + ' ('+str(selisih_waktu.strftime('%H:%M:%S'))+') '
    
    # waktu cucian dimasukkan ke antrean Soang
    selisih_waktu = today + datetime.timedelta(minutes = 10)
    antrean_soang = str(selisih_waktu.strftime(
        '%d-%m-%y')) + ' ('+str(selisih_waktu.strftime('%H:%M:%S'))+') '
    
    
    des_berat = float(berat)
    str_berat = str(des_berat)+' Kg'

    # layanan laundry bojong
    if jenis_paket == '1':
        paket = 'Ekonomis'
        harga_bojong = str(int(des_berat * 5000))
        waktu_pengerjaan = today + \
            datetime.timedelta(
                days=3) + datetime.timedelta(minutes=0) + datetime.timedelta(minutes=0)
        ambil_laundry_bojong = str(waktu_pengerjaan.strftime(
            '%d-%m-%y')) + ' ('+str(waktu_pengerjaan.strftime('%H:%M:%S'))+') '
    elif jenis_paket == '2':
        paket = 'Standar'
        harga_bojong = str(int(des_berat * 7500))
        waktu_pengerjaan = today + \
            datetime.timedelta(
                days=2) + datetime.timedelta(minutes=0) + datetime.timedelta(minutes=0)
        ambil_laundry_bojong = str(waktu_pengerjaan.strftime(
            '%d-%m-%y')) + ' ('+str(waktu_pengerjaan.strftime('%H:%M:%S'))+') '
    elif jenis_paket == '3':
        paket = 'Premium'
        harga_bojong = str(int(des_berat * 9000))
        waktu_pengerjaan = today + \
            datetime.timedelta(
                days=1) + datetime.timedelta(minutes=0) + datetime.timedelta(minutes=0)
        ambil_laundry_bojong = str(waktu_pengerjaan.strftime(
            '%d-%m-%y')) + ' ('+str(waktu_pengerjaan.strftime('%H:%M:%S'))+') '


    # layanan laundry soang
    if jenis_paket == '1':
        harga_soang = str(int(des_berat * 6000))
        waktu_pengerjaan = today + \
            datetime.timedelta(
                days=2) + datetime.timedelta(minutes=20) + datetime.timedelta(minutes=0)
        ambil_laundry_soang = str(waktu_pengerjaan.strftime(
            '%d-%m-%y')) + ' ('+str(waktu_pengerjaan.strftime('%H:%M:%S'))+') '
    elif jenis_paket == '2':
        harga_soang = str(int(des_berat * 8500))
        waktu_pengerjaan = today + \
            datetime.timedelta(
                days=1) + datetime.timedelta(minutes=20) + datetime.timedelta(minutes=0)
        ambil_laundry_soang = str(waktu_pengerjaan.strftime(
            '%d-%m-%y')) + ' ('+str(waktu_pengerjaan.strftime('%H:%M:%S'))+') '
    elif jenis_paket == '3':
        harga_soang = str(int(des_berat * 10000))
        waktu_pengerjaan = today + \
            datetime.timedelta(
                hours=12) + datetime.timedelta(minutes=20) + datetime.timedelta(minutes=0)
        ambil_laundry_soang = str(waktu_pengerjaan.strftime(
            '%d-%m-%y')) + ' ('+str(waktu_pengerjaan.strftime('%H:%M:%S'))+') '

    # output hasil perbandingan
    x = PrettyTable()
    x.field_names = ['Laundry','Nama', 'Waktu Pengajuan', 'Berat (kg)', 'Kategori Paket', 'Masuk Antrean', 'Pengembalian Cucian', 'Harga']
    bj = "Bojong"
    sg = "Soang"
    x.add_row([bj, nama, waktu_pengajuan, str_berat, paket, antrean_bojong, ambil_laundry_bojong, harga_bojong])
    x.add_row([sg, nama, waktu_pengajuan, str_berat, paket, antrean_soang, ambil_laundry_soang, harga_soang])
    print(f'\n ==== Perbandingan waktu dan harga dari kedua Laundry ====\n')
    print(x)



def ExitMenu():
    time.sleep(3)
    print('')
    print('Keluar dari program.....')

# menu utama
if __name__ == '__main__':
    status = True
    while status:
        os.system('cls')
        print('')
        print('+-----------------------------------+')
        print('|        Masukan data laundry       |')
        print('+-----------------------------------+')
        nama = input('Nama          : ')
        berat = input('Berat (kg)    : ')
        print('')
        print('+-----------------------------------+')
        print('|       Pilih Kategori Paket        |')
        print('+-----------------------------------+')
        print('1. Ekonomis')
        print('2. Standar')
        print('3. Premium')
        jenis_paket = input('Pilih nomor kategori paket : ')
        if jenis_paket == '1' or jenis_paket == '2' or jenis_paket == '3':
            banding_waktu(nama,berat,jenis_paket)
            menu()
            pil = input('pilih menu berlangganan laundry : ')
            print('')
            if pil=="1":
                fed = input(f'Lanjutkan pesanan atau tidak? (y/n) \n -> ')
                if fed == 'y' or fed == 'Y':
                    sub_pesan()
                    langganan_bojong(nama, berat, jenis_paket)
                    last = input('lanjut? (y/n)')
                    if last == 'y' or last == 'Y':
                        status=True
                    else:
                        status=False
                else:
                    status = False
                    print('program berhenti...')
                    time.sleep(2)
            elif pil=="2":
                cek = input(f'Lanjutkan pesanan atau tidak? (y/n) \n -> ')
                if cek == 'y' or cek == 'Y':
                    langganan_soang(nama, berat, jenis_paket)
                    lanjut = input('lanjut? (y/n)')
                    if lanjut == 'y' or lanjut == "Y":
                        status = True
                    else:
                        status = False
                else:
                    status = False
                    print('program berhenti...')
                    time.sleep(2)
            elif pil=='3':
                status = False
                os.system('cls')
                ExitMenu()

                
        
        else:
            time.sleep(2)
            print('')
            print('+-----------------------------------+')
            print('|       Mohon maaf, input salah     |')
            print('+-----------------------------------+')
            fed = input('Coba lagi ? (y/n) ')
            if fed == 'Y' or fed == 'y':
                time.sleep(3)
                status = True
            else:
                status = False
                print('')
                print('Program berhenti...')
                time.sleep(2)

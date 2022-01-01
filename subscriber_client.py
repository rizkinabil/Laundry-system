import paho.mqtt.client as mqtt
import datetime
import time 

from tabulate import tabulate
from prettytable import Prettytable
from IPython.display import clear_output
import os


# implementasi menu subscriber

def menu():
    table = Prettytable(['No', 'Menu'])
    table.add_row(['1', 'Langganan ke Laundry Bojong (Port : 2222)'])
    table.add_row(['2', 'Langganan ke Laundry Soang (Port : 3333)'])
    table.add_row(['3', 'Melihat perbandingan waktu (Port : 4444)'],)
    table.add_row(['4', 'Exit'])
    table.align = '1'
    print(table)


# menu laundry bojong

def LaundryBojong():
    listBojong = []

    # message fuction apabila berhasil terhubung
    def connect_laundryBojong(client, userdata, flags, rc):
        time.sleep(1.5)
        print('')
        print('Berhasil terhubung ke Laundry Bojong')

    
    def message_laundryBojong(client, userdata, message):
        print('')
        data = str(message.payload.decode('utf-8')).split('|')
        listBojong.append(data)
        clear_output(wait=True)
        os.system('cls')
        print('+--------------------------------------------------------------------------------------------+')
        print('|                                    Data Laundry Bojong                                      ')
        nomor_list = range(1, len(listBojong)+1)
        print(tabulate(listBojong, headers=[
            '   Nama    ', 'Tanggal & waktu Laundry', ' Berat   ', 'Jenis paket', 'Tempat   Penjemputan baju', 'Pengambilan Baju','      total harga     '
        ], tablefmt='pretty'))


    # setup ip broker dan membuat client
    ip_broker = 'localhost'
    client = mqtt.Client('LaundryBojong', clean_session=True)

    # mengirim pesan ketika terhubung dan pesan status dari laundryBojong
    client.on_connect = connect_laundryBojong
    client.on_message = message_laundryBojong
    client.connect(ip_broker, port=2222)

    client.loop_start()

    #
    client.subscribe('dataLaundry', qos=1)
    while True:
        time.sleep(1)

    client.loop_stop()


# menu laundry Soang
def LaundrySoang():
    # inisialisasi data ke laundry soang
    listSoang = []

    # message fuction apabila berhasil terhubung
    def connect_laundrySoang(client, userdata, flags, rc):
        time.sleep(1.5)
        print('')
        print('Berhasil terhubung ke Laundry Soang...')


    def message_laundrySoang(client, userdata, message):
        print('')
        data = str(message.payload.decode('utf-8')).split('|')
        listSoang.append(data)
        clear_output(wait=True)
        os.system('cls')
        print('+--------------------------------------------------------------------------------------------+')
        print('|                                    Data Laundry Soang                                       ')
        nomor_list = range(1, len(listSoang)+1)
        print(tabulate(listSoang, headers=['    Nama    ','Tanggal & Waktu Pengajuan','    Berat   ','Jenis Paket','Tempat Penjemputan Baju','Pengambilan Baju','      Total Harga     '], tablefmt='pretty'))


    # setup ip broker dan membuat client
    ip_broker = 'localhost'
    client = mqtt.Client('LaundrySoang', clean_session=True)

    # mengirim pesan ketika terhubung dan pesan status dari LaundrySoang
    client.on_connect = connect_laundrySoang
    client.on_message = message_laundrySoang
    client.connect(ip_broker, port=3333)

    client.loop_start()

    #
    client.subscribe('dataLaundry', qos=1)
    while True:
        time.sleep(1)

    client.loop_stop()



    # menu perbandingan waktu
def perbandinganWaktu():
    # inisialisasi data ke list perbandingan
    listBanding = []

    # message fuction apabila berhasil terhubung
    def connect_perbandinganWaktu(client, userdata, flags, rc):
        time.sleep(1.5)
        print('')
        print('Berhasil terhubung ke hasil banding waktu...')


    def message_perbandinganWaktu(client, userdata, message):
        print('')
        data = str(message.payload.decode('utf-8')).split('|')
        listBanding.append(data)
        clear_output(wait=True)
        os.system('cls')
        print('+-------------------------------------------------------------------------------------------------+')
        print('|                                    Data Perbandingan Waktu                                       ')
        
        print(tabulate(listBanding, headers=[' Laundry ','  Nama  ','Tanggal & Waktu Pengajuan',' Berat (kg) ','Jenis Paket',
            'Tempat Penjemputan Baju','Pengambilan Baju','      Total Harga     ' ], tablefmt='pretty'))
        print('')


    # setup ip broker dan membuat client
    ip_broker = 'localhost'
    client = mqtt.Client('LaundrySoang', clean_session=True)

    # mengirim pesan ketika terhubung dan pesan status dari LaundrySoang
    client.on_connect = connect_perbandinganWaktu
    client.on_message = message_perbandinganWaktu
    client.connect(ip_broker, port=4444)

    client.loop_start()

    #
    client.subscribe('dataLaundry', qos=1)
    while True:
        time.sleep(1)

    client.loop_stop()


# Menu Exit
def ExitMenu():
    time.sleep(5)
    print('')
    print('Keluar dari program.....')


# menu utama
os.system('cls')
status = True
while status:
    in_pilihan = input('Silahkan pilih menu dibawah ini: ')
    if(in_pilihan == '1'):
        LaundryBojong()
    elif(in_pilihan == '2'):
        LaundrySoang()
    elif(in_pilihan == '3'):
        perbandinganWaktu()
    elif(in_pilihan == '4'):
        status = False
        exit()
    else:
        time.sleep(3)
        print('')
        print('---------------------------------')
        print('|     Inputan tidak sesuai!!     ')
        print('---------------------------------')
        print('')
        in_pilihan = input('Proses ulang? (y/n)')
        time.sleep(5)
        if(in_pilihan == 'y' or in_pilihan == 'Y'):
            os.system('cls')
            menu()
        else:
            status = False
            time.sleep(5)
            print('')
            print('Program berakhir....')

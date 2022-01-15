
"""
pada tugas ini kami mengimplementasikan metode publish and subscribe yang dikombinasi
sehingga object user dapat berkomunikasi 2 arah
pada sisi client ini pertama melakukan subscribe terlebih dahulu lalu akan menerima pesan 'terima kasih' dari laundry
disaat yang sama laundry men-subscribe topik pesanan laundry yang akan dibuat oleh client.

"""

# import library yang akan digunakan
import datetime
from logging import NullHandler
import time
import os
from paho import mqtt
from tabulate import tabulate


from IPython.core.display import clear_output

from prettytable import PrettyTable

from paho.mqtt import client as mqtt_client


# server broker yang digunakan untuk menghubungkan antara client dan laundry
broker = 'broker.emqx.io'
port = 1883

# inisialisasi topik untuk pesan ketika sudah berlangganan laundry bojong
topic_cl2bj = "berlangganan bojong"

# inisialisasi topik untuk pesan ketika sudah berlangganan laundry soang
topic_cl2sn = "berlangganan soang"


# function subscribe pesan feedback terima kasih dari Laundry bojong
def sub_pesan_bojong() :
    client = mqtt_client.Client('pesan')

    # on_message func untuk message apabila client telah berlangganan laundry bojong
    def message_langgananBojong(client, userdata, msg):
        print('')
        pesan = str(msg.payload.decode('utf-8'))
        print(f'Pesan dari Laundry Bojong : ',pesan)

    client.connect(broker, port)
    client.loop_start()
    client.subscribe(topic_cl2bj, qos=1)

    client.on_message = message_langgananBojong




# function untuk berlangganan Laundry Bojong
def langganan_bojong(nama, berat, no_kategori):
    
    # on_connect func untuk berlangganan
    def connect_laundryBojong(client, userdata, flags, rc):
        time.sleep(1.5)
        print('')
        if rc == 0:
            print('Pesanan berhasil terkirim...')
        else:
            print('gagal terhubung!')
    
    
    # function untuk publish pesanan ke Laundry Bojong
    def publish_reverse(client_reverse, nama, berat, no_kategori):
        # kategori dideklarasikan dengan nomor kategori sebagai berikut
        if no_kategori == '1':
            kategori = 'Ekonomis'
        elif no_kategori == '2':
            kategori = 'Standar'
        elif no_kategori == '3':
            kategori = 'Premium'

        # deklarasi topik untuk publish pesanan ke laundry bojong
        topic_auto = 'autosub'
        
        # template pesan yang akan dikirim ke Laundry
        data_pesanan = nama+' membuat pesanan : \n -> laundry = '+berat+' Kg \n -> Kategori = '+kategori
        client_reverse.connect(broker, port)
        client_reverse.loop_start()
        print('')
        print('------ membuat pesanan ke laundry bojong ------')
        time.sleep(2)
        print('')

        # mempublish pesanan ke Laundry Bojong
        client_reverse.publish(topic_auto, data_pesanan, qos=1, retain=False)
        client_reverse.loop_stop()

    # deklrasi client untuk topic pesan terima kasih dari laundry bojong
    client = mqtt_client.Client('bojong', clean_session=True)
    client.on_connect = connect_laundryBojong
    client.connect(broker, port)

    # menjalankan proses publish pesanan ke Laundry Bojong
    client.loop_start()
    publish_reverse(client, nama, berat, no_kategori)

    client.loop_stop()

# function subscribe pesan feedback terima kasih dari Laundry soang
def sub_pesan_soang() :
    client = mqtt_client.Client('pesan')

    # on_message func untuk pesan apabila client telah berlangganan laundry soang
    def message_langgananSoang(client, userdata, msg):
        print('')
        pesan = str(msg.payload.decode('utf-8'))
        print(f'Pesan dari Laundry Soang : ',pesan)

    client.connect(broker, port)
    client.loop_start()
    client.subscribe(topic_cl2sn, qos=1)

    client.on_message = message_langgananSoang

# function untuk berlangganan Laundry Soang
def langganan_soang(nama, berat, no_kategori):
    
    # on_connect func untuk berlangganan
    def connect_laundrySoang(client, userdata, flags, rc):
        time.sleep(1.5)
        print('')
        if rc == 0:
            print('Pesanan berhasil terkirim...')
        else:
            print('gagal terhubung!')

    # function untuk publish pesanan ke Laundry Soang
    def publish_reverse(client_reverse, nama, berat, no_kategori):
        # kategori dideklarasikan dengan nomor kategori sebagai berikut
        if no_kategori == '1':
            kategori = 'Ekonomis'
        elif no_kategori == '2':
            kategori = 'Standar'
        elif no_kategori == '3':
            kategori = 'Premium'

        # deklarasi topik untuk publish pesanan ke laundry soang
        topic_auto = 'autosub soang'
        # client_reverse = mqtt_client.Client(topic_auto)

        # template pesan yang akan dikirim ke Laundry
        data_pesanan = nama+' membuat pesanan : \n -> laundry = '+berat+' Kg \n -> Kategori = '+kategori
        client_reverse.connect(broker, port)
        client_reverse.loop_start()
        print('')
        print('------ membuat pesanan ke Laundry Soang ------')
        time.sleep(2)
        print('')

        # mempublish pesanan ke Laundry Soang
        client_reverse.publish(topic_auto, data_pesanan, qos=1, retain=False)
        client_reverse.loop_stop()

    # deklrasi client untuk topic pesan terima kasih dari laundry soang
    client = mqtt_client.Client('soang', clean_session=True)
    client.on_connect = connect_laundrySoang
    client.connect(broker, port)

    # menjalankan proses publish pesanan ke Laundry Soang
    client.loop_start()
    publish_reverse(client, nama, berat, no_kategori)

    client.loop_stop()

# menu untuk berlangganan
def menu():
    # menggunakan modul PrettyTable untuk membuat tabel
    table = PrettyTable(['No', 'Menu'])
    table.add_row(['1', 'Langganan ke Laundry Bojong'])
    table.add_row(['2', 'Langganan ke Laundry Soang'])
    table.add_row(['3', 'Exit'])
    table.align = 'l'
    print(table)

# function untuk membandingkan waktu pengerjaan dan harga antara kedua laundry
def banding_waktu(nama, berat, jenis_paket):
    # waktu pengajuan laundry bojong dan soang sesuai hari client buat pesanan
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

    # layanan laundry Bojong
    if jenis_paket == '1':
        # untuk paket ekonomis pada laudnry bojong dikenakan biaya sebesar Rp 5.000 per Kg nya
        paket = 'Ekonomis'
        harga_bojong = str(int(des_berat * 5000))

        # proses pengerjaan sekitar 3 hari
        waktu_pengerjaan = today + \
            datetime.timedelta(
                days=3) + datetime.timedelta(minutes=0) + datetime.timedelta(minutes=0)
        ambil_laundry_bojong = str(waktu_pengerjaan.strftime(
            '%d-%m-%y')) + ' ('+str(waktu_pengerjaan.strftime('%H:%M:%S'))+') '

    elif jenis_paket == '2':
        # untuk paket standar pada laundry bojong dikenakan biaya sebesar Rp 7.500 per Kg nya
        paket = 'Standar'
        harga_bojong = str(int(des_berat * 7500))

        # proses pengerjaan sekitar 2 hari
        waktu_pengerjaan = today + \
            datetime.timedelta(
                days=2) + datetime.timedelta(minutes=0) + datetime.timedelta(minutes=0)
        ambil_laundry_bojong = str(waktu_pengerjaan.strftime(
            '%d-%m-%y')) + ' ('+str(waktu_pengerjaan.strftime('%H:%M:%S'))+') '

    elif jenis_paket == '3':
        # untuk paket premium pada laundry bojong dikenakan biaya sebesar Rp 9.000 per Kg nya
        paket = 'Premium'
        harga_bojong = str(int(des_berat * 9000))

        # proses pengerjaan sekitar 1 hari
        waktu_pengerjaan = today + \
            datetime.timedelta(
                days=1) + datetime.timedelta(minutes=0) + datetime.timedelta(minutes=0)
        ambil_laundry_bojong = str(waktu_pengerjaan.strftime(
            '%d-%m-%y')) + ' ('+str(waktu_pengerjaan.strftime('%H:%M:%S'))+') '


    # layanan laundry soang
    if jenis_paket == '1':
        # untuk paket ekonomis pada laundry soang dikenakan biaya sebesar Rp 6.000 per Kg nya
        harga_soang = str(int(des_berat * 6000))

        # proses pengerjaan sekitar 2 hari 20 menit
        waktu_pengerjaan = today + \
            datetime.timedelta(
                days=2) + datetime.timedelta(minutes=20) + datetime.timedelta(minutes=0)
        ambil_laundry_soang = str(waktu_pengerjaan.strftime(
            '%d-%m-%y')) + ' ('+str(waktu_pengerjaan.strftime('%H:%M:%S'))+') '
    elif jenis_paket == '2':
        # untuk paket standar pada laundry soang dikenakan biaya sebesar Rp 8.500 per Kg nya
        harga_soang = str(int(des_berat * 8500))

        # proses pengerjaan sekitar 1 hari 20 menit
        waktu_pengerjaan = today + \
            datetime.timedelta(
                days=1) + datetime.timedelta(minutes=20) + datetime.timedelta(minutes=0)
        ambil_laundry_soang = str(waktu_pengerjaan.strftime(
            '%d-%m-%y')) + ' ('+str(waktu_pengerjaan.strftime('%H:%M:%S'))+') '
    elif jenis_paket == '3':
        # untuk paket premium pada laundry soang dikenakan biaya sebesar Rp 10.000 per Kg nya
        harga_soang = str(int(des_berat * 10000))

        # proses pengerjaan sekitar 12 jam 20 menit
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


# tampilan menu exit
def ExitMenu():
    time.sleep(3)
    print('')
    print('Keluar dari program.....')

# menu utama
if __name__ == '__main__':
    status = True
    while status:
        # client menginput data - data untuk pesan laundry
        os.system('cls')
        print('')
        print('+-----------------------------------+')
        print('|        Masukan data laundry       |')
        print('+-----------------------------------+')
        nama = input('Nama          : ')
        berat = input('Berat (kg)    : ')
        # pilih kategori paket
        print('')
        print('+-----------------------------------+')
        print('|       Pilih Kategori Paket        |')
        print('+-----------------------------------+')
        print('1. Ekonomis')
        print('2. Standar')
        print('3. Premium')
        jenis_paket = input('Pilih nomor kategori paket : ')
        if jenis_paket == '1' or jenis_paket == '2' or jenis_paket == '3':
            # menampilkan perbandingan waktu dan harga antar kedua laundry
            banding_waktu(nama,berat,jenis_paket)
            menu()
            pil = input('pilih menu berlangganan laundry : ')
            print('')
            if pil=="1":
                # validasi lanjut pesanan
                fed = input(f'Lanjutkan pesanan atau tidak? (y/n) \n -> ')
                if fed == 'y' or fed == 'Y':

                    """
                        pada bagian proses order client melakukan subscribe pesan terimakasih dari laundry yang dipilih terlebih dahulu
                        selanjutnya by program pihak laundry melakukan subscribe topik pesanan, sehingga client tinggal melakukan publish pesanannya.

                    """

                    # proses order laundry bojong
                    sub_pesan_bojong()
                    langganan_bojong(nama, berat, jenis_paket)

                    # validasi apakah ingin melakukan pesan lagia atau tidak
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

                    # proses order laundry soangm
                    sub_pesan_soang()
                    langganan_soang(nama, berat, jenis_paket)
                    lanjut = input('lanjut? (y/n)')
                    if lanjut == 'y' or lanjut == "Y":
                        status = True
                    else:
                        status = False
                else:
                    # handle error ketika salah input
                    status = False
                    print('program berhenti...')
                    time.sleep(2)
            elif pil=='3':
                # exit
                status = False
                os.system('cls')
                ExitMenu()

                
        
        else:
            # handle error ketika salah input
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

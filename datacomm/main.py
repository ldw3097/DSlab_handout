def main():
    while True:
        print('Morse Code Data Communication 2022')
        print('[1] Send data over sound (play)')
        print('[2] Receive data over sound (record)')
        print('[q] Exit')
        select = input('Select menu: ').strip().upper()
        if select == '1':
            send_data()
        elif select == '2':
            receive_data()
        elif select == 'Q':
            print('Terminating...')
            break;


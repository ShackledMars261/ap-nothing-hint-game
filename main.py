import archipelago
import asyncio

if __name__ == '__main__':
    ip: str = input(f'What is the server\'s IP? (Leave blank for archipelago.gg): ')
    port: int = int(input(f'What is the server\'s port?: '))
    slot_name: str = input(f'What is your slot\'s name?: ')
    password: str = input(f'What is the server\'s password? Leave blank if there isn\'t one.: ')
    asyncio.run(archipelago.main(ip, port, slot_name, password))
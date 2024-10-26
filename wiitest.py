#!/usr/bin/python3
import cwiid
import time
import sys
import os

def connect_wimote():
    print('Starting Wii Remote connection process...')
    print('Please wait 2 seconds before pressing 1 + 2...')
    time.sleep(2)
    
    # Set the timeout through environment variable
    os.environ['WIIMOTE_TIMEOUT'] = '15'
    
    attempts = 0
    max_attempts = 3
    
    while attempts < max_attempts:
        try:
            print(f'\nAttempt {attempts + 1} of {max_attempts}')
            print('Press and hold 1 + 2 on your Wii Remote now...')
            
            # Try to connect without timeout parameter
            wiimote = cwiid.Wiimote()
            
            # If we get here, connection was successful
            print('\nWii Remote connected successfully!')
            
            # Initialize with lower rumble to avoid power issues
            wiimote.led = 0
            wiimote.rumble = False
            time.sleep(0.1)
            wiimote.rpt_mode = cwiid.RPT_BTN
            
            return wiimote
            
        except RuntimeError as e:
            print(f'Connection attempt failed: {e}')
            attempts += 1
            
            if attempts < max_attempts:
                print('\nWaiting 5 seconds before next attempt...')
                print('Please make sure Wii Remote is in discovery mode (press 1+2)')
                time.sleep(5)
            else:
                print('\nFailed to connect after all attempts.')
                return None
        
        except Exception as e:
            print(f'Unexpected error: {e}')
            return None
            
    return None

# Main program
def main():
    print('Starting DarkMark Wii Remote Program...')
    print('Initializing Bluetooth...')
    time.sleep(1)
    
    # Try to connect
    wiimote = connect_wimote()
    
    if wiimote is None:
        print('\nCould not connect to Wii Remote.')
        print('Please check:')
        print('1. Batteries are fresh')
        print('2. No other devices are connected to the Wii Remote')
        print('3. You are within 3 feet of the Raspberry Pi')
        sys.exit(1)
        
    print('Setup complete! Wii Remote is ready.')
    
    # Your existing code continues here...

if __name__ == "__main__":
    main()
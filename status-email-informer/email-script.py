import smtplib
import requests
import time

from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# EMAIL CONFIGURATION
MY_ADDRESS = 'your@email.com'
PASSWORD = 'password'
EMAIL_HOST = 'smtp-mail.outlook.com'
EMAIL_PORT = 587
MESSAGE_FILE = '/home/hanchon/development/message.txt'
RECIPIENTS = ['jhon@email.com', 'jhon2@email.com']

# BITCOIN RPC CONFIGURATION
RPC_ADDRESS = "http://127.0.0.1:8332"
RPC_USER = "bitcoin"
RPC_PASSWORD = "password"

# GLOBALs
LAST_HEIGHT = "504031"
LAST_HASH = "0000000000000000011ebf65b60d0a3de80b8175be709d653b4c1a1beeb6ab9c"
LAST_DIFF = "522462745900.0715"
LAST_TIME = "1510606688"
LAST_MTP = "1510601033"

# RPC FUNCTIONS


def send_curl(payload):
    headers = {'content-type': 'text/plain;'}
    return requests.post(RPC_ADDRESS, data=payload, headers=headers, auth=(RPC_USER, RPC_PASSWORD))


def get_info():
    payload = '{"jsonrpc": "1.0", "id":"curltest", "method": "getinfo", "params": [] }'
    return send_curl(payload)


def get_block_hash(height):
    payload = '{"jsonrpc": "1.0", "id":"curltest", "method": "getblockhash", "params": [' + str(
        height) + '] }'
    return send_curl(payload)


def get_block(hash):
    payload = '{"jsonrpc": "1.0", "id":"curltest", "method": "getblock", "params": ["' + str(
        hash) + '"] }'
    return send_curl(payload)

# INIC FUNCTIONS


def inic_globals():
    global LAST_HEIGHT, LAST_HASH, LAST_DIFF, LAST_TIME, LAST_MTP
    info = get_info()
    if (info.status_code == requests.codes.ok):
        block_hash = get_block_hash(info.json()['result']['blocks'])
        if (block_hash.status_code == requests.codes.ok):
            block = get_block(block_hash.json()['result'])
            if (block.status_code == requests.codes.ok):
                json = block.json()['result']
                LAST_HEIGHT = json['height']
                LAST_HASH = json['hash']
                LAST_DIFF = json['difficulty']
                LAST_TIME = json['time']
                LAST_MTP = json['mediantime']
                return True
    return False

# BLOCKHAIN FUNCTIONS


def process_info():
    global LAST_HEIGHT, LAST_HASH, LAST_DIFF, LAST_TIME, LAST_MTP
    info = get_info()
    if (info.status_code == requests.codes.ok):
        if (info.json()['result']['blocks'] > int(LAST_HEIGHT)):
            # There is a new block
            block_hash = get_block_hash(info.json()['result']['blocks'])
            if (block_hash.status_code == requests.codes.ok):
                block = get_block(block_hash.json()['result'])
                if (block.status_code == requests.codes.ok):
                    json = block.json()['result']
                    data = []
                    # OLD BLOCK
                    data.append(LAST_HEIGHT)
                    data.append(LAST_HASH)
                    data.append(LAST_DIFF)
                    data.append(LAST_TIME)
                    data.append(LAST_MTP)
                    # NEW BLOCK
                    data.append(json['height'])
                    data.append(json['hash'])
                    data.append(json['difficulty'])
                    data.append(json['time'])
                    data.append(json['mediantime'])

                    # Send email
                    send_email(data)

                    # Update globals
                    LAST_HEIGHT = json['height']
                    LAST_HASH = json['hash']
                    LAST_DIFF = json['difficulty']
                    LAST_TIME = json['time']
                    LAST_MTP = json['mediantime']

                    # Wait for new blocks
                    time.sleep(20)

    time.sleep(20)

# EMAIL FUNCTIONS


def read_template(filename):
    # Read from file
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def send_email(data):
    # set up the SMTP server
    s = smtplib.SMTP(host=EMAIL_HOST, port=EMAIL_PORT)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(MY_ADDRESS, PASSWORD)

    # message to send
    message_template = read_template(MESSAGE_FILE)
    message = message_template.substitute(PREV_HEIGHT=data[0], PREV_HASH=data[1], PREV_DIFF=data[
                                          2], PREV_TIME=data[3], PREV_MTP=data[4], HEIGHT=data[5], HASH=data[6], DIFF=data[7], TIME=data[8], MTP=data[9])
    # show it
    print(message)

    for email in RECIPIENTS:
        msg = MIMEMultipart()
        msg['From'] = MY_ADDRESS
        msg['To'] = email
        msg['Subject'] = "BCC old chain minned the block: " + str(data[5])
        msg.attach(MIMEText(message, 'plain'))
        s.send_message(msg)
        del msg

    # Terminate the SMTP session and close the connection
    s.quit()

if __name__ == '__main__':
    if (inic_globals()):
        while True:
            process_info()

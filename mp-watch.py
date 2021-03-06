import urllib2
from lxml import html
import argparse
import time
from sets import Set
import Tkinter as tk
import ttk
import smtplib
from threading import Thread

NORM_FONT= ("Verdana", 10)

def send_popup_notification(t):
    msg = 'Hi, Michael!  Hope you\'re having a wonderful day.  The topic \'' + t + '\' was just posted to the MP forums.'.encode('ascii', 'ignore')
    popup = tk.Tk()
    popup.wm_title("!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Thanks, Matt", command = popup.destroy)
    B1.pack()
    popup.mainloop()
    print('Closed popup')

def send_email_notification(t, username, password, toaddr):
    msg = 'Hi Michael!  Hope you\'re having a wonderful day.  The topic \'' + t + '\' was just posted to the MP forums.'.encode('ascii', 'ignore')

    server = smtplib.SMTP('smtp.gmail.com:587', timeout=10)
    server.starttls()
    server.login(username, password)
    try:
        server.sendmail(username, toaddr, msg)
    except:
        print('Error sending email')
        return
    server.quit()
    print('Sent email notification')

def main():
    parser = argparse.ArgumentParser(description='Keep Michael productive without missing great deals.')
    parser.add_argument('time_interval', type=int, help='How often to check mountain project (seconds)')
    parser.add_argument('-k', '--keywords', nargs='+', help='<Required> list of keywords to search for', required=True)
    parser.add_argument('--send_email', action='store_true', help='Send an email notification.  Must include email account details arguments')
    parser.add_argument('--email', help='Email to use to send notification')
    parser.add_argument('--password', help='Email password to use to send notification')
    parser.add_argument('--to_addr', help='Where you are sending the notification')
    args = parser.parse_args()

    sent_topics = Set() 

    while True:
        try:
            url = "http://www.mountainproject.com/"
            request = urllib2.Request(url)
            request.add_header('User-Agent', 'Mozilla/5.0')
            request.add_header('Pragma', 'no-cache')
            contents = urllib2.build_opener().open(request).read()
        except:
            print('Failed to get website contents')
            continue
        tree = html.fromstring(contents)
        topics = tree.xpath('//a[@class="topic"]/text()')
        for k in args.keywords:
            for t in topics:
                if k.lower() in t.lower() and t not in sent_topics:
                    thread = Thread(target = send_popup_notification, args = (t, ))
                    thread.start()
                    if args.send_email is True:
                        if not ( args.email is not None and args.password is not None and args.to_addr is not None):
                            print 'Michael... you need to give your email account info to send an email notification'
                            return
                        send_email_notification(t, args.email, args.password, args.to_addr)
                    print(t)
                    sent_topics.add(t)
        time.sleep(args.time_interval)

if __name__ == '__main__':
    main()

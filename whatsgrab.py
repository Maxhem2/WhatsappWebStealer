import cv2
import mss
from time import sleep
import ftplib
import pyautogui
import mouse
import psutil
import os
from win32api import GetSystemMetrics
import numpy as np
from pyautogui import position as pag
import keyboard

ftpadress="myserver.com/Ip"
ftpuser="admin"
ftppassword="password"
ftpwhatshookfolderlocation="httpsdocs/WhatsHook"

def QRCodeComparer(current_qrcode):
    image = cv2.imread(current_qrcode)

    qrCodeDetector = cv2.QRCodeDetector()
    
    decodedText, points, _ = qrCodeDetector.detectAndDecode(image)

    cropImage = image[int(tuple(points.tolist()[0][0])[1]):int(tuple(points.tolist()[0][2])[1]), int(tuple(points.tolist()[0][0])[0]):int(tuple(points.tolist()[0][1])[0])]

    cv2.imwrite("qrcode.png", cropImage)

    return (points.tolist()[0][0][0]+90, points.tolist()[0][0][1]+90)

wad = False
waw = False
clear = lambda: os.system('cls')

while True:
    print('What WhatsApp Version will you be using?')

    print('Enter 1 for WhatsApp Desktop\n')

    print('Enter 2 for WhatsApp Web\n')

    choice = int(input('Enter your choice: '))

    if choice == 1:
        wad = True
        break

    if choice == 2:
        waw = True
        break
    else:
        print('Invalid choice')
        sleep(1)
        clear()

if wad == True:
    sct = mss.mss()
    os.system("TASKKILL /F /IM WhatsApp.exe")
    sleep(1)
    process_name = "WhatsApp"
    pid = None
    for proc in psutil.process_iter():
        if process_name in proc.name():
            pid = proc.pid
    if pid == None:
        os.system('start WhatsApp:')
    print("Hover over the Let's go button and press enter!")
    if keyboard.read_key() == "enter":
            WhatsAppLetsGoButton = pag()
            print("Recorded: "+ str(WhatsAppLetsGoButton))
    # The screen part to capture
    monitor = {"top": WhatsAppLetsGoButton[1]-9, "left": WhatsAppLetsGoButton[0]-22, "width": 50, "height": 20}

    # Grab the data
    sct_img = sct.grab(monitor)

    # Save to the picture file
    mss.tools.to_png(sct_img.rgb, sct_img.size, output="WhatsAppLetsGoButton.png")
    sleep(1)
    print("Open WhatsApp Beta, login and scan the qr code (you can use your own whatsapp account, does not matter yet) and hover over the Whatsapp Logo Image in WhatsApp Beta (where the chat normally is), then press enter!")
    if keyboard.read_key() == "enter":
            WhatsappLogoImage = pag()
            print("Recorded: "+str(WhatsappLogoImage))
    # The screen part to capture
    monitor = {"top": WhatsappLogoImage[1]-20, "left": WhatsappLogoImage[0]-22, "width": 50, "height": 50}

    # Grab the data
    sct_img = sct.grab(monitor)

    # Save to the picture file
    mss.tools.to_png(sct_img.rgb, sct_img.size, output="WhatsappLogoImage.png")

    print("Setup done! Now logout of WhatsApp.")
    while True:
        sleep(1)
        pid = None
        for proc in psutil.process_iter():
            if process_name in proc.name():
                pid = proc.pid
        if pid == None:
            os.system('start WhatsApp:')
        img_rgb = cv2.cvtColor(np.array(sct.grab({"top": 0, "left": 0, "width": GetSystemMetrics(0), "height": GetSystemMetrics(1)})), cv2.COLOR_RGBA2RGB)
        img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
        template = cv2.imread("WhatsAppLetsGoButton.png",0)
        res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
        threshold = 0.7
        loc = np.where( res >= threshold)
        cords = (GetSystemMetrics(0)+1, GetSystemMetrics(1)+1)
        for pt in zip(*loc[::-1]):
            if pt[1] <= cords[1]:
                cords = (pt[0], pt[1])
                t_cords = (pt[0]+1, pt[1]+1)
        if cords != (GetSystemMetrics(0)+1, GetSystemMetrics(1)+1):
            pyautogui.moveTo(t_cords)
            mouse.press(button='left')
            sleep(0.1)
            mouse.release(button='left')
            break
    end = False
    while True:
        try:
            try:
                sleep(1)
                pos = QRCodeComparer(sct.shot())
                i=0
                print("QrCode found!")
                # to file 
                session = ftplib.FTP(ftpadress,ftpuser,ftppassword)
                file = open("qrcode.png",'rb')
                session.cwd(ftpwhatshookfolderlocation)
                session.storbinary('STOR qrcode.gif', file)
                file.close()
                session.quit()
            except:
                ##check if logged it first
                i = 0
                while True:
                    i+=1
                    img_rgb = cv2.cvtColor(np.array(sct.grab({"top": 0, "left": 0, "width": GetSystemMetrics(0), "height": GetSystemMetrics(1)})), cv2.COLOR_RGBA2RGB)
                    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
                    template = cv2.imread("WhatsappLogoImage.png",0)
                    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
                    threshold = 0.7
                    loc = np.where( res >= threshold)
                    cords = (GetSystemMetrics(0)+1, GetSystemMetrics(1)+1)
                    for pt in zip(*loc[::-1]):
                        if pt[1] <= cords[1]:
                            cords = (pt[0], pt[1])
                            t_cords = (pt[0]+1, pt[1]+1)
                    if cords != (GetSystemMetrics(0)+1, GetSystemMetrics(1)+1):
                        end = True
                        break
                    if i == 3:
                        break
                if end == True:
                    break
                session = ftplib.FTP(ftpadress,ftpuser,ftppassword)
                file = open("qrcodenotfound.png",'rb')
                session.cwd(ftpwhatshookfolderlocation)
                session.storbinary('STOR qrcode.gif', file)
                file.close()
                session.quit()
                if pos == 0:
                    pass
                os.system("TASKKILL /F /IM WhatsApp.exe")
                while True:
                    sleep(1)
                    pid = None
                    for proc in psutil.process_iter():
                        if process_name in proc.name():
                            pid = proc.pid
                    if pid == None:
                        os.system('start WhatsApp:')
                        break
                while True:
                    sleep(1)
                    for proc in psutil.process_iter():
                        if process_name in proc.name():
                            pid = proc.pid
                    if pid != None:
                        while True:
                            sleep(1)
                            img_rgb = cv2.cvtColor(np.array(sct.grab({"top": 0, "left": 0, "width": GetSystemMetrics(0), "height": GetSystemMetrics(1)})), cv2.COLOR_RGBA2RGB)
                            img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
                            template = cv2.imread("WhatsAppLetsGoButton.png",0)
                            res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
                            threshold = 0.7
                            loc = np.where( res >= threshold)
                            cords = (GetSystemMetrics(0)+1, GetSystemMetrics(1)+1)
                            for pt in zip(*loc[::-1]):
                                if pt[1] <= cords[1]:
                                    cords = (pt[0], pt[1])
                                    t_cords = (pt[0]+1, pt[1]+1)
                            if cords != (GetSystemMetrics(0)+1, GetSystemMetrics(1)+1):
                                pyautogui.moveTo(t_cords)
                                mouse.press(button='left')
                                sleep(0.1)
                                mouse.release(button='left')
                                break
                        break
                print("Updated QrCode!")
                sleep(3)
        except:
            print("QrCode not found yet!")
    os.remove("monitor-1.png")
    os.remove("WhatsappLogoImage.png")
    os.remove("WhatsAppLetsGoButton.png")
    os.remove("qrcode.png")
    # to file
    session = ftplib.FTP(ftpadress,ftpuser,ftppassword)
    file = open("operationfinished.png",'rb')
    session.cwd(ftpwhatshookfolderlocation)
    session.storbinary('STOR qrcode.gif', file)
    file.close()
    session.quit()
    print("Now you should be logged in. / You can close this window now")
    input()

if waw == True:
    sct = mss.mss()
    print("Open your browser, go to web.whatsapp.com and scan the qr code (you can use your own whatsapp account, does not matter yet) and hover over the WhatsappLaptopImage in WhatsApp Web (where the chat normally is), then press enter!")
    sleep(1)
    if keyboard.read_key() == "enter":
            WhatsAppLaptopImage = pag()
            print("Recorded: "+ str(WhatsAppLaptopImage))
    # The screen part to capture
    monitor = {"top": WhatsAppLaptopImage[1]-20, "left": WhatsAppLaptopImage[0]-22, "width": 50, "height": 50}

    # Grab the data
    sct_img = sct.grab(monitor)

    # Save to the picture file
    mss.tools.to_png(sct_img.rgb, sct_img.size, output="WhatsAppLaptopImage.png")
    print("Now logout of whatsapp web and your done.")
    while True:
        try:
            sleep(1)
            pos = QRCodeComparer(sct.shot())
            i=0
            print("QrCode found!")
            # to file 
            session = ftplib.FTP(ftpadress,ftpuser,ftppassword)
            file = open("qrcode.png",'rb')
            session.cwd(ftpwhatshookfolderlocation)
            session.storbinary('STOR qrcode.gif', file)
            file.close()
            session.quit()
            break
        except:
            pass
    print("Setup done!")
    end = False
    while True:
        try:
            try:
                sleep(1)
                pos = QRCodeComparer(sct.shot())
                i=0
                print("QrCode found!")
                # to file 
                session = ftplib.FTP(ftpadress,ftpuser,ftppassword)
                file = open("qrcode.png",'rb')
                session.cwd(ftpwhatshookfolderlocation)
                session.storbinary('STOR qrcode.gif', file)
                file.close()
                session.quit()
                pyautogui.moveTo(pos)
                mouse.press(button='left')
                sleep(0.1)
                mouse.release(button='left')
            except:
                ##check if logged it first
                while True:
                    img_rgb = cv2.cvtColor(np.array(sct.grab({"top": 0, "left": 0, "width": GetSystemMetrics(0), "height": GetSystemMetrics(1)})), cv2.COLOR_RGBA2RGB)
                    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
                    template = cv2.imread("WhatsAppLaptopImage.png",0)
                    res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
                    threshold = 0.7
                    loc = np.where( res >= threshold)
                    cords = (GetSystemMetrics(0)+1, GetSystemMetrics(1)+1)
                    for pt in zip(*loc[::-1]):
                        if pt[1] <= cords[1]:
                            cords = (pt[0], pt[1])
                            t_cords = (pt[0]+1, pt[1]+1)
                    if cords != (GetSystemMetrics(0)+1, GetSystemMetrics(1)+1):
                        end = True
                    break
                if end == True:
                    break
                session = ftplib.FTP(ftpadress,ftpuser,ftppassword)
                file = open("qrcodenotfound.png",'rb')
                session.cwd(ftpwhatshookfolderlocation)
                session.storbinary('STOR qrcode.gif', file)
                file.close()
                session.quit()
                if pos == 0:
                    pass
                sleep(1)
        except:
            print("QrCode not found yet!")
    os.remove("monitor-1.png")
    os.remove("qrcode.png")
    os.remove("WhatsAppLaptopImage.png")
    # to file
    session = ftplib.FTP(ftpadress,ftpuser,ftppassword)
    file = open("operationfinished.png",'rb')
    session.cwd(ftpwhatshookfolderlocation)
    session.storbinary('STOR qrcode.gif', file)
    file.close()
    session.quit()
    print("Now you should be logged in. / You can close this window now")
    input()
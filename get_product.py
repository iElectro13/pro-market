import cv2 as cv
import numpy as np
from windowcapture import WindowCapture
from datetime import datetime
import pytesseract
import pyautogui
import time
import openpyxl

pyautogui.FAILSAFE = False
pytesseract.pytesseract.tesseract_cmd = r"F:\Program Files\Tesseract-OCR\tesseract"
capture = WindowCapture()

class Scrapper:
    items = ["axe ring", "dwarven ring", "life ring", "might ring", "prismatic ring", "ring of blue plasma", "ring of green plasma", "ring of healing", "ring of red plasma", "stealth ring", "sword ring", "time ring"]
    wait_time = 0.2
    wb = openpyxl.load_workbook("items.xlsx")
    item_list = []
    t = time.localtime()

    def __init__(self):
        balance = 0

    def search_info(self):
        for item in self.items:
            pyautogui.moveTo(760, 641, self.wait_time, pyautogui.easeOutQuad)
            pyautogui.click()
            pyautogui.moveTo(472, 599, self.wait_time, pyautogui.easeOutQuad)
            pyautogui.click()
            pyautogui.moveTo(405, 600, self.wait_time, pyautogui.easeOutQuad)
            pyautogui.click()
            pyautogui.write(item, interval=0.05)
            pyautogui.moveTo(384, 303, self.wait_time, pyautogui.easeOutQuad)
            pyautogui.click()
            time.sleep(0.4)
            offers = capture.get_video()
            offers = offers[167:299, 491:1038]
            #offers = cv.cvtColor(offers, cv.COLOR_BGR2GRAY)
            #offers = cv.inRange(offers, self.minimo_actual, self.maximo_actual)
            pyautogui.moveTo(841, 643, self.wait_time, pyautogui.easeOutQuad)
            pyautogui.click()
            time.sleep(0.1)
            details = capture.get_video()
            details = details[328:471, 491:1038]
            #details = cv.cvtColor(details, cv.COLOR_BGR2GRAY)
            #details = cv.inRange(details, self.minimo_detail, self.maximo_detail)
            conc = cv.vconcat([offers, details])
            cv.imwrite(f"{item}.png", conc)

    def find_coor(self):

        for item in self.items:
            detail_list = []
            info = cv.imread(f"{item}.png")
            actual_price = info[17:32, 191:273]
            actual_price = self.extract_number(actual_price, 0)

            high_price = info[230:243, 12:240]
            high_price = self.extract_number(high_price, -2)

            average_price = info[243:256, 12:240]
            average_price = self.extract_number(average_price, -2)

            low_price = info[256:269, 12:240]
            low_price = self.extract_number(low_price, -2)

            current_time = time.strftime("%H:%M:%S", self.t)
            current_date = datetime.today().strftime('%Y-%m-%d')

            detail_list.append(current_date)
            detail_list.append(current_time)
            detail_list.append(actual_price)
            detail_list.append(high_price)
            detail_list.append(average_price)
            detail_list.append(low_price)
            detail_list = tuple(detail_list)
            hoja = self.wb[f"{item}"]
            self.wb.active = hoja
            hoja.append(detail_list)
        self.wb.save("items.xlsx")
        print("Done!")

    def extract_number(self, price, index):
        price = pytesseract.image_to_string(price, config="--psm 10 --oem 3")
        price = price[:-1]
        price = price.split()
        price = price[index]
        price = str(price)
        price = price.replace(",", "")
        try:
            price = int(price)
        except:
            pass
        return price
    
    def sheet_creator(self):
        sheets = ["axe ring", "dwarven ring", "life ring", "might ring", "prismatic ring", "ring of blue plasma", "ring of green plasma", "ring of healing", "ring of red plasma", "stealth ring", "sword ring", "time ring"]
        for sheet in sheets:
            if sheet not in self.items:
                ws = self.wb.create_sheet(f"{sheet}")
            else:
                pass
        self.wb.save("items.xlsx")

time.sleep(2)
scrapper = Scrapper()
scrapper.search_info()
scrapper.find_coor()
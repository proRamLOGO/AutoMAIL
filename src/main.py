#!/usr/bin/env python

import pandas as pd
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

from sendMail import sendMail
from config import CER_PATH, DATA_PATH
import os

BASE_DIR = os.getcwd()


def createDic(df, lst):
    dic = {}
    for (n, e), rest in df.groupby(lst):
        dic[e] = n.lower().replace(' ', '_')

    return dic


def drawName(msg, fnt='bahnschrift', fnt_sz=45, show=False):
    img = Image.open(os.path.join(BASE_DIR, CER_PATH))
    img_draw = ImageDraw.Draw(img)
    W, H = img.size

    font = ImageFont.truetype(
        f"C:/Users/System-Pc/Desktop/{fnt}.ttf", fnt_sz)

    w, h = font.getsize(msg)

    # saurabh45
    # img_draw.text(((W-w)/2, (H-h)/2 + 65),
    #               msg.replace("_", " ").title(), fill='black', font=font)

    # cat70
    img_draw.text(((W-w)/2, (H-h)/2 + 145),
                  msg.replace("_", " ").title(), fill='black', font=font)

    # nidhi100
    # img_draw.text(((W-w)/2 + 15, (H-h)/2 + 90),
    #               msg.replace("_", " ").title(), fill='black', font=font)

    if show:
        img.show()
    else:
        op = os.path.join(BASE_DIR, 'output')
        os.makedirs(op, exist_ok=True)
        img.save(os.path.join(
            BASE_DIR, f'output/{msg.lower().replace(" ", "_")}.pdf'))


def run(m_data):
    failed = {}
    for mail in m_data:
        name = m_data[mail]
        print(f"Processing...{name.upper()} : {mail}")
        drawName(name, fnt_sz=70)
        try:
            sendMail(name, mail)
        except Exception as e:
            failed[name] = mail
            print("ERROR :", e)

    print("\n\nProcess Complted , Total :", len(m_data)-len(failed), "sent")
    print("\nFailed Tasks : ", failed)


# if __name__ == "__main__":
#     try:
#         df = pd.read_csv(os.path.join(os.getcwd(), DATA_PATH))
#         mail_data = createDic(df, ['name', 'email'])
#         run(mail_data)
#     except Exception as e:
#         print("ERROR : ", e)

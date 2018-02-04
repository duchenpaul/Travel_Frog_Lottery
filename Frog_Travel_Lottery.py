import sys, subprocess, os, time, random
from PIL import Image, ImageChops

# adb tcpip 5555
# adb connect 192.168.2.103:5555


blue_patten = (89, 167, 227, 255)
green_patten = (134, 211, 101, 255)
white_patten = (247, 243, 227, 255)
red_patten = (239, 102, 89, 255)
yellow_patten = (235, 207, 105, 255)

screenshot_way = 2

def equal(im1, im2): 
    return ImageChops.difference(im1, im2).getbbox() is None

def pull_screenshot(): 
    '''
    新的方法请根据效率及适用性由高到低排序
    '''
    global screenshot_way
    if screenshot_way == 2 or screenshot_way == 1:
        process = subprocess.Popen('adb shell screencap -p', shell=True, stdout=subprocess.PIPE)
        screenshot = process.stdout.read()
        if screenshot_way == 2:
            binary_screenshot = screenshot.replace(b'\r\n', b'\n')
        else:
            binary_screenshot = screenshot.replace(b'\r\r\n', b'\n')
        f = open('screenshot.png', 'wb')
        f.write(binary_screenshot)
        f.close()
    elif screenshot_way == 0:
        os.system('adb shell screencap -p /sdcard/screenshot.png')
        os.system('adb pull /sdcard/screenshot.png .')

def check_screenshot():
    '''
    检查获取截图的方式
    '''
    global screenshot_way
    if os.path.isfile('autojump.png'):
        os.remove('autojump.png')
    if (screenshot_way < 0):
        print('暂不支持当前设备')
        sys.exit()
    pull_screenshot()
    try:
        Image.open('./autojump.png').load()
        print('采用方式 {} 获取截图'.format(screenshot_way))
    except Exception:
        screenshot_way -= 1
        check_screenshot()

def android_tap(x, y):
    cmd  =  'adb shell input tap {x} {y}'.format(x = x, y = y)
    # print(cmd)
    os.system(cmd)

def enter_store():
    print('[Tap] Enter Store')
    android_tap(991, 1677)
    time.sleep(.5)
    android_tap(997, 100)
    time.sleep(.5)

def roll_lottery():
    while not isBuyButton():
        select_one()
        ok_button()
    
    print('[Tap] roll lottery')
    android_tap(276, 1649)
    time.sleep(3)

def get_marble():
    print('[Tap] Get marble')
    android_tap(545, 936)

def select_one():
    # 1
    # android_tap(528, 686)  
    # 2
    # android_tap(347, 953)
    # 3
    # android_tap(471, 1128)
    # 4
    # android_tap(471, 1366)
    # 5
    # android_tap(471, 1499)
    print('[Tap] pick an award')
    item = (686, 953, 1128, 1366, 1499)
    android_tap(471, random.choice(item))
    time.sleep(1)

def ok_button():
    print('[Tap] OK')
    android_tap(393, 1091)
    time.sleep(.5)

def isBuyButton():
    pull_screenshot()
    im = Image.open('./screenshot.png')
    im_pixel = im.load()
    bounds = (100, 1555, 473, 1724)
    cutoutIm = im.crop(bounds)
    # print(cutoutIm)
    buyButton = Image.open('./buy_button.png')
    # print(buyButton)
    return equal(buyButton, cutoutIm)

def log_color(color):
	with open('./color.log', 'a') as f:
		f.write(color + '\n')

if __name__ == '__main__':
    if not isBuyButton():
        enter_store()
    
    while True:
        roll_lottery()
        pull_screenshot()
        im = Image.open('./screenshot.png')
        im_pixel = im.load()
        # im.show()
        start_x = 418
        start_y = 798

        bounds = (start_x, start_y, start_x + 240, start_y + 240)
        cutoutIm = im.crop(bounds)
        # cutoutIm.show()
        cutoutIm_pix = cutoutIm.load()
        print(cutoutIm_pix[120, 120])
        if cutoutIm_pix[120, 120] == white_patten:
            print("White!")
            log_color("White!")
            get_marble()
            ok_button()

        elif cutoutIm_pix[120, 120] == green_patten:
            print("Green!")
            log_color("Green!")
            get_marble()
            select_one()
            ok_button()

        elif cutoutIm_pix[120, 120] == blue_patten:
            print("Blue!")
            log_color("Blue!")
            get_marble()
            select_one()
            ok_button()

        elif cutoutIm_pix[120, 120] == red_patten:
            print("Red!")
            log_color("Red!")
            get_marble()
            select_one()
            ok_button()

        elif cutoutIm_pix[120, 120] == yellow_patten:
            print("Yellow!")
            log_color("Yellow!")
            get_marble()
            select_one()
            ok_button()

        else:
            print("New color pattern found, or the process is crashed, shutting down...")
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            with open('./log.txt', 'a') as f:
                f.write(timestamp + ' - ' + str(cutoutIm_pix[120, 120]) + '\n')
            im.save('./' + timestamp + '.png',format = 'png')
            quit()
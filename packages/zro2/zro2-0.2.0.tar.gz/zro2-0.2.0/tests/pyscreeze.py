from time import sleep
import pyautogui
import screeninfo
from zro2.pyscreeze import boxcenter, waitTillImage

monitor=screeninfo.get_monitors()[2]
w = waitTillImage(
    "./tests/image1.png",
    confidence=0.65,
    monitor = monitor
)

sleep(1)
pyautogui.click(boxcenter(w))
sleep(1)
pass
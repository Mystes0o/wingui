from WinGuiBase import Win
from ImageBase import utils

"""屏幕录制"""
class EreScreen(Win):
    def __init__(self):
        super().__init__(handle_title="EreWindowBar")

webcam = utils.read_images(r'../test/webcam.png')
if __name__ == '__main__':
    ereScreen = EreScreen()
    ereScreen.screenshot()
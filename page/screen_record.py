from WinGuiBase import Win
from ImageBase import utils

"""屏幕录制"""
class EreScreen(Win):
    def __init__(self):
        super().__init__(handle_title="EreWindowBar")

recordButton = utils.read_images(r'../test/recordButton.png')
if __name__ == '__main__':
    ereScreen = EreScreen()
    ereScreen.click(recordButton)
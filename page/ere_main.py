from WinGuiBase import Win
from ImageBase import utils

"""主界面"""
class EreMain(Win):
    def __init__(self):
        super().__init__(handle_title="EaseUs RecExperts")


screen = utils.read_images(r'../test/screen.png')
window = utils.read_images(r'../test/window.png')
game = utils.read_images(r'../test/game.png')
audio = utils.read_images(r'../test/audio.png')
webcam = utils.read_images(r'../test/webcam.png')

if __name__ == '__main__':
    main = EreMain()

    main.click(template=audio)



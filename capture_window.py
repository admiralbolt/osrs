import utils

utils.focus_runescape()
print(utils.find_on_screen(window_bounds=utils.TILE_LOC_BOUND, template_path="images/ztiny_fake.png", save_grab=True))
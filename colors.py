class Colors:
    dark_grey = (27, 34, 46)
    dark_blue = (37, 44, 56)
    light_blue = (53, 67, 84)

    white = (228, 214, 189)
    mint = (139, 190, 169)
    lavender = (180, 155, 204)

    green = (139, 174, 112)
    red = (214, 135, 135)
    orange = (218, 158, 112)
    yellow = (225, 198, 119)
    purple = (145, 112, 176)
    cyan = (112, 177, 190)
    blue = (112, 143, 190)

    background = (37, 44, 56)
    panel = (53, 67, 84)
    panel_light = (67, 81, 99)
    text = (228, 214, 189)
    muted_text = (169, 178, 184)
    accent = (185, 165, 204)
    accent_hover = (202, 184, 218)
    
    @classmethod
    def get_cell_color(cls):
        return [cls.dark_grey, cls.green, cls.red, cls.orange, cls.yellow, cls.purple, cls.cyan, cls.blue, cls.mint, cls.lavender]
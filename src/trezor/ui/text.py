from micropython import const
from trezor import ui

TEXT_HEADER_HEIGHT = const(48)
TEXT_LINE_HEIGHT = const(26)
TEXT_MARGIN_LEFT = const(14)
TEXT_MAX_LINES = const(4)

BR = const(-1)


class Text(ui.Widget):
    def __init__(self,
                 header_text: str,
                 header_icon: bytes,
                 *content: list,
                 new_lines: bool = True,
                 max_lines: int = TEXT_MAX_LINES,
                 icon_color: int = ui.ORANGE_ICON):
        self.header_text = header_text
        self.header_icon = header_icon
        self.content = content
        self.new_lines = new_lines
        self.max_lines = max_lines
        self.icon_color = icon_color

    def render(self):
        # draw the component header
        ui.header(self.header_text, self.header_icon, ui.TITLE_GREY, ui.BG, self.icon_color)

        # initial drawing state
        offset_x = TEXT_MARGIN_LEFT
        offset_x_max = ui.WIDTH
        offset_y = TEXT_HEADER_HEIGHT + TEXT_LINE_HEIGHT
        offset_y_max = TEXT_HEADER_HEIGHT + TEXT_LINE_HEIGHT * self.max_lines
        font = ui.NORMAL
        fg = ui.FG
        bg = ui.BG
        space = ui.display.text_width(' ', font)
        # dash = ui.display.text_width('-', ui.BOLD)
        # ellipsis = ui.display.text_width('...', ui.BOLD)

        for word in self.content:
            if isinstance(word, str):
                width = ui.display.text_width(word, font)

                if offset_x > TEXT_MARGIN_LEFT and offset_x + width > offset_x_max:
                    # line break
                    if offset_y >= offset_y_max:
                        ui.display.text(offset_x, offset_y, '...', ui.BOLD, ui.GREY, bg)
                        return
                    offset_x = TEXT_MARGIN_LEFT
                    offset_y += TEXT_LINE_HEIGHT

                while offset_x + width > offset_x_max:
                    # word is too wide, find a part that fits on this line
                    for i in range(len(word) - 1, 1, -1):
                        part = word[:i]
                        partwidth = ui.display.text_width(part, font)
                        if offset_x + partwidth > offset_x_max:
                            continue
                        # render word part
                        ui.display.text(offset_x, offset_y, part, font, fg, bg)
                        offset_x += partwidth
                        # render ellipsis instad of dash if we are at the end
                        if offset_y >= offset_y_max:
                            ui.display.text(offset_x, offset_y, '...', ui.BOLD, ui.GREY, bg)
                            return
                        # render dash and break the line
                        ui.display.text(offset_x, offset_y, '-', ui.BOLD, ui.GREY, bg)
                        offset_x = TEXT_MARGIN_LEFT
                        offset_y += TEXT_LINE_HEIGHT
                        # continue with the rest of the word
                        word = word[i:]
                        width = ui.display.text_width(word, font)
                        break

                # render word
                ui.display.text(offset_x, offset_y, word, font, fg, bg)
                offset_x += width
                offset_x += space

                # line break
                if self.new_lines:
                    if offset_y >= offset_y_max:
                        ui.display.text(offset_x, offset_y, '...', ui.BOLD, ui.GREY, bg)
                        return
                    offset_x = TEXT_MARGIN_LEFT
                    offset_y += TEXT_LINE_HEIGHT

            elif word == BR:
                # line break
                if offset_y >= offset_y_max:
                    ui.display.text(offset_x, offset_y, '...', ui.BOLD, ui.GREY, bg)
                    return
                offset_x = TEXT_MARGIN_LEFT
                offset_y += TEXT_LINE_HEIGHT

            elif word == ui.NORMAL or word == ui.BOLD or word == ui.MONO:
                # change of font style
                font = word

            else:
                # change of foreground color
                fg = word

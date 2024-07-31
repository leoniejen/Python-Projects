"""
File: babygraphics.py
Name: Leonie
--------------------------------
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt',
    'data/full/baby-2020.txt'
]
CANVAS_WIDTH = 1080
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950,
         1960, 1970, 1980, 1990, 2000, 2010, 2020]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index where the current year is in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                            with the current year.
    """
    return GRAPH_MARGIN_SIZE + year_index*(width - GRAPH_MARGIN_SIZE*2)/len(YEARS)


def draw_fixed_lines(canvas):
    """
    Draws the fixed background lines on the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # Draw two horizontal fixed lines
    canvas.create_line(GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, CANVAS_WIDTH-GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE)
    canvas.create_line(GRAPH_MARGIN_SIZE, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, CANVAS_WIDTH-GRAPH_MARGIN_SIZE, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE)

    # Draw vertical lines and add year label, numbers depended by len(YEARS)
    for i in range(len(YEARS)):
        canvas.create_line(get_x_coordinate(CANVAS_WIDTH, i), 0, get_x_coordinate(CANVAS_WIDTH, i), CANVAS_HEIGHT)
        canvas.create_text(get_x_coordinate(CANVAS_WIDTH, i)+TEXT_DX, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, text=YEARS[i], anchor=tkinter.NW)


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    def get_y_coordinate(y):
        # print(y)
        if y == '*':
            return CANVAS_HEIGHT - GRAPH_MARGIN_SIZE
        else:
            return int(y) * (CANVAS_HEIGHT - 2 * GRAPH_MARGIN_SIZE) / 1000 + GRAPH_MARGIN_SIZE

    for lookup_name in lookup_names:
        if lookup_name in name_data:
            # print(name_data[lookup_name])
            # print(name_data[lookup_name]['1900'])

            year_rank = {}
            for i in range(len(YEARS)):
                # save lookup_name's data of year and rank in year_rank dict
                if str(YEARS[i]) in name_data[lookup_name]:
                    year_rank[YEARS[i]] = name_data[lookup_name][str(YEARS[i])]
                else:
                    year_rank[YEARS[i]] = '*'

                # add lines and text for each lookup_name
                if i == 0:    # manipulate first year's data of each name
                    previous_point = get_x_coordinate(CANVAS_WIDTH, 0), get_y_coordinate(year_rank[YEARS[0]])
                    canvas.create_text(get_x_coordinate(CANVAS_WIDTH, 0)+TEXT_DX, get_y_coordinate(year_rank[YEARS[0]]),
                                       text=f'{lookup_name} {year_rank[YEARS[0]]}', anchor=tkinter.SW,
                                       fill=COLORS[lookup_names.index(lookup_name) % len(COLORS)])
                else:  # manipulate the other year's data of each name
                    canvas.create_line(*previous_point, get_x_coordinate(CANVAS_WIDTH, i), get_y_coordinate(year_rank[YEARS[i]]), width=LINE_WIDTH, fill=COLORS[lookup_names.index(lookup_name) % len(COLORS)])
                    canvas.create_text(get_x_coordinate(CANVAS_WIDTH, i) + TEXT_DX,
                                       get_y_coordinate(year_rank[YEARS[i]]),
                                       text=f'{lookup_name} {year_rank[YEARS[i]]}', anchor=tkinter.SW,
                                       fill=COLORS[lookup_names.index(lookup_name) % len(COLORS)])
                    previous_point = get_x_coordinate(CANVAS_WIDTH, i), get_y_coordinate(year_rank[YEARS[i]])  # iterate previous_point to current point


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()

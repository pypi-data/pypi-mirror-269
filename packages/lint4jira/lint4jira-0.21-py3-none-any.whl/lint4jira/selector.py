import curses


class Selector:
    @staticmethod
    def print_menu(stdscr, selected_idx, options, start_idx):
        stdscr.clear()
        h, w = stdscr.getmaxyx()
        max_rows = h - 2

        # Display search prompt
        search_prompt = "Search: "
        stdscr.addstr(0, 0, search_prompt)

        # Calculate visible items based on current start index
        slice_end = start_idx + max_rows
        visible_items = options[start_idx:slice_end]

        for idx, (name, _) in enumerate(visible_items):
            x = w // 2 - len(name) // 2
            y = idx + 2  # Adjust for search prompt row
            if idx + start_idx == selected_idx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, name)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, name)
        stdscr.refresh()

    def search_fields(options, query):
        # Simple case-insensitive search
        return [(name, id) for name, id in options if query.lower() in name.lower()]

    def select_field(stdscr, fields: dict):
        curses.curs_set(1)  # Show the cursor for typing search queries
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        current_index = 0
        start_index = 0
        search_query = ""
        options = list(fields.items())
        max_rows = 10
        while True:
            filtered_options = Selector.search_fields(options, search_query)
            Selector.print_menu(stdscr, current_index, filtered_options, start_index)
            key = stdscr.getch()

            if key == curses.KEY_BACKSPACE or key == 127:
                search_query = search_query[:-1]
                start_index = 0
                current_index = 0
            elif key == curses.KEY_UP and current_index > 0:
                current_index -= 1
                if current_index < start_index:
                    start_index -= 1
            elif key == curses.KEY_DOWN and current_index < len(filtered_options) - 1:
                current_index += 1
                if current_index - start_index >= max_rows:
                    start_index += 1
            elif key == curses.KEY_ENTER or key in [10, 13]:
                if filtered_options:
                    return filtered_options[current_index][0]
            elif key in range(32, 127):  # ASCII printable characters range
                search_query += chr(key)
                start_index = 0
                current_index = 0

    def checkbox_menu(stdscr, options):
        curses.curs_set(0)  # Hide the cursor
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

        current_index = 0
        checked = [False] * len(options)  # List to keep track of checked items

        while True:
            Selector.print_menu(stdscr, current_index, options, checked)
            key = stdscr.getch()

            if key == curses.KEY_UP and current_index > 0:
                current_index -= 1
            elif key == curses.KEY_DOWN and current_index < len(options) - 1:
                current_index += 1
            elif key == 32:  # Space key to toggle checkbox
                checked[current_index] = not checked[current_index]
            elif key == curses.KEY_ENTER or key in [10, 13]:  # Enter key to confirm selections
                # Return list of selected items based on their checked status
                return [options[i][0] for i in range(len(options)) if checked[i]]
            elif key == 27:  # ESC key to cancel
                return None

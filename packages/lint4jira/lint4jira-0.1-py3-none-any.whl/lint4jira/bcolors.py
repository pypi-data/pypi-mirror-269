class BCOLORS:
    ### Text Effects
    HEADER = '\033[95m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'


    ### Notification Colors
    WARNING = '\033[93m'
    WARNING_BACKGROUND = '\033[43m'
    FAIL = '\033[91m'
    FAIL_BACKGROUND = '\033[41m'
    ERROR = '\033[91m'
    ERROR_BACKGROUND = '\033[41m'
    SUCCESS = '\033[92m'
    SUCCESS_BACKGROUND = '\033[42m'

    ### Text Colors
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    ORANGE = '\033[33m'
    RED = '\033[31m'
    GRAY = '\033[90m'

    ### Background Colors
    YELLOW_BACKGROUND = '\033[43m'
    RED_BACKGROUND = '\033[41m'
    GRAY_BACKGROUND = '\033[100m'
    GREEN_BACKGROUND = '\033[42m'
    BLUE_BACKGROUND = '\033[44m'
    CYAN_BACKGROUND = '\033[46m'
    WHITE_BACKGROUND = '\033[47m'
    RED_BACKGROUND_WHITE_TEXT_AS_BOLD = '\033[41m\033[97m\033[1m'


    def dot_line():
        print(f"{BCOLORS.GRAY}------------------------{BCOLORS.ENDC}")


    def print_header(text):
        print(f"{BCOLORS.RED_BACKGROUND_WHITE_TEXT_AS_BOLD} - {text} - {BCOLORS.ENDC}")

    def print_bold(text):
        print(f"{BCOLORS.BOLD}{text}{BCOLORS.ENDC}")

    def print_underline(text):
        print(f"{BCOLORS.UNDERLINE}{text}{BCOLORS.ENDC}")

    def print_warning(text, condition=True):
        print(f"{BCOLORS.WARNING_BACKGROUND}WARNING: {BCOLORS.ENDC} {BCOLORS.WARNING}{text}{BCOLORS.ENDC}")

    def print_fail(text, condition=True):
        print(f"{BCOLORS.FAIL_BACKGROUND}FAIL: {BCOLORS.ENDC} {BCOLORS.FAIL}{text}{BCOLORS.ENDC}")

    def print_error(text, condition=True):
        print(f"{BCOLORS.ERROR_BACKGROUND}ERROR: {BCOLORS.ENDC} {BCOLORS.ERROR}{text}{BCOLORS.ENDC}")

    def print_success(text, condition=True):
        print(f"{BCOLORS.GREEN_BACKGROUND}SUCCESS: {BCOLORS.ENDC} {BCOLORS.SUCCESS}{text}{BCOLORS.ENDC}")

    def reset():
        """
        Reset the terminal and clear the screen
        :return:
        """
        print("\033[H\033[J")

    def space(param):
        for i in range(param):
            print("\n")

    def print_info(text):
        print(f"{BCOLORS.OKBLUE}{text}{BCOLORS.ENDC}")

    @classmethod
    def print_cross_color(cls, text, is_even):
        color = BCOLORS.OKGREEN if is_even else BCOLORS.OKCYAN
        print(f"{color}{text}{BCOLORS.ENDC}")

        






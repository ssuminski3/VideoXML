import get_google_image
import os

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    print(os.getcwd())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    get_google_image.DownloadImageGoogle("cat", r"C:\Users\sebas\OneDrive\Pulpit\VideoXML\images")


# See PyCharm help at https://www.jetbrains.com/help/pycharm/

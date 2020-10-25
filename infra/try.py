from util.get_faq import get_faq

def main():
    FILENAME = "static/dataset/cnc_troubleshooting.xlsx"
    faq_list = get_faq(FILENAME)
    print(faq_list)


if __name__ == '__main__':
    main()
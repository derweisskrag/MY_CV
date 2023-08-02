from resume import Resume
from lib.data import data


def main():
    print("Hello, Python!")
    my_cv = Resume(data, "my_cv.pdf")
    my_cv.generate_cv()


if __name__ == "__main__":
    main()
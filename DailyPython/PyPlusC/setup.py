from distutils.core import setup, Extension

def main():
    setup(name="fputs",
          version="1.0.0",
          description="Python interface for the fputs C library function",
          author="Austin Schaffer",
          author_email="schaffer.austin.t@gmail.com",
          ext_modules=[Extension("fputs", ["fputs.c"])])

if __name__ == "__main__":
    main()

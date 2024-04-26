from setuptools import setup, find_packages

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Intended Audience :: Education",
    "Operating System :: Microsoft :: Windows :: Windows 11",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3"
]

setup(
    name="temalib",
    version="3.6",
    description="a library that was for working with files i guess",
    long_description="""
idk how to use the restructedtext thingy so uhh
all commands in this library:

smthfile(fp, mode):
    does the same what codecs.open(fp, mode, encoding="utf-8") does
    also check openfile(fp) and editfile(fp)

get_folder_path(caller, *args, create_folders):
    constructs a folder path relative to the caller's directory, optionally creating missing folders
    fore xample 👾👾👾👾👾👾:
        print(temalib.get_folder_path(
            __file__, "i", "am", "going", "to", "invade", "denmark"
        ))
        # output: file's_subfolder/i/am/going/to/invade/denmark

get_file_path(caller, *args, create_folders, create_file):
    does same what get_folder_path but last arg is a file (also optionally created)

add_line(fp, line):
    formerly altteotf() (add line to the end of the file)

remove_line(fp, line):
    if theres that line in the file then removes it

listpaths(fp):
    return list of paths
    """,
    url="",
    author="tema5002",
    author_email="xtema5002x@gmail.com",
    license="MIT",
    classifiers=classifiers,
    keywords="bullshuy",
    packages=find_packages(),
    install_requires=[""],
    long_description_content_type="text/plain"
)
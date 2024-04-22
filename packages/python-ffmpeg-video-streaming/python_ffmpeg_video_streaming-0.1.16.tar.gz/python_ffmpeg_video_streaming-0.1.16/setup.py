import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-ffmpeg-video-streaming",
    version="0.1.16",
    author="Amin Yazdanpanah",
    author_email="contact@aminyazdanpanah.com",
    description="Package media content for online streaming(DASH and HLS) using ffmpeg",
    long_description=long_description,
    project_urls={
        "Bug Tracker": "https://github.com/quasarstream/python-ffmpeg-video-streaming/issues",
        "Documentation": "https://quasarstream.com/op/python/ffmpeg-streaming/",
        "Source Code": "https://github.com/quasarstream/python-ffmpeg-video-streaming",
    },
    long_description_content_type="text/markdown",
    url="https://github.com/quasarstream/python-ffmpeg-video-streaming",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
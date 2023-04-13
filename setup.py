import sys
from setuptools import setup
from minecraft import __version__
from os import remove
import platform
import os

path = "minecraft/chromedriver_"

print(f"CHECK_SYSTEM: {platform.system()}")
print(f"CHECK_MACHINE: {platform.machine()}")


if platform.system == 'Windows' and platform.machine == 'i386':
    platform.system(f"unzip {path}windows32.zip -d minecraft")
    print("Finished webdriver setup")


def read(filename):
    """
    Puts a file into a string.
    """
    with open(filename, "r") as f:
        return f.read()


MAIN_AUTHORS = ["Ammar Askar <ammar@ammaraskar.com>",
                "Jeppe Klitgaard <jeppe@dapj.dk>"]

URL = "https://github.com/ammaraskar/pyCraft"

setup(name="pyCraft",
      version=__version__,
      description="Python MineCraft library",
      long_description=read("README.rst"),
      url=URL,
      download_url=URL + "/tarball/" + __version__,
      author=", ".join(MAIN_AUTHORS),
      install_requires=["cryptography>=1.5",
                        "requests",
                        "pynbt",
                        ],
      packages=["minecraft",
                "minecraft.networking",
                "minecraft.networking.packets",
                "minecraft.networking.packets.clientbound",
                "minecraft.networking.packets.clientbound.status",
                "minecraft.networking.packets.clientbound.handshake",
                "minecraft.networking.packets.clientbound.login",
                "minecraft.networking.packets.clientbound.play",
                "minecraft.networking.packets.serverbound",
                "minecraft.networking.packets.serverbound.status",
                "minecraft.networking.packets.serverbound.handshake",
                "minecraft.networking.packets.serverbound.login",
                "minecraft.networking.packets.serverbound.play",
                "minecraft.networking.types",
                ],
      keywords=["MineCraft", "networking", "pyCraft", "minecraftdev", "mc"],
      classifiers=["Development Status :: 3 - Alpha",
                   "Intended Audience :: Developers",
                   "License :: OSI Approved :: Apache Software License",
                   "Natural Language :: English",
                   "Operating System :: OS Independent",
                   "Programming Language :: Python",
                   "Programming Language :: Python :: 2",
                   "Programming Language :: Python :: 2.7",
                   "Programming Language :: Python :: 3",
                   "Programming Language :: Python :: 3.3",
                   "Programming Language :: Python :: 3.4",
                   "Programming Language :: Python :: 3.5",
                   "Programming Language :: Python :: 3.6",
                   "Topic :: Games/Entertainment",
                   "Topic :: Software Development :: Libraries",
                   "Topic :: Utilities"
                   ]
      )

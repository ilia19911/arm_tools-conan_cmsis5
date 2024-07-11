from conan import ConanFile, tools
from conan.tools.scm import Git
from conan.tools.cmake import CMake
from conan.tools.files import get, copy
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
import os
from enum import Enum
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import re


class ArmGccConan(ConanFile):
    name = "cmsis_5"
    version = "1.0"
    license = "GPL-3.0-only"
    homepage = ""
    url = ""
    author = "Ostanin <iahve1991@gmail.com>"
    description = "пакет cmsis для arm"
    topics = ("conan", "cmsis", "arm")
    # options = {"source_url": ["ANY"]}
    # default_options = {"source_url": "None"}
    # settings = "os", "arch"
    package_type = "application"
    programs = {}
    sha = {}
    archive_name = {}
    exports_sources = "cmsis.cmake"
    # generators = "CMakeToolchain"

    # generators = "CMakeDeps"

    def system_requirements(self):
        print("CMSIS_PYTHON_REQUIREMENTS")

    # def requirements(self):
    #     self.requires("bs4/4.10.0")
    def validate(self):
        print("CMSIS_VALIDATION")
        # self.options.source_url = str(self.options.source_url)

    def package_id(self):
        print("CMSIS_PACKAGE_ID")

    def source(self):
        print("CMSIS_SOURCE")
        cmake = CMake(self)
        cmake.configure()
        cmake.build()


    def generate(self):
        tc = CMakeToolchain(self)
        tc.generate()
    def build(self):
        print("CMSIS_BUILD")


    def package(self):
        print("CMSIS_PACKAGE")
        print("source folder: ", self.source_folder)
        print("export files: ", self.exports_sources)
        # self.run(f"ls -la .")
        copy(self, "*", dst=self.package_folder + "/cmsis", src=self.source_folder +"/cmsis")
        copy(self, "*.cmake", dst=self.package_folder+"/cmake", src=self.source_folder)

    def source(self):
        print("CMSIS_SOURCE")

        # git.checkout("master")
    def package_info(self):
        print("CMSIS_PACKAGE_INFO")
        toolchain_path = os.path.join(self.package_folder, "cmake/cmsis.cmake")
        print("CMSIS TOOLCHAIN IS: ", toolchain_path)
        # self.conf_info.define("tools.cmake.cmaketoolchain:user_toolchain", toolchain_path)
        self.cpp_info.builddirs.append(os.path.join(self.package_folder, "cmake"))

        token = "r8EEQ327YSe3_kegTCvu"
        git = Git(self)
        repo_url = f"https://oauth2:{token}@git.orlan.in/breo_mcu/drivers/CMSIS_5.git"
        if not os.path.exists("../cmsis"):
            git.clone(repo_url, "../cmsis")
            print("project cloned. It contains..")
        self.run(f"ls -la ../cmsis")
        self.run("cd ../cmsis && git checkout master")



    def generate(self):
        print("CMSIS_GENERATE")


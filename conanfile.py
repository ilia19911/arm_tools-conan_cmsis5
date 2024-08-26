from conan import ConanFile, tools
from conan.tools.scm import Git
from conan.tools.cmake import CMake
from conan.tools.files import get, copy
from conan.tools.cmake import CMakeToolchain, CMake, cmake_layout
import os


class ArmGccConan(ConanFile):
    name = "cmsis"
    # version = "1.0"
    license = "GPL-3.0-only"
    homepage = ""
    url = ""
    author = "Ostanin <iahve1991@gmail.com>"
    description = "пакет cmsis для arm"
    topics = ("conan", "cmsis", "arm")
    # options = {"source_url": ["ANY"]}
    # default_options = {"source_url": "None"}
    settings = "os", "arch", "compiler", "build_type"
    # package_type = "library"
    programs = {}
    sha = {}
    archive_name = {}
    exports_sources = "CMakeLists.txt"
    generators = "CMakeDeps", "CMakeToolchain"
    arm_cpus = ["cortex-m0", "cortex-m1", "cortex-m3", "cortex-m4", "cortex-m7"]

    # generators = "CMakeDeps"

    def system_requirements(self):
        print("CMSIS_PYTHON_REQUIREMENTS")

    def requirements(self):
        print("REQUIRES")
        # Указываем зависимости от тулчейнов
        self.requires("arm-gcc/13.2.rel1")

    # def build_requirements(self):
    #     print("TOOL REQUIRES")
    #     self.build_requires("arm-gcc/13.2.rel1")
    # def requirements(self):
    #     self.tool_requires("arm-gcc/13.2.rel1")
    def validate(self):
        print("CMSIS_VALIDATION")
        # self.options.source_url = str(self.options.source_url)

    def package_id(self):
        print("CMSIS_PACKAGE_ID")

    def source(self):
        print("CMSIS_SOURCE")
        url = os.getenv("URL")
        print("URL: ", url)
        tag = os.getenv("TAG")
        print("TAG: ", tag)

        with open(f"source_url.txt", "w") as file:
            file.write(url + "\n")
            file.write(tag + "\n")
            file.close()
        with open('source_url.txt', 'r') as file:
            # Чтение содержимого файла
            lines = file.readlines()
            repo_url = lines[0].strip()
            tag = lines[1].strip()
        print("repo url: ", repo_url)
        print("tag: ", tag)
        git = Git(self)
        if not os.path.exists("./cmsis"):
            git.clone(repo_url, "./cmsis")
            print("project cloned. It contains..")
        self.run(f"ls -la ./cmsis")
        self.run(f"cd ./cmsis && git checkout {tag}")

        # cmake = CMake(self)
        # cmake.configure()
        # cmake.build()

    def generate(self):
        # tc = CMakeToolchain(self)
        # tc.generate()
        toolchain = tools.cmake.CMakeToolchain.filename
        with open(toolchain, 'r') as template_file:
            template_content = template_file.read()
        with open(toolchain, "w") as file:
            file.write(template_content)
            file.write("include(arm-gcc-toolchain)\n")

        # # # Явное подключение тулчейна, если Conan не добавил его автоматически
        # toolchain_file = self.dependencies.build["arm-gcc/13.2.rel1"].cpp_info.get_property("cmake_toolchain_file", "CMakeToolchain")
        # if toolchain_file:
        #     with open("conan_toolchain.cmake", "a") as toolchain:
        #         toolchain.write(f'include("{toolchain_file}")\n')

    def build(self):
        print("CMSIS_BUILD")
        cmake = CMake(self)
        # cmake.configure({
        #             "VERSION": self.version,
        #             "ARM_CPU": "cortex-m4"
        #         })
        # cmake.build()
        for cpu in self.arm_cpus:
            cmake.configure({
                "VERSION": self.version,
                "ARM_CPU": cpu
            }, cli_args=[f"-B {self.package_folder}/build/{cpu}"])
            self.run(f"cmake --build {self.package_folder}/build/{cpu} -j32")

    def package(self):
        print("CMSIS_PACKAGE")
        print("source folder: ", self.source_folder)
        print("export files: ", self.exports_sources)

        # self.run(f"ls -la .")
        copy(self, "source_url.txt", dst=self.package_folder, src=self.source_folder)
        copy(self, "*.cmake", dst=self.package_folder + "/cmake", src=self.source_folder)
        copy(self, "cmsis/*", dst=self.package_folder, src=self.source_folder)
        # Установка проекта в директорию упаковки
        cmake = CMake(self)
        # cmake.install()
        for cpu in self.arm_cpus:
            build_dir = f"{self.package_folder}/{cpu}"
            # Install the project
            self.run(f"cmake --install {self.package_folder}/build/{cpu}  --prefix {self.package_folder}/{cpu}")

    def package_info(self):
        print("CMSIS_PACKAGE_INFO")
        # toolchain_path = os.path.join(self.package_folder, "cmake/cmsis.cmake")
        # print("CMSIS TOOLCHAIN IS: ", toolchain_path)
        # self.conf_info.define("tools.cmake.cmaketoolchain:user_toolchain", toolchain_path)
        # self.conf_info.append("tools.cmake.cmaketoolchain:user_toolchain", toolchain_path)
        for cpu in self.arm_cpus:
            self.cpp_info.builddirs.append(os.path.join(self.package_folder, f"{cpu}/lib/cmake"))
        # self.cpp_info.builddirs.append(os.path.join(self.package_folder, "cmake"))
        # self.cpp_info.includedirs.append(os.path.join(self.package_folder, "include"))

#export URL="https://oauth2:bb8czxqpbkzn5PHp3nda@git.orlan.in/breo_mcu/drivers/CMSIS_5.git" && export TAG="5.9.1-dev" && conan create . -pr:h=./profiles/armv7  --version=5.9.1-dev --build-require -r=BREO
#conan upload cmsis/5.9.1-dev -r=BREO

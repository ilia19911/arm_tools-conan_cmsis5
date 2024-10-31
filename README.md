# Related projects

[CMSIS_5](https://github.com/ARM-software/CMSIS_5)

[https://github.com/ilia19911/arm_tools-conan_cmsis5](https://github.com/ilia19911/arm_tools-conan_gcc)

# Motivation

The motivation for creating this build system comes from the availability of all necessary tools for building ARM32 projects freely on the internet, but the lack of any satisfactory build system implementation. I believe that a build system should allow easy switching between compilers, separation of hardware logic from business logic, and support multiple versions of CMSIS HAL without needing to copy them into each project.

Additionally, CMSIS often does not include precompiled NN and DSP libraries, so these must be compiled manually. Many users search for alternative ways to integrate DSP files into their projects for various reasons (e.g., large binary size), even though DSP/Source/CMakeLists.txt contains clear build instructions. Moreover, CMSIS can be built for a PC, simplifying algorithm testing.

Typically, one project assumes one target with flags for your processor, which is not convenient when you have tests running on a PC or projects where more than one firmware must be compiled, for example for f1 and f4. This project solves this problem and allows the user to fine-tune targets to suit their goals, even with tests on PC

When generating a project in CubeMX, users often struggle to easily control which version of libraries will be used in the project, and sometimes CubeMX hasn't yet been updated to the latest versions, such as HAL, CMSIS, or FatFS. As a result, depending on the machine where the project was generated, the libraries may have different versions, leading to potential compatibility issues or even the use of outdated libraries. This project solves the problem by allowing easy switching between different library versions or even locking a specific version for the entire development team.

CMSIS provides driver interface descriptions in C, but today, writing embedded projects purely in C for STM32 is becoming less common due to increasing algorithmic complexity. It’s essential to adapt to modern development needs. Furthermore, the compiler flags required to reduce binary size and apply proper processor settings remain a mystery to many users.

If you disagree with any of my points or have resources to share, I welcome any feedback or constructive criticism.

# Common

This project was created to generate precompiled CMSIS packages for the Conan framework. Since CMSIS includes a compilation feature for PC, it is possible to build a package for your platform.

The system makes it easy to switch between build targets and test the entire business logic on a PC using a proposed pattern for separating lower and upper levels of the program. This project includes a CMakeLists file for generating static libraries and packaging them into a single exportable CMSIS library, which can be integrated into your project using find_package.The CMSIS package includes many libraries grouped into DSP and NN. Their compilation must be done with specific compiler flags to ensure proper linking with the target and to reduce the size of the resulting binary file. All these features are included in the package, and the additional libraries are automatically built for the selected platform.

 *IMPORTANT*: it is not necessary to build the package to use it, as it is already hosted on my server. All you need to do is add my Conan package server to your list of repositories.

# Abstract overwiev
This package is part of a custom build system based on Conan, CMake, GCC, GTest, CMSIS, HAL tools, and libraries. CMSIS is a library developed by ARM to support its microcontrollers across various series, including ARM32 and ARM64. Depending on the controller, DSP libraries with NEON and SIMD instructions can be integrated.

The Keil build system includes CMSIS with correctly compiled DSP and NN libraries, optimized for different platforms. However, since Keil is a paid platform, the compiler flags are predefined by the manufacturer, and it does not allow creating a private package server. For my needs, it is more convenient to use my own build system on a free platform.

Moreover, this approach enables dynamic switching of the build platform from one controller to another, or even to a PC, for testing purposes—without any changes to the code or complex logic in CMake.

This project provides instructions for building CMSIS package wrappers for Conan, simplifying the process of integrating the package into a project based on the selected platform.

# Requirements
- Python 3 and required libraries (install the necessary ones for your system)
- Conan client installed (find instructions at https://conan.io/downloads)
  
# Fast start

  To use the package, add my repository to the list of Conan repositories, and you will be able to find the required GCC version with the necessary host and target options.
  
  ```
  conan remote add arm-tools  https://artifactory.nextcloud-iahve.ru/artifactory/api/conan/arm-tools
  ```

# Private Artifactory

If you want to set up your own build system, you will need to install your own JFrog Artifactory server. This can be done by following the instructions at JFrog Open Source. I use the Community Edition because it’s free and supports C/C++ packages (which is all I need). After installation, you can either build packages or fetch my existing ones to your PC and upload them to your private Artifactory.


# Library ranging
The library includes various CMSIS versions for different platforms. The libraries are placed in the CMSIS namespace
- CORTEX_M0
- CORTEX_M1
- CORTEX_M2
- CORTEX_M3
- CORTEX_M4
- CORTEX_M5
- CORTEX_M6
- CORTEX_M7
If you need more cpu's , please, text me or add it yourself
# How to use

 You can find an example in another [repository](https://github.com/ilia19911/arm_tools-simple_stm32f4) of mine, where I use several packages and separate logic from hardware using C++ drivers.

 # Build
To build the package, clone the repository:  *git clone https://github.com/ilia19911/arm_tools-conan_gcc.git*

It's important to have a network disk or web-accessible location where you keep toolchains, as the Python script conanfile.py will try to locate archive files in a specific format and sha256asc.txt files. Alternatively, you can use my repository as written in the script.

Conan provides an easy way to create packages with conanfile.py. Just navigate to the root of the repo and run:

```
conan create .
```
This will build the package for your system. For STM32, we need to create specific host/target options, so I designed a format for creating packages. You can improve this if you have time.

Example command for arm32 platform:
 ```
conan create . -pr:h=./profiles/armv7  --version=5.9.1-dev --build-require -r=arm-tools

conan create . -pr:h=./profiles/linux_x86_64  --version=5.9.1-dev --build-require -r=arm-tools
 ```


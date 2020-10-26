from conans import ConanFile, AutoToolsBuildEnvironment, tools, RunEnvironment
from conans.errors import ConanInvalidConfiguration
import os

class ESMFConan(ConanFile):
    name = "esmf"
    version = "8.1.0"
    license = "MIT"
    author = ""
    url = "https://esmf-org.github.io/"
    description = "Earth System Modeling Framework "
    settings = "os", "compiler", "build_type", "arch"
    # options = {"shared": [True, False]}
    # default_options = "shared=True"
    generators = "cmake"

    def source(self):
        git = tools.Git(folder="")
        git.clone("https://github.com/esmf-org/esmf.git")

        # self.run("git clone --depth=1 https://github.com/esmf-org/esmf.git")

    def build(self):
        env_build = AutoToolsBuildEnvironment(self)
        env_build.vars
        with tools.environment_append({"ESMF_F90COMPILEOPTS": "-fallow-argument-mismatch -fallow-invalid-boz",
                                           "ESMF_INSTALL_PREFIX":self.package_folder,
                                           "ESMF_DIR": self.build_folder,
                                           "ESMF_COMM":"mpiuni"}):
            self.run('make -j10', run_environment=True)


    def package(self):
        env_build = AutoToolsBuildEnvironment(self)
        env_build.vars
        with tools.environment_append({"ESMF_F90COMPILEOPTS": "-fallow-argument-mismatch -fallow-invalid-boz",
                                           "ESMF_INSTALL_PREFIX":self.package_folder,
                                           "ESMF_DIR": self.build_folder,
                                           "ESMF_COMM":"mpiuni"}):
            self.run('make -j10 install', run_environment=True)
        
        self.copy('*.cmake','cmake','cmake')

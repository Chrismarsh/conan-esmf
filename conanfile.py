from conans import ConanFile, AutoToolsBuildEnvironment, tools, RunEnvironment
from conans.errors import ConanInvalidConfiguration
from conans.model.version import Version
import os
from six import StringIO
import re

class ESMFConan(ConanFile):
    name = "esmf"
    version = "8.1.0"
    license = "MIT"
    author = ""
    url = "https://esmf-org.github.io/"
    description = "Earth System Modeling Framework "
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    

    def source(self):
        git = tools.Git(folder="")
        git.clone("https://github.com/esmf-org/esmf.git")


    def _get_envars(self):

        esmf_envars = {}

        # gcc 10 requires a special set of compiler flags.                                    
        is_gfortran_10 = False

        if self.settings.compiler == 'gcc' and Version(self.settings.compiler.version.value) >= "10.0":
            is_gfortran_10 = True
        
        # if we use macos with default apple-clang but use a gcc10 gfortran from homebrew, conan doesn't know about this
        # so manually grab the $PATH gfortran version 
        if tools.os_info.is_macos and not is_gfortran_10:
            mybuf = StringIO()                                   
            self.run('gfortran --version',mybuf)

            ver = mybuf.getvalue()
            ver = re.findall("([0-9]+)\.[0-9]+\.[0-9]+",ver)
            if len(ver) ==0:
                self.output.error('Gfortran not found')
            if int(ver[0]) >= 10:
                is_gfortran_10 = True

        esmf_envars["ESMF_INSTALL_PREFIX"] =self.package_folder
        esmf_envars["ESMF_DIR"] = self.build_folder
        esmf_envars["ESMF_COMM"] = "mpiuni"

        if is_gfortran_10:
            esmf_envars["ESMF_F90COMPILEOPTS"] = "-fallow-argument-mismatch -fallow-invalid-boz"

        return esmf_envars

    def build(self):

        esmf_envars = self._get_envars()

        env_build = AutoToolsBuildEnvironment(self)
        env_build.make(vars=esmf_envars)


    def package(self):
        esmf_envars = self._get_envars()

        env_build = AutoToolsBuildEnvironment(self)
        env_build.install(vars=esmf_envars)
        
        self.copy('*.cmake','cmake','cmake')

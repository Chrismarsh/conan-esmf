from cpt.packager import ConanMultiPackager
from collections import defaultdict
from sys import platform

if __name__ == "__main__":

    command=""
    if platform == "linux":
        command = "sudo apt-get -qq update && sudo apt-get -qq install gfortran"

    builder = ConanMultiPackager(cppstds=[14],
                                archs=["x86_64"],
                                build_types=["Release"],
                                docker_entry_script = command)
                              
    builder.add_common_builds(pure_c=False)

    builder.remove_build_if(lambda build: build.settings["compiler.libcxx"] == "libstdc++")
    builder.remove_build_if(lambda build: build.settings["shared"] == "static")

    named_builds = defaultdict(list)
    for settings, options, env_vars, build_requires, reference in builder.items:

        named_builds[settings['compiler']].append([settings, options, env_vars, build_requires, reference])

    builder.named_builds = named_builds

    builder.run()


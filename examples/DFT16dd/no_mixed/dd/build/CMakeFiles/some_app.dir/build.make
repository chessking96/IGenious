# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/user/master-thesis/examples/DFT16dd/no_mixed/dd/build

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/user/master-thesis/examples/DFT16dd/no_mixed/dd/build

# Include any dependencies generated for this target.
include CMakeFiles/some_app.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/some_app.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/some_app.dir/flags.make

CMakeFiles/some_app.dir/main.c.o: CMakeFiles/some_app.dir/flags.make
CMakeFiles/some_app.dir/main.c.o: main.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/user/master-thesis/examples/DFT16dd/no_mixed/dd/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/some_app.dir/main.c.o"
	gcc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/some_app.dir/main.c.o   -c /home/user/master-thesis/examples/DFT16dd/no_mixed/dd/build/main.c

CMakeFiles/some_app.dir/main.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/some_app.dir/main.c.i"
	gcc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/user/master-thesis/examples/DFT16dd/no_mixed/dd/build/main.c > CMakeFiles/some_app.dir/main.c.i

CMakeFiles/some_app.dir/main.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/some_app.dir/main.c.s"
	gcc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/user/master-thesis/examples/DFT16dd/no_mixed/dd/build/main.c -o CMakeFiles/some_app.dir/main.c.s

# Object files for target some_app
some_app_OBJECTS = \
"CMakeFiles/some_app.dir/main.c.o"

# External object files for target some_app
some_app_EXTERNAL_OBJECTS =

some_app: CMakeFiles/some_app.dir/main.c.o
some_app: CMakeFiles/some_app.dir/build.make
some_app: CMakeFiles/some_app.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/user/master-thesis/examples/DFT16dd/no_mixed/dd/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable some_app"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/some_app.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/some_app.dir/build: some_app

.PHONY : CMakeFiles/some_app.dir/build

CMakeFiles/some_app.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/some_app.dir/cmake_clean.cmake
.PHONY : CMakeFiles/some_app.dir/clean

CMakeFiles/some_app.dir/depend:
	cd /home/user/master-thesis/examples/DFT16dd/no_mixed/dd/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/user/master-thesis/examples/DFT16dd/no_mixed/dd/build /home/user/master-thesis/examples/DFT16dd/no_mixed/dd/build /home/user/master-thesis/examples/DFT16dd/no_mixed/dd/build /home/user/master-thesis/examples/DFT16dd/no_mixed/dd/build /home/user/master-thesis/examples/DFT16dd/no_mixed/dd/build/CMakeFiles/some_app.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/some_app.dir/depend


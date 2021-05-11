# ================================================================================
# Add here user defined variables
# ================================================================================
if (NOT DEFINED INTERVAL_COMPILATION)
    set(INTERVAL_COMPILATION "f64i_sv") # ddi_sv, f64i_sv, f64i_ss, fil, bst, gal or baseline.
endif()

set(ATLAS_SOURCE    /home/cgo2021/artifact/ATLAS)
set(ATLAS_INCLUDE   /home/cgo2021/artifact/ATLAS/install/include)
set(IGEN_INCLUDE    /home/cgo2021/artifact/igen_lib)
set(IGEN_COMMON     /home/cgo2021/artifact/common)

# ================================================================================
# User configuration. E.g. compiler, debug, verbose, etc
# ================================================================================
set(PROJECT_NAME ATLAS_gemm_scalar)         # Specify project name
set(CONFIG_COMPILER "GNU")           # GNU, Clang or Intel
set(CONFIG_DEBUG "OFF")              # ON or OFF
set(CONFIG_GENERATE_ASSEMBLY "OFF")  # ON or OFF
set(CMAKE_VERBOSE_MAKEFILE "OFF")    # ON or OFF
set(CONFIG_FLAGS "-O3 -march=skylake")
set(CONFIG_LIBRARIES mpfr prim m gaol gdtoa crlibm) # Used libraries, e.g. crlibm, mpfr


# ================================================================================
# Include directories, set source files and user definitions
# ================================================================================
if (${INTERVAL_COMPILATION} STREQUAL "f64i_sv" OR ${INTERVAL_COMPILATION} STREQUAL "ddi_sv")
    add_definitions(-DIGEN_LIB_VECTORIZED)
endif()

add_definitions(
        # ATLAS necessary defines (extracted from compilation process)
        -DL2SIZE=33554432
        -DAdd_
        -DF77_INTEGER=int
        -DStringSunStyle
        -DATL_OS_Linux
        -DATL_ARCH_Corei4
        -DATL_CPUMHZ=2289
        -DATL_AVXMAC
        -DATL_AVX
        -DATL_SSE3
        -DATL_SSE2
        -DATL_SSE1
        -DATL_USE64BITS
        -DATL_GAS_x8664
        -DATL_NCPU=12
        -DDREAL
        -DNoTransA_
        -DNoTransB_
        -DALPHAX
        -DBETAX
        -DATL_UCLEANM
        -DATL_UCLEANN
        -DATL_UCLEANK
 )

if (${INTERVAL_COMPILATION} STREQUAL f64i_sv)
    add_definitions(-DF64I_TEST)
    include_directories(atlas_f64i)
elseif(${INTERVAL_COMPILATION} STREQUAL f64i_ss)
    add_definitions(-DF64I_TEST)
    include_directories(atlas_f64i)
elseif(${INTERVAL_COMPILATION} STREQUAL ddi_sv)
    add_definitions(-DDDI_TEST)
    include_directories(atlas_ddi)
elseif(${INTERVAL_COMPILATION} STREQUAL fil)
    add_definitions(-DFIL_TEST)
    include_directories(atlas_fil)
elseif(${INTERVAL_COMPILATION} STREQUAL bst)
    add_definitions(-DBST_TEST)
    include_directories(atlas_bst)
elseif(${INTERVAL_COMPILATION} STREQUAL gal)
    add_definitions(-DGAL_TEST)
    include_directories(atlas_gal)
endif()

include_directories(
        ${ATLAS_SOURCE}/include
        ${ATLAS_INCLUDE}/atlas
        ${IGEN_COMMON}
        ${IGEN_INCLUDE}
)

AUX_SOURCE_DIRECTORY(atlas_f64i IGEN_F64_SRC)
AUX_SOURCE_DIRECTORY(atlas_ddi IGEN_DD_SRC)
AUX_SOURCE_DIRECTORY(atlas_source ATLAS_SRC)

if (${INTERVAL_COMPILATION} STREQUAL f64i_sv OR ${INTERVAL_COMPILATION} STREQUAL f64i_ss)
    set(SOURCE_FILES
            test/accuracy_f64i.cpp
            atlas_f64i/igen_ATL_col2blk.c
            atlas_f64i/igen_ATL_dNBmm_b0.c
            atlas_f64i/igen_ATL_dNBmm_b1.c
            atlas_f64i/igen_ATL_dNBmm_b1_redu.cpp
#            atlas_f64i/igen_ATL_dNBmm_b1_vec.c # Uncomment to test vectorized input (IGen-vv)
            atlas_f64i/igen_ATL_gemm.c
            atlas_f64i/igen_ATL_gemmXX.c
            atlas_f64i/igen_ATL_mmJIK.c
            atlas_f64i/igen_ATL_putblk.c
            atlas_f64i/igen_ATL_row2blkT.c
            atlas_f64i/igen_cblas_dgemm.c
            atlas_f64i/igen_dummy_symbols.c
            dgemm_simple_f64i.cpp
            dgemm_bench_f64i.cpp
            )
elseif(${INTERVAL_COMPILATION} STREQUAL ddi_sv)
    set(SOURCE_FILES
            test/accuracy_ddi.cpp
            atlas_ddi/igen_ATL_col2blk.c
            atlas_ddi/igen_ATL_dNBmm_b0.c
            atlas_ddi/igen_ATL_dNBmm_b1.c
            atlas_ddi/igen_ATL_gemm.c
            atlas_ddi/igen_ATL_gemmXX.c
            atlas_ddi/igen_ATL_mmJIK.c
            atlas_ddi/igen_ATL_putblk.c
            atlas_ddi/igen_ATL_row2blkT.c
            atlas_ddi/igen_cblas_dgemm.c
            atlas_ddi/igen_dummy_symbols.c
            dgemm_simple_ddi.cpp
            dgemm_bench_ddi.cpp
            )
elseif(${INTERVAL_COMPILATION} STREQUAL fil)
    set(SOURCE_FILES
            atlas_fil/ATL_col2blk.cpp
            atlas_fil/ATL_dNBmm_b0.cpp
            atlas_fil/ATL_dNBmm_b1.cpp
            atlas_fil/ATL_gemm.cpp
            atlas_fil/ATL_gemmXX.cpp
            atlas_fil/ATL_mmJIK.cpp
            atlas_fil/ATL_putblk.cpp
            atlas_fil/ATL_row2blkT.cpp
            atlas_fil/cblas_dgemm.cpp
            atlas_fil/dummy_symbols.cpp
            dgemm_bench_fil.cpp
            dgemm_simple_fil.cpp
            )
elseif(${INTERVAL_COMPILATION} STREQUAL bst)
    set(SOURCE_FILES
            atlas_bst/ATL_col2blk.cpp
            atlas_bst/ATL_dNBmm_b0.cpp
            atlas_bst/ATL_dNBmm_b1.cpp
            atlas_bst/ATL_gemm.cpp
            atlas_bst/ATL_gemmXX.cpp
            atlas_bst/ATL_mmJIK.cpp
            atlas_bst/ATL_putblk.cpp
            atlas_bst/ATL_row2blkT.cpp
            atlas_bst/cblas_dgemm.cpp
            atlas_bst/dummy_symbols.cpp
            dgemm_bench_bst.cpp
            dgemm_simple_bst.cpp
            )
elseif(${INTERVAL_COMPILATION} STREQUAL gal)
    set(SOURCE_FILES
            atlas_gal/ATL_col2blk.cpp
            atlas_gal/ATL_dNBmm_b0.cpp
            atlas_gal/ATL_dNBmm_b1.cpp
            atlas_gal/ATL_gemm.cpp
            atlas_gal/ATL_gemmXX.cpp
            atlas_gal/ATL_mmJIK.cpp
            atlas_gal/ATL_putblk.cpp
            atlas_gal/ATL_row2blkT.cpp
            atlas_gal/cblas_dgemm.cpp
            atlas_gal/dummy_symbols.cpp
            dgemm_bench_gal.cpp
            dgemm_simple_gal.cpp
            )
else()
    set(SOURCE_FILES
            ${ATLAS_SRC}
            dgemm_bench_scalar.cpp
            dgemm_simple.cpp
            )
endif()

set(SOURCE_FILES
        ${SOURCE_FILES}

        benchmark/tsc_x86.cpp
        main.cpp

        # Auxilary files
        ${IGEN_COMMON}/util.cpp
        )

# ================================================================================
# Do not modify the following
# ================================================================================
cmake_minimum_required(VERSION 3.10)
project(${PROJECT_NAME})
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_C_STANDARD 11)

# ================================================================================
# Specify compiler and flags (do not change this)
# ================================================================================
if (${CONFIG_COMPILER} STREQUAL GNU)
    set(CMAKE_C_COMPILER "gcc")
    set(CMAKE_CXX_COMPILER "g++")
    set(CMAKE_C_COMPILER_ID "GNU")
    set(CMAKE_CXX_COMPILER_ID "GNU")
elseif(${CONFIG_COMPILER} STREQUAL Clang)
    set(CMAKE_C_COMPILER "clang")
    set(CMAKE_CXX_COMPILER "clang++")
    set(CMAKE_C_COMPILER_ID "Clang")
    set(CMAKE_CXX_COMPILER_ID "Clang")
elseif(${CONFIG_COMPILER} STREQUAL Intel)
    set(CMAKE_C_COMPILER "/opt/intel/bin/icc")
    set(CMAKE_CXX_COMPILER "/opt/intel/bin/icpc")
    set(CMAKE_C_COMPILER_ID "Intel")
    set(CMAKE_CXX_COMPILER_ID "Intel")
else()
    message([FATAL_ERROR] " Compiler not selected correctly in CMakeLists. Using default config" ...)
endif ()

# Reset compiler flags to get full control
set(CMAKE_C_FLAGS           "")
set(CMAKE_CXX_FLAGS         "")
set(CMAKE_C_FLAGS_RELEASE   "")
set(CMAKE_CXX_FLAGS_RELEASE "")
set(CMAKE_C_FLAGS_DEBUG     "")
set(CMAKE_CXX_FLAGS_DEBUG   "")

# Define standard
set(CMAKE_C_FLAGS   "-std=c11 -Wno-deprecated")
set(CMAKE_CXX_FLAGS "-std=c++11 -Wno-deprecated")

if (${CONFIG_DEBUG} STREQUAL "ON")
    # Debug flag
    set(CMAKE_C_FLAGS     "${CMAKE_C_FLAGS} -O0 -g -march=native --coverage")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O0 -g -march=native --coverage")
else()
    # Set compiler flags
    set(CMAKE_C_FLAGS      "${CMAKE_C_FLAGS} ${CONFIG_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${CONFIG_FLAGS}")
endif ()


# ================================================================================
# Define binary executable and libraries to be linked (Do not change this)
# ================================================================================
add_executable(${PROJECT_NAME} ${SOURCE_FILES})

if (${CONFIG_GENERATE_ASSEMBLY} MATCHES "ON")
    set_target_properties(${PROJECT_NAME} PROPERTIES COMPILE_FLAGS -save-temps)
endif ()

# Add math library for floating point environment
target_link_libraries(${PROJECT_NAME} ${CONFIG_LIBRARIES})

cmake_minimum_required(VERSION 3.8)

project(talk)

# add_subdirectory(example)

file(GLOB examples ${CMAKE_CURRENT_SOURCE_DIR}/example/*.cpp
                   ${CMAKE_CURRENT_SOURCE_DIR}/example/*.hpp)

add_custom_command(
    OUTPUT
        index.html
    COMMAND
        ${CMAKE_CURRENT_SOURCE_DIR}/slides/sample_code.py
        --in-file ${CMAKE_CURRENT_SOURCE_DIR}/slides/index.html.in
        --cpp-root ${CMAKE_CURRENT_SOURCE_DIR}/example
    DEPENDS
        ${CMAKE_CURRENT_SOURCE_DIR}/slides/index.html.in
        ${examples}
    COMMENT
        "Generating index.html from index.html.in and source code samples."
)

add_custom_target(gen_index_html ALL DEPENDS index.html)

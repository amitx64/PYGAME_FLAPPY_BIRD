import cx_Freeze



executables = [cx_Freeze.Executable("main.py", base = "Win32GUI")]

cx_Freeze.setup(

    name="FlappyBird",
    options={"build_exe": {"packages":["pygame","sys","random"],"include_files": ["C:\\Users\\AMIT\\Desktop\\example\\PYGAME_FLAPPY_BIRD\\gallery","C:\\Users\\AMIT\\Desktop\\example\\PYGAME_FLAPPY_BIRD\\04B_19.TTF"],
                           }},
    executables = executables

    )

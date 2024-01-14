from window_test import WindowTest
from window_skybox import WindowSkybox
import moderngl_window as mglw


def main():
    # mglw.run_window_config(WindowTest)
    mglw.run_window_config(WindowSkybox)


if __name__ == "__main__":
    main()

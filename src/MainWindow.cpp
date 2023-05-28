//
// Created by YarAllex on 28.05.23.
//

#include "../include/MainWindow.h"
#include <gtkmm.h>

MainWindow::MainWindow()
{
    set_title("Mariyka");
    set_default_size(640, 480);
}

int main(int argc, char* argv[]) {
    auto app = Gtk::Application::create("org.gtkmm.examples.base");

    return app->make_window_and_run<MainWindow>(argc, argv);
}

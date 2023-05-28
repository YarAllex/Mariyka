//
// Created by YarAllex on 28.05.23.
//

#include "../include/MainWindow.h"
#include <gtkmm.h>
#include <iostream>
#include <thread>

class MainWindow : public Gtk::Window {

private:

    const int MARGIN_TOP_BOX = 10;
    const int MARGIN_WIDGET = 5;

    Gtk::Button* chooseFileButton;
    Gtk::Button* startButton;
    Gtk::Button* stopButton;

    Gtk::Box* topBox;
    Gtk::Box* buttonBox;
    Gtk::Box* videoSrcBox;

    Gtk::Label* pathLabel;
    Gtk::Text* pathEntry;

    std::string pathString;

public:

    MainWindow() {
        set_title("Mariyka");
        set_default_size(640, 480);

        topBox = new Gtk::Box(Gtk::Orientation::VERTICAL);
        topBox->set_margin(MARGIN_TOP_BOX);
        set_child(*topBox);

        videoSrcBox = new Gtk::Box(Gtk::Orientation::HORIZONTAL);
        topBox->append(*videoSrcBox);

        buttonBox = new Gtk::Box(Gtk::Orientation::HORIZONTAL);
        topBox->append(*buttonBox);

        createVideoSrcWidgets();
        createButtons();
    }

private:

    void createButtons(){
        chooseFileButton = new Gtk::Button("Choose the file...");
        startButton = new Gtk::Button("Start" , true);
        stopButton = new Gtk::Button("Stop" , true);

        chooseFileButton->set_margin(MARGIN_WIDGET);
        startButton->set_margin(MARGIN_WIDGET);
        stopButton->set_margin(MARGIN_WIDGET);

        chooseFileButton->set_hexpand();
        startButton->set_hexpand();
        stopButton->set_hexpand();

        buttonBox->append(*chooseFileButton);
        buttonBox->append(*startButton);
        buttonBox->append(*stopButton);

//        startButton->set_sensitive(false);
        stopButton->set_sensitive(false);

        chooseFileButton->signal_clicked().connect(sigc::mem_fun(*this, &MainWindow::onChooseFileClicked));
        startButton->signal_clicked().connect(sigc::mem_fun(*this, &MainWindow::onStartClicked));
    }

    void createVideoSrcWidgets() {
        pathLabel = new Gtk::Label("Video source: ");
        pathLabel->set_margin(MARGIN_WIDGET);
//        pathLabel->set_hexpand(true);
        videoSrcBox->append(*pathLabel);

        pathEntry = new Gtk::Text();
        pathEntry->set_margin(MARGIN_WIDGET);
        pathEntry->set_hexpand(true);
        pathEntry->set_sensitive(false);
        videoSrcBox->append(*pathEntry);
    }

    void onStartClicked() {
//        std::thread thread(runCmd());
    }

    void runCmd() {
        //        system("intellij-idea-community");
        FILE * pipe = popen("intellij-idea-community", "w");

//        write
        pclose(pipe);
    }

    void onChooseFileClicked() {
        auto fileDialog = Gtk::FileDialog::create();
//        fileDialog->set_modal(true);
        fileDialog->open(*this, sigc::bind(sigc::mem_fun(*this, &MainWindow::onFileChooserResponse), fileDialog));
    }

    void onFileChooserResponse(const Glib::RefPtr<Gio::AsyncResult>& result, const Glib::RefPtr<Gtk::FileDialog>& dialog) {
        auto file = dialog->open_finish(result);
        pathString = file->get_path();
        if (!pathString.empty()) {
            startButton->set_sensitive(true);
        }
        pathEntry->set_text(pathString);
        std::cout << "File selected: " << pathString << std::endl;
    }
};

int main(int argc, char* argv[]) {
    auto app = Gtk::Application::create("org.gtkmm.examples.base");

    return app->make_window_and_run<MainWindow>(argc, argv);
}

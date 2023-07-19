import os
import pathlib
from kivy.uix.boxlayout import BoxLayout
from typing import Any
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from SourceCode import facade


class DesignControl(BoxLayout):
    """
     Handles the graphical user interface logic.
     It allows users to select images or directories of images and perform colorblindness detection on them.
     The class also manages the display of images and the results of the colorblindness detection.
    """
    def __init__(self, **kwargs: Any) -> None:
        """
        Initializes the DesignControl instance.
        Sets up variables and components needed for the GUI and the application logic.
        :param kwargs:
        """
        super(DesignControl, self).__init__(**kwargs)

        self.manager_open = False
        self.directory = ''
        self.image_extensions = ['.jpg', '.png']
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager,
            select_path=self.select_path,
            preview=False,
            ext=self.image_extensions)
        self.image_stack = []
        self.image_index = 0
        self.issue_labels = [self.ids.prop_issue_label, self.ids.deut_issue_label, self.ids.trit_issue_label]
        self.logic_control = facade.Facade()

    def file_manager_open(self) -> None:
        """
        Opens the file manager, allowing users to select image or directory of images.
        """
        self.manager_open = True
        self.file_manager.show(os.path.dirname(os.getcwd()))

    def select_path(self, path: str) -> None:
        """
        Callback function for the file manager when a path is selected
        Processes the selected path to obtain a list of image paths
        :param path: User selected path
        """
        self.directory = pathlib.Path(path)
        self.image_stack = []
        if os.path.isdir(self.directory):
            for i in os.listdir(self.directory):
                if pathlib.Path(i).suffix in self.image_extensions:
                    self.image_stack.append(os.path.join(self.directory, i))
        else:
            self.image_stack.append(os.path.join(self.directory))
        self.exit_manager()
        self.show_image()

    def exit_manager(self, *args: Any) -> None:
        """
        Callback function for the file manager when it is closed.
        """
        self.manager_open = False
        self.file_manager.close()

    def show_image(self) -> None:
        """
        Displays the current image from the 'image_stack' to the GUI.
        """
        if self.image_stack:
            self.reset_issue_labels()
            img_path = self.image_stack[self.image_index]
            self.ids.cover_img.source = img_path
            self.ids.img_name_label.text = os.path.basename(img_path)
            self.ids.img_name_label.opacity = 1

    def change_image(self, direction: int) -> None:
        """
        Changes the currently displayed image based on the direction.
        Displays next image if direction is 1 and previous image if direction is -1
        :param direction: 1 or -1
        """
        if 0 <= self.image_index + direction < len(self.image_stack):
            self.image_index += direction
            self.show_image()

    def start_eval(self, bt):
        """
        Initiates the colorblindness detection for the current image.
        Updates issue labels based on the results
        :param bt: Button that evoked this method, the CHECK button
        """
        if 0 <= self.image_index < len(self.image_stack):
            path = self.image_stack[self.image_index]
            if os.path.exists(path):
                self.logic_control.find_issues(path, self.ids.prot_check.active, self.ids.deut_check.active, self.ids.trit_check.active)
                for label, color_deficiency in zip(self.issue_labels, self.logic_control.report_result_list):
                    if color_deficiency.found:
                        label.opacity = 1
        bt.text = "CHECK"
        bt.disabled = False

    def show_process_button(self, bt) -> None:
        """
        Shows "PROCESSING" button text and disables the button
        :param bt: Button that evoked this method, the CHECK button
        """
        self.reset_issue_labels()
        bt.text = "PROCESSING"
        bt.disabled = True

    def show_download_button(self, bt) -> None:
        """
        Shows "PROCESSING" button text and disables the button if any colorblindness issues are found
        :param bt: Button that evoked this method, the DOWNLOAD button
        """
        if any(issues.found for issues in self.logic_control.report_result_list):
            bt.text = "PROCESSING"
            bt.disabled = True

    def download_report(self, bt) -> None:
        """
        Initiates report generation for the current image
        :param bt: Button that evoked this method, the DOWNLOAD button
        """
        if bt.disabled:
            self.logic_control.generate_report(self.image_stack[self.image_index])
            bt.text = "DOWNLOAD"
            bt.disabled = False

    def reset_issue_labels(self) -> None:
        """
        Sets the visibility of issue labels back to invisible.
        """
        for label in self.issue_labels:
            label.opacity = 0


class Design(MDApp):
    title = 'ColorBlindDetector'

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        return DesignControl()

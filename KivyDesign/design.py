import os
import pathlib
from kivy.uix.boxlayout import BoxLayout
from typing import Any
from kivymd.app import MDApp
from kivymd.uix.filemanager import MDFileManager
from SourceCode import facade


class DesignControl(BoxLayout):
    def __init__(self, **kwargs: Any) -> None:
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
        self.manager_open = True
        self.file_manager.show(os.path.dirname(os.getcwd()))

    def select_path(self, path: str) -> None:
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
        self.manager_open = False
        self.file_manager.close()

    def show_image(self):
        if self.image_stack:
            self.reset_issue_labels()
            img_path = self.image_stack[self.image_index]
            self.ids.cover_img.source = img_path
            self.ids.img_name_label.text = os.path.basename(img_path)
            self.ids.img_name_label.opacity = 1

    def change_image(self, direction):
        if 0 <= self.image_index + direction < len(self.image_stack):
            self.image_index += direction
            self.show_image()

    def start_eval(self, bt):
        if 0 <= self.image_index < len(self.image_stack):
            path = self.image_stack[self.image_index]
            self.logic_control.find_issues(path, self.ids.prot_check.active, self.ids.deut_check.active, self.ids.trit_check.active)
            for label, color_deficiency in zip(self.issue_labels, self.logic_control.report_result_list):
                if color_deficiency.found:
                    label.opacity = 1
        bt.text = "CHECK"
        bt.disabled = False

    def show_process_button(self, bt):
        self.reset_issue_labels()
        bt.text = "PROCESSING"
        bt.disabled = True

    def show_download_button(self, bt):
        if any(issues.found for issues in self.logic_control.report_result_list):
            bt.text = "PROCESSING"
            bt.disabled = True

    def download_report(self, bt):
        if bt.disabled:
            self.logic_control.generate_report(self.image_stack[self.image_index])
            bt.text = "DOWNLOAD"
            bt.disabled = False

    def reset_issue_labels(self):
        for label in self.issue_labels:
            label.opacity = 0


class Design(MDApp):
    title = 'ColorBlindDetector'

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        return DesignControl()

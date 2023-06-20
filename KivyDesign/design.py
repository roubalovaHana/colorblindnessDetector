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
        self.logic_control = facade.LogicControl()

    def file_manager_open(self) -> None:
        self.manager_open = True
        self.file_manager.show(os.path.expanduser(os.getcwd()))

    def select_path(self, path: str) -> None:
        self.directory = pathlib.Path(path)
        self.image_stack = []
        print(path)
        if os.path.isdir(self.directory):
            for i in os.listdir(self.directory):
                if pathlib.Path(i).suffix in self.image_extensions:
                    self.image_stack.append(os.path.join(self.directory, i))
        else:
            self.image_stack.append(os.path.join(self.directory))
        self.exit_manager()
        self.show_image()

    def exit_manager(self) -> None:
        self.manager_open = False
        self.file_manager.close()

    def show_image(self):
        self.reset_issue_labels()
        self.ids.cover_img.source = self.image_stack[self.image_index]

    def change_image(self, direction):
        if 0 <= self.image_index + direction < len(self.image_stack):
            self.image_index += direction
            self.show_image()

    def start_eval(self, bt):
        pass

    def show_process_button(self, bt):
        pass

    def show_download_button(self, bt):
        pass

    def download_report(self, bt):
        pass

    def reset_issue_labels(self):
        pass


class Design(MDApp):
    title = 'ColorBlindDetector'

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        return DesignControl()

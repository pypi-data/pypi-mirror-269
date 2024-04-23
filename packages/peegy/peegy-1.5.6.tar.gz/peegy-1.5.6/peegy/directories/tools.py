import os
from os.path import sep
import shutil


class DirectoryPaths(object):
    def __init__(self,
                 file_path: str = '',
                 delete_all: bool = False,
                 delete_figures: bool = False,
                 figures_folder: str = None,
                 figures_subset_folder=''):
        file_path = os.path.expanduser(file_path)
        self.file_path = file_path
        self.file_directory = os.path.dirname(os.path.abspath(file_path))
        self.file_basename_path = os.path.abspath(os.path.splitext(file_path)[0])
        self.delete_all = delete_all
        self.delete_figures = delete_figures
        self.figures_folder = figures_folder
        if self.figures_folder is None:
            self.figures_folder = os.path.join(self.file_directory, 'figures')
        if (self.delete_all or self.delete_figures) and os.path.exists(self.figures_folder):
            try:
                shutil.rmtree(self.figures_folder)
            except OSError:
                print((OSError.message))
        if not os.path.exists(self.figures_folder):
            os.makedirs(self.figures_folder)

        data_directory = os.path.join(self.file_directory, '.data')
        if self.delete_all and os.path.exists(data_directory):
            try:
                shutil.rmtree(data_directory)
            except OSError:
                print((OSError.message))
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)
        self.data_dir = data_directory
        self.figures_subset_folder = figures_subset_folder

    def get_figure_basename_path(self):
        return os.path.join(self.figure_subset_path, os.path.basename(self.file_path).split('.')[0])

    figure_basename_path = property(get_figure_basename_path)

    def get_data_basename_path(self):
        return os.path.join(self.data_subset_path, os.path.basename(self.file_path).split('.')[0])

    data_basename_path = property(get_data_basename_path)

    def get_figure_subset_path(self):
        _path = os.path.join(self.figures_folder, self.figures_subset_folder) + sep
        if not os.path.exists(_path):
            os.makedirs(_path)
        return _path

    figure_subset_path = property(get_figure_subset_path)

    def get_data_subset_path(self):
        _path = os.path.join(self.data_dir, self.figures_subset_folder)
        if not os.path.exists(_path):
            os.makedirs(_path)
        return _path

    data_path = property(get_data_subset_path)
    figures_current_dir = property(get_figure_subset_path)

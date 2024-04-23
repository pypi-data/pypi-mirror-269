from behavysis_core.data_models.bouts import Bout
from behavysis_viewer.utils.constants import CHECKSTATE2VALUE, VALUE2CHECKSTATE, VALUE2COLOR
from PySide6.QtCore import QAbstractListModel, Qt
from PySide6.QtGui import QColor


class BoutInspectListModel(QAbstractListModel):
    """
    NOTE: bout_dict is a dict entry in bouts_dict. It is thus a pointer and editing
    items in it will also edit bouts_dict.

    TODO: will this work for pydantic model??
    """

    bout: Bout
    is_selected: bool

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bout = Bout(start=-1, stop=-1, behaviour="nil", actual=0, user_defined={})
        self.is_selected = False

    @property
    def start(self):
        return self.bout.start

    @property
    def stop(self):
        return self.bout.stop

    @property
    def actual(self):
        return self.bout.actual

    @property
    def user_defined(self):
        return list(self.bout.user_defined.items())

    @actual.setter
    def actual(self, value: int) -> None:
        self.bout.actual = value
        self.layoutChanged.emit()

    def data(self, index, role):
        """
        Displays data in QListView.

        This is a required function.
        """
        behav_name, behav_val = self.user_defined[index.row()]
        # Displays text
        if role == Qt.ItemDataRole.DisplayRole:
            return f"{behav_name}"
        # Displays checkbox
        if role == Qt.ItemDataRole.CheckStateRole:
            return VALUE2CHECKSTATE[behav_val]
        # Displays background colour
        if role == Qt.ItemDataRole.BackgroundRole:
            return QColor(VALUE2COLOR[behav_val])

    def setData(self, index, value, role):
        behav_name, behav_val = self.user_defined[index.row()]
        # Updates checkbox
        if role == Qt.ItemDataRole.CheckStateRole:
            value = CHECKSTATE2VALUE[value]
            self.bout.user_defined[behav_name] = value
        self.dataChanged.emit(index, index)
        return True

    def load(self, bout: Bout):
        self.bout = bout
        self.is_selected = True
        # For QListView
        self.layoutChanged.emit()

    def rowCount(self, index):
        """
        Gets number of rows for QListView.

        This is a required function.
        """
        return len(self.user_defined)

    def flags(self, index):
        return (
            Qt.ItemFlag.ItemIsEnabled
            | Qt.ItemFlag.ItemIsSelectable
            | Qt.ItemFlag.ItemIsUserCheckable
        )

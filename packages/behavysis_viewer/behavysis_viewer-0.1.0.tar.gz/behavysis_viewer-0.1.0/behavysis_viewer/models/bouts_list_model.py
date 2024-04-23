import numpy as np
from behavysis_core.data_models.bouts import Bouts
from behavysis_core.mixins.behaviour_mixin import BehaviourMixin
from behavysis_core.mixins.df_io_mixin import DFIOMixin
from behavysis_viewer.pydantic_models.experiment_configs import ExperimentConfigs
from behavysis_viewer.utils.constants import VALUE2COLOR
from PySide6.QtCore import QAbstractListModel, Qt
from PySide6.QtGui import QColor


class BoutsListModel(QAbstractListModel):

    bouts: Bouts

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.bouts = Bouts(start=-1, stop=-1, bouts=[])

    def data(self, index, role):
        """
        Displays data in QListView.

        This is a required function.
        """
        bout = self.bouts.bouts[index.row()]
        # Displays text
        if role == Qt.ItemDataRole.DisplayRole:
            return f"{bout.behaviour} - {index.row()}"
        # Displays background colour
        if role == Qt.ItemDataRole.BackgroundRole:
            return QColor(VALUE2COLOR[bout.actual])

    def setData(self, index, value, role):
        # Updates checkbox
        # if role == Qt.ItemDataRole.CheckStateRole:
        #     self.bouts_df[index.row()][3] = value
        # self.dataChanged.emit(index, index)
        return True

    def load(self, fp: str, configs: ExperimentConfigs):
        # Getting necessary configs
        user_behavs = configs.user.classify_behaviours.user_behavs
        # Loading data
        behavs_df = DFIOMixin.read_feather(fp)
        # Adding actual and user_behavs to behavs_df (if they aren't already there)
        behavs_df = BehaviourMixin.frames_add_behaviour(behavs_df, user_behavs)
        # behavs_df to bouts
        self.bouts = BehaviourMixin.frames_2_bouts(behavs_df)
        # print(self.bouts.model_dumps_json(indent=2))
        self.layoutChanged.emit()

    def rowCount(self, index):
        """
        Gets number of rows for QListView.

        This is a required function.
        """
        return len(self.bouts.bouts)

    def flags(self, index):
        return (
            Qt.ItemFlag.ItemIsEnabled
            | Qt.ItemFlag.ItemIsSelectable
            | Qt.ItemFlag.ItemIsUserCheckable
        )


def serialiser(i):
    if isinstance(i, np.integer):
        return int(i)
    else:
        return i

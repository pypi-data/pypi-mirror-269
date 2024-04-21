from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QTreeView

from silicon_analyser.grid import Grid
from silicon_analyser.treeitem import TreeItem

class AbstractTreeHelper(QTreeView):
    evtTreeSelectionChanged: pyqtSignal
    
    def selectedType(self) -> str:
        raise NotImplementedError()
    
    def selectedLabel(self) -> str:
        raise NotImplementedError()

    def getSelectedItem(self) -> QStandardItem:
        raise NotImplementedError()
    
    def getSelectedGrid(self):
       raise NotImplementedError()

    def getSelectedAIGrid(self):
        raise NotImplementedError()
    
    def isItemSelected(self, rectLabel, gridName, gridItemType) -> bool:
        raise NotImplementedError()
            
    def addTreeItem(self, text, type="auto", parent_obj=None, parent_item=None) -> tuple[Grid, TreeItem]:
        raise NotImplementedError()
    
    def clearAIItem(self):
        raise NotImplementedError()
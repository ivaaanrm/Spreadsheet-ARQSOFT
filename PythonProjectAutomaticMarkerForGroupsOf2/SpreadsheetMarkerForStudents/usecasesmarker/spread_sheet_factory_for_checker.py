import sys, os
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent.parent))
sys.path.append(str(Path(__file__).parent.parent))

from usecasesmarker.spreadsheet_controller_for_checker import ISpreadsheetControllerForChecker
from SpreadsheetController import SpreadsheetController

class SpreadSheetFactoryForChecker:

    ##@brief Creates and returns an object of a class that implements the methods specified within
    # ISpreadsheetControllerForChecker (this emulates an interface for encapsulating your particular implementation of
    # a controller, and that includes only the methods required for marking your project features). This method
    # must create the framework of objects that allow that, once finalized its execution,
    # everything is ready for invoking the methods of the object implementing the methods specified within
    # ISpreadsheetControllerForChecker and starting setting contents in the spreadsheet cells and start checking results
    # and marking your code
    # @return an object of a class that implements the methods specified within ISpreadsheetControllerForChecker.

    def create_spreadsheet_controller() -> ISpreadsheetControllerForChecker:
        
        controller = SpreadsheetController()
        controller.new_spreadsheet()
        return controller
        
        raise Exception("SpreadsheetFactoryForChecker::" \
                        + "create_spreadsheet_controller(). You MUST implement the code of " \
                        + "this method in this class. The code MUST create a class that " \
                        + "implements the methods specified within ISpreadsheetControllerForChecker. " \
                        + "This code must create the framework of objects that allow that, once finalized its execution, " \
                        + "everything is ready for invoking the methods of the object implementing the methods specified within " \
                        + "ISpreadsheetControllerForChecker and starting setting contents in the spreadsheet cells and start checking results " \
                        + "marking your code"
                        )
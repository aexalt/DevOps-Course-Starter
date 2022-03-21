from todo_app.app import ViewModel
from todo_app.data.trello_items import Item

class TestItemViewModel:

    @staticmethod
    def test_todo_items():

        #arrange
        items = create_items()
        viewmodel = ViewModel(items, "result")

        #act
        filtered_items = viewmodel.todo_items()

        #assert
        assert len(filtered_items) == 2

    @staticmethod
    def test_doing_items():

        #arrange
        items = create_items()
        viewmodel = ViewModel(items, "result")

        #act
        filtered_items = viewmodel.doing_items()

        #assert
        assert len(filtered_items) == 3

    @staticmethod
    def test_done_items():

        #arrange
        items = create_items()
        viewmodel = ViewModel(items, "result")

        #act
        filtered_items = viewmodel.done_items()

        #assert
        assert len(filtered_items) == 1

def create_items():
    items = []
    items.append(Item(123, "task1","desc",None,"To Do"))
    items.append(Item(124, "task2","desc",None,"To Do"))
    items.append(Item(125, "task3","desc",None,"Done"))
    items.append(Item(126, "task4","desc",None,"Doing"))
    items.append(Item(127, "task5","desc",None,"Doing"))
    items.append(Item(127, "task6","desc",None,"Doing"))
    return items
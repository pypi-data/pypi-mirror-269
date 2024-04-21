import pytest
from tracking_decorator.track_changes import track_changes

class ReferenceClass:
    def __init__(self):
        self.var = 0

@track_changes("base_variable", "reference")
class BaseClass():
    def __init__(self, reference: ReferenceClass):
        self.base_variable = 0
        self.reference = reference
        self.untracked = "hello"

@track_changes("child_variable")
class ChildClass(BaseClass):
    def __init__(self, reference: ReferenceClass):
        super().__init__(reference)
        self.child_variable = 0
    
    def tracked_variable(self):
        return self.child_variable * 2
    
@track_changes(("update_tuple_variable", "tracked_tuple_variable"))
class TupleClass:
    def __init__(self):
        self.tracked_tuple_variable = "based"
    

def test_tracks_correctly():
    ref = ReferenceClass()
    base = BaseClass(ref)

    base.base_variable = 5
    base.reference.var = 5 # doesn't track whether value changes, only pointer
    base.untracked = "hi" #doesn't track untracked variables

    assert base.tracked_attributes == {"base_variable"}

def test_tracks_tuples_correctly():
    tup = TupleClass()

    tup.update_tuple_variable = "hi" # adds tracked attribute
    assert tup.tracked_attributes == {"tracked_tuple_variable"}

    tup.clear()
    tup.tracked_tuple_variable = "woke" # doesn't add anything
    assert tup.tracked_attributes == set()

def test_tracks_children_correctly():
    ref = ReferenceClass()
    child = ChildClass(ref)

    child.base_variable = 5 # tracks base class variable
    child.child_variable = 5 # tracks child class variable
    assert child.tracked_attributes == {"base_variable", "child_variable"}

def test_not_class_variable():
    ref = ReferenceClass()
    b1 = BaseClass(ref)
    b2 = BaseClass(ref)

    b1.base_variable = 5 # only updates b2's tracked_variables
    assert b1.tracked_attributes == {"base_variable"}
    assert b2.tracked_attributes == set()

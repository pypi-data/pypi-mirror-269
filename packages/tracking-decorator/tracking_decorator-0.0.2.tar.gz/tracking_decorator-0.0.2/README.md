# Tracking Decorator Package

This decorator tracks when the pointers to specified attributes of a class change.
Whenever this occurs, the attribute is added to a set of tracked attributes.
These attributes can be accessed with Clas.tracked_attributes, and cleared with Class.clear()

The current primary usage is for delta compression in socket communications.
Delta compression effectively means reducing the information to be sent, by only sending that which has changed since the last call.

Is intuitive and short to write, and has extremely minimal impact on performace.

Further functionality and customizability to come.

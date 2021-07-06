import abc

#interface for creating body vitals class
class BodyVitalsFactory(metaclass = abc.ABCMeta):
    #checks whether the subclass contains all the methods
    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'create_vitals') and 
                callable(subclass.create_vitals))

    #check for createVitals method title in subclass
    @abc.abstractmethod
    def create_vitals(self):
        raise NotImplementedError
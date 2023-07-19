from abc import ABC, abstractmethod

class MLBase(ABC):

    @abstractmethod
    def predict(self, data):
        return self.model.predict(data)
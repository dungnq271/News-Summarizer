from abc import ABC, abstractmethod


class BasePipeline(ABC):
    def __init__(self, splitter, chain):
        self.splitter = splitter
        self.chain = chain

    @abstractmethod
    def run(self, *args, **kwargs):
        """Execute the pipeline process."""

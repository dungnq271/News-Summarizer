from typing import Optional

from src.summarize import load_map_reduce_chain

from .base_pipe import BasePipeline


class NewsSummarizePipeline(BasePipeline):
    def __init__(
        self, llm, splitter, chain_type: Optional[str] = "map_reduce"
    ):
        chain = load_map_reduce_chain(llm)

        if chain_type != "map_reduce":
            raise NotImplementedError

        super().__init__(splitter, chain)

    def run(self, *args, **kwargs):
        splits = self.splitter.create_documents([args[-1]])
        output = self.chain.invoke(splits)
        return output["output_text"]

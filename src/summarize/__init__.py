from langchain.chains.summarize import load_summarize_chain

from .map_reduce_prompt import PROMPT_COMBINE, PROMPT_INIT


def load_map_reduce_chain(llm):
    return load_summarize_chain(
        llm,
        chain_type="map_reduce",
        map_prompt=PROMPT_INIT,
        combine_prompt=PROMPT_COMBINE,
    )

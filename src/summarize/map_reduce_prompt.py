from langchain_core.prompts import PromptTemplate

prompt_template = """
Sau đây là một nội dung được trích xuất của một văn bản,
nhiệm vụ của bạn là hãy tóm tắt nó
---CONTEXT---
{text}
---END CONTEXT---
Hãy đưa ra tóm tắt của văn bản trên.
Tôi chỉ cần phần tóm tắt, và không cần thêm bất kì thứ gì khác.
Tóm Tắt:
"""
PROMPT_INIT = PromptTemplate(
    template=prompt_template, input_variables=["text"]
)


combine_template = """
Dưới đây là các đoạn tóm tắt của từng đoạn nhỏ của một văn bản lớn.
---CONTEXT---
{text}
---END CONTEXT---
Dựa trên các đoạn trên, hãy đưa ra tóm tắt tổng của tất cả các đoạn trên.
Tôi chỉ cần tóm tắt tổng, không cần thêm bất kì thứ gì khác.
Tóm tắt tổng:
"""
PROMPT_COMBINE = PromptTemplate(
    template=combine_template, input_variables=["text"]
)

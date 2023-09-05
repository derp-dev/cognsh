from continuedev.src.continuedev.core.models import Models
from continuedev.src.continuedev.libs.llm.together import TogetherLLM

config = ContinueConfig(
    ...
    models=Models(
        default=TogetherLLM(
            api_key="<API_KEY>",
            model="togethercomputer/CodeLlama-13b-Instruct"
        )
    )
)
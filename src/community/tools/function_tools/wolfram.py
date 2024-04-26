# https://python.langchain.com/docs/integrations/tools/wolfram_alpha/

import os
from typing import Any, Dict, List

import dotenv
from langchain_community.utilities.wolfram_alpha import WolframAlphaAPIWrapper

from community.tools import BaseFunctionTool


class WolframAlphaFunctionTool(BaseFunctionTool):
    def __init__(self):
        if "WOLFRAM_ALPHA_APP_ID" not in os.environ:
            raise ValueError(
                "Please set the WOLFRAM_ALPHA_APP_ID environment variable."
            )

        self.app_id = os.environ["WOLFRAM_ALPHA_APP_ID"]
        self.tool = WolframAlphaAPIWrapper(wolfram_alpha_appid=self.app_id)

    def call(self, parameters: str, **kwargs: Any) -> List[Dict[str, Any]]:
        to_evaluate = parameters.get("expression", "")
        result = self.tool.run(to_evaluate)
        return {"result": result, "text": result}


if __name__ == "__main__":
    dotenv.load_dotenv()
    retriever = WolframAlphaFunctionTool()
    retriever.call({"expression": "what is 1+1?"})

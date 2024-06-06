from typing import Any, Dict, List

from py_expression_eval import Parser

from backend.tools.base import BaseTool


class Calculator(BaseTool):
    """
    Function Tool that evaluates mathematical expressions.
    """

    @classmethod
    def is_available(cls) -> bool:
        return True

    def call(self, parameters: dict, **kwargs: Any) -> List[Dict[str, Any]]:
        math_parser = Parser()
        expression = parameters.get("code", "")
        
        # remove lines that start with # and empty lines
        expression = "\n".join(
            [line for line in expression.split("\n") if not line.startswith("#")]
        )

        to_evaluate = expression.replace("pi", "PI").replace("e", "E")

        result = []
        try:
            result = {"text": math_parser.parse(to_evaluate).evaluate({})}
        except Exception as e:
            result = {"text": f"Parsing error - syntax not allowed."}
        
        return result

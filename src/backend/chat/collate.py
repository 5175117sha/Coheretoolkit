from itertools import zip_longest
from typing import Any, Dict, List

from backend.model_deployments.base import BaseDeployment

RELEVANCE_THRESHOLD = 0.5


def combine_documents(
    tool_results: List[Dict[str, Any]],
    model: BaseDeployment,
) -> List[Dict[str, Any]]:
    """
    Combines documents from different retrievers and reranks them.

    Args:
        tool_results (List[Dict[str, Any]]): List of tool_results from different retrievers.
            Each tool_result contains a ToolCall and a list of Outputs.
        model (BaseDeployment): Model deployment.

    Returns:
        List[Dict[str, Any]]: List of combined documents.
    """
    return rerank_and_chunk(tool_results, model)


def rerank_and_chunk(
    tool_resuls: List[Dict[str, Any]], model: BaseDeployment
) -> Dict[str, List[Dict[str, Any]]]:
    """
    Takes a list of tool_results and internally reranks the documents for each query, if there's one e.g:
    [{"q1":[1, 2, 3],"q2": [4, 5, 6]] -> [{"q1":[2 , 3, 1],"q2": [4, 6, 5]]

    Args:
        tool_resuls (List[Dict[str, Any]]): List of tool_results from different retrievers.
            Each tool_result contains a ToolCall and a list of Outputs.
        model (BaseDeployment): Model deployment.

    Returns:
        Dict[str, List[Dict[str, Any]]]: Dictionary from queries of lists of reranked documents.
    """
    # If rerank is not enabled return documents as is:
    if not model.rerank_enabled:
        return tool_resuls

    reranked_results = {}
    for tool_result in tool_resuls:
        tool_call = tool_result["call"]

        # Only rerank if there is a query
        if not tool_call.parameters.get("query") and not tool_call.parameters.get(
            "search_query"
        ):
            reranked_results[str(tool_call)] = tool_result
            continue

        query = tool_call.parameters.get("query") or tool_call.parameters.get(
            "search_query"
        )

        chunked_outputs = []
        for output in tool_result["outputs"]:
            text = output.get("text")

            if not text:
                chunked_outputs.append([output])
                continue

            chunks = chunk(text)
            chunked_outputs.extend([dict(output, text=chunk) for chunk in chunks])

        # If no documents to rerank, continue to the next query
        if not chunked_outputs:
            continue

        res = model.invoke_rerank(query=query, documents=chunked_outputs)

        # Sort the results by relevance score
        res.results.sort(key=lambda x: x.relevance_score, reverse=True)

        # Map the results back to the original documents
        # Merges the results with the same tool call and parameters
        tool_call_hashable = str(tool_call)
        if tool_call_hashable not in reranked_results.keys():
            reranked_results[tool_call_hashable] = {"call": tool_call, "outputs": []}

        reranked_results[tool_call_hashable]["outputs"].extend(
            [
                chunked_outputs[r.index]
                for r in res.results
                if r.relevance_score > RELEVANCE_THRESHOLD
            ]
        )

    return list(reranked_results.values())


def chunk(content, compact_mode=False, soft_word_cut_off=100, hard_word_cut_off=300):
    if compact_mode:
        content = content.replace("\n", " ")

    chunks = []
    current_chunk = ""
    words = content.split()
    word_count = 0

    for word in words:
        if word_count + len(word.split()) > hard_word_cut_off:
            # If adding the next word exceeds the hard limit, finalize the current chunk
            chunks.append(current_chunk)
            current_chunk = ""
            word_count = 0

        if word_count + len(word.split()) > soft_word_cut_off and word.endswith("."):
            # If adding the next word exceeds the soft limit and the word ends with a period, finalize the current chunk
            current_chunk += " " + word
            chunks.append(current_chunk.strip())
            current_chunk = ""
            word_count = 0
        else:
            # Add the word to the current chunk
            if current_chunk == "":
                current_chunk = word
            else:
                current_chunk += " " + word
            word_count += len(word.split())

    # Add any remaining content as the last chunk
    if current_chunk != "":
        chunks.append(current_chunk.strip())

    return chunks

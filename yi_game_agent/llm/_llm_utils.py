# -*- coding: utf-8 -*-
"""Utils for models"""
from typing import Optional, List

def _verify_text_content_in_openai_delta_response(response: dict) -> bool:
    """Verify if the text content exists in the openai streaming response

    Args:
        response (`dict`):
            The JSON-format OpenAI response (After calling `model_dump`
             function)

    Returns:
        `bool`: If the text content exists
    """

    if len(response.get("choices", [])) == 0:
        return False

    if response["choices"][0].get("delta", None) is None:
        return False

    if response["choices"][0]["delta"].get("content", None) is None:
        return False

    return True


def _verify_text_content_in_openai_message_response(response: dict) -> bool:
    """Verify if the text content exists in the openai streaming response

    Args:
        response (`dict`):
            The JSON-format OpenAI response (After calling `model_dump`
             function)

    Returns:
        `bool`: If the text content exists
    """

    if len(response.get("choices", [])) == 0:
        return False

    if response["choices"][0].get("message", None) is None:
        return False

    if response["choices"][0]["message"].get("content", None) is None:
        return False

    return True

def _update_tool_calls(tool_calls: List[dict], tool_calls_delta: Optional[List[dict]]) -> List[dict]:
    """
    Use the tool_calls_delta objects received from openai stream chunks
    to update the running tool_calls object.

    Args:
        tool_calls (List[dict]): the list of tool calls
        tool_calls_delta (Optional[List[dict]): the delta to update tool_calls

    Returns:
        List[dict]: the updated tool calls
    """
    if tool_calls_delta is None:
        return tool_calls
    
    tc_delta = tool_calls_delta[0]

    if len(tool_calls) == 0:
        tool_calls.append(tc_delta)
    else:
        # we need to either update latest tool_call or start a
        # new tool_call (i.e., multiple tools in this turn) and
        # accumulate that new tool_call with future delta chunks
        t = tool_calls[-1]
        if t["index"] != tc_delta["index"]:
            # the start of a new tool call, so append to our running tool_calls list
            tool_calls.append(tc_delta)
        else:
            # not the start of a new tool call, so update last item of tool_calls

            # validations to get passed by mypy
            assert t["function"] is not None
            assert tc_delta["function"] is not None
            assert t["function"]["arguments"] is not None
            assert t["function"]["name"] is not None
            assert t["id"] is not None

            t["function"]["arguments"] += tc_delta["function"]["arguments"] or ""
            t["function"]["name"]  += tc_delta["function"]["name"]  or ""
            t["id"] += tc_delta["id"] or ""
            
    return tool_calls
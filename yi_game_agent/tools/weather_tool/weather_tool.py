from yi_game_agent.tools.service_response import ServiceResponse, ServiceExecStatus


def get_weather(location: str, unit: str) -> ServiceResponse:
    """Retrieves the current weather information for a given location.

    Args:
        location (str): The name of the location for which to retrieve the weather.
        unit (str): The unit for temperature measurement. Must be either 'c' for Celsius
                    or 'f' for Fahrenheit.

    Returns:
        ServiceResponse: A dictionary with two variables: `status` and
        `content`. The `status` variable is from the ServiceExecStatus enum,
        and `content` is a list of search results or error information,
        which depends on the `status` variable.
    """
    # Validate parameters
    if not isinstance(location, str):
        raise TypeError("location must be a string")
    if unit not in ["c", "f"]:
        raise ValueError("unit must be 'c' or 'f'")

    # Simulate getting weather information
    # In practice, you would call a real weather API here
    sample_weather_data = {
        "location": location,
        "temperature": 20 if unit == "c" else 68,
        "unit": unit,
        "description": "Clear",
    }
    result = f"{location}'s temperature is {sample_weather_data['temperature']} {sample_weather_data['unit']} and the weather is {sample_weather_data['description']}"

    return ServiceResponse(ServiceExecStatus.SUCCESS, result)

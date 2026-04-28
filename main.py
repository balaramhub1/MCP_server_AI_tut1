"""
MCP server entry point for exposing cryptocurrency pricing as a tool.

This module defines and runs a FastMCP server with one tool:
`get_cryptocurrency_price`, which fetches the latest cryptocurrency price from
CoinGecko's public API.
"""

from mcp.server.fastmcp import FastMCP
import requests

# Create the MCP server instance that will host tool definitions.
mcp = FastMCP()


@mcp.tool(
    name="get_cryptocurrency_price",
    description="Get the current price of a cryptocurrency in USD from the CoinGecko.",
)
def get_cryptocurrency_price(coin: str, currency: str = "usd") -> float:
    """
    Retrieve the current price for a cryptocurrency from CoinGecko.

    Args:
        coin: CoinGecko coin ID (for example: "bitcoin", "ethereum").
        currency: Target fiat/quote currency code (default: "usd").

    Returns:
        The latest numeric price for `coin` in `currency`.

    Raises:
        ValueError: If the response does not contain the expected coin/currency data.
        requests.RequestException: If the HTTP request fails (connection, timeout, etc.).
        ValueError: If JSON decoding fails.
    """
    # Normalize user input for API compatibility.
    coin = coin.lower()
    currency = currency.lower()

    # CoinGecko endpoint for simple spot pricing.
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": coin,
        "vs_currencies": currency,
    }

    # Call CoinGecko and parse the JSON payload.
    response = requests.get(url, params=params, timeout=10)
    data = response.json()

    # Guard clause for missing response fields.
    if coin not in data and currency in data[coin]:
        raise ValueError(f"Could not retrieve price for {coin} in {currency}.")

    return data[coin][currency]


if __name__ == "__main__":
    # Start the MCP server using SSE transport for client communication.
    mcp.run(transport="sse")

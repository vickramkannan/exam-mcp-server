
import hashlib
import os

from mcp.server.fastmcp import FastMCP, Context

EMAIL = "22f3000616@ds.study.iitm.ac.in"

mcp = FastMCP(
    "Exam Challenge Server",
    host="0.0.0.0",
    port=int(os.environ.get("PORT", "10000")),
)


@mcp.tool()
async def solve_challenge(ctx: Context) -> str:
    """Solve the current exam challenge from the HTTP request headers."""
    request = ctx.request_context.request
    challenge = request.headers.get("x-exam-challenge")

    if not challenge:
        raise ValueError("Missing X-Exam-Challenge header")

    normalized_email = EMAIL.strip().lower()
    message = f"{challenge}:{normalized_email}"
    return hashlib.sha256(message.encode("utf-8")).hexdigest()[:16]


if __name__ == "__main__":
    mcp.run(transport="streamable-http")

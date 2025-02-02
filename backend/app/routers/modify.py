from fastapi import APIRouter, Request
from dotenv import load_dotenv
from app.services.claude_service import ClaudeService
from app.services.stackspot_service import StackSpotService
from app.core.limiter import limiter
from anthropic._exceptions import RateLimitError
from app.prompts import SYSTEM_MODIFY_PROMPT
from pydantic import BaseModel

load_dotenv()

router = APIRouter(prefix="/modify", tags=["Generation"])

# Initialize services
claude_service = ClaudeService()
stackspot_service = StackSpotService()

# Define the request body model


class ModifyRequest(BaseModel):
    diagram: str
    explanation: str
    instructions: str
    api_key: str | None = None
    use_stackspot: bool = False


@router.post("")
# @limiter.limit("1/minute;5/day") # TEMP: disable rate limit for growth??
async def modify(request: Request, body: ModifyRequest):
    try:
        # Choose which service to use based on use_stackspot flag
        ai_service = stackspot_service if body.use_stackspot else claude_service

        # Call the chosen AI service
        modified_diagram = ai_service.call_stackspot_api(
            system_prompt=SYSTEM_MODIFY_PROMPT,
            data={
                "diagram": body.diagram,
                "explanation": body.explanation,
                "instructions": body.instructions,
            },
            api_key=body.api_key,
        ) if body.use_stackspot else ai_service.call_claude_api(
            system_prompt=SYSTEM_MODIFY_PROMPT,
            data={
                "diagram": body.diagram,
                "explanation": body.explanation,
                "instructions": body.instructions,
            },
            api_key=body.api_key,
        )

        # Check for BAD_INSTRUCTIONS response
        if "BAD_INSTRUCTIONS" in modified_diagram:
            return {"error": "Invalid or unclear instructions provided"}

        return {"diagram": modified_diagram}
    except RateLimitError as e:
        raise HTTPException(
            status_code=429,
            detail="Service is currently experiencing high demand. Please try again in a few minutes.",
        )
    except Exception as e:
        return {"error": str(e)}

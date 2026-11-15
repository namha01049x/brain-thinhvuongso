from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict, Any, List

router = APIRouter(prefix="/api/studio", tags=["Studio & Skills"])

# Danh sách kỹ năng chính xác theo Javis OS thực tế (Ảnh 3)
SKILLS_LIST = [
    {
        "id": "html-to-webcake",
        "name": "HTML to Webcake",
        "tag": "system",
        "category": "Marketing",
        "enabled": True,
        "description": "Turn an HTML page into a .pke file the Webcake builder can open, keeping the original colours, type sizes, images and layout.",
        "badges": ["Marketing", "html-to-webcake"]
    },
    {
        "id": "ingest-source",
        "name": "Ingest Source",
        "tag": "system",
        "category": "AI",
        "enabled": True,
        "description": "Digest one raw source into the Second Brain and distil it into wiki knowledge that compounds.",
        "badges": ["AI", "ingest-source"]
    },
    {
        "id": "javis-builder",
        "name": "Javis Builder",
        "tag": "system",
        "category": "AI",
        "enabled": True,
        "description": "Create or edit a Javis capability: agent, skill, workflow, loop, plugin. Ships file templates and the rules against duplicates.",
        "badges": ["AI", "javis-builder"]
    },
    {
        "id": "lint-wiki",
        "name": "Lint Wiki",
        "tag": "system",
        "category": "AI",
        "enabled": True,
        "description": "Audit the health of the Second Brain wiki and hand back a list of problems. Never mass-edits on its own.",
        "badges": ["AI", "lint-wiki"]
    },
    {
        "id": "notes",
        "name": "Notes",
        "tag": "system",
        "category": "AI",
        "enabled": True,
        "description": "Save the current message verbatim into sources/ (images included), then distil it up to the wiki if it earns a place.",
        "badges": ["AI", "notes"]
    },
    {
        "id": "query-wiki",
        "name": "Query Wiki",
        "tag": "system",
        "category": "AI",
        "enabled": True,
        "description": "Mine the knowledge held in the Second Brain: synthesis, comparison, hypotheses. Every answer carries citations.",
        "badges": ["AI", "query-wiki"]
    },
    {
        "id": "facebook-ads-mcp",
        "name": "Facebook Ads & CPA Optimizer",
        "tag": "system",
        "category": "Marketing",
        "enabled": True,
        "description": "Query Meta Ads Graph API, calculate real-time CPA, link clicks, ROAS and detect burning adsets.",
        "badges": ["Marketing", "meta-ads"]
    },
    {
        "id": "zalo-agent-cli",
        "name": "Zalo Agent CLI Bridge",
        "tag": "system",
        "category": "Social",
        "enabled": True,
        "description": "Read and dispatch Zalo direct messages via safe authenticated local command line bridge.",
        "badges": ["Social", "zalo-cli"]
    }
]

@router.get("/skills")
def list_skills():
    ai_count = sum(1 for s in SKILLS_LIST if s["category"] == "AI")
    mkt_count = sum(1 for s in SKILLS_LIST if s["category"] == "Marketing")
    return {
        "skills": SKILLS_LIST,
        "counts": {
            "all": len(SKILLS_LIST),
            "ai": ai_count,
            "marketing": mkt_count,
            "social": 1
        }
    }

class ToggleSkillPayload(BaseModel):
    skill_id: str
    enabled: bool

@router.post("/toggle-skill")
def toggle_skill(payload: ToggleSkillPayload):
    for s in SKILLS_LIST:
        if s["id"] == payload.skill_id:
            s["enabled"] = payload.enabled
            return {"status": "success", "skill": s}
    return {"status": "error", "message": "Skill not found"}

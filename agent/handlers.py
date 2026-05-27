import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"


def load_json(filename: str) -> dict:
    with open(DATA_DIR / filename) as f:
        return json.load(f)


def save_json(filename: str, data: dict):
    with open(DATA_DIR / filename, "w") as f:
        json.dump(data, f, indent=2)


def list_open_positions(department: str = None) -> dict:
    data = load_json("positions.json")
    positions = [p for p in data["positions"] if p["status"] == "open"]
    if department:
        positions = [p for p in positions if p["department"].lower() == department.lower()]
    return {"count": len(positions), "positions": positions}


def get_candidate(query: str) -> dict:
    data = load_json("candidates.json")
    query_lower = query.lower()
    for candidate in data["candidates"]:
        if candidate["id"].lower() == query_lower or candidate["name"].lower() == query_lower:
            return {"found": True, "candidate": candidate}
    for candidate in data["candidates"]:
        if query_lower in candidate["name"].lower():
            return {"found": True, "candidate": candidate}
    return {"found": False, "message": f"No candidate found matching '{query}'"}


def list_candidates(stage: str = None, position_id: str = None) -> dict:
    data = load_json("candidates.json")
    candidates = data["candidates"]
    if stage:
        candidates = [c for c in candidates if c["stage"] == stage]
    if position_id:
        candidates = [c for c in candidates if c["applying_for"] == position_id]
    return {"count": len(candidates), "candidates": candidates}


def get_available_slots(date: str) -> dict:
    data = load_json("calendar.json")
    slots = data["available_slots"].get(date, [])
    if not slots:
        return {"available": False, "date": date, "message": "No slots available on this date"}
    return {"available": True, "date": date, "slots": slots}


def book_interview(candidate_id: str, date: str, time: str) -> dict:
    calendar = load_json("calendar.json")
    candidates = load_json("candidates.json")
    candidate = next((c for c in candidates["candidates"] if c["id"] == candidate_id), None)
    if not candidate:
        return {"success": False, "message": f"Candidate {candidate_id} not found"}
    available = calendar["available_slots"].get(date, [])
    if time not in available:
        return {"success": False, "message": f"Slot {time} on {date} is not available"}
    calendar["available_slots"][date].remove(time)
    booking = {
        "id": f"B{len(calendar['bookings']) + 1:03d}",
        "candidate_id": candidate_id,
        "candidate_name": candidate["name"],
        "position_id": candidate["applying_for"],
        "date": date,
        "time": time,
        "booked_at": datetime.now().isoformat()
    }
    calendar["bookings"].append(booking)
    save_json("calendar.json", calendar)
    return {"success": True, "booking": booking, "message": f"Interview booked: {candidate['name']} on {date} at {time}"}


def update_candidate_notes(candidate_id: str, notes: str) -> dict:
    data = load_json("candidates.json")
    for candidate in data["candidates"]:
        if candidate["id"] == candidate_id:
            candidate["notes"] = notes
            save_json("candidates.json", data)
            return {"success": True, "message": f"Notes updated for {candidate['name']}"}
    return {"success": False, "message": f"Candidate {candidate_id} not found"}


def list_upcoming_interviews(date: str = None) -> dict:
    data = load_json("calendar.json")
    bookings = data["bookings"]
    if date:
        bookings = [b for b in bookings if b["date"] == date]
    return {"count": len(bookings), "interviews": sorted(bookings, key=lambda b: (b["date"], b["time"]))}


def run_tool(tool_name: str, tool_input: dict) -> str:
    dispatch = {
        "list_open_positions": list_open_positions,
        "get_candidate": get_candidate,
        "list_candidates": list_candidates,
        "get_available_slots": get_available_slots,
        "book_interview": book_interview,
        "update_candidate_notes": update_candidate_notes,
        "list_upcoming_interviews": list_upcoming_interviews,
    }
    func = dispatch.get(tool_name)
    if not func:
        return json.dumps({"error": f"Unknown tool: {tool_name}"})
    return json.dumps(func(**tool_input))
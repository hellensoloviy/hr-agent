TOOLS = [
    {
        "name": "list_open_positions",
        "description": "Returns all currently open job positions at the company. Use when the recruiter asks about available roles, open positions, or job openings.",
        "input_schema": {
            "type": "object",
            "properties": {
                "department": {
                    "type": "string",
                    "description": "Optional: filter by department name (e.g., 'Mobile', 'Platform')"
                }
            },
            "required": []
        }
    },
    {
        "name": "get_candidate",
        "description": "Looks up a candidate's profile, application status, and notes by name or ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Candidate name or ID (e.g., 'Alice Chen' or 'C001')"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "list_candidates",
        "description": "Returns all candidates, optionally filtered by stage or the position they are applying for.",
        "input_schema": {
            "type": "object",
            "properties": {
                "stage": {
                    "type": "string",
                    "description": "Filter by stage: 'initial_screen', 'technical_screen', 'final_round'"
                },
                "position_id": {
                    "type": "string",
                    "description": "Filter by position ID (e.g., 'P002')"
                }
            },
            "required": []
        }
    },
    {
        "name": "get_available_slots",
        "description": "Returns available interview time slots for a given date.",
        "input_schema": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "Date to check in YYYY-MM-DD format"
                }
            },
            "required": ["date"]
        }
    },
    {
        "name": "book_interview",
        "description": "Books an interview slot for a candidate. Always confirm the slot and candidate name before calling this.",
        "input_schema": {
            "type": "object",
            "properties": {
                "candidate_id": {
                    "type": "string",
                    "description": "Candidate ID (e.g., 'C001')"
                },
                "date": {
                    "type": "string",
                    "description": "Date in YYYY-MM-DD format"
                },
                "time": {
                    "type": "string",
                    "description": "Time in HH:MM format (24-hour)"
                }
            },
            "required": ["candidate_id", "date", "time"]
        }
    },
    {
        "name": "update_candidate_notes",
        "description": "Adds or updates notes on a candidate's profile.",
        "input_schema": {
            "type": "object",
            "properties": {
                "candidate_id": {
                    "type": "string",
                    "description": "Candidate ID"
                },
                "notes": {
                    "type": "string",
                    "description": "The new notes to set for this candidate"
                }
            },
            "required": ["candidate_id", "notes"]
        }
    },
    {
        "name": "list_upcoming_interviews",
        "description": "Shows all upcoming booked interviews, optionally filtered by date.",
        "input_schema": {
            "type": "object",
            "properties": {
                "date": {
                    "type": "string",
                    "description": "Optional: filter to a specific date in YYYY-MM-DD format"
                }
            },
            "required": []
        }
    }

]
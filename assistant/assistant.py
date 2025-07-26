from fastapi import FastAPI, HTTPException

app = FastAPI()

# This is our mock knowledge base.
# In a real system, this would come from a database, vector store, or config management.
KNOWLEDGE_BASE = {
    "connection_error": {
        "title": "Fixing Connection Errors",
        "solutions": [
            "Check if the target service (database, API) is running and accessible.",
            "Verify firewall rules on both source and destination hosts. Port might be blocked.",
            "Ensure the DNS name is resolving to the correct IP address. Use `nslookup` or `dig`.",
            "Review service configuration files for incorrect hostnames or ports."
        ]
    },
    "auth_failure": {
        "title": "Fixing Authentication Failures",
        "solutions": [
            "Verify that the API key, password, or token is correct and has not expired.",
            "Check if the user account has the necessary permissions to access the resource.",
            "Ensure the correct authentication scheme (e.g., Bearer, Basic) is being used."
        ]
    }
}

@app.get("/")
def read_root():
    return {"message": "🤖 AI Recovery Assistant is online."}


@app.get("/get-solution/{pattern_id}")
def get_solution(pattern_id: str):
    """
    Retrieves a known solution for a given error pattern ID.
    """
    if pattern_id in KNOWLEDGE_BASE:
        return KNOWLEDGE_BASE[pattern_id]
    
    raise HTTPException(status_code=404, detail="Solution not found for this pattern.")
import os
import google.generativeai as genai
import json
import logging
import subprocess
from src.services.cyberpanel_service import CyberPanelService
from main import db
from src.models import SystemLog

class AIAgentService:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        self.cp_service = CyberPanelService()

    def analyze_and_propose(self, issue_description):
        if not self.api_key:
            return {"error": "API Key not configured"}
            
        prompt = f"""
        You are an Ultimate Admin Bot for BlackPhnix Hub.
        Issue: {issue_description}
        
        Analyze the issue and provide a fix.
        Respond ONLY with a JSON object:
        {{
            "analysis": "Short explanation",
            "proposed_fix": "Description of fix",
            "commands": ["command1", "command2"],
            "risk_level": "low/medium/high"
        }}
        """
        try:
            response = self.model.generate_content(prompt)
            # Remove markdown code blocks if present
            clean_text = response.text.replace('```json', '').replace('```', '').strip()
            return json.loads(clean_text)
        except Exception as e:
            logging.error(f"AI Error: {str(e)}")
            return {"error": str(e), "analysis": "Failed to analyze", "proposed_fix": "Manual check required", "commands": [], "risk_level": "high"}

    def execute_provisioning(self, username, password, email):
        return self.cp_service.create_user(username, password, email)

    def self_destruct(self):
        # Emergency security measure: clear sensitive logs and notify admin
        logging.critical("SELF-DESTRUCT INITIATED: Clearing sensitive runtime data.")
        try:
            # Clear system logs in DB as a safety measure
            SystemLog.query.delete()
            db.session.commit()
            return True
        except Exception as e:
            logging.error(f"Self-destruct failed: {str(e)}")
            return False

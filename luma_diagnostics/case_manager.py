"""Case management system for LUMA diagnostics."""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from . import utils
from .system_info import get_system_info
from .messages import print_info, print_success, print_error

class Case:
    """Represents a diagnostic case."""
    
    def __init__(self, case_id: str, title: str, description: str, created_at: str):
        self.case_id = case_id
        self.title = title
        self.description = description
        self.created_at = created_at
        self.results: List[Dict] = []
    
    @classmethod
    def create(cls, title: str, description: str) -> 'Case':
        """Create a new case."""
        return cls(
            case_id=utils.generate_id(),
            title=title,
            description=description,
            created_at=datetime.now().isoformat()
        )
    
    def to_dict(self) -> Dict:
        """Convert case to dictionary."""
        return {
            "case_id": self.case_id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at,
            "results": self.results
        }
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Case':
        """Create case from dictionary."""
        case = cls(
            case_id=data["case_id"],
            title=data["title"],
            description=data["description"],
            created_at=data["created_at"]
        )
        case.results = data.get("results", [])
        return case

class CaseManager:
    """Manages diagnostic cases."""
    
    def __init__(self):
        self.cases_dir = utils.get_case_dir("")
        self.cases_dir.mkdir(parents=True, exist_ok=True)
        self.current_case: Optional[Case] = None
    
    def create_case(self, title: str, description: str) -> Case:
        """Create a new case."""
        case = Case.create(title, description)
        self._save_case(case)
        self.current_case = case
        print_success(f"Created case: {case.title} (ID: {case.case_id})")
        return case
    
    def list_cases(self) -> List[Case]:
        """List all cases."""
        cases = []
        for file in self.cases_dir.glob("*.json"):
            try:
                with open(file, 'r') as f:
                    data = json.load(f)
                    cases.append(Case.from_dict(data))
            except (json.JSONDecodeError, KeyError) as e:
                print_error(f"Error reading case file {file}: {e}")
                continue
        return sorted(cases, key=lambda x: x.created_at, reverse=True)
    
    def get_case(self, case_id: str) -> Optional[Case]:
        """Get a case by ID."""
        file = self.cases_dir / f"{case_id}.json"
        if not file.exists():
            return None
        try:
            with open(file, 'r') as f:
                return Case.from_dict(json.load(f))
        except (json.JSONDecodeError, KeyError) as e:
            print_error(f"Error reading case {case_id}: {e}")
            return None
    
    def add_test_result(self, result: Dict) -> None:
        """Add a test result to the current case."""
        if not self.current_case:
            print_error("No active case. Create or select a case first.")
            return
        
        # Add system info and timestamp
        result.update({
            "timestamp": datetime.now().isoformat(),
            "system_info": get_system_info()
        })
        
        self.current_case.results.append(result)
        self._save_case(self.current_case)
        print_info(f"Added test result to case {self.current_case.title}")
    
    def _save_case(self, case: Case) -> None:
        """Save a case to disk."""
        file = self.cases_dir / f"{case.case_id}.json"
        with open(file, 'w') as f:
            json.dump(case.to_dict(), f, indent=2)
    
    def select_case(self, case_id: str) -> Optional[Case]:
        """Select a case as the current case."""
        case = self.get_case(case_id)
        if case:
            self.current_case = case
            print_success(f"Selected case: {case.title}")
        return case
    
    def format_case_summary(self, case: Case) -> str:
        """Format a case summary for display."""
        summary = [
            f"Case: {case.title}",
            f"ID: {case.case_id}",
            f"Created: {case.created_at}",
            f"Description: {case.description}",
            f"\nTest Results ({len(case.results)}):"
        ]
        
        for i, result in enumerate(case.results, 1):
            summary.append(f"\n{i}. Test at {result['timestamp']}")
            if result.get("error"):
                summary.append(f"   Error: {result['error']}")
            if result.get("success"):
                summary.append(f"   Success: {result['success']}")
        
        return "\n".join(summary)
    
    def export_case(self, case_id: str, output_dir: Optional[str] = None) -> str:
        """Export a case to a file that can be sent to support."""
        case = self.get_case(case_id)
        if not case:
            raise ValueError(f"Case {case_id} not found")
        
        output_dir = output_dir or os.getcwd()
        output_file = os.path.join(output_dir, f"luma_case_{case_id}.json")
        
        with open(output_file, 'w') as f:
            json.dump(case.to_dict(), f, indent=2)
        
        return output_file

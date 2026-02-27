"""
Skill Extractor
High-performance matching using optimized regular expressions.
"""

import re

class SkillExtractor:
    # ... (SKILLS_DB remains the same)

    def __init__(self):
        # Create a reverse mapping for case restoration: {'python': 'Python'}
        self.skill_map = {}
        for category, skills in self.SKILLS_DB.items():
            for s in skills:
                self.skill_map[s.lower()] = s
        
        # Compile a single master regex for speed
        # Sorting by length descending ensures 'JavaScript' matches before 'Java'
        sorted_skills = sorted(self.skill_map.keys(), key=len, reverse=True)
        pattern_string = r'\b(' + '|'.join(re.escape(s) for s in sorted_skills) + r')\b'
        self.master_regex = re.compile(pattern_string, re.IGNORECASE)

    def extract_skills(self, text):
        """
        Extracts skills in a single pass over the text.
        """
        if not text:
            return []

        # Find all matches
        matches = self.master_regex.findall(text)
        
        # Restore casing and remove duplicates
        found_skills = {self.skill_map[m.lower()] for m in matches if m.lower() in self.skill_map}
        
        return list(found_skills)

    def get_skills_by_category(self, found_skills):
        """
        Groups the extracted skills back into their original categories.
        """
        categorized = {cat: [] for cat in self.SKILLS_DB.keys()}
        for skill in found_skills:
            for cat, skill_list in self.SKILLS_DB.items():
                if skill in skill_list:
                    categorized[cat].append(skill)
        return {k: v for k, v in categorized.items() if v}
import re
import os
import uuid
from werkzeug.utils import secure_filename

class ResumeService:
    # ... (init and extraction methods remain similar)

    def process_resume(self, user_id, file, filename):
        """
        Processes and sanitizes resume data.
        """
        # 1. Secure filename to prevent directory traversal attacks
        clean_filename = secure_filename(filename)
        file_ext = clean_filename.rsplit('.', 1)[1].lower() if '.' in clean_filename else ''
        
        if file_ext not in self.ALLOWED_EXTENSIONS:
            return None, "Unsupported file format."

        # 2. Unique storage path using UUID to avoid collisions
        unique_name = f"{user_id}_{uuid.uuid4().hex[:8]}_{clean_filename}"
        file_path = os.path.join(self.UPLOAD_FOLDER, unique_name)
        file.save(file_path)

        # 3. Extraction with error handling
        text, error = (self.extract_text_from_pdf(file_path) if file_ext == 'pdf' 
                       else self.extract_text_from_docx(file_path))
        
        if error:
            return None, error

        # 4. Cognitive Parsing
        parsed_data = self._parse_resume_text(text)

        # 5. Database Upsert
        resume = Resume.query.filter_by(user_id=user_id).first()
        if resume:
            if os.path.exists(resume.file_path):
                os.remove(resume.file_path)
            resume.filename = clean_filename
            resume.file_path = file_path
            resume.raw_text = text
            resume.parsed_data = json.dumps(parsed_data)
        else:
            resume = Resume(
                user_id=user_id,
                filename=clean_filename,
                file_path=file_path,
                file_type=file_ext,
                raw_text=text,
                parsed_data=json.dumps(parsed_data)
            )
            db.session.add(resume)

        db.session.commit()
        self._populate_skills_from_resume(user_id, parsed_data)
        
        return resume, None

    def _extract_experience_years(self, text):
        """
        Enhanced regex to catch '5+ years' or 'Jan 2020 - Present' logic.
        """
        # Look for explicit mentions first
        patterns = [
            r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:exp|experience)',
            r'(?:exp|experience)[:\-\s]*(\d+)\+?\s*(?:years?|yrs?)'
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return float(match.group(1))
        
        # Fallback: Count year ranges like 2018-2022
        year_ranges = re.findall(r'(20\d{2})[\s\-\u2013]+(20\d{2}|Present|Current)', text)
        total_years = 0
        for start, end in year_ranges:
            end_year = 2026 if end.lower() in ['present', 'current'] else int(end)
            total_years += (end_year - int(start))
            
        return max(0, total_years)
"""
Data Processor for Cognitive Career Recommendation System
Handles job market data, skill taxonomies, and data preprocessing
"""

import pandas as pd
import numpy as np
import json
import requests
from typing import Dict, List, Any, Tuple
import sqlite3
from datetime import datetime, timedelta
import os

class DataProcessor:
    """
    Data processing utilities for job market data and skill taxonomies
    """
    
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), '..', 'data')
        self.job_data = None
        self.skill_taxonomy = None
        self.salary_data = None
        
        # Initialize data
        self._initialize_data()
    
    def _initialize_data(self):
        """Initialize or load existing data"""
        try:
            # Try to load existing data
            self.job_data = pd.read_csv(os.path.join(self.data_path, 'job_dataset.csv'))
            with open(os.path.join(self.data_path, 'skill_taxonomy.json'), 'r') as f:
                self.skill_taxonomy = json.load(f)
            self.salary_data = pd.read_csv(os.path.join(self.data_path, 'salary_data.csv'))
        except FileNotFoundError:
            # Create sample data if files don't exist
            self._create_sample_data()
    
    def _create_sample_data(self):
        """Create sample datasets for development and testing"""
        
        # Sample job dataset
        job_data = {
            'job_id': range(1, 101),
            'job_title': [
                'Data Scientist', 'Software Engineer', 'Product Manager', 'UX Designer',
                'DevOps Engineer', 'Business Analyst', 'Marketing Manager', 'Sales Manager',
                'Project Manager', 'Quality Assurance Engineer'
            ] * 10,
            'company': [
                'Google', 'Microsoft', 'Amazon', 'Apple', 'Facebook',
                'Netflix', 'Uber', 'Airbnb', 'Tesla', 'SpaceX'
            ] * 10,
            'location': (
                [
                    'San Francisco, CA', 'Seattle, WA', 'New York, NY', 'Austin, TX',
                    'Boston, MA', 'Chicago, IL', 'Los Angeles, CA', 'Denver, CO'
                ] * 13
            )[:100],
            'required_skills': [
                'Python, Machine Learning, SQL, Statistics',
                'Java, Python, SQL, Git, Agile',
                'Strategy, Analytics, Communication, Leadership',
                'Design, Prototyping, User Research, Figma',
                'Docker, Kubernetes, AWS, Python, Linux',
                'SQL, Excel, Analytics, Communication',
                'Marketing, Analytics, Communication, Strategy',
                'Sales, Communication, CRM, Leadership',
                'Project Management, Agile, Communication, Leadership',
                'Testing, Automation, Python, SQL'
            ] * 10,
            'experience_level': [
                'Entry Level', 'Mid Level', 'Senior Level', 'Executive'
            ] * 25,
            'employment_type': [
                'Full-time', 'Part-time', 'Contract', 'Remote'
            ] * 25,
            'industry': (
                [
                    'Technology', 'Healthcare', 'Finance', 'Education',
                    'Retail', 'Manufacturing', 'Entertainment', 'Consulting'
                ] * 13
            )[:100],
            'salary_min': np.random.randint(50000, 120000, 100),
            'salary_max': np.random.randint(80000, 200000, 100),
            'posted_date': pd.date_range(start='2024-01-01', periods=100, freq='D'),
            'description': [
                'Exciting opportunity to work with cutting-edge AI and ML technologies.',
                'Join our engineering team to build scalable software solutions.',
                'Lead product strategy and work cross-functionally with engineering teams.',
                'Design intuitive user experiences for our mobile and web applications.',
                'Manage cloud infrastructure and deployment pipelines.',
                'Analyze business data to drive strategic decision-making.',
                'Develop and execute marketing campaigns for our products.',
                'Drive sales growth and manage key customer relationships.',
                'Coordinate cross-functional projects and ensure timely delivery.',
                'Ensure quality standards through automated testing and validation.'
            ] * 10
        }
        
        self.job_data = pd.DataFrame(job_data)
        
        # Fix salary_max to be greater than salary_min
        self.job_data.loc[self.job_data['salary_max'] <= self.job_data['salary_min'], 'salary_max'] = \
            self.job_data['salary_min'] + 20000
        
        # Sample skill taxonomy
        self.skill_taxonomy = {
            "technical_skills": {
                "programming_languages": {
                    "python": {
                        "category": "Programming",
                        "difficulty": "Intermediate",
                        "market_demand": 0.95,
                        "related_skills": ["pandas", "numpy", "machine learning"],
                        "learning_resources": [
                            "Python.org Tutorial",
                            "Codecademy Python Course",
                            "Python Crash Course Book"
                        ]
                    },
                    "javascript": {
                        "category": "Programming",
                        "difficulty": "Intermediate",
                        "market_demand": 0.92,
                        "related_skills": ["react", "node.js", "html", "css"],
                        "learning_resources": [
                            "MDN Web Docs",
                            "JavaScript30 Course",
                            "You Don't Know JS Book Series"
                        ]
                    },
                    "java": {
                        "category": "Programming",
                        "difficulty": "Intermediate",
                        "market_demand": 0.88,
                        "related_skills": ["spring", "hibernate", "maven"],
                        "learning_resources": [
                            "Oracle Java Tutorials",
                            "Java: The Complete Reference",
                            "Spring Framework Documentation"
                        ]
                    }
                },
                "data_science": {
                    "machine_learning": {
                        "category": "AI/ML",
                        "difficulty": "Advanced",
                        "market_demand": 0.97,
                        "related_skills": ["python", "statistics", "pandas", "scikit-learn"],
                        "learning_resources": [
                            "Coursera Machine Learning Course",
                            "Hands-On Machine Learning Book",
                            "Kaggle Learn ML Course"
                        ]
                    },
                    "statistics": {
                        "category": "Mathematics",
                        "difficulty": "Advanced",
                        "market_demand": 0.85,
                        "related_skills": ["r", "python", "data analysis"],
                        "learning_resources": [
                            "Khan Academy Statistics",
                            "Think Stats Book",
                            "Statistical Learning Course"
                        ]
                    }
                },
                "web_development": {
                    "react": {
                        "category": "Frontend",
                        "difficulty": "Intermediate",
                        "market_demand": 0.90,
                        "related_skills": ["javascript", "html", "css", "node.js"],
                        "learning_resources": [
                            "React Official Documentation",
                            "React Complete Guide Course",
                            "Create React App Tutorial"
                        ]
                    }
                }
            },
            "soft_skills": {
                "communication": {
                    "category": "Interpersonal",
                    "difficulty": "Intermediate",
                    "market_demand": 0.99,
                    "related_skills": ["leadership", "teamwork", "presentation"],
                    "learning_resources": [
                        "Toastmasters International",
                        "Crucial Conversations Book",
                        "TED Talks on Communication"
                    ]
                },
                "leadership": {
                    "category": "Management",
                    "difficulty": "Advanced",
                    "market_demand": 0.93,
                    "related_skills": ["communication", "project management", "strategy"],
                    "learning_resources": [
                        "Harvard Leadership Courses",
                        "The Leader in Me Book",
                        "Leadership Challenge Workshop"
                    ]
                }
            }
        }
        
        # Sample salary data
        salary_data = {
            'job_title': [
                'Data Scientist', 'Software Engineer', 'Product Manager', 'UX Designer',
                'DevOps Engineer', 'Business Analyst', 'Marketing Manager'
            ],
            'experience_level': ['Entry Level'] * 7,
            'location': ['San Francisco, CA'] * 7,
            'average_salary': [95000, 85000, 105000, 75000, 90000, 70000, 80000],
            'salary_range_min': [70000, 65000, 80000, 55000, 70000, 55000, 60000],
            'salary_range_max': [120000, 105000, 130000, 95000, 110000, 85000, 100000]
        }
        
        # Duplicate for different experience levels
        base_count = len(salary_data['job_title'])
        for level in ['Mid Level', 'Senior Level']:
            for i in range(base_count):
                title = salary_data['job_title'][i]
                multiplier = 1.3 if level == 'Mid Level' else 1.6
                salary_data['job_title'].append(title)
                salary_data['experience_level'].append(level)
                salary_data['location'].append('San Francisco, CA')
                salary_data['average_salary'].append(int(salary_data['average_salary'][i] * multiplier))
                salary_data['salary_range_min'].append(int(salary_data['salary_range_min'][i] * multiplier))
                salary_data['salary_range_max'].append(int(salary_data['salary_range_max'][i] * multiplier))
        
        self.salary_data = pd.DataFrame(salary_data)
        
        # Save sample data
        self._save_data_to_files()
    
    def _save_data_to_files(self):
        """Save data to files"""
        os.makedirs(self.data_path, exist_ok=True)
        
        self.job_data.to_csv(os.path.join(self.data_path, 'job_dataset.csv'), index=False)
        
        with open(os.path.join(self.data_path, 'skill_taxonomy.json'), 'w') as f:
            json.dump(self.skill_taxonomy, f, indent=2)
        
        self.salary_data.to_csv(os.path.join(self.data_path, 'salary_data.csv'), index=False)
    
    def get_job_market_data(self, filters: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Get processed job market data with optional filters
        
        Args:
            filters: Optional filters (location, experience_level, industry, etc.)
            
        Returns:
            Processed job market data
        """
        filtered_data = self.job_data.copy()
        
        # Apply filters if provided
        if filters:
            if 'location' in filters:
                filtered_data = filtered_data[filtered_data['location'].str.contains(filters['location'], case=False, na=False)]
            
            if 'experience_level' in filters:
                filtered_data = filtered_data[filtered_data['experience_level'] == filters['experience_level']]
            
            if 'industry' in filters:
                filtered_data = filtered_data[filtered_data['industry'] == filters['industry']]
            
            if 'employment_type' in filters:
                filtered_data = filtered_data[filtered_data['employment_type'] == filters['employment_type']]
        
        # Generate market insights
        market_data = {
            'total_jobs': len(filtered_data),
            'top_companies': filtered_data['company'].value_counts().head(10).to_dict(),
            'top_locations': filtered_data['location'].value_counts().head(10).to_dict(),
            'experience_distribution': filtered_data['experience_level'].value_counts().to_dict(),
            'industry_distribution': filtered_data['industry'].value_counts().to_dict(),
            'average_salary_by_title': self._calculate_average_salaries(filtered_data),
            'top_skills': self._extract_top_skills(filtered_data),
            'jobs_by_date': self._get_job_trends(filtered_data),
            'employment_types': filtered_data['employment_type'].value_counts().to_dict()
        }
        
        return market_data
    
    def get_skills_taxonomy(self) -> Dict[str, Any]:
        """
        Get the complete skills taxonomy with learning resources and market demand
        
        Returns:
            Complete skills taxonomy
        """
        return self.skill_taxonomy
    
    def get_skill_demand_data(self, skill_name: str) -> Dict[str, Any]:
        """
        Get market demand data for a specific skill
        
        Args:
            skill_name: Name of the skill
            
        Returns:
            Skill demand analysis
        """
        skill_name_lower = skill_name.lower()
        
        # Count occurrences of skill in job postings
        skill_count = 0
        total_jobs = len(self.job_data)
        
        for skills_list in self.job_data['required_skills']:
            if skill_name_lower in skills_list.lower():
                skill_count += 1
        
        demand_percentage = (skill_count / total_jobs) * 100 if total_jobs > 0 else 0
        
        # Get salary data for jobs requiring this skill
        jobs_with_skill = self.job_data[
            self.job_data['required_skills'].str.contains(skill_name_lower, case=False, na=False)
        ]
        
        skill_demand = {
            'skill_name': skill_name,
            'demand_percentage': round(demand_percentage, 2),
            'jobs_requiring_skill': len(jobs_with_skill),
            'average_salary': {
                'min': int(jobs_with_skill['salary_min'].mean()) if len(jobs_with_skill) > 0 else 0,
                'max': int(jobs_with_skill['salary_max'].mean()) if len(jobs_with_skill) > 0 else 0
            },
            'top_job_titles': jobs_with_skill['job_title'].value_counts().head(5).to_dict(),
            'top_companies': jobs_with_skill['company'].value_counts().head(5).to_dict(),
            'growth_trend': 'Increasing',  # This would be calculated from historical data
            'related_skills': self._get_related_skills(skill_name)
        }
        
        return skill_demand
    
    def get_salary_insights(self, job_title: str, location: str = None, experience_level: str = None) -> Dict[str, Any]:
        """
        Get salary insights for specific job title and criteria
        
        Args:
            job_title: Job title to analyze
            location: Optional location filter
            experience_level: Optional experience level filter
            
        Returns:
            Salary insights and comparisons
        """
        # Filter salary data
        filtered_salary = self.salary_data[
            self.salary_data['job_title'].str.contains(job_title, case=False, na=False)
        ]
        
        if location:
            filtered_salary = filtered_salary[
                filtered_salary['location'].str.contains(location, case=False, na=False)
            ]
        
        if experience_level:
            filtered_salary = filtered_salary[
                filtered_salary['experience_level'] == experience_level
            ]
        
        if len(filtered_salary) == 0:
            return {'error': 'No salary data found for the specified criteria'}
        
        salary_insights = {
            'job_title': job_title,
            'average_salary': int(filtered_salary['average_salary'].mean()),
            'salary_range': {
                'min': int(filtered_salary['salary_range_min'].min()),
                'max': int(filtered_salary['salary_range_max'].max())
            },
            'percentiles': {
                '25th': int(filtered_salary['average_salary'].quantile(0.25)),
                '50th': int(filtered_salary['average_salary'].median()),
                '75th': int(filtered_salary['average_salary'].quantile(0.75))
            },
            'experience_level_comparison': self._get_experience_salary_comparison(job_title),
            'location_comparison': self._get_location_salary_comparison(job_title),
            'data_points': len(filtered_salary)
        }
        
        return salary_insights
    
    def analyze_career_progression(self, current_title: str, target_title: str) -> Dict[str, Any]:
        """
        Analyze career progression path between two job titles
        
        Args:
            current_title: Current job title
            target_title: Target job title
            
        Returns:
            Career progression analysis
        """
        # Get data for both titles
        current_jobs = self.job_data[
            self.job_data['job_title'].str.contains(current_title, case=False, na=False)
        ]
        target_jobs = self.job_data[
            self.job_data['job_title'].str.contains(target_title, case=False, na=False)
        ]
        
        if len(current_jobs) == 0 or len(target_jobs) == 0:
            return {'error': 'Insufficient data for career progression analysis'}
        
        # Analyze skill differences
        current_skills = self._extract_skills_from_jobs(current_jobs)
        target_skills = self._extract_skills_from_jobs(target_jobs)
        
        # Calculate skill gaps
        missing_skills = [skill for skill in target_skills if skill not in current_skills]
        common_skills = [skill for skill in target_skills if skill in current_skills]
        
        # Salary progression
        current_avg_salary = (current_jobs['salary_min'].mean() + current_jobs['salary_max'].mean()) / 2
        target_avg_salary = (target_jobs['salary_min'].mean() + target_jobs['salary_max'].mean()) / 2
        salary_increase = ((target_avg_salary - current_avg_salary) / current_avg_salary) * 100
        
        progression_analysis = {
            'current_title': current_title,
            'target_title': target_title,
            'skill_gap_analysis': {
                'missing_skills': missing_skills[:10],  # Top 10 missing skills
                'common_skills': common_skills[:10],    # Top 10 common skills
                'skill_overlap_percentage': (len(common_skills) / len(target_skills)) * 100 if target_skills else 0
            },
            'salary_progression': {
                'current_average': int(current_avg_salary),
                'target_average': int(target_avg_salary),
                'potential_increase': round(salary_increase, 2),
                'salary_increase_amount': int(target_avg_salary - current_avg_salary)
            },
            'transition_difficulty': self._assess_transition_difficulty(missing_skills),
            'recommended_learning_path': self._generate_learning_path(missing_skills),
            'estimated_transition_time': self._estimate_transition_time(missing_skills)
        }
        
        return progression_analysis
    
    def _calculate_average_salaries(self, job_data: pd.DataFrame) -> Dict[str, int]:
        """Calculate average salaries by job title"""
        job_data['avg_salary'] = (job_data['salary_min'] + job_data['salary_max']) / 2
        return job_data.groupby('job_title')['avg_salary'].mean().round().astype(int).to_dict()
    
    def _extract_top_skills(self, job_data: pd.DataFrame) -> Dict[str, int]:
        """Extract top skills from job postings"""
        all_skills = []
        
        for skills_string in job_data['required_skills']:
            if pd.notna(skills_string):
                skills = [skill.strip().lower() for skill in skills_string.split(',')]
                all_skills.extend(skills)
        
        from collections import Counter
        skill_counts = Counter(all_skills)
        return dict(skill_counts.most_common(15))
    
    def _get_job_trends(self, job_data: pd.DataFrame) -> Dict[str, int]:
        """Get job posting trends by date"""
        job_data['posted_date'] = pd.to_datetime(job_data['posted_date'])
        weekly_counts = job_data.groupby(job_data['posted_date'].dt.isocalendar().week).size()
        return weekly_counts.to_dict()
    
    def _get_related_skills(self, skill_name: str) -> List[str]:
        """Get related skills for a given skill"""
        skill_name_lower = skill_name.lower()
        
        # Search in skill taxonomy
        for category in self.skill_taxonomy.get('technical_skills', {}).values():
            for skill, details in category.items():
                if skill == skill_name_lower:
                    return details.get('related_skills', [])
        
        # If not found in taxonomy, return empty list
        return []
    
    def _get_experience_salary_comparison(self, job_title: str) -> Dict[str, int]:
        """Get salary comparison across experience levels"""
        title_data = self.salary_data[
            self.salary_data['job_title'].str.contains(job_title, case=False, na=False)
        ]
        
        return title_data.groupby('experience_level')['average_salary'].mean().round().astype(int).to_dict()
    
    def _get_location_salary_comparison(self, job_title: str) -> Dict[str, int]:
        """Get salary comparison across locations"""
        title_data = self.salary_data[
            self.salary_data['job_title'].str.contains(job_title, case=False, na=False)
        ]
        
        return title_data.groupby('location')['average_salary'].mean().round().astype(int).to_dict()
    
    def _extract_skills_from_jobs(self, job_data: pd.DataFrame) -> List[str]:
        """Extract unique skills from job postings"""
        all_skills = []
        for skills_string in job_data['required_skills']:
            if pd.notna(skills_string):
                skills = [skill.strip().lower() for skill in skills_string.split(',')]
                all_skills.extend(skills)
        
        return list(set(all_skills))
    
    def _assess_transition_difficulty(self, missing_skills: List[str]) -> str:
        """Assess the difficulty of career transition based on missing skills"""
        if len(missing_skills) <= 2:
            return 'Easy'
        elif len(missing_skills) <= 5:
            return 'Moderate'
        else:
            return 'Challenging'
    
    def _generate_learning_path(self, missing_skills: List[str]) -> List[Dict[str, Any]]:
        """Generate a learning path for missing skills"""
        learning_path = []
        
        for i, skill in enumerate(missing_skills[:5]):  # Focus on top 5 skills
            learning_item = {
                'skill': skill,
                'priority': i + 1,
                'estimated_time': f"{2 + i} weeks",  # Simple estimation
                'resources': self._get_learning_resources(skill),
                'difficulty': 'Intermediate'  # Default difficulty
            }
            learning_path.append(learning_item)
        
        return learning_path
    
    def _get_learning_resources(self, skill: str) -> List[str]:
        """Get learning resources for a skill"""
        # Search in skill taxonomy
        for category in self.skill_taxonomy.get('technical_skills', {}).values():
            for skill_name, details in category.items():
                if skill_name == skill.lower():
                    return details.get('learning_resources', [])
        
        # Default resources if not found in taxonomy
        return [
            f"Online courses for {skill}",
            f"{skill} documentation and tutorials",
            f"Practice projects using {skill}"
        ]
    
    def _estimate_transition_time(self, missing_skills: List[str]) -> str:
        """Estimate time needed for career transition"""
        num_skills = len(missing_skills)
        
        if num_skills <= 2:
            return "3-6 months"
        elif num_skills <= 5:
            return "6-12 months"
        else:
            return "12-18 months"
    
    def update_job_data(self, new_data: pd.DataFrame):
        """Update job dataset with new data"""
        self.job_data = pd.concat([self.job_data, new_data], ignore_index=True)
        self._save_data_to_files()
    
    def get_market_trends(self) -> Dict[str, Any]:
        """Get current market trends and insights"""
        trends = {
            'trending_skills': self._get_trending_skills(),
            'growing_industries': self._get_growing_industries(),
            'remote_work_percentage': self._calculate_remote_work_percentage(),
            'salary_trends': self._analyze_salary_trends(),
            'job_posting_trends': self._analyze_job_posting_trends()
        }
        
        return trends
    
    def _get_trending_skills(self) -> List[Dict[str, Any]]:
        """Identify trending skills in the market"""
        # This would typically involve time-series analysis of job postings
        # For now, return high-demand skills from our taxonomy
        trending = [
            {'skill': 'machine learning', 'growth_rate': 25, 'demand_score': 0.95},
            {'skill': 'cloud computing', 'growth_rate': 30, 'demand_score': 0.90},
            {'skill': 'data science', 'growth_rate': 20, 'demand_score': 0.92},
            {'skill': 'cybersecurity', 'growth_rate': 28, 'demand_score': 0.88},
            {'skill': 'react', 'growth_rate': 15, 'demand_score': 0.85}
        ]
        
        return trending
    
    def _get_growing_industries(self) -> List[Dict[str, Any]]:
        """Identify growing industries"""
        return [
            {'industry': 'Technology', 'growth_rate': 18, 'job_openings': 2500},
            {'industry': 'Healthcare', 'growth_rate': 22, 'job_openings': 1800},
            {'industry': 'Finance', 'growth_rate': 12, 'job_openings': 1200},
            {'industry': 'Education', 'growth_rate': 15, 'job_openings': 900}
        ]
    
    def _calculate_remote_work_percentage(self) -> float:
        """Calculate percentage of remote work opportunities"""
        remote_jobs = len(self.job_data[self.job_data['employment_type'] == 'Remote'])
        total_jobs = len(self.job_data)
        return round((remote_jobs / total_jobs) * 100, 2) if total_jobs > 0 else 0
    
    def _analyze_salary_trends(self) -> Dict[str, float]:
        """Analyze salary trends across different categories"""
        return {
            'overall_growth': 5.2,  # Percentage growth
            'tech_growth': 8.5,
            'entry_level_growth': 4.8,
            'senior_level_growth': 6.2
        }
    
    def _analyze_job_posting_trends(self) -> Dict[str, int]:
        """Analyze job posting trends over time"""
        # This would involve historical data analysis
        return {
            'this_month': len(self.job_data),
            'last_month': int(len(self.job_data) * 0.85),  # Simulated
            'growth_rate': 15  # Percentage
        }
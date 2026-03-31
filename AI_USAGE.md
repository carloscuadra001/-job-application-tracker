# AI Usage Log

This document tracks key prompts and tools used for AI-related tasks in this project.


## Key Prompts

### Routes
- Build out a Python Flask app with 6 pages (Dashboard, Companies, Jobs, Applications, Contacts, Job Match), MySQL integration, and config file management. Read my_job_tracker.sql for table definitions. No authentication required.
- Add input validation for many NOT NULL fields with client-side and backend validation
- Add full CRUD API endpoints for companies, jobs, applications, and contacts with cascade deletes for foreign key relationships

### Smooth Workflow
- Add a button to companies to the left of +Add New Company that takes you back to Dashboard and cascade the approach down following the hamburger menu order
- Standardize the navigation button set: back with name and arrow, +add in the center, and forward with name and arrow. Make buttons fixed length so they expand edge to edge and wrap on mobile
- Make dashboard tiles clickable links to their respective pages and recent applications clickable to auto-open the edit modal
- Currency increment and decrement should be by $1K and by $5K if held longer

### Meaningful Job Match
- Implement Job Match feature with skill-based job matching algorithm that calculates match percentages and identifies missing skills
- Remove min and max salary from match criteria, replace with desired salary that checks if it falls between the job's min and max
- Fix 100% match when user has fewer years of experience than required — factor experience levels into the match percentage
- Fix 100% false matches for jobs with no requirements by skipping them

### Meaningful Use of JSON Objects
- Implement jobs.requirements as a tag-style skill and experience level input storing JSON arrays of {skill, level} objects
- Implement applications.interview_data as structured interview rounds with round name, date, interviewer, outcome, and notes — with Add Round as local-only and Save & Close to persist
- Update job match to accept [{skill, level}] objects from tag input and show "You: X / Req: Y" experience comparisons in results

## Tools Used
- GitHub Copilot (Claude): Used for code generation, project scaffolding, debugging, and feature implementation.

---
*This file provides a simple record of AI interactions and the models/tools leveraged for project development.*

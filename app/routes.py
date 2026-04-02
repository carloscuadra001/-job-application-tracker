from app import app, mysql
from flask import render_template, request, jsonify
import re
import json
from datetime import datetime

# Validation helper functions
def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_url(url):
    """Validate URL format"""
    pattern = r'^https?://.+'
    return re.match(pattern, url) is not None

def validate_phone(phone):
    """Validate phone number format"""
    pattern = r'^[\d\s\-\+\(\)]{10,}$'
    return re.match(pattern, phone) is not None if phone else True

def validate_salary(salary_str):
    """Validate salary is a valid decimal"""
    try:
        salary = float(salary_str)
        return salary >= 0
    except:
        return False

def format_phone(phone):
    """Format phone number as (XXX) XXX-XXXX"""
    if not phone:
        return phone
    digits = re.sub(r'\D', '', phone)
    if len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    if len(digits) == 11 and digits[0] == '1':
        return f"({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    return phone

# Dashboard
@app.route('/')
def dashboard():
    cursor = mysql.connection.cursor()
    
    # Active applications (not Rejected or Withdrawn)
    cursor.execute("SELECT COUNT(*) FROM applications WHERE status NOT IN ('Rejected', 'Withdrawn')")
    active_apps = cursor.fetchone()[0]
    
    # Companies tracked
    cursor.execute("SELECT COUNT(*) FROM companies")
    total_companies = cursor.fetchone()[0]
    
    # In interviews (status is Interview OR has interview rounds recorded)
    cursor.execute("SELECT COUNT(*) FROM applications WHERE status = 'Interview' OR (interview_data IS NOT NULL AND interview_data != '[]' AND interview_data != '')")
    in_interviews = cursor.fetchone()[0]
    
    # Job offers
    cursor.execute("SELECT COUNT(*) FROM applications WHERE status = 'Offer'")
    job_offers = cursor.fetchone()[0]
    
    # Recent applications (last 5)
    cursor.execute("""
        SELECT a.application_id, j.job_title, c.company_name, a.status, a.application_date
        FROM applications a
        JOIN jobs j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        ORDER BY a.application_date DESC
        LIMIT 5
    """)
    recent_apps = cursor.fetchall()

    # Companies list (names only)
    cursor.execute("SELECT company_id, company_name FROM companies ORDER BY company_name")
    companies_list = cursor.fetchall()

    # Applications list (not Rejected or Withdrawn)
    cursor.execute("""
        SELECT a.application_id, j.job_title, c.company_name
        FROM applications a
        JOIN jobs j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        WHERE a.status NOT IN ('Rejected', 'Withdrawn')
        ORDER BY j.job_title
    """)
    apps_list = cursor.fetchall()

    # Interview list (status Interview or has interview data)
    cursor.execute("""
        SELECT a.application_id, j.job_title, c.company_name
        FROM applications a
        JOIN jobs j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        WHERE a.status = 'Interview' OR (a.interview_data IS NOT NULL AND a.interview_data != '[]' AND a.interview_data != '')
        ORDER BY j.job_title
    """)
    interviews_list = cursor.fetchall()

    # Offers list
    cursor.execute("""
        SELECT a.application_id, j.job_title, c.company_name
        FROM applications a
        JOIN jobs j ON a.job_id = j.job_id
        JOIN companies c ON j.company_id = c.company_id
        WHERE a.status = 'Offer'
        ORDER BY j.job_title
    """)
    offers_list = cursor.fetchall()

    cursor.close()
    
    return render_template('dashboard.html',
        active_apps=active_apps,
        total_companies=total_companies,
        in_interviews=in_interviews,
        job_offers=job_offers,
        recent_apps=recent_apps,
        companies_list=companies_list,
        apps_list=apps_list,
        interviews_list=interviews_list,
        offers_list=offers_list
    )

# Companies routes
@app.route('/companies')
def companies():
    return render_template('companies.html')

@app.route('/api/companies', methods=['GET'])
def get_companies():
    """Get all companies - used for both dropdowns and display"""
    try:
        cursor = mysql.connection.cursor()
        dropdown_mode = request.args.get('dropdown', 'false').lower() == 'true'
        
        if dropdown_mode:
            # Simple list for dropdowns
            cursor.execute("SELECT company_id, company_name FROM companies ORDER BY company_name")
            companies = cursor.fetchall()
            cursor.close()
            return jsonify({
                'success': True,
                'companies': [{'id': c[0], 'name': c[1]} for c in companies]
            }), 200
        else:
            # Full details for display
            cursor.execute("""
                SELECT company_id, company_name, industry, website, city, state, notes, created_at 
                FROM companies 
                ORDER BY company_name
            """)
            companies = cursor.fetchall()
            cursor.close()
            
            companies_list = []
            for c in companies:
                companies_list.append({
                    'id': c[0],
                    'name': c[1],
                    'industry': c[2],
                    'website': c[3],
                    'city': c[4],
                    'state': c[5],
                    'notes': c[6],
                    'created_at': str(c[7]) if c[7] else None
                })
            
            return jsonify({
                'success': True,
                'companies': companies_list
            }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/companies', methods=['POST'])
def add_company():
    """Add a new company with validation"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['company_name', 'industry', 'website', 'city', 'state', 'notes']
        for field in required_fields:
            if not data.get(field) or not str(data.get(field)).strip():
                return jsonify({'success': False, 'error': f'{field.replace("_", " ").title()} is required'}), 400
        
        # Validate URL format
        if data.get('website') and not validate_url(data['website']):
            return jsonify({'success': False, 'error': 'Invalid website URL format. Must start with http:// or https://'}), 400
        
        # Validate string lengths
        if len(data['company_name']) > 100:
            return jsonify({'success': False, 'error': 'Company name must be 100 characters or less'}), 400
        if len(data['industry']) > 50:
            return jsonify({'success': False, 'error': 'Industry must be 50 characters or less'}), 400
        
        cursor = mysql.connection.cursor()
        cursor.execute("""
            INSERT INTO companies (company_name, industry, website, city, state, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data['company_name'].strip(),
            data['industry'].strip(),
            data['website'].strip(),
            data['city'].strip(),
            data['state'].strip(),
            data['notes'].strip()
        ))
        mysql.connection.commit()
        new_id = cursor.lastrowid
        cursor.close()
        
        return jsonify({'success': True, 'message': 'Company added successfully', 'id': new_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/companies/<int:company_id>', methods=['PUT'])
def update_company(company_id):
    """Update an existing company with validation"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['company_name', 'industry', 'website', 'city', 'state', 'notes']
        for field in required_fields:
            if not data.get(field) or not str(data.get(field)).strip():
                return jsonify({'success': False, 'error': f'{field.replace("_", " ").title()} is required'}), 400
        
        # Validate URL format
        if data.get('website') and not validate_url(data['website']):
            return jsonify({'success': False, 'error': 'Invalid website URL format. Must start with http:// or https://'}), 400
        
        # Validate string lengths
        if len(data['company_name']) > 100:
            return jsonify({'success': False, 'error': 'Company name must be 100 characters or less'}), 400
        if len(data['industry']) > 50:
            return jsonify({'success': False, 'error': 'Industry must be 50 characters or less'}), 400
        
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE companies 
            SET company_name = %s, industry = %s, website = %s, city = %s, state = %s, notes = %s
            WHERE company_id = %s
        """, (
            data['company_name'].strip(),
            data['industry'].strip(),
            data['website'].strip(),
            data['city'].strip(),
            data['state'].strip(),
            data['notes'].strip(),
            company_id
        ))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'success': True, 'message': 'Company updated successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/companies/<int:company_id>/jobs')
def get_company_jobs(company_id):
    """Get all jobs for a specific company"""
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT job_id, job_title, job_type, salary_min, salary_max, job_url, date_posted
            FROM jobs WHERE company_id = %s ORDER BY date_posted DESC
        """, (company_id,))
        rows = cursor.fetchall()
        cursor.close()
        jobs = [{'id': r[0], 'title': r[1], 'type': r[2],
                 'salary_min': float(r[3]) if r[3] else 0,
                 'salary_max': float(r[4]) if r[4] else 0,
                 'url': r[5], 'date_posted': str(r[6]) if r[6] else ''} for r in rows]
        return jsonify({'success': True, 'jobs': jobs})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/companies/<int:company_id>', methods=['DELETE'])
def delete_company(company_id):
    """Delete a company and all related records (jobs, applications, contacts)"""
    try:
        cursor = mysql.connection.cursor()
        # Delete applications linked to this company's jobs
        cursor.execute("""
            DELETE a FROM applications a
            JOIN jobs j ON a.job_id = j.job_id
            WHERE j.company_id = %s
        """, (company_id,))
        # Delete jobs linked to this company
        cursor.execute("DELETE FROM jobs WHERE company_id = %s", (company_id,))
        # Delete contacts linked to this company
        cursor.execute("DELETE FROM contacts WHERE company_id = %s", (company_id,))
        # Delete the company itself
        cursor.execute("DELETE FROM companies WHERE company_id = %s", (company_id,))
        mysql.connection.commit()
        cursor.close()
        
        return jsonify({'success': True, 'message': 'Company deleted successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Jobs routes
@app.route('/jobs')
def jobs():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT company_id, company_name, website FROM companies ORDER BY company_name")
        companies = cursor.fetchall()
        companies_list = [{'id': c[0], 'name': c[1], 'website': c[2] or ''} for c in companies]

        cursor.execute("""
            SELECT j.job_id, j.job_title, j.job_type, j.salary_min, j.salary_max,
                   j.job_url, j.date_posted, c.company_name, j.company_id, j.requirements
            FROM jobs j
            JOIN companies c ON j.company_id = c.company_id
            ORDER BY j.date_posted DESC
        """)
        jobs_data = cursor.fetchall()
        cursor.close()
        jobs_list = []
        for j in jobs_data:
            reqs = j[9]
            if reqs and isinstance(reqs, str):
                try:
                    reqs = json.loads(reqs)
                except:
                    reqs = None
            jobs_list.append({
                'id': j[0], 'title': j[1], 'type': j[2],
                'salary_min': j[3], 'salary_max': j[4],
                'url': j[5], 'date_posted': j[6], 'company': j[7],
                'company_id': j[8], 'requirements': reqs or []
            })

        return render_template('jobs.html', companies=companies_list, jobs=jobs_list)
    except Exception as e:
        print(f"Error fetching data: {e}")
        return render_template('jobs.html', companies=[], jobs=[])

@app.route('/api/jobs', methods=['POST'])
def add_job():
    """Add a new job with validation"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['company_id', 'job_title', 'job_type', 'salary_min', 'salary_max', 'job_url', 'date_posted']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'{field.replace("_", " ").title()} is required'}), 400
        
        # Validate company exists
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT company_id FROM companies WHERE company_id = %s", (data['company_id'],))
        if not cursor.fetchone():
            cursor.close()
            return jsonify({'success': False, 'error': 'Selected company does not exist'}), 400
        
        # Validate job type
        valid_job_types = ['Full-time', 'Part-time', 'Contract', 'Internship']
        if data['job_type'] not in valid_job_types:
            cursor.close()
            return jsonify({'success': False, 'error': 'Invalid job type'}), 400
        
        # Validate salaries
        if not validate_salary(data['salary_min']):
            cursor.close()
            return jsonify({'success': False, 'error': 'Minimum salary must be a valid number >= 0'}), 400
        if not validate_salary(data['salary_max']):
            cursor.close()
            return jsonify({'success': False, 'error': 'Maximum salary must be a valid number >= 0'}), 400
        
        salary_min = float(data['salary_min'])
        salary_max = float(data['salary_max'])
        if salary_min > salary_max:
            cursor.close()
            return jsonify({'success': False, 'error': 'Minimum salary cannot be greater than maximum salary'}), 400
        
        # Validate URL
        if not validate_url(data['job_url']):
            cursor.close()
            return jsonify({'success': False, 'error': 'Invalid job URL format. Must start with http:// or https://'}), 400
        
        # Validate date format
        try:
            datetime.strptime(data['date_posted'], '%Y-%m-%d')
        except:
            cursor.close()
            return jsonify({'success': False, 'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        requirements = data.get('requirements', [])
        req_json = json.dumps(requirements) if requirements else None

        cursor.execute("""
            INSERT INTO jobs (company_id, job_title, job_type, salary_min, salary_max, job_url, date_posted, requirements)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['company_id'],
            data['job_title'].strip(),
            data['job_type'],
            salary_min,
            salary_max,
            data['job_url'].strip(),
            data['date_posted'],
            req_json
        ))
        mysql.connection.commit()
        new_id = cursor.lastrowid
        cursor.close()
        
        return jsonify({'success': True, 'message': 'Job added successfully', 'id': new_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/jobs/<int:job_id>', methods=['PUT'])
def update_job(job_id):
    """Update an existing job with validation"""
    try:
        data = request.get_json()

        required_fields = ['company_id', 'job_title', 'job_type', 'salary_min', 'salary_max', 'job_url', 'date_posted']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'{field.replace("_", " ").title()} is required'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT company_id FROM companies WHERE company_id = %s", (data['company_id'],))
        if not cursor.fetchone():
            cursor.close()
            return jsonify({'success': False, 'error': 'Selected company does not exist'}), 400

        valid_job_types = ['Full-time', 'Part-time', 'Contract', 'Internship']
        if data['job_type'] not in valid_job_types:
            cursor.close()
            return jsonify({'success': False, 'error': 'Invalid job type'}), 400

        if not validate_salary(data['salary_min']) or not validate_salary(data['salary_max']):
            cursor.close()
            return jsonify({'success': False, 'error': 'Salary must be a valid number >= 0'}), 400

        salary_min = float(data['salary_min'])
        salary_max = float(data['salary_max'])
        if salary_min > salary_max:
            cursor.close()
            return jsonify({'success': False, 'error': 'Minimum salary cannot be greater than maximum salary'}), 400

        if not validate_url(data['job_url']):
            cursor.close()
            return jsonify({'success': False, 'error': 'Invalid job URL format. Must start with http:// or https://'}), 400

        try:
            datetime.strptime(data['date_posted'], '%Y-%m-%d')
        except:
            cursor.close()
            return jsonify({'success': False, 'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

        requirements = data.get('requirements', [])
        req_json = json.dumps(requirements) if requirements else None

        cursor.execute("""
            UPDATE jobs
            SET company_id = %s, job_title = %s, job_type = %s, salary_min = %s,
                salary_max = %s, job_url = %s, date_posted = %s, requirements = %s
            WHERE job_id = %s
        """, (
            data['company_id'],
            data['job_title'].strip(),
            data['job_type'],
            salary_min,
            salary_max,
            data['job_url'].strip(),
            data['date_posted'],
            req_json,
            job_id
        ))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'success': True, 'message': 'Job updated successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/jobs/<int:job_id>', methods=['DELETE'])
def delete_job(job_id):
    """Delete a job and its applications"""
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM applications WHERE job_id = %s", (job_id,))
        cursor.execute("DELETE FROM jobs WHERE job_id = %s", (job_id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'success': True, 'message': 'Job deleted successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Applications routes
@app.route('/applications')
def applications():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT job_id, job_title, company_name FROM jobs JOIN companies ON jobs.company_id = companies.company_id ORDER BY job_title")
        jobs_data = cursor.fetchall()
        jobs_list = [{'id': j[0], 'title': j[1], 'company': j[2]} for j in jobs_data]

        cursor.execute("""
            SELECT a.application_id, a.application_date, a.status, a.resume_version,
                   a.cover_letter_sent, a.interview_data, j.job_title, c.company_name, a.job_id,
                   j.requirements, c.company_id
            FROM applications a
            JOIN jobs j ON a.job_id = j.job_id
            JOIN companies c ON j.company_id = c.company_id
            ORDER BY a.application_date DESC
        """)
        apps_data = cursor.fetchall()
        cursor.close()
        apps_list = []
        for a in apps_data:
            idata = a[5]
            if idata and isinstance(idata, str):
                try:
                    idata = json.loads(idata)
                except:
                    idata = None
            # Handle both old format (plain array) and new format (object)
            if isinstance(idata, list):
                interviews = idata
                skills_on_resume = []
            elif isinstance(idata, dict):
                interviews = idata.get('interviews', [])
                skills_on_resume = idata.get('skills_on_resume', [])
            else:
                interviews = []
                skills_on_resume = []

            # Parse job requirements for match calculation
            reqs = a[9]
            if reqs and isinstance(reqs, str):
                try:
                    reqs = json.loads(reqs)
                except:
                    reqs = []
            job_req_skills = {}
            if isinstance(reqs, list):
                for r in reqs:
                    if isinstance(r, dict) and r.get('skill'):
                        job_req_skills[r['skill'].strip().lower()] = r.get('level', '')
                    elif isinstance(r, str) and r.strip():
                        job_req_skills[r.strip().lower()] = ''

            # Build resume skills dict {name_lower: level}
            resume_skills = {}
            for s in skills_on_resume:
                if isinstance(s, dict) and s.get('skill'):
                    resume_skills[s['skill'].strip().lower()] = s.get('level', '')
                elif isinstance(s, str) and s.strip():
                    resume_skills[s.strip().lower()] = ''

            if job_req_skills and resume_skills:
                import re as _re
                def _parse_yrs(level_str):
                    if not level_str:
                        return 0
                    m = _re.search(r'(\d+)', str(level_str))
                    return int(m.group(1)) if m else 0

                total_score = 0
                for req_skill, req_level in job_req_skills.items():
                    if req_skill in resume_skills:
                        user_yrs = _parse_yrs(resume_skills[req_skill])
                        job_yrs = _parse_yrs(req_level)
                        if job_yrs > 0 and user_yrs > 0:
                            total_score += min(user_yrs / job_yrs, 1.0)
                        else:
                            total_score += 1.0
                match_pct = int((total_score / len(job_req_skills)) * 100)
            else:
                match_pct = None

            apps_list.append({
                'id': a[0], 'date': a[1], 'status': a[2],
                'resume_version': a[3], 'cover_letter': a[4],
                'interviews': interviews, 'skills_on_resume': skills_on_resume,
                'job_title': a[6], 'company': a[7], 'job_id': a[8],
                'match_pct': match_pct, 'company_id': a[10]
            })

        # Sort by latest interview date (most recent first), apps with no interviews last
        def _latest_interview_date(app):
            dates = [iv.get('date', '') for iv in app['interviews'] if iv.get('date')]
            return max(dates) if dates else ''
        apps_list.sort(key=_latest_interview_date, reverse=True)

        return render_template('applications.html', jobs=jobs_list, applications=apps_list)
    except Exception as e:
        print(f"Error fetching applications: {e}")
        return render_template('applications.html', jobs=[], applications=[])

@app.route('/api/applications', methods=['POST'])
def add_application():
    """Add a new application with validation"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['job_id', 'application_date', 'resume_version']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'{field.replace("_", " ").title()} is required'}), 400
        
        # Validate job exists
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT job_id FROM jobs WHERE job_id = %s", (data['job_id'],))
        if not cursor.fetchone():
            cursor.close()
            return jsonify({'success': False, 'error': 'Selected job does not exist'}), 400
        
        # Validate date format
        try:
            datetime.strptime(data['application_date'], '%Y-%m-%d')
        except:
            cursor.close()
            return jsonify({'success': False, 'error': 'Invalid date format. Use YYYY-MM-DD'}), 400
        
        # Validate status if provided
        if data.get('status'):
            valid_statuses = ['Applied', 'Screening', 'Interview', 'Offer', 'Rejected', 'Withdrawn']
            if data['status'] not in valid_statuses:
                cursor.close()
                return jsonify({'success': False, 'error': 'Invalid application status'}), 400
        
        cover_letter = 1 if data.get('cover_letter_sent') else 0

        skills_on_resume = data.get('skills_on_resume', [])
        interview_json = json.dumps({'interviews': [], 'skills_on_resume': skills_on_resume})

        cursor.execute("""
            INSERT INTO applications (job_id, application_date, status, resume_version, cover_letter_sent, interview_data)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data['job_id'],
            data['application_date'],
            data.get('status'),
            data['resume_version'].strip(),
            cover_letter,
            interview_json
        ))
        mysql.connection.commit()
        new_id = cursor.lastrowid
        cursor.close()
        
        return jsonify({'success': True, 'message': 'Application logged successfully', 'id': new_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/applications/<int:app_id>', methods=['PUT'])
def update_application(app_id):
    """Update an existing application"""
    try:
        data = request.get_json()

        required_fields = ['job_id', 'application_date', 'resume_version']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'{field.replace("_", " ").title()} is required'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT job_id FROM jobs WHERE job_id = %s", (data['job_id'],))
        if not cursor.fetchone():
            cursor.close()
            return jsonify({'success': False, 'error': 'Selected job does not exist'}), 400

        try:
            datetime.strptime(data['application_date'], '%Y-%m-%d')
        except:
            cursor.close()
            return jsonify({'success': False, 'error': 'Invalid date format. Use YYYY-MM-DD'}), 400

        if data.get('status'):
            valid_statuses = ['Applied', 'Screening', 'Interview', 'Offer', 'Rejected', 'Withdrawn']
            if data['status'] not in valid_statuses:
                cursor.close()
                return jsonify({'success': False, 'error': 'Invalid application status'}), 400

        cover_letter = 1 if data.get('cover_letter_sent') else 0

        # Preserve existing interviews, update skills_on_resume
        cursor.execute("SELECT interview_data FROM applications WHERE application_id = %s", (app_id,))
        row = cursor.fetchone()
        existing = {}
        if row and row[0]:
            try:
                parsed = json.loads(row[0]) if isinstance(row[0], str) else row[0]
                if isinstance(parsed, dict):
                    existing = parsed
                elif isinstance(parsed, list):
                    existing = {'interviews': parsed}
            except:
                pass
        existing['skills_on_resume'] = data.get('skills_on_resume', existing.get('skills_on_resume', []))

        cursor.execute("""
            UPDATE applications SET job_id=%s, application_date=%s, status=%s,
                   resume_version=%s, cover_letter_sent=%s, interview_data=%s
            WHERE application_id=%s
        """, (
            data['job_id'],
            data['application_date'],
            data.get('status'),
            data['resume_version'].strip(),
            cover_letter,
            json.dumps(existing),
            app_id
        ))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'success': True, 'message': 'Application updated successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/applications/<int:app_id>', methods=['DELETE'])
def delete_application(app_id):
    """Delete an application"""
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM applications WHERE application_id = %s", (app_id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'success': True, 'message': 'Application deleted successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/applications/<int:app_id>/interviews', methods=['PUT'])
def update_interviews(app_id):
    """Update interview data for an application"""
    try:
        data = request.get_json()
        interviews = data.get('interviews', [])

        # Validate each interview round
        valid_types = ['Phone Screen', 'Technical', 'Behavioral', 'Onsite', 'Final', 'Other']
        valid_outcomes = ['Pending', 'Pass', 'Fail']
        for r in interviews:
            if not isinstance(r, dict):
                return jsonify({'success': False, 'error': 'Invalid interview round format'}), 400
            if r.get('round') and r['round'] not in valid_types:
                return jsonify({'success': False, 'error': f'Invalid round type: {r["round"]}'}), 400
            if r.get('outcome') and r['outcome'] not in valid_outcomes:
                return jsonify({'success': False, 'error': f'Invalid outcome: {r["outcome"]}'}), 400

        # Preserve skills_on_resume when saving interviews
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT interview_data FROM applications WHERE application_id = %s", (app_id,))
        row = cursor.fetchone()
        existing_skills = []
        if row and row[0]:
            try:
                parsed = json.loads(row[0]) if isinstance(row[0], str) else row[0]
                if isinstance(parsed, dict):
                    existing_skills = parsed.get('skills_on_resume', [])
            except:
                pass

        interview_obj = json.dumps({'interviews': interviews, 'skills_on_resume': existing_skills})
        cursor.execute("""
            UPDATE applications SET interview_data = %s WHERE application_id = %s
        """, (interview_obj, app_id))

        # Auto-update status to Offer if Final round passed
        if any(r.get('round') == 'Final' and r.get('outcome') == 'Pass' for r in interviews):
            cursor.execute("UPDATE applications SET status = 'Offer' WHERE application_id = %s", (app_id,))

        mysql.connection.commit()
        cursor.close()

        return jsonify({'success': True, 'message': 'Interview data updated successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Contacts routes
@app.route('/api/contacts/company/<int:company_id>')
def get_contacts_by_company(company_id):
    """Get all contacts for a specific company"""
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT contact_id, contact_name, title
            FROM contacts
            WHERE company_id = %s
            ORDER BY contact_name
        """, (company_id,))
        rows = cursor.fetchall()
        cursor.close()
        contacts_list = [{'id': r[0], 'name': r[1], 'title': r[2] or ''} for r in rows]
        return jsonify({'success': True, 'contacts': contacts_list})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/contacts')
def contacts():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT company_id, company_name FROM companies ORDER BY company_name")
        companies = cursor.fetchall()
        companies_list = [{'id': c[0], 'name': c[1]} for c in companies]

        cursor.execute("""
            SELECT c.contact_id, c.contact_name, c.title, c.email, c.phone,
                   c.linkedin_url, c.notes, co.company_name, c.company_id
            FROM contacts c
            JOIN companies co ON c.company_id = co.company_id
            ORDER BY c.contact_name
        """)
        contacts_rows = cursor.fetchall()
        cursor.close()
        contacts_list = [{
            'id': r[0], 'name': r[1], 'title': r[2], 'email': r[3],
            'phone': format_phone(r[4]), 'linkedin_url': r[5], 'notes': r[6],
            'company': r[7], 'company_id': r[8]
        } for r in contacts_rows]

        return render_template('contacts.html', companies=companies_list, contacts=contacts_list)
    except Exception as e:
        print(f"Error fetching contacts: {e}")
        return render_template('contacts.html', companies=[], contacts=[])

@app.route('/api/contacts', methods=['POST'])
def add_contact():
    """Add a new contact with validation"""
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data.get('company_id') or not data.get('contact_name'):
            return jsonify({'success': False, 'error': 'Company and Contact Name are required'}), 400
        
        # Validate company exists
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT company_id FROM companies WHERE company_id = %s", (data['company_id'],))
        if not cursor.fetchone():
            cursor.close()
            return jsonify({'success': False, 'error': 'Selected company does not exist'}), 400
        
        # Validate email if provided
        if data.get('email') and not validate_email(data['email']):
            cursor.close()
            return jsonify({'success': False, 'error': 'Invalid email format'}), 400
        
        # Validate phone if provided
        if data.get('phone') and not validate_phone(data['phone']):
            cursor.close()
            return jsonify({'success': False, 'error': 'Invalid phone format'}), 400
        
        # Validate LinkedIn URL if provided
        if data.get('linkedin_url') and not validate_url(data['linkedin_url']):
            cursor.close()
            return jsonify({'success': False, 'error': 'Invalid LinkedIn URL format'}), 400
        
        cursor.execute("""
            INSERT INTO contacts (company_id, contact_name, title, email, phone, linkedin_url, notes)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data['company_id'],
            data['contact_name'].strip(),
            data.get('title', '').strip() if data.get('title') else None,
            data.get('email', '').strip() if data.get('email') else None,
            data.get('phone', '').strip() if data.get('phone') else None,
            data.get('linkedin_url', '').strip() if data.get('linkedin_url') else None,
            data.get('notes', '').strip() if data.get('notes') else None
        ))
        mysql.connection.commit()
        new_id = cursor.lastrowid
        cursor.close()
        
        return jsonify({'success': True, 'message': 'Contact added successfully', 'id': new_id}), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/contacts/<int:contact_id>', methods=['PUT'])
def update_contact(contact_id):
    """Update an existing contact"""
    try:
        data = request.get_json()

        if not data.get('company_id') or not data.get('contact_name'):
            return jsonify({'success': False, 'error': 'Company and Contact Name are required'}), 400

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT company_id FROM companies WHERE company_id = %s", (data['company_id'],))
        if not cursor.fetchone():
            cursor.close()
            return jsonify({'success': False, 'error': 'Selected company does not exist'}), 400

        if data.get('email') and not validate_email(data['email']):
            cursor.close()
            return jsonify({'success': False, 'error': 'Invalid email format'}), 400

        if data.get('phone') and not validate_phone(data['phone']):
            cursor.close()
            return jsonify({'success': False, 'error': 'Invalid phone format'}), 400

        if data.get('linkedin_url') and not validate_url(data['linkedin_url']):
            cursor.close()
            return jsonify({'success': False, 'error': 'Invalid LinkedIn URL format'}), 400

        cursor.execute("""
            UPDATE contacts SET company_id=%s, contact_name=%s, title=%s, email=%s,
                   phone=%s, linkedin_url=%s, notes=%s
            WHERE contact_id=%s
        """, (
            data['company_id'],
            data['contact_name'].strip(),
            data.get('title', '').strip() if data.get('title') else None,
            data.get('email', '').strip() if data.get('email') else None,
            data.get('phone', '').strip() if data.get('phone') else None,
            data.get('linkedin_url', '').strip() if data.get('linkedin_url') else None,
            data.get('notes', '').strip() if data.get('notes') else None,
            contact_id
        ))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'success': True, 'message': 'Contact updated successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/contacts/<int:contact_id>', methods=['DELETE'])
def delete_contact(contact_id):
    """Delete a contact"""
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("DELETE FROM contacts WHERE contact_id = %s", (contact_id,))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'success': True, 'message': 'Contact deleted successfully'}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Job Match route
@app.route('/job_match')
def job_match():
    return render_template('job_match.html')

@app.route('/api/job-skills')
def job_skills():
    """Return unique skills from all job requirements"""
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT requirements FROM jobs WHERE requirements IS NOT NULL")
        rows = cursor.fetchall()
        cursor.close()
        skills = set()
        for (req,) in rows:
            if req:
                try:
                    data = json.loads(req) if isinstance(req, str) else req
                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict) and 'skill' in item:
                                skills.add(item['skill'].strip())
                except:
                    pass
        return jsonify({'success': True, 'skills': sorted(skills, key=str.lower)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/industries')
def industries():
    """Return unique industries from companies"""
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT DISTINCT industry FROM companies WHERE industry IS NOT NULL AND industry != '' ORDER BY industry")
        rows = cursor.fetchall()
        cursor.close()
        return jsonify({'success': True, 'industries': [r[0] for r in rows]})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/job-match', methods=['POST'])
def job_match_search():
    """Match user skills against job requirements"""
    try:
        data = request.get_json()
        
        # Parse user skills (accepts array of {skill, level} or comma-separated string)
        skills_input = data.get('skills', '')
        user_skills = {}  # {skill_name_lower: level}
        if isinstance(skills_input, list):
            for item in skills_input:
                if isinstance(item, dict) and item.get('skill'):
                    user_skills[item['skill'].strip().lower()] = item.get('level', '')
                elif isinstance(item, str) and item.strip():
                    user_skills[item.strip().lower()] = ''
        elif isinstance(skills_input, str) and skills_input.strip():
            for skill in skills_input.split(','):
                skill = skill.strip().lower()
                if skill:
                    user_skills[skill] = ''
        
        if not user_skills:
            return jsonify({'success': False, 'error': 'Please enter at least one skill'}), 400
        
        # Get filter criteria
        desired_salary = data.get('desired_salary')
        job_type = data.get('job_type')
        industry = data.get('industry', '').strip().lower()
        
        cursor = mysql.connection.cursor()
        
        # Build query to get all jobs
        query = """
            SELECT j.job_id, j.job_title, j.salary_min, j.salary_max, j.job_type, 
                   j.requirements, c.company_name, c.industry
            FROM jobs j
            JOIN companies c ON j.company_id = c.company_id
            WHERE 1=1
        """
        params = []
        
        # Apply filters - desired salary must be <= job's max salary
        if desired_salary:
            try:
                query += " AND j.salary_max >= %s"
                sal = float(desired_salary)
                params.append(sal)
            except:
                pass
        
        if job_type and job_type != 'Any':
            query += " AND j.job_type = %s"
            params.append(job_type)
        
        cursor.execute(query, params)
        jobs = cursor.fetchall()
        cursor.close()
        
        # Calculate matches
        matches = []
        user_skill_names = set(user_skills.keys())
        
        for job in jobs:
            job_id, job_title, salary_min, salary_max, job_type_val, requirements, company_name, job_industry = job
            
            # Parse job requirements {skill_name_lower: level}
            job_skills = {}
            if requirements:
                try:
                    req_data = json.loads(requirements) if isinstance(requirements, str) else requirements
                    if isinstance(req_data, list):
                        for item in req_data:
                            if isinstance(item, dict) and 'skill' in item:
                                job_skills[item['skill'].strip().lower()] = item.get('level', '')
                            elif isinstance(item, str) and item.strip():
                                job_skills[item.strip().lower()] = ''
                    elif isinstance(req_data, dict) and 'skills' in req_data:
                        for skill in req_data['skills']:
                            if skill:
                                job_skills[skill.strip().lower()] = ''
                except:
                    pass
            
            job_skill_names = set(job_skills.keys())
            
            # Skip jobs with no requirements - cannot determine a match
            if not job_skill_names:
                continue
            
            # Calculate match - factor in experience levels
            matched = user_skill_names & job_skill_names
            missing = job_skill_names - user_skill_names

            def parse_years(level_str):
                """Extract numeric years from level string like '3+ years'"""
                if not level_str:
                    return 0
                import re as _re
                m = _re.search(r'(\d+)', str(level_str))
                return int(m.group(1)) if m else 0

            matching_skills = []
            total_score = 0
            for s in matched:
                user_yrs = parse_years(user_skills[s])
                job_yrs = parse_years(job_skills[s])
                # Score: ratio of user experience to required, capped at 1.0
                if job_yrs > 0 and user_yrs > 0:
                    skill_score = min(user_yrs / job_yrs, 1.0)
                else:
                    skill_score = 1.0  # No level specified = full credit
                total_score += skill_score
                matching_skills.append({'skill': s, 'user_level': user_skills[s], 'job_level': job_skills[s]})

            missing_skills = [{'skill': s, 'job_level': job_skills[s]} for s in missing]
            # Each skill worth equal weight; missing skills score 0
            match_percent = int((total_score / len(job_skill_names)) * 100)
            
            # Apply industry filter if specified
            if industry and industry not in job_industry.lower():
                match_percent = 0
            
            if match_percent > 0:  # Only include jobs with some match
                matches.append({
                    'job_id': job_id,
                    'job_title': job_title,
                    'company_name': company_name,
                    'industry': job_industry,
                    'salary_min': float(salary_min) if salary_min else 0,
                    'salary_max': float(salary_max) if salary_max else 0,
                    'job_type': job_type_val,
                    'match_percent': match_percent,
                    'matching_skills': matching_skills,
                    'missing_skills': missing_skills,
                    'total_required': len(job_skill_names)
                })
        
        # Sort by match percentage (descending)
        matches.sort(key=lambda x: x['match_percent'], reverse=True)
        
        return jsonify({
            'success': True,
            'user_skills': [{'skill': k, 'level': v} for k, v in sorted(user_skills.items())],
            'matches': matches,
            'total_matches': len(matches)
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

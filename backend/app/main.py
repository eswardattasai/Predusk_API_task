from typing import Optional
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select, or_
from .database import init_db, get_session
from .models import Profile, Links, Education, Skill, Project, WorkExperience
from .auth import require_write
app = FastAPI(title="Me-API Playground", version="1.2 (CRUD complete)")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
@app.on_event("startup")
def startup(): init_db()
@app.get("/api/v1/health")
def health(): return {"status":"ok"}
# READ profile (denormalized)
@app.get("/api/v1/profile")
def get_profile(session: Session = Depends(get_session)):
    p = session.exec(select(Profile)).first()
    if not p: raise HTTPException(404, "Profile not found. Seed the database.")
    links = session.exec(select(Links).where(Links.profile_id==p.id)).first()
    edus = session.exec(select(Education).where(Education.profile_id==p.id)).all()
    skills = session.exec(select(Skill).where(Skill.profile_id==p.id)).all()
    projects = session.exec(select(Project).where(Project.profile_id==p.id)).all()
    work = session.exec(select(WorkExperience).where(WorkExperience.profile_id==p.id)).all()
    return {"profile": p.dict(), "links": links.dict() if links else None,
            "educations": [e.dict() for e in edus], "skills": [s.dict() for s in skills],
            "projects": [pr.dict() for pr in projects], "work_experiences": [w.dict() for w in work]}
# CREATE profile
@app.post("/api/v1/profile", dependencies=[Depends(require_write)])
def create_profile(profile: Profile, session: Session = Depends(get_session)):
    existing = session.exec(select(Profile)).first()
    #if existing: raise HTTPException(400, "Profile already exists — use PUT to update instead.")
    session.add(profile); session.commit(); session.refresh(profile); return profile
# UPDATE profile
@app.put("/api/v1/profile/{profile_id}", dependencies=[Depends(require_write)])
def update_profile(profile_id:int, payload:Profile, session:Session=Depends(get_session)):
    p = session.get(Profile, profile_id)
    if not p: raise HTTPException(404, "Profile not found")
    for k,v in payload.dict(exclude_unset=True).items(): setattr(p,k,v)
    session.add(p); session.commit(); session.refresh(p); return p
# DELETE profile (and all related via ON DELETE CASCADE if configured; here we'll do manual cleanup)
@app.delete("/api/v1/profile/{profile_id}", dependencies=[Depends(require_write)])
def delete_profile(profile_id:int, session:Session=Depends(get_session)):
    p = session.get(Profile, profile_id)
    if not p: raise HTTPException(404, "Profile not found")
    # manual cleanup
    for model in (Links, Education, Skill, Project, WorkExperience):
        for row in session.exec(select(model).where(getattr(model, "profile_id")==profile_id)).all():
            session.delete(row)
    session.delete(p); session.commit(); return {"deleted": profile_id}
# Utility: paginate
def paginate(q, page:int, limit:int, session:Session):
    total = len(session.exec(q).all())
    items = session.exec(q.offset((page-1)*limit).limit(limit)).all()
    return {"total": total, "page": page, "limit": limit, "items": items}
# Skills CRUD
@app.get("/api/v1/skills")
def list_skills(page:int=1, limit:int=100, session:Session=Depends(get_session)):
    q = select(Skill).order_by(Skill.level.desc(), Skill.name.asc())
    data = paginate(q, page, limit, session); data["items"]=[s.dict() for s in data["items"]]; return data
@app.post("/api/v1/skills", dependencies=[Depends(require_write)])
def create_skill(skill:Skill, session:Session=Depends(get_session)):
    session.add(skill); session.commit(); session.refresh(skill); return skill
@app.delete("/api/v1/skills/{skill_id}", dependencies=[Depends(require_write)])
def delete_skill(skill_id:int, session:Session=Depends(get_session)):
    s = session.get(Skill, skill_id); 
    if not s: raise HTTPException(404, "Skill not found")
    session.delete(s); session.commit(); return {"deleted": skill_id}
# Projects CRUD + filter
@app.get("/api/v1/projects")
def list_projects(skill: Optional[str]=None, page:int=1, limit:int=50, session:Session=Depends(get_session)):
    q = select(Project)
    if skill:
        q = q.where(Project.profile_id.in_(select(Skill.profile_id).where(Skill.name.ilike(f"%{skill}%"))))
    data = paginate(q, page, limit, session); data["items"]=[p.dict() for p in data["items"]]; return data
@app.post("/api/v1/projects", dependencies=[Depends(require_write)])
def create_project(project:Project, session:Session=Depends(get_session)):
    session.add(project); session.commit(); session.refresh(project); return project
@app.put("/api/v1/projects/{project_id}", dependencies=[Depends(require_write)])
def update_project(project_id:int, payload:Project, session:Session=Depends(get_session)):
    p = session.get(Project, project_id); 
    if not p: raise HTTPException(404, "Project not found")
    for k,v in payload.dict(exclude_unset=True).items(): setattr(p,k,v)
    session.add(p); session.commit(); session.refresh(p); return p
@app.delete("/api/v1/projects/{project_id}", dependencies=[Depends(require_write)])
def delete_project(project_id:int, session:Session=Depends(get_session)):
    p = session.get(Project, project_id); 
    if not p: raise HTTPException(404, "Project not found")
    session.delete(p); session.commit(); return {"deleted": project_id}
# Education
@app.post("/api/v1/education", dependencies=[Depends(require_write)])
def create_education(education:Education, session:Session=Depends(get_session)):
    session.add(education); session.commit(); session.refresh(education); return education
@app.delete("/api/v1/education/{edu_id}", dependencies=[Depends(require_write)])
def delete_education(edu_id:int, session:Session=Depends(get_session)):
    e = session.get(Education, edu_id); 
    if not e: raise HTTPException(404, "Education not found")
    session.delete(e); session.commit(); return {"deleted": edu_id}
# Work
@app.post("/api/v1/work", dependencies=[Depends(require_write)])
def create_work(work:WorkExperience, session:Session=Depends(get_session)):
    session.add(work); session.commit(); session.refresh(work); return work
@app.put("/api/v1/work/{work_id}", dependencies=[Depends(require_write)])
def update_work(work_id:int, payload:WorkExperience, session:Session=Depends(get_session)):
    w = session.get(WorkExperience, work_id); 
    if not w: raise HTTPException(404, "Work not found")
    for k,v in payload.dict(exclude_unset=True).items(): setattr(w,k,v)
    session.add(w); session.commit(); session.refresh(w); return w
@app.delete("/api/v1/work/{work_id}", dependencies=[Depends(require_write)])
def delete_work(work_id:int, session:Session=Depends(get_session)):
    w = session.get(WorkExperience, work_id); 
    if not w: raise HTTPException(404, "Work not found")
    session.delete(w); session.commit(); return {"deleted": work_id}
# Search + top skills
@app.get("/api/v1/search",)
def search(q:str=Query(..., min_length=1), session:Session=Depends(get_session)):
    like = f"%{q}%"
    projects = session.exec(select(Project).where(or_(Project.skills.like(f'%{q}%'), Project.description.ilike(like)))).all()
    skill = session.exec(select(Skill).where(Skill.name.ilike(like))).all()
    return {"q": q, "projects":[p.dict() for p in projects], "skills":[s.dict() for s in skill]}
@app.get("/api/v1/skills/top")
def top_skills(limit:int=5, session:Session=Depends(get_session)):
    skills = session.exec(select(Skill).order_by(Skill.level.desc()).limit(limit)).all()
    return [s.dict() for s in skills]

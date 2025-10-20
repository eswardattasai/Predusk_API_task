from sqlmodel import Session, select
from .database import engine, init_db
from .models import Profile, Links, Education, Skill, Project, WorkExperience
def run():
    init_db()
    with Session(engine) as s:
        if s.exec(select(Profile)).first(): return
        me = Profile(
            name="Uma Eswar Datta Sai",
            email="be23b030@smail.iitm.ac.in",
            work_summary=("B.Tech Biological Engineering student at IIT Madras (CGPA 8.54/10) "
                          "with strong programming experience (C++/Python, DSA, ML/DL) and hands-on "
                          "projects across fintech, bioinformatics, blockchain, and web apps."),
            portfolio=""
        )
        s.add(me); s.commit(); s.refresh(me)
        s.add(Links(profile_id=me.id, github="https://github.com/eswardattasai",
                    linkedin="https://www.linkedin.com/in/k-eswar-datta-sai-371690264/",
                    codeforces="https://codeforces.com/profile/dattasai25"))
        s.add_all([
            Education(profile_id=me.id, school="Indian Institute of Technology Madras",
                      degree="B.Tech in Biological Engineering", start_year=2023, end_year=2027, score="8.54/10"),
            Education(profile_id=me.id, school="Narayana Junior College, Hyderabad",
                      degree="XI + XII (TS State Board)", start_year=2021, end_year=2022, score="98.5%"),
            Education(profile_id=me.id, school="Pragati Vidyaniketan, Hyderabad",
                      degree="X (TS State Board)", start_year=2019, end_year=2020, score="10/10"),
        ])
        skills=[("c++",4),("c",3),("python",5),("html",3),("css",3),("javascript",3),("react",3),
                ("node.js",3),("express.js",3),("mongodb",3),("git",4),("github",4),("postman",3),
                ("matlab",2),("gnu octave",2),("data structures & algorithms",4),
                ("competitive programming",3),("solidity",2),("hardhat",2),("web3",2),
                ("machine learning",3),("statistics",3)]
        s.add_all([Skill(profile_id=me.id, name=n, level=l) for n,l in skills])
        gh="https://github.com/eswardattasai"
        
        s.add_all([
            Project(profile_id=me.id, title="CredOpt",
                    description="Platform that boosted user savings by 13%...",
                    links=gh,
                    skills=["python", "fastapi", "react"]),

            Project(profile_id=me.id, title="Smart SplitZ",
                    description="Decentralized app to split bills (Solidity/Hardhat/Web3).",
                    links=gh,
                    skills=["solidity", "hardhat", "web3", "javascript"]),

            Project(profile_id=me.id, title="ECmarker (course project)",
                    description="ML/DL biomarkers for Hypertension Nephropathy.",
                    links=gh,
                    skills=["python", "pandas", "machine learning"]),

            Project(profile_id=me.id, title="Drug Microbiome Index",
                    description="GMB index on 50k+ profiles; LASSO feature selection.",
                    links=gh,
                    skills=["python", "biostatistics", "data analysis"]),

            Project(profile_id=me.id, title="Movie Database App",
                    description="React PWA with offline pre-caching.",
                    links=gh,
                    skills=["react", "javascript", "frontend"])
])

        s.add_all([
            WorkExperience(profile_id=me.id, company="CFI Biotech Club, IIT Madras", title="Team Head",
                           description="Led 35-member team; 3.5L+ budget; 11 projects."),
            WorkExperience(profile_id=me.id, company="CFI Biotech Club, IIT Madras", title="Coordinator",
                           description="Ran 5+ events; taught in CFI summer school; Best club '24.")
        ])
        s.commit()
if __name__ == "__main__": run()

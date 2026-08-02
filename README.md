<h2>Interview Preparation</h2>

This repository contains resources to prepare for technical interviews. You will find common algorithms,
well known data structures, and some coding questions found through websites like careerup.

<h2>Development</h2>

Run the whole stack with `docker compose up` — the app is served on
http://localhost:3100 and the api on http://localhost:8001.

The content under `knowledge/` (coding questions + lessons) is compiled into
static JSON under `app/public/data/` (gitignored) by `backend/build_content.py`.
The api container runs it on boot; after editing `knowledge/`, regenerate with:

```
docker compose exec api python build_content.py
```

It only needs the stdlib, so it also runs on the host without a container:

```
CONTENT_OUT=app/public/data python3 backend/build_content.py
```

The database ETL (`docker compose exec api python etl.py`) loads the same
content into SQLite and is still what the api serves today.

<h2>Other Ressources</h2>

Coding challenges:
- [leetcode](https://leetcode.com/discuss/compensation/?currentPage=1&orderBy=recent_activity&query=)

Salaries:
- [Google-T5-Engineering-Offer-Review](https://www.teamblind.com/article/Google-T5-Engineering-Offer-Review-xGCadF2r)
- [levels.fyi](https://www.levels.fyi/trajectory.html)

List of questions to ask during the interview process:
- [Questions I'm asking in interviews
](http://jvns.ca/blog/2013/12/30/questions-im-asking-in-interviews/) by Julia Evans

Salary negociation:
- [Ten Rules for Negotiating a Job Offer
](https://medium.freecodecamp.com/ten-rules-for-negotiating-a-job-offer-ee17cccbdab6#.jdrwp2umb) by [Haseeb Qureshi](http://haseebq.com/)
- [Salary Negotiation: how not to set a bunch of money on fire](https://medium.freecodecamp.com/salary-negotiation-how-not-to-set-a-bunch-of-money-on-fire-605aabbaf84b#.i52wufqnq) by [Quincy Larson](https://medium.freecodecamp.com/@quincylarson)
- [Salaries Analysis](http://serebryakov.info/h1b/) - Source from Visa sponsoring.

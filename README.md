<h2>Interview Preparation</h2>

This repository contains resources to prepare for technical interviews. You will find common algorithms,
well known data structures, and some coding questions found through websites like careerup.

<h2>Running the trainer app</h2>

```
docker compose up
```

The frontend is on http://localhost:3000 and the API on http://localhost:8000
(override with `APP_PORT` / `API_PORT`).

The knowledge content (coding questions + lessons) is served as static JSON from
`app/public/data/`, generated from `knowledge/` by `backend/build_content.py`.
The api container builds it on boot; re-run it after editing `knowledge/`:

```
docker compose exec api python build_content.py
```

It only needs the standard library, so it also runs on the host:

```
CONTENT_OUT=app/public/data python3 backend/build_content.py
```

<h3>Browser identity</h3>

Each browser gets a `user_id` on first load: the app generates a UUID with
`crypto.randomUUID()` and stores it in a `user_id` cookie (`path=/`,
`SameSite=Lax`, one-year max-age, `Secure` only over HTTPS, and readable from
JavaScript — the frontend writes it). Because the API is same-origin, the
browser sends it with every request on its own; no API call site passes it. The
server resolves it in exactly one place, `current_user()` in `backend/user.py`,
which validates the UUID shape and answers **400** if the cookie is missing or
malformed.

**This is not authentication and there is no recovery path.** The id is minted
by the client and never verified, so anyone can set the cookie to another value
and read that state. Clear your cookies, switch browser, or open a private
window, and you get a brand-new identity — the old state still exists on the
server, and nothing can prove it was yours or hand it back.

The SQLite database on the server holds only user state (saved code, test runs,
timed attempts); the content is never stored in it. The browser builds its own
in-memory SQLite (sql.js) over the generated JSON and answers search, filtering,
pagination, the curriculum roll-ups and the stats page from it — no request per
keystroke. The WASM build is vendored at `app/public/sql-wasm.wasm`; refresh it
after upgrading the dependency:

```
cp app/node_modules/sql.js/dist/sql-wasm.wasm app/public/sql-wasm.wasm
```

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

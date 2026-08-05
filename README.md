<h2>Interview Preparation</h2>

This repository contains resources to prepare for technical interviews. You will find common algorithms,
well known data structures, and some coding questions found through websites like careerup.

<h2>Running the trainer app</h2>

```
docker compose up
```

The frontend is on http://localhost:3000, the API on http://localhost:8000 and
DynamoDB Local on http://localhost:8002 (override with `APP_PORT` / `API_PORT` /
`DDB_PORT`).

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

The server stores only user state (saved code, test runs, timed attempts) and it
stores it in DynamoDB — locally the `dynamodb` container, which is
[DynamoDB Local](https://hub.docker.com/r/amazon/dynamodb-local). One table,
`trainer`, keyed by `pk` (`U#<user_id>`) and `sk` (`P#`, `RUN#` or `SLV#` plus
the problem id), so everything one user owns sits in one partition and every
read is a `GetItem` or a single-partition `Query`. The api container creates the
table on boot when `DDB_ENDPOINT` is set; the data survives `docker compose
down` in the `dynamodb_data` volume and is thrown away by `docker compose down
-v`. To poke at it directly:

```
aws dynamodb scan --table-name trainer --endpoint-url http://localhost:8002
```

**The `user_id` is a cookie, not a login.** On load the app looks for a
`trainer_uid` cookie and, if there is none, generates one with
`crypto.randomUUID()` and stores it for a year (`app/src/user.ts`). A cookie
rather than `localStorage` because same-origin `fetch` sends it automatically,
so no API call site has to know it exists. The server reads it in one place
(`current_user()` in `backend/server.py`), validates it is a UUID before it
reaches a key, and rejects a request without one with a 400.

This is **not authentication**: the id is generated in the browser and the
server takes it at face value, so anyone can set the cookie to someone else's id
and read their data. It is a partition key for a single-user prototype. The
practical consequence is that identity lives entirely in that cookie — clearing
cookies, or opening the app in a different browser or a private window, mints a
new id and shows an empty history, and there is no way to get the old one back.

The browser builds its own
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

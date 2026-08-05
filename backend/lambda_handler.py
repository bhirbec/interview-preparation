"""AWS Lambda entrypoint for the same FastAPI app uvicorn serves locally.

In AWS the API is a Lambda with a Function URL that only CloudFront can call,
mounted on the website's own distribution under /api/* (see aws/bin/aws.ts).
That keeps the browser same-origin exactly as the Vite dev proxy does: the
user_id cookie rides along on its own and no CORS preflight is involved.

Mangum is the ASGI adapter — it turns the Function URL's payload-format-2.0
event into the ASGI scope server.py already speaks, so not a line of the eight
routes changes between `docker compose up` and production.

lifespan="off": the app's only lifespan work is db.init_db(), which creates the
tables and is deliberately a no-op outside development (in AWS the tables belong
to the CDK app). Running it on every cold start would buy nothing.
"""

from mangum import Mangum
from server import app

handler = Mangum(app, lifespan="off")

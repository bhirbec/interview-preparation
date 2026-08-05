# CDK

Infrastructure for the coding trainer, in AWS account **332778514565**
(`us-east-1`), reached through the local `interview-prep` profile. `bin/aws.ts`
refuses to run against any other account: the default profile is the org payer,
and a forgotten `--profile` would otherwise aim at it.

The account has no hosted zone and no domain on purpose — nothing here creates
one.

## Stacks

`submissions-table`, `attempts-table`, `runs-table` — the user state that
`backend/db.py` reads and writes. All on-demand, all keyed by `user_id` + `sk`,
all `RETAIN`: they hold the only copy of a user's progress.

`trainer-website` — the site itself, live on
**https://d2xq9qs5gi6j3t.cloudfront.net**. An S3 bucket behind CloudFront, plus
the FastAPI app of `backend/` as a Lambda on the *same* distribution under
`/api/*`. One distribution means the browser is same-origin, so there is no CORS
setup anywhere and `app/src/api.ts` uses the same relative `/api/...` paths in
production as it does behind the Vite dev proxy.

The stack deploys the API; the site's files are published separately by
`app/scripts/deploy`, which reads the bucket name and distribution id back from
this stack's outputs.

### The Lambda bundle

`lib/backend-code.ts` builds it from `backend/uv.lock` with `uv`, asking for
Linux/ARM wheels from whatever machine is deploying — so the Lambda runs the
same versions `docker compose up` runs, without a Docker bundling step. `uv`
must be installed. The entrypoint is `backend/lambda_handler.py` (Mangum over
the unchanged `server.py`).

### Two things about the function URL

CloudFront reaches the Lambda through a function URL locked to `AWS_IAM`, signed
by an origin access control. That arrangement has two sharp edges, both of which
show up as a 403 that the distribution's error response rewrites into the SPA's
`index.html` — an API that answers HTML:

1. AWS requires **two** resource-based permissions, `lambda:InvokeFunctionUrl`
   *and* `lambda:InvokeFunction`. `StaticWebsiteStack` grants the first;
   `bin/aws.ts` adds the second.
2. Lambda rejects unsigned payloads, and CloudFront does not read request
   bodies, so any request **with a body** must carry its own
   `x-amz-content-sha256`. `app/src/api.ts` computes it — that is why the
   frontend hashes what it POSTs and PUTs.

Both are documented under [Restrict access to an AWS Lambda function URL
origin](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-lambda.html).

## Deploy

`@devkit/cdk` is linked from `../../devkit/packages/cdk` and its `dist/` is
gitignored there, so build it once before anything else. Install with **yarn**:
`link:` is yarn's protocol and npm rejects it.

```bash
(cd ../../devkit/packages/cdk && npm run build)
yarn install
```

`constructs` is pinned to 10.4.5 rather than the usual `^10.0.0`: the linked
devkit resolves `constructs` from its own `node_modules`, and two different
10.x copies in one synth fail with `scope.node._scopes is not iterable`. Keep
this equal to whatever devkit installs.

Then:

```bash
npx cdk deploy <stack> --profile interview-prep
```

The account is bootstrapped (`CDKToolkit`, `us-east-1`); a new region or account
would need `npx cdk bootstrap --profile interview-prep` first.

## Useful Commands

* `npm run build`   - Compile TypeScript files to JavaScript
* `npm run watch`   - Watch for file changes and recompile automatically
* `npm run test`    - Run Jest unit tests
* `npx cdk deploy`  - Deploy the stack to your default AWS account and region
* `npx cdk diff`    - Compare the deployed stack with the current state
* `npx cdk synth`   - Generate the synthesized CloudFormation template

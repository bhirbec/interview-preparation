# CDK

Infrastructure for the coding trainer, in AWS account **332778514565**
(`us-east-1`), reached through the local `interview-prep` profile. `bin/aws.ts`
refuses to run against any other account: the default profile is the org payer,
and a forgotten `--profile` would otherwise aim at it.

The account has no hosted zone and no domain on purpose — nothing here creates
one.

## Stacks

Three DynamoDB tables holding the user state that `backend/db.py` reads and
writes: `submissions-table`, `attempts-table` and `runs-table`. All on-demand,
all keyed by `user_id` + `sk`, all `RETAIN` — they hold the only copy of a
user's progress.

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

The account has not been bootstrapped yet; the first deploy needs
`npx cdk bootstrap --profile interview-prep`.

## Useful Commands

* `npm run build`   - Compile TypeScript files to JavaScript
* `npm run watch`   - Watch for file changes and recompile automatically
* `npm run test`    - Run Jest unit tests
* `npx cdk deploy`  - Deploy the stack to your default AWS account and region
* `npx cdk diff`    - Compare the deployed stack with the current state
* `npx cdk synth`   - Generate the synthesized CloudFormation template

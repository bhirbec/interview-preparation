#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { DynamoStack } from '@devkit/cdk';

const app = new cdk.App();
const account = process.env.CDK_DEFAULT_ACCOUNT || "0";
const region = process.env.CDK_DEFAULT_REGION;
const env = { account, region };

const validAccounts = {
  332778514565: "prod",
};

// The *default* profile is the org payer, so a forgotten --profile would aim
// every command at the wrong account. Fail before the app is even built.
if (!(account in validAccounts)) {
  console.error(
    `❌ Invalid AWS account: ${account}\n` +
    `Make sure you're using the correct AWS profile.\n\n` +
    `👉 Example:\n` +
    `    cdk deploy <stack> --profile interview-prep`
  );
  process.exit(1);
}

if (!region) {
  throw new Error('CDK_DEFAULT_REGION is required.');
}

const tableNames = {
  submissions: 'submissions',
  attempts: 'attempts',
  runs: 'runs',
};

// User state: the saved code, the timed attempts and the test runs of every
// browser that has ever used the app. Deliberately table-per-entity rather than
// single-table — it is a 1:1 translation of the SQLite schema it replaced, and
// backend/db.py reads the same way.
//
// All three share one key shape:
//   user_id (pk)  the cookie id from backend/user.py, so every read is scoped
//                 to one browser and never needs a scan or a GSI
//   sk            the problem id (submissions), or "<problem_id>#<ulid>"
//                 (attempts, runs) — ULIDs sort by creation time, which is what
//                 makes "newest first" a plain descending query
//
// RETAIN on all three: these hold the only copy of a user's progress, and there
// is no recovery path — the id lives in a cookie nobody can prove ownership of.
const stateTable = (name: string) => ({
  env,
  tableProps: {
    tableName: name,
    partitionKey: { name: 'user_id', type: cdk.aws_dynamodb.AttributeType.STRING },
    sortKey: { name: 'sk', type: cdk.aws_dynamodb.AttributeType.STRING },
    billingMode: cdk.aws_dynamodb.BillingMode.PAY_PER_REQUEST,
    removalPolicy: cdk.RemovalPolicy.RETAIN,
  },
});

new DynamoStack(app, 'submissions-table', stateTable(tableNames.submissions));
new DynamoStack(app, 'attempts-table', stateTable(tableNames.attempts));
new DynamoStack(app, 'runs-table', stateTable(tableNames.runs));

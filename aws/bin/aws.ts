#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import { DynamoStack, StaticWebsiteStack } from '@devkit/cdk';
import { backendLambdaCode } from '../lib/backend-code';

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

// Built from account + region rather than by importing the table constructs:
// the names are fixed above, so this needs no cross-stack export and the
// website stack can be deployed, rolled back or replaced on its own.
const tableArn = (name: string) => `arn:aws:dynamodb:${region}:${account}:table/${name}`;

// The site itself: S3 behind CloudFront, with the FastAPI app of backend/ as a
// Lambda on the *same* distribution under /api/*.
//
// No `domainName` — the account has no hosted zone on purpose, so the site is
// served on CloudFront's own d<...>.cloudfront.net name and the stack creates
// no Route 53 record and no ACM certificate.
//
// Same distribution means same origin, which is the whole point: the browser
// sends the user_id cookie by itself, app/src/api.ts keeps calling relative
// /api/... paths, and there is no CORS hop — identical to what the Vite dev
// proxy does locally.
const site = new StaticWebsiteStack(app, 'trainer-website', {
  env,
  bucketName: 'interview-prep-trainer-website',
  // The default is /404.html, which this app does not build: every unknown path
  // is a client-side route, and index.html is what boots the router.
  notFoundPage: '/index.html',
  api: {
    functionProps: {
      functionName: 'trainer-api',
      runtime: lambda.Runtime.PYTHON_3_13,
      // Graviton, matching the wheels lib/backend-code.ts asks uv for.
      architecture: lambda.Architecture.ARM_64,
      handler: 'lambda_handler.handler',
      code: backendLambdaCode(),
      // Pyodide runs the tests in the browser; every endpoint here is a handful
      // of DynamoDB calls, so the ceiling only has to cover a cold start.
      timeout: cdk.Duration.seconds(15),
      memorySize: 512,
      logRetention: cdk.aws_logs.RetentionDays.ONE_MONTH,
    },
    // backend/db.py defaults to these same names; passing them keeps the
    // deployed API pointing at the tables this app owns rather than at a
    // default that happens to agree.
    environmentVariables: {
      SUBMISSIONS_TABLE: tableNames.submissions,
      ATTEMPTS_TABLE: tableNames.attempts,
      RUNS_TABLE: tableNames.runs,
    },
    // Read and write: every endpoint but /api/health touches user state.
    permissionArns: {
      dynamodb: { write: Object.values(tableNames).map(tableArn) },
    },
  },
});

// StaticWebsiteStack grants CloudFront lambda:InvokeFunctionUrl, which is not
// enough on its own: AWS documents *two* statements for an OAC-signed function
// URL origin, and without this second one every /api/* request is rejected at
// the function URL — before the Lambda is even invoked, so nothing shows up in
// its logs. It surfaces as a 403 that the distribution's error response turns
// into the SPA's index.html, i.e. a site whose API silently answers HTML.
// https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-lambda.html
site.apiFunction?.addPermission('cloudfront-invoke-function', {
  principal: new cdk.aws_iam.ServicePrincipal('cloudfront.amazonaws.com'),
  action: 'lambda:InvokeFunction',
  sourceArn: `arn:aws:cloudfront::${account}:distribution/${site.distribution.distributionId}`,
});

// app/scripts/deploy reads both back at runtime instead of hardcoding ids that
// change whenever the stack is replaced. The distribution id and domain name
// are already emitted by StaticWebsiteStack.
new cdk.CfnOutput(site, 'website-bucket-name', { value: site.bucket.bucketName });

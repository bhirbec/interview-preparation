import * as cdk from 'aws-cdk-lib';
import { Template } from 'aws-cdk-lib/assertions';
import { DynamoStack, StaticWebsiteStack } from '@devkit/cdk';

// bin/aws.ts is a script (it reads env and calls process.exit), so the table
// shape is asserted on an equivalent stack rather than by importing it.
function table(name: string) {
  const app = new cdk.App();
  const stack = new DynamoStack(app, `${name}-table`, {
    env: { account: '332778514565', region: 'us-east-1' },
    tableProps: {
      tableName: name,
      partitionKey: { name: 'user_id', type: cdk.aws_dynamodb.AttributeType.STRING },
      sortKey: { name: 'sk', type: cdk.aws_dynamodb.AttributeType.STRING },
      billingMode: cdk.aws_dynamodb.BillingMode.PAY_PER_REQUEST,
      removalPolicy: cdk.RemovalPolicy.RETAIN,
    },
  });
  return Template.fromStack(stack);
}

describe.each(['submissions', 'attempts', 'runs'])('%s table', (name) => {
  test('is on-demand, composite-keyed and retained', () => {
    const t = table(name);
    t.hasResourceProperties('AWS::DynamoDB::Table', {
      TableName: name,
      BillingMode: 'PAY_PER_REQUEST',
      KeySchema: [
        { AttributeName: 'user_id', KeyType: 'HASH' },
        { AttributeName: 'sk', KeyType: 'RANGE' },
      ],
    });
    // The only copy of the user's progress — a stack delete must not take it.
    t.hasResource('AWS::DynamoDB::Table', { DeletionPolicy: 'Retain' });
  });

  test('has no secondary indexes', () => {
    // Every read in backend/db.py is a GetItem or a single-partition Query; a
    // GSI appearing here would mean that stopped being true.
    const props = Object.values(
      table(name).findResources('AWS::DynamoDB::Table')
    )[0].Properties;
    expect(props.GlobalSecondaryIndexes).toBeUndefined();
    expect(props.LocalSecondaryIndexes).toBeUndefined();
  });
});

// Same story for the website stack: an equivalent stack, with the Lambda's code
// inlined so the test does not have to build the real bundle (lib/backend-code.ts
// shells out to uv). Everything asserted below is a consequence of the props,
// not of what is inside the zip.
function website() {
  const app = new cdk.App();
  const stack = new StaticWebsiteStack(app, 'trainer-website', {
    env: { account: '332778514565', region: 'us-east-1' },
    bucketName: 'interview-prep-trainer-website',
    notFoundPage: '/index.html',
    api: {
      functionProps: {
        functionName: 'trainer-api',
        runtime: cdk.aws_lambda.Runtime.PYTHON_3_13,
        code: cdk.aws_lambda.Code.fromInline(' '),
        handler: 'lambda_handler.handler',
      },
    },
  });
  return Template.fromStack(stack);
}

describe('website stack', () => {
  // The account has no hosted zone and no domain: omitting `domainName` is what
  // keeps the site on CloudFront's own *.cloudfront.net name, and a zone lookup
  // appearing here would mean it stopped being omitted.
  test('creates no Route 53 or ACM resources', () => {
    const t = website();
    expect(t.findResources('AWS::Route53::RecordSet')).toEqual({});
    expect(t.findResources('AWS::Route53::HostedZone')).toEqual({});
    expect(t.findResources('AWS::CertificateManager::Certificate')).toEqual({});
    expect(
      Object.values(t.findResources('AWS::CloudFront::Distribution'))[0]
        .Properties.DistributionConfig.Aliases,
    ).toBeUndefined();
  });

  // Same distribution as the site = same origin in the browser, which is what
  // lets app/src/api.ts keep calling relative /api/... paths with no CORS.
  test('routes /api/* to the Lambda origin', () => {
    const config = Object.values(
      website().findResources('AWS::CloudFront::Distribution')
    )[0].Properties.DistributionConfig;

    const behavior = config.CacheBehaviors.find((b: any) => b.PathPattern === '/api/*');
    expect(behavior).toBeDefined();

    const lambdaOrigin = config.Origins.find(
      (o: any) => o.Id === behavior.TargetOriginId,
    );
    // A Lambda function URL, reachable only through this distribution (OAC).
    expect(lambdaOrigin.DomainName['Fn::Select']).toBeDefined();
    expect(lambdaOrigin.OriginAccessControlId).toBeDefined();
    // The default behavior still serves the S3 site.
    expect(config.DefaultCacheBehavior.TargetOriginId).not.toEqual(behavior.TargetOriginId);
  });
});

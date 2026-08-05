import * as cdk from 'aws-cdk-lib';
import { Template } from 'aws-cdk-lib/assertions';
import { DynamoStack } from '@devkit/cdk';

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

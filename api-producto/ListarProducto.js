const AWS = require('aws-sdk');
const lambda = new AWS.Lambda();
const dynamodb = new AWS.DynamoDB.DocumentClient();
const TABLE_NAME = 't_productos';

exports.handler = async (event) => {
  try {
    const body = JSON.parse(event.body);
    const token = event.headers.Authorization;

    const tokenResult = await lambda.invoke({
      FunctionName: 'ValidarTokenAcceso',
      InvocationType: 'RequestResponse',
      Payload: JSON.stringify({ token })
    }).promise();
    const validation = JSON.parse(tokenResult.Payload);
    if (validation.statusCode === 403) {
      return { statusCode: 403, body: 'Token inválido' };
    }

    const { tenant_id, limit = 5, start_key } = body;
    const params = {
      TableName: TABLE_NAME,
      KeyConditionExpression: 'tenant_id = :tenant_id',
      ExpressionAttributeValues: { ':tenant_id': tenant_id },
      Limit: limit
    };
    if (start_key) params.ExclusiveStartKey = start_key;

    const response = await dynamodb.query(params).promise();
    return {
      statusCode: 200,
      body: JSON.stringify({
        tenant_id,
        productos: response.Items,
        lastEvaluatedKey: response.LastEvaluatedKey || null
      })
    };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};

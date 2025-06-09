const AWS = require('aws-sdk');
const lambda = new AWS.Lambda();
const dynamodb = new AWS.DynamoDB.DocumentClient();
const TABLE_NAME = 't_productos';

exports.handler = async (event) => {
  try {
    const { tenant_id, producto_id, producto_datos } = JSON.parse(event.body);
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

    const updateExpr = 'set ' + Object.keys(producto_datos).map(k => `${k} = :${k}`).join(', ');
    const exprAttrVals = {};
    for (let k in producto_datos) exprAttrVals[`:${k}`] = producto_datos[k];

    const result = await dynamodb.update({
      TableName: TABLE_NAME,
      Key: { tenant_id, producto_id },
      UpdateExpression: updateExpr,
      ExpressionAttributeValues: exprAttrVals,
      ReturnValues: 'UPDATED_NEW'
    }).promise();

    return {
      statusCode: 200,
      body: JSON.stringify(result.Attributes)
    };
  } catch (err) {
    return { statusCode: 500, body: JSON.stringify({ error: err.message }) };
  }
};

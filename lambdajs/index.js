'use strict';

import { Series, DataFrame } from 'pandas-js';

const AWS = require('aws-sdk')
const w2v = require('word2vec')

const s3 = new AWS.S3({httpOptions: {timeout: 10000}})

let model

exports.testFunc = async () => {
    testWord2Vec = w2v.loadModel('./recommender.w2v', (err, data) => {
        model = data
        print(data)
    })
}
 
testFunc()

// Route the incoming request based on intent.
// The JSON body of the request is provided in the event slot.
exports.handler = async (intentRequest) => {
    try{
        // const data = await s3.getObject({
        //     Bucket: "recommender-model",
        //     Key: "recommender.w2v"
        // }).promise()
        
        const model = await w2v.loadModel(data).promise()
        
        console.log('Model:', model)
        
        console.log(`request received for userId=${intentRequest.userId}, intentName=${intentRequest.currentIntent.name}`);
        const sessionAttributes = intentRequest.sessionAttributes;
        const slots = intentRequest.currentIntent.slots;
        
        const name = slots.Name;
        const hobby = slots.Hobby;
        
        const message = {'contentType': 'PlainText', 'content': `Okay, your name is ${name} and your hobby is ${hobby}. I recommend the product ${hobbyProductMapping[hobby]}`}
        const fulfillmentState = 'Fulfilled'
        
        return {
        sessionAttributes,
        dialogAction: {
            type: 'Close',
            fulfillmentState,
            message,
        }
    };
    }catch(err){
        console.log(err)
    }
};

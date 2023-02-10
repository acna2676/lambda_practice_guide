## 初期データの登録
```
aws dynamodb put-item --table-name mailaddress2 --item "{\"email\":{\"S\":\"acna2676@gmail.com\"},\"username\":{\"S\":\"nakaishi\"},\"haserror\":{\"N\":\"0\"},\"issend\":{\"N\":\"0\"}}"
```
[AWS CLI で「Error parsing parameter」が発生するときの対処方法](https://dev.classmethod.jp/articles/tsnote-how-to-deal-with-error-parsing-paramete-that-occurs-in-aws-cli/)

## S3バケットへのファイルの格納
```
aws s3 cp example.txt s3://mailbody222222/
```


## バウンスメールの通知先を設定する
```
TOPICARN="aws cloudformation describe-stacks --stack-name \"stack-sam-example-email\" --query "Stack[0].Outputs[?OutputKey==\'BounceTopicArn\'].OPutputValue\" --output text"
echo $TOPICARN
aws ses set-identity-notification-topic --identity acna2676@gmail.com --notification-type Bounce --sns-topic $TOPICARN
```

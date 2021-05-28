import boto3
import json

comprehend = boto3.client(service_name='comprehend', region_name='ap-northeast-2')
                
text = "원빈의 전무후무한 명연기, 명대사 그리고 지금은 유명해진 조연들 찾는 재미까지"

print('Calling DetectSentiment')
print(json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode="ko"), sort_keys=True))
print('End of DetectSentiment\n')
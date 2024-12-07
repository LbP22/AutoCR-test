# AutoCR-test
Backend repo of an automatic code review application

## Docker containers setup
bash autocr_test/inventory/run.sh

## Backend setup
1. fill the .env file by pattern of .env.sample
2. poetry install
3. poetry run dev

## Docs
Docs can be accessed on localhost:8000/docs


## A few words about scaling
1. How to handle 100+ new requests per minute
There are few strategies for that one, it depends on the priorities. If we prioritize fast responses, we need to create a few instances where OpenAI/GitHub clients will be running and loadbalancer over it to balance the traffic between those machines.
Another way, is usable if we can queue requests without providing immediate response for users. So yes, the queue is the answer and probably it may be a better way in some cases, because of global services load (they may be loaded not only by our requests, but with total users traffic)

2. How to handle large repos
There are also not only one way for it. But this question, honestly, need an experiments in my opinion. Because as I know from ChatGPT, it can analyze the urls that you're sending to it and one of my ideas right now is to publish data on our and use some api key as path parameter and pass it in the prompt so only the AI and our service will have the key and will be able to check this data. Another question is if it can analyze this url's content or it may work the same as the input of tokens and will cause the 429 error? Needs to be tested.

And that is also an answer on how to save costs. If it will not charge tokens for analyzing urls, this can be used for asking for a multiple reviews in one request that will also affect on service reviewing speed
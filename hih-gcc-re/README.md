# Hashish Investment Holding — GCC Real Estate Intelligence

## Run locally
```bash
uvicorn app:make_app --reload --port 8000
```

## Kick a job
```bash
curl -X POST http://127.0.0.1:8000/analyze  -H "Content-Type: application/json"  -d '{
   "deal_id":"gcc-demo-001",
   "data_room_url":"https://drive.google.com/drive/folders/1wof3dSNcuqoE1Edvr4ffDxRDqp_s1B-W",
   "region":"dubai",
   "filters":{"min_price":400000,"max_price":10000000,"for":"sale","property_types":["apartment","villa"]}
 }'
```

## Check status
```bash
curl http://127.0.0.1:8000/status/gcc-demo-001
```

# Kibana

- localhost:5601

## Dev Tools

- Management >> Dev Tools
- Use Dev Tools to run Elasticsearch queries (HTTP requests below)

## Create Index

```bash
# delete index if it exists
DELETE /tickets_location

# create index with location field
PUT /tickets_location
{
  "mappings": {
    "properties": {
      "location": {
        "type": "geo_point"
      }
    }
  }
}

# reindex tickets to tickets_location (fill data)
POST /_reindex
{
  "source": {
    "index": "tickets" # spark writes to ES index named tickets
  },
  "dest": {
    "index": "tickets_location" # new index with location field
  },
  "script": {
    "source": """
      if (ctx._source.latitude != null && ctx._source.longitude != null) {
        ctx._source.location = ['lat': ctx._source.latitude, 'lon': ctx._source.longitude]
      }
    """
  }
}
```

### Verify

```bash
# view schema
GET /tickets_location/_mapping

# get sample data's location field
GET /tickets_location/_search
{
  "_source": ["location"],
  "size": 5
}
```

## Create Data View

- Management >> Stack Management >> Data Views >> Create Data View
- Select `tickets_location` index

## Creating map data

- Analytics >> Maps
- Add layer

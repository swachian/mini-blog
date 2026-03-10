To run the test:

```
pytest -m "not slow" 

```

or

```
pytest
```


Make a search filter so that the blogs can be queried in this way.

```
http://127.0.0.1:8000/posts/?filters=[{"field":"authorName","operator":"eq","value":"Danny"}]&page=1&pageSize=10

```

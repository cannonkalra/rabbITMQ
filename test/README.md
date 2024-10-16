## Test the Telegraf Configuration

```bash
docker run --rm -w /data -v $(pwd):/data -it telegraf:1.32 telegraf --config telegraf.conf --test 
```
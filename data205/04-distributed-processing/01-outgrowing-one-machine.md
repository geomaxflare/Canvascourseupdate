# When Data Outgrows a Single Machine

A single computer has fixed limits: its memory (RAM), its processor cores, and how fast it can read from disk. **Scaling** is how we respond when a workload hits those limits.

### Warning signs

- The data no longer fits in memory, so tools crash or slow to a crawl.
- Jobs that once took minutes now take hours and miss their deadlines.
- Data arrives faster than one machine can process it.
- Many users run heavy queries at the same time.

### Two ways to scale

| | Scale up (vertical) | Scale out (horizontal) |
| --- | --- | --- |
| How | Use a bigger machine: more memory, more cores | Spread the work across many machines (a *cluster*) |
| Pros | No code changes; simpler | Nearly unlimited capacity; can survive one machine failing |
| Cons | There is always a largest machine, and big machines are expensive | More complex; data must move over the network between machines |

### Try these first

Distributed processing adds cost and complexity. Before reaching for a cluster, try:

1. **Read less data:** select only needed columns and filter early.
2. **Use better formats:** a columnar Parquet file can be many times smaller and faster than the same CSV.
3. **Use a warehouse engine:** cloud SQL warehouses already distribute the work behind the scenes.
4. **Scale up:** a larger machine may be enough, and single-machine engines have become very fast.

Today, data in the range of a few gigabytes is usually handled comfortably on one machine. Distributed processing earns its complexity when data reaches hundreds of gigabytes or more, or when work must be spread out to finish in time.

### The core idea of distribution

Distributed engines **divide** data into pieces, **process** each piece on a different machine at the same time, then **combine** the partial results. Summing a billion sales rows becomes many small sums added together.

### Check yourself

1. What is the difference between scaling up and scaling out?
2. Name two things to try before moving a workload to a cluster.
3. Why does moving data between machines slow distributed jobs down?

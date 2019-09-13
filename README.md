# Geo Distributed LRU
<b>Problem:</b>
At Ormuco, we want to optimize every bits of software we write. Your goal is to write a new
library that can be integrated to the Ormuco stack. Dealing with network issues everyday,
latency is our biggest problem. Thus, your challenge is to write a new Geo Distributed LRU (Least
Recently Used) cache with time expiration. This library will be used extensively by many of our
services so it needs to meet the following criteria:
 <br/>
    1 - Simplicity. Integration needs to be dead simple. <br/>
    2 - Resilient to network failures or crashes. <br/>
    3 - Near real time replication of data across Geolocation. Writes need to be in real time. <br/>
    4 - Data consistency across regions <br/>
    5 - Locality of reference, data should almost always be available from the closest region <br/>
    6 - Flexible Schema <br/>
    7 - Cache can expire <br/>

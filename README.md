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

<b>Solution:</b><br/>
To solve the issue this  solution proposes a multicast client server architecture. </br>
where each chache server is running on a flusk based environement exposing API's </br>
for operations Exposed API's are as follows.</br>
a) /heartbeat - Returns a success message to signify that server is up and running </br>
b) /getCacheItem - retruns as single cache item. Request type is as follows</br>
   /getCacheItem?item_key=key3</br>
   It takes input as single key and returns the details of values.</br>
c) /setCacheItem - set's the cache item value sample request type is as follows: </br>
{</br>
  "item_key":"key5",</br>
  "item_value":"sample5",</br>
  "expires_at":10</br>
}</br>
d) /deleteCacheItem - deletes as single item from cache. Request structure as follows </br>
/deleteCacheItem?item_key=key3 </br>
e) updateCacheItem - updates the cache item send as request as multicast receiver</br>
{</br>
  "item_key":"key5",</br>
  "item_value":"sample5",</br>
  "expires_at":10</br>
  "action":"update" </br>
}</br>
Or if it is a delete case then 
{</br>
  "item_key":"key5",</br>
  "item_value":null,</br>
  "expires_at":null,</br>
  "action":"delete" </br>
}</br>
f) apart from the API's each server module contains a sender function that takes data as incoming request  </br>
and forwards it to the multicast receiver application on specific multicast IP.</br>
g) multicast_reciver app intercepts sender applications request and forwards it on the </br>
localhost to cache server update url as mentioned in e)updateCacheItem. 

<b>How to Run The Application:</b><br/>



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
You can  run lru_cache_server as below <br/>
app.run(host='127.0.0.1', port=5453, debug=True)<br/>
It will start on the sender application as well.<br/>
You also need to start MultiCastReceiver application as below<br/>
    rec = MulticastReceiver(CommonConstants.MULTICAST_GROUP_IP, CommonConstants.MULTICAST_PORT_VALUE, 5454)<br/>
    sock = rec.get_reciver_socket()<br/>
    rec.listen_incoming_request_send_update_to_cache(sock)<br/>
In order to test the application you have to also run another copy of lru_server as below <br/>
    app.run(host='127.0.0.1', port=5454, debug=True)<br/>
    
After running the above commands you can start interacting with cache server as you need.<br/>

<b>Functionanilites covered:</b><br/>
    This application only demonstrates some one the required functionalities and is <br/>
    under evolution. In the due course of time rest of the functionalities can be implemented.
    <b>1 - Simplicity. Integration needs to be dead simple. <br/>
    2 - Resilient to network failures or crashes. <br/>
    3 - Near real time replication of data across Geolocation. Writes need to be in real time. <br/>
    4 - Data consistency across regions <br/>
    5 - Flexible Schema <br/><b>
   Locality of refernce and cache expiry will be taken under future functionlities.<br/>
   
    

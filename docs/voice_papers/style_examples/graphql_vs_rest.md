Now, if you’re like me: alarm bells are already ringing. These shootouts happen all the time, and in many cases the experimental design is seriously flawed. In my opinion, this paper is no exception. So rather than take this article at face value (and report their findings as fact), we’re going to take a more critical lens. I am going to present their research and their findings, but I’ll spend much more time than usual on history and context, and then I'll use that to inform counter-arguments to their analysis. This study is imperfect, but it’s not without value. They did unearth some interesting findings, I just don’t think those findings should be taken at face value; so we won’t. The way we'll get the most out of this paper is through a critical, interrogative lens, so let's do that.

Before we get to the paper itself, let’s review some history:

SOAP: Before any of the options above, there was SOAP. SOAP is an XML based protocol that’s heavy, complicated, difficult to document, and bad at a number of things. But, it did set the playing field for what was to come: a generic and serializable format for data interchange over HTTP. With SOAP, two systems built with completely different stacks could exchange data without knowing anything about the other system, other than the WSDL (specification document) for the endpoint that was exposed. In the early days of the web, this was a fairly novel idea. For a few years it became the de-facto standard, replacing XML-RPC (its predecessor) for many of the major public APIs of the time.
Then, in 2000 Roy Fielding defined the concept of REST in his doctoral dissertation. REST, which stands for Representational State Transfer, had three design advantages over SOAP:

It was inherently stateless: To build an API the “RESTful” way, was to embrace the concept that state could be embedded within the request itself, and passed around from machine to machine, (rather than having state stored in a central server). This allowed the request to be processed by any part of a distributed system. This was crucial for the burgeoning web, as it was amenable to the horizontal scaling of backend resources.
It used idiomatic HTTP: With REST, the protocol that developers already knew (HTTP) could be used to design their APIs. It was simple, and there was virtually no learning curve. A RESTful API was just nouns and verbs. CRUD operations mapped to the HTTP verbs POST, GET, PUT and DELETE (and eventually PATCH and OPTIONS would catch on too), and resources were defined as nouns in a URL path. Easy.
It used JSON: Though its chosen interchange format wasn’t explicitly called out (you could, technically use XML if you wanted to), JSON very quickly became best-practice. Since JavaScript was already built into browsers, the data stored on web-clients was already structured as JavaScript objects by default. Allowing interchange via JSON meant that frontend objects no longer had to be mapped to some other structure (XML), and this meant much less work and headache for frontend de500 requests ran serially or in smaller batches over the course of 5 minutes. Again one set of tests fetched flat data and the next set fetched nested data.
Let’s go over what the tests revealed:

​
​Concurrent requests: At the highest level of concurrency tested (500)

Flat data: gRPC averaged 2 seconds per request, REST averaged 4, and GraphQL averaged 21, while CPU utilization averaged 36%, 48%, and 142% respectively.
Nested data: gRPC averaged 14 seconds per request, REST averaged 16, and GraphQL averaged 29, while CPU utilization averaged 84%, 123%, and 177% respectively.
​
​Consecutive requests: At the highest level of throughput tested (500)

Flat data: gRPC averaged 67ms per request, REST averaged 149, and GraphQL averaged 204, while CPU utilization averaged 6%, 7%, and 33% respectively.
Nested data: gRPC averaged 748ms per request, REST averaged 798, and GraphQL averaged 1035ms, while CPU utilization averaged 41%, 22%, and 90% respectively.
So, in short, in all head-to-head comparisons (other than the last nested test), the results were the same: gRPC was fastest, REST was next, and GraphQL was far behind. In their evaluation of the study, the authors conclude:

This superiority can be attributed to gRPC’s adoption of the HTTP/2 protocol, a departure from REST and GraphQL, which rely on the HTTP/1 protocol. The efficient handling of data exchange provided by the HTTP/2 protocol is a significant factor contributing to gRPC’s enhanced performance in comparison to its counterparts.

I’d argue that the abo not RAM, network I/O, disk I/O or anything else) doesn’t give us a full picture of the resource-hungriness of these different systems. The authors' analysis presupposes that higher CPU utilization is universally bad, but it's much more complicated than that: What if, for example, one process takes 3x the CPU but a fraction of the Network I/O and half the RAM? What then?

Lastly, (and I’ll stop here just for brevity’s sake, not because I’ve run out of red-flags in this paper): this whole paper was about benchmarking read-requests at high concurrency. In reality, this isn’t particularly meaningful, as any modern application operating at this level of concurrency would have caches sitting in front of their reads. A much more interesting benchmark would be inserts, updates, and deletes.

At the end of the day, I think there are some interesting takeaways from this paper. Largely that the GraphQL application does seem CPU hungry under heavy reads. But, as we explored in earlier, reads-per-second and CPU utilization was never where GraphQL was meant to shine in the first place. Additionally, this research shows that gRPC is extremely fast, which is great, but what it doesn’t show is how the 3rd-party-developer experience is affected when you force them to consume a gRPC API instead of a RESTful or GraphQL one. These things matter. At the end of the day we’re building these applications and exposing these APIs so that other software engineers can build things on top of them. We should be kind to them. Speed matters, but so does usability.

Try as the authors may to paint gRPC, REST and GraphQL as interchangeable sister technologies shooting it out in a winner-take-all competition, that’s just not reality. These tools are each good at different things, for different use-cases, different consumers, and different invocation patterns. If you’re a Software Engineer I’d encourage you to keep all three in your bag of tricks, you’ll undoubtedly find a time and place where each one of them shines.of the overhead that would be felt by the other options for every request. In idiomatic REST, one way to counter this limitation is to:

Only send the first request to the authentication endpoint. That endpoint returns some kind of bearer token.
That bearer token can be embedded in subsequent requests.
Subsequent requests talk directly to the individual microservices rather than needing to be proxied by the authentication service. Each microservice can authenticate the veracity of the bearer token on their own, through a shared secret.
With a design-change such as the above the REST system, for example, could eliminate roughly 50% of the total network requests, effectively raising the capacity of the system.

Additionally, only profiling CPU utilization (andored behind their own microservice, and then setup a shootout to compare how long it takes each protocol to fetch the same amount of interrelated data out of the system. If GraphQL is capable of pulling it all out with one fetch, while REST and gRPC have to perform dozens or even hundreds of consecutive fetches, then the conclusion we’d draw from the shootout might be much different. This difference would likely grow even more if the GraphQL system was sitting in front of a graph database instead of Redis.

Another issue is that of the application design. gRPC can keep connections open (since it’s running over HTTP/2 which is full-duplex). This means that after the initial connection is open to the server it never needs to be opened again. This reduces some ve paragraph does a reasonably good job of explaining the difference between the results of REST and gRPC. But for this experiment, both GraphQL and REST were running over HTTP/1, so what explains the difference in performance between those two options? In other words, why did REST nearly keep pace with gRPC, while GraphQL fell far behind? Well, I think this research is fundamentally missing the point of GraphQL. Remember: GraphQL emerged as a solution that allows you to send a smaller total number of requests to fetch the same information. So benchmarking it on the number of requests it can handle per second is misguided. This is not comparing apples to apples. A true comparison would be if the authors setup a series of interrelated objects that were all stvided by Hasanuddin University. That dataset contains data about lecturers and those lecturers' educational backgrounds. You can think of it almost like the type of data that would be stored to power a site like LinkedIn. They loaded the data into MySQL, and then put a Redis cache in from of the DB. Essentially the Redis instance functioned as a read-replica for the database. Virtually all the data was pulled into Redis, which in essence moved it into RAM, allowing for quick and efficient reads.

Next, for each cluster they built three different microservices in Golang:

One endpoint offering authentication
One endpoint for fetching “flat” data out of Redis (meaning: an object of key-value pairs without any nesting)
One endpoint for fetching “nested” data out of Redis
Each endpoint was structured as a standalone application and lived in its own container. Service #2 and #3 would both sit behind service #1, so in order to fetch either flat or nested data you’d have to pass through the authentication service, which would act as the gateway to the rest of the system. They built one cluster of containers for gRPC, one for REST, and one for GraphQL.

Then it was time to benchmark the performance of each cluster. For this they used Apache jMeter, and ran a series of load-tests simulating two different types of invocation patterns:

Concurrent requests: 100, 200, 300, 400 and 500 requests sent at nearly the same time. One set of tests fetched flat data and the next set fetched nested data.
Consecutive requests: 100 - to-server communication within an organization. We haven’t yet seen it used extensively as protocol for public APIs for 3rd parties. That is still the domain of REST and GraphQL.

Okay, sorry, that was actually way more history than I thought I was going to give you. Now that you have all that backstory under your belt, we’re able to turn to this study and examine it using all that context as a tool in our analysis.

For this study the researchers’ plan was simple: They would create the same API three times:

One in REST
One in GraphQL
One in gRPC
Then they would load test it, examine the response times of each, examine the resource utilization of the servers that were running each, and then pick a winner.

First they pulled down a dataset called SISTER, protobuf were largely using it as part of RPC (remote procedure call) clusters. At Google, the full system was called Stubby, and they kept it under wraps. That was until 2016 when they released the replacement for Stubby: gRPC. From the ground up, gRPC was built for efficiency. Unlike REST, which traditionally runs on HTTP/1 and usually uses JSON, gRPC runs on top of HTTP/2 and uses protocol buffers. In a nutshell: this makes gRPC capable of a level of bidirectional realtime communication at scale that would be extremely difficult to attain any other way. But, this comes at a cost. Namely: complexity. gRPC is extremely powerful, and flexible, but also has a significant learning curve. Because of this, today, it’s still largely used for high-performance server-AP, etc) there was a delay associated with the serialization and deserialization of data. When a single client is talking to a single server, this delay might not be noticeable, but when a server needs to process a request by talking to many other servers and those other servers need to talk to even more servers, all that communication being serialized and de-serialized has a significant cumulative cost.

In response to this challenge, in 2001 they developed something called Protocol Buffers “protobuf”. They wouldn’t release it publicly until 2008. Protobuf is a binary format, and is designed from the ground up to be interoperable, tiny and fast. But on it’s own, it’s just a format, not an API protocol or a system. Google and the other companies adopting pro Facebook poured time and resources into developing a project called TAO, which would store the relationships between objects as first-class data, allowing a query to traverse the "social graph" far more efficiently than in an RDBMS.
A new API protocol called GraphQL. This was designed to read/write data from related objects in as few requests as possible. Rather than expose strict endpoints, GraphQL exposed a query language over the wire, providing a level of flexibility that simultaneously solved both the "underfetching" and the "overfetching" problems inherent in resource-based API designs. With GraphQL, a developer could say “Give me this user, and all of their recent orders, and all of their recent comments” in a single fetch. In REST that likely would have been at least 3 separate requests to different resources. So in essence, GraphQL made the client-side work much easier. On the server-side, Facebook's switch from traditional RDBMS systems to graph-storage meant that these kinds of requests could be converted into efficient queries and could pull data out of the datastores in far fewer operations. Facebook open-sourced GraphQL in 2015.
Meanwhile, down the road at Google, they were facing a different problem. Google’s competitive edge had always been speed. But as they scaled and their systems became more distributed, that speed was harder and harder to maintain. This was partly in due to the overhead of the interchange happening between servers. For the options available to them at the time (XML-RPC, SOlowing) with each other.
People formed into groups.
There were other entities (like companies and institutions) that could form various types of relationships with each other.
Entities of all kinds could create posts, and other users would have interactions and reactions to those posts.
Etc
As the objects in the system grew and the relationships between those objects grew, fetching information out of the system through a RESTful facade became slower and slower, and sending information to the system required chains of API requests and multistep database transactions. In response to these challenges, Facebook helped push two concepts into the mainstream:

The graph database. Graph databases had been around for decades, but were rarely used for web development.velopers. The rise of Node.js would eventually make this true for backend developers as well.
For over a decade, REST was the undisputed king of web API protocols. If you were building a new web API, especially a public one from the mid-2000s to the mid 2010s there’s a huge chance you were building it as REST. Twitter’s extremely popular API was REST. As was Amazon’s, Flickr’s and Google Maps. And importantly: so was Facebook’s.

Unlike the other sites, REST wasn’t working that well for Facebook as they scaled. Facebook was, famously, originally built as something like a LAMP stack. But as they grew they ended up with a novel set of issues:

They didn’t just have a lot of data, they had a lot of relationships between their data.
People formed relationships (friendships, fol

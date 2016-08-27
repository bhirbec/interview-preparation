A couple tips specifically if you're solving this problem using Java:

# Running

Some combination of this should execute the sample java project:
```bash
$ cd stripe-interview/request-replay/java
$ mvn clean -e install
$ mvn -e exec:java
```

Libraries
---------

We recommend you use [Google's GSON][google/gson] and [Square's OkHttp][square/okhttp] for implementation, but you can use whichever library you want.
We've added both libraries to this project, and included a `pom.xml` that includes them.
You don't need to use our provided `pom.xml` file, feel free to use whichever format you want.

GSON
----

The json library tries to parse classes from the JSON. We've provided a class
that can be parsed from the JSON -- `com.stripe.interview.MyLog`.
Hopefully this will reduce the amount of work that you need to do.

[google/gson]: https://github.com/google/gson
[square/okhttp]: https://github.com/square/okhttp

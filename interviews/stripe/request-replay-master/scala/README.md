A couple tips specifically if you're solving this problem using Scala:

# Running

Some combination of this should execute the sample java project:
```bash
$ cd stripe-interview/request-replay/scala
$ sbt
 > run
 > test
```

Libraries
---------

We recommend you use [Spray-json][spray/spray-json] and [Scalaj HTTP][scalaj/scalaj-http] for implementation,
but you can use whichever library you want if there is something you are more familiar with. We've added both
libraries to this project, and included a `build.sbt` that includes them. You don't need to use our provided
`build.sbt` file; feel free to use whichever build system you want.

Spray-json
----------

Since learning all of spray-json during an interview would be very challenging,
We've provided a class with some shotcuts to the JSON parsing --
`com.stripe.interview.MyLog`. it includes all the custom json formats you might need.
Hopefully this will reduce the amount of work that you need to do.

If you have not used it before, section of the documentation is particularly helpful
https://github.com/spray/spray-json#usage

Scalaj-http
------------
There are better libraries than Scalaj-http in Scala, but it is very easy to learn and use for this exercise.

[spray/spray-json]: https://github.com/spray/spray-json
[scalaj/scalaj-http]: https://github.com/scalaj/scalaj-http

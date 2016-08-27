A couple tips specifically if you're solving this problem using C++:

Libraries
---------

We recommend you use [nlohmann's json library][nlohmann/json] and
[cpr][whoshuu/cpr] for implementation. We've added both libraries to
this project, and included a Makefile that will build them in, as well
as enabling debug symbols and C++11. You'll need to have libcurl
installed - we'll link it automatically.

json
----

The json library tries to be pretty magical. Don't be afraid to use
`.get<type>()` instead of relying on it to coerce.

Iterating over json objects is tricky. The best solution we found was
to assign the object to a `std::map<string, json>` and iterate over
that.

cpr
---

If you want to set custom headers, know that `cpr::Header` is just a
`std::map<string, string>` - you don't have to use their initializer
list syntax.

We also made a small change from the public docs: `cpr::Payload` has
an overloaded constructor which can take a `std::string`, instead of
only accepting a list of key/value pairs.

[nlohmann/json]: https://github.com/nlohmann/json
[whoshuu/cpr]: https://github.com/whoshuu/cpr

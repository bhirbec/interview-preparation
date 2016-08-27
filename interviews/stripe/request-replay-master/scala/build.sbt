name := "request-replay-scala"

scalaVersion := "2.11.7"

libraryDependencies ++= Seq(
  "org.scalaj" %% "scalaj-http" % "2.2.1",
  "io.spray" %%  "spray-json" % "1.3.2",
  "org.scalatest" %% "scalatest" % "3.0.0" % "test",
  "org.scalactic" %% "scalactic" % "3.0.0",
  "org.scalacheck" %% "scalacheck" % "1.13.2" % "test"
)

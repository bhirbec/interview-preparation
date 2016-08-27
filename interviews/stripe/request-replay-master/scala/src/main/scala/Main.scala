package com.stripe.interview

import spray.json._
import MyLog._
// import scalaj.http._

object Main {

  def main(args: Array[String]): Unit = {
    val strings = useSprayForSomething("hello world")
    print(strings.toJson.prettyPrint)
  }

  def useSprayForSomething(input: String): List[String] = {
    val source = s"""["$input","a","b","c"]"""
    source.parseJson.convertTo[List[String]]
  }
}

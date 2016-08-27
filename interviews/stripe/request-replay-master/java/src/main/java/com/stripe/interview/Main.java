package com.stripe.interview;

import com.google.gson.GsonBuilder;

public class Main {
	public static void main(String... args) {
		useGSONForSomeReason("hello\n");
		System.out.println("Hello world!");
	}

	public static void useGSONForSomeReason(String input) {
		new GsonBuilder().create().toJson(input, System.out);
	}
}

package com.stripe.interview;

import java.util.Map;

public class MyLog {
	public MyRequest request;
	public MyResponse response;

	public MyRequest getRequest() {
		return request;
	}

	public MyResponse getResponse() {
		return response;
	}

	public static class MyResponse {
		public String body;
		public int code;

		public String getBody() {
			return body;
		}

		public int getCode() {
			return code;
		}
	}

	public static class MyRequest {
		public String url;
		public Map<String, String> headers;
		public String body;

		public String getUrl() {
			return url;
		}

		public Map<String, String> getHeaders() {
			return headers;
		}

		public String getBody() {
			return body;
		}
	}
}

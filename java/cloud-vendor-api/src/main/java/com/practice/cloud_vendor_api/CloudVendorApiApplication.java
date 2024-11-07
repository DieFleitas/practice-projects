package com.practice.cloud_vendor_api;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import springfox.documentation.builders.PathSelectors;
import springfox.documentation.builders.RequestHandlerSelectors;
import springfox.documentation.service.ApiInfo;
import springfox.documentation.service.Contact;
import springfox.documentation.spi.DocumentationType;
import springfox.documentation.spring.web.plugins.Docket;

import java.util.Collections;

@SpringBootApplication
public class CloudVendorApiApplication {

	public static void main(String[] args) {
		SpringApplication.run(CloudVendorApiApplication.class, args);
	}

	@Bean
	public Docket swaggerConfiguration() {
		return new Docket(DocumentationType.SWAGGER_2)
				.select()
				.paths(PathSelectors.ant("/cloudvendor/*"))
				.apis(RequestHandlerSelectors.basePackage("com.practice.cloud_vendor_api"))
				.build()
				.apiInfo(apiCustomData());
	}

	private ApiInfo apiCustomData() {
		return new ApiInfo(
				"Cloud Vendor API Application",
				"Cloud vendor documentation",
				"1.0",
				"Cloud vendor service terms",
				new Contact("Jon Smith","https://www.johnsmith.com", "johnsmith@hotmail.com"),
				"License",
				"https://www.license.com",
				Collections.emptyList()
		);
	}

}

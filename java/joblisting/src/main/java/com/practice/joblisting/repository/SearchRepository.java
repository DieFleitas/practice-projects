package com.practice.joblisting.repository;

import com.practice.joblisting.models.Post;

import java.util.List;

public interface SearchRepository {

    List<Post> findByText(String text);
}

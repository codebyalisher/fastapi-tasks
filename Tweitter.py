class Twitter:
    def __init__(self):
        self.count = 0
        self.followMap = defaultdict(set)
        self.tweetMap = defaultdict(list)

    def postTweet(self, userId: int, tweetId: int) -> None:
        self.tweetMap[userId].append((tweetId,self.count))
        self.count += 1

    def getNewsFeed(self, userId: int) -> List[int]:
        minHeap = []
        res = []

        self.followMap[userId].add(userId)
        for followedId in self.followMap[userId]:
            if followedId in self.tweetMap:
                index = len(self.tweetMap[followedId]) - 1
                tweetId, count = self.tweetMap[followedId][index]
                heapq.heappush(minHeap, (count, tweetId, followedId, index - 1))
        
        while minHeap and len(res) < 10:
            count, tweetId, followedId, index = heapq.heappop(minHeap)
            res.append(tweetId)
            if index >= 0:
                tweetId, count = self.tweetMap[followedId][index]
                heapq.heappush(minHeap, (count, tweetId, followedId, index - 1))

        return res

    def follow(self, followerId: int, followeeId: int) -> None:
        self.followMap[followerId].add(followeeId)

    def unfollow(self, followerId: int, followeeId: int) -> None:
        if followeeId in self.followMap[followerId]:
            self.followMap[followerId].remove(followeeId)
        


### `defaultdict`

'''`defaultdict` is a subclass of the built-in Python dictionary (`dict`). It overrides one method and adds one writable instance variable. The main functionality of `defaultdict` is that it provides a default value for the dictionary being accessed, which means you don't have to check if a key exists before accessing or modifying it.

Here's an example:

```python
from collections import defaultdict

# Create a defaultdict with default type as list
d = defaultdict(list)

# Accessing a non-existent key returns the default value (an empty list in this case)
print(d['key'])  # Output: []

# You can then append to this list
d['key'].append(1)
print(d['key'])  # Output: [1]
```

In the provided code, `defaultdict` is used to initialize `followMap` and `tweetMap`:

- `self.followMap = defaultdict(set)`: This means that `followMap` is a dictionary where each key maps to a set. If you try to access a key that doesn't exist, it will return an empty set by default.
- `self.tweetMap = defaultdict(list)`: This means that `tweetMap` is a dictionary where each key maps to a list. If you try to access a key that doesn't exist, it will return an empty list by default.

### `def getNewsFeed(self, userId: int) -> List[int]`

This is a method definition in Python with type hints. Let's break it down:

- `def getNewsFeed(self, userId: int) -> List[int]`: This defines a method named `getNewsFeed` that takes two parameters:
  - `self`: This is a reference to the current instance of the class. It's a convention in Python to name the first parameter of instance methods `self`.
  - `userId: int`: This indicates that the `userId` parameter should be of type `int`.
  
- `-> List[int]`: This is a return type hint. It indicates that the method is expected to return a list of integers. The `List` type is imported from the `typing` module.

Here's a simplified example:

```python
from typing import List

class Example:
    def getNumbers(self) -> List[int]:
        return [1, 2, 3, 4, 5]

example = Example()
print(example.getNumbers())  # Output: [1, 2, 3, 4, 5]
```

In the provided code, `getNewsFeed` is a method that returns a list of tweet IDs (integers) for a given user, based on the tweets from the users they follow. The method uses a min-heap to efficiently retrieve the most recent tweets.
'''
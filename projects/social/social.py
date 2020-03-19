import random
from util import Queue


class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}

        # Add users
        # iterate over 0 to num users...
        for u in range(0, num_users):
            # add user using an f-string
            self.add_user(f'User {u}')

        # Create friendships
        # generate all possible friendship combinations
        possible_friendships = []

        # avoid dups by making sure the first number is smaller than the second
        # iterate over user id in users...
        for user_id in self.users:
            # iterate over friend id in in a range from user id + 1 to last id + 1...
            for friend_id in range(user_id + 1, self.last_id + 1):
                # append a user id and friend id tuple to the possible friendships
                possible_friendships.append((user_id, friend_id))

        # shuffle friendships random import
        random.shuffle(possible_friendships)

        # create friendships for the first N pairs of the list
        # N is determined by the formula: num users * avg friendships // 2
        # NOTE: need to divide by 2 since each add_friendship() creates 2 friendships
        # iterate over a range using the formula as the end base...
        for i in range(num_users * avg_friendships // 2):
            # set friendship to possible friendships at index
            friendship = possible_friendships[i]
            # add friendship of frienship[0], friendship[1]
            self.add_friendship(friendship[0], friendship[1])

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        queue = Queue()
        queue.enqueue([user_id])

        while queue.size() > 0:
            path = queue.dequeue()
            vertex = path[-1]
            if vertex not in visited:
                neighbors = self.friendships[vertex]
                for neighbor in neighbors:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.enqueue(new_path)
                visited[vertex] = path

        return visited

    def get_extended_social_network(self, user_id):
        paths = self.get_all_social_paths(user_id)
        total_extended_users = []
        degrees_of_separation = []
        for user in paths:
            path = paths[user]
            path_size = len(path)
            degree_separation = 0
            if path_size > 2:
                degree_separation = path_size - 2
                for friend in path:
                    if friend not in total_extended_users and friend is not user_id and friend is not user:
                        total_extended_users.append(friend)
            degrees_of_separation.append(degree_separation)

        average_degree_of_separation = float("{0:.2f}".format(
            sum(degrees_of_separation) / len(degrees_of_separation)))
        percentage_of_other_users = float("{0:.2f}".format(
            len(total_extended_users) / len(self.users) * 100))
        return (percentage_of_other_users, average_degree_of_separation)


"""
To create 100 users with an average of 10 friends each, how many times would you need to call add_friendship()? Why?
500 times because we are adding 100 * 10 = 1000 friendships but only 500 are unique.
If you create 1000 users with an average of 5 random friends each, what percentage of other users will be in a particular user's extended social network? What is the average degree of separation between a user and those in his/her extended network?
1000 * 5 = 5000 // 2 = 2500
41.5 to 44.2 % of other users in extended social network
3 to 4 average degree of separation
STRETCH
You might have found the results from question #2 above to be surprising. Would you expect results like this in real life? If not, what are some ways you could improve your friendship distribution model for more realistic results?
If you followed the hints for part 1, your populate_graph() will run in O(n^2) time. Refactor your code to run in O(n) time. Are there any tradeoffs that come with this implementation?
"""

if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(1000, 5)
    print(sg.friendships)
    # test case
    # sg.friendships = {1: {8, 10, 5}, 2: {10, 5, 7}, 3: {4}, 4: {9, 3}, 5: {8, 1, 2}, 6: {10}, 7: {2}, 8: {1, 5}, 9: {4}, 10: {1, 2, 6}}
    connections = sg.get_all_social_paths(1)
    print(connections)
    print('Percentage of other users', sg.get_extended_social_network(1))

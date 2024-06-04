import random
from django.contrib.auth.models import User
from api.models import FriendRequest

# Function to create random friend requests
def create_friend_requests(users, num_requests):
    for _ in range(num_requests):
        from_user = random.choice(users)
        to_user = random.choice(users)
        
        # Ensure from_user and to_user are different and the friend request doesn't already exist
        while from_user == to_user or FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            from_user = random.choice(users)
            to_user = random.choice(users)
        
        FriendRequest.objects.create(from_user=from_user, to_user=to_user, status='pending')

# Create 10 users
for i in range(1, 11):
    username = f'user{i}'
    email = f'user{i}@example.com'
    password = 'password123'
    User.objects.create_user(username=username, email=email, password=password)

# Retrieve all users from the database
users = User.objects.all()

# Number of friend requests to create
num_friend_requests = 20

# Create friend requests
create_friend_requests(users, num_friend_requests)

print(f"{num_friend_requests} friend requests created successfully!")

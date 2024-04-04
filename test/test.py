import pytest
#com
class User:
    def __init__(self, username, user_id, password, salary, age, position):
        self.username = username
        self.id = user_id
        self.set_password(password)
        self.salary = salary
        self.age = age
        self.position = position
        self.bank_account = 0
        self.is_active = True
        self.followers = set()
        self.following = set()
        self.posts = []

    def set_password(self, password):
        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase character")
        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one digit")
        self.password = password

    def deactivate(self):
        self.is_active = False

    def follow(self, user):
        if user != self:
            self.following.add(user)
            user.followers.add(self)

    def unfollow(self, user):
        if user in self.following:
            self.following.remove(user)
            user.followers.remove(self)

    def is_following(self, user):
        return user in self.following

    def is_followed_by(self, user):
        return user in self.followers

    def create_post(self, content):
        post = Post(content, self)
        self.posts.append(post)
        return post

    def deposit_to_bank_account(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.bank_account += amount

    def withdraw_from_bank_account(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self.bank_account < amount:
            raise ValueError("Insufficient funds")
        self.bank_account -= amount

class Post:
    def __init__(self, content, author):
        self.content = content
        self.author = author
        self.likes = 0

    def like(self):
        self.likes += 1

def test_user_can_deposit_to_bank_account():
    user = User("test_user1", 1, "Password1", 50000, 30, "Developer")
    user.deposit_to_bank_account(100)
    assert user.bank_account == 100

def test_user_can_withdraw_from_bank_account():
    user = User("test_user2", 2, "Password2", 60000, 35, "Manager")
    user.deposit_to_bank_account(100)
    user.withdraw_from_bank_account(50)
    assert user.bank_account == 50

def test_user_cannot_deposit_negative_amount():
    user = User("test_user3", 3, "Password3", 70000, 40, "Designer")
    with pytest.raises(ValueError):
        user.deposit_to_bank_account(-100)

def test_user_cannot_withdraw_negative_amount():
    user = User("test_user4", 4, "Password4", 80000, 45, "Engineer")
    user.deposit_to_bank_account(100)
    with pytest.raises(ValueError):
        user.withdraw_from_bank_account(-50)

def test_user_cannot_withdraw_more_than_balance():
    user = User("test_user5", 5, "Password5", 90000, 50, "Analyst")
    user.deposit_to_bank_account(100)
    with pytest.raises(ValueError):
        user.withdraw_from_bank_account(150)
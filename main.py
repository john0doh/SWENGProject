from github import Github
from rich import *
import os

token = os.getenv('GITHUB_TOKEN')
gh = Github(token)
#username1 = input("enter person 1 ")
#username2 = input("enter person 2 ")

user1 = gh.get_user("torvalds")
#user2 = gh.get_user(username2)

org = gh.get_organization("DROPCitizenShip")
for members in org.get_members():
    print (members.name)

# print (user1.name)

# for follows in user1.get_followers():
#     print(follows.name)
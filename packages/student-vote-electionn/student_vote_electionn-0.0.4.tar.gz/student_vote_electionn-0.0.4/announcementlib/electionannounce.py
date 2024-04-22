import time

announcements = [
    "Don't forget to cast your vote in the student election!",
]

def rotate_announcements():
    for announcement in announcements:
        print(announcement)
        return announcement
    

rotate_announcements()
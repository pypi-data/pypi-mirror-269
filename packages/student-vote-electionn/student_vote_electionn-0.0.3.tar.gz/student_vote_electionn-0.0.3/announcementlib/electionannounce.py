import time

announcements = [
    "Announcement 1: Don't forget to cast your vote in the student election!",
    "Announcement 2: Meet the candidates at the upcoming debate on Friday.",
    "Announcement 3: The voting deadline has been extended to accommodate more students.",
    "Announcement 4: Check your email for important election updates.",
    "Announcement 5: Voting booths are open in the student center from 9 AM to 5 PM.",
    "Announcement 6: Get involved in shaping the future of our campus - vote now!",
]

def rotate_announcements():
    index = 0
    while True:
        yield announcements[index]
        index = (index + 1) % len(announcements)
        time.sleep(5)
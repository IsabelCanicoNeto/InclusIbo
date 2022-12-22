from constants import *
from DashInclusive import *
import asyncio
import struct
from bleak import BleakScanner
from bleak import BleakClient



def DashSoundTest (rbdash, sound = "ALL"  ):

    # play the sound , recorded in the robot as requested in sound or all of them

    sounds = {
        "elephant",
        "tiresqueal",
        "hi",
        "bragging",
        "ohno",
        "ayayay",
        "confused2",
        "confused3",
        "confused5",
        "confused8",
        "brrp",
        "charge",
        "huh",
        "okay",
        "yawn",
        "tada",
        "wee",
        "bye",
        "horse",
        "cat",
        "dog",
        "dino",
        "lion",
        "goat",
        "croc",
        "siren",
        "horn",
        "engine",
        "tires",
        "helicopter",
        "jet",
        "boat",
        "train",
        "beep",
        "laser",
        "gobble",
        "buzz",
        "squeek",
        "my1",
        "my2",
        "my3",
        "my4",
        "my5",
        "my6",
        "my7",
        "my8",
        "my9",
        "my10",
    }

    if sound == "ALL":

        for k in sounds:
            print (k)
            rbdash.dash.say(k)
            time.sleep(0.5)
    else:
        print(sound)
        rbdash.dash.say(sound)
        time.sleep(0.5)

def SimpleBehavior (rbdash):

    rbdash.dash.name()

    print("reset")
    rbdash.dash.reset(4)
    time.sleep(2)

    rbdash.dash.eye(0b1010101010101)

    rbdash.dash.say("hi")
    rbdash.dash.say("ayayay")
    rbdash.dash.say("huh")
    rbdash.dash.say("okay")
    rbdash.dash.neck_color("yellow")
    time.sleep(2)

    rbdash.dash.move(100)
    time.sleep(2)
    rbdash.dash.turn(45)

    time.sleep(2)
    rbdash.dash.ear_color("red")
    time.sleep(2)
    rbdash.dash.head_yaw(10)
    time.sleep(2)

    #dash.eye(255)
    rbdash.dash.eye(100)
    #dash.eye(8191)

def TETest (rbdash, explicit = True, organic = False, slowPace = False):

    begin = time.time()
    print("turn 1 -> 2 ")
    actualSpeaker = 1
    nextSpeaker = 2
    nextSpeakerName = "my9"


    rbdash.turnexchange(actualSpeaker, nextSpeaker, nextSpeakerName, slowPace, organic, explicit)
    end = time.time()
    print("TE " + str(explicit) + str(end-begin))

    begin = time.time()
    print("turn 2 -> 3 ")
    actualSpeaker = 2
    nextSpeaker = 3
    nextSpeakerName = "my10"
    rbdash.turnexchange(actualSpeaker, nextSpeaker, nextSpeakerName, slowPace, organic, explicit)
    end = time.time()
    print("TE " + str(explicit) + str(end-begin))

    begin = time.time()
    print("turn 3 -> 2 ")
    actualSpeaker = 3
    nextSpeaker = 2
    nextSpeakerName = "my9"
    rbdash.turnexchange(actualSpeaker, nextSpeaker, nextSpeakerName, slowPace, organic, explicit)
    end = time.time()
    print("TE " + str(explicit) + str(end-begin))

    begin = time.time()
    print("turn 2 -> 1 ")
    actualSpeaker = 2
    nextSpeaker = 1
    nextSpeakerName = "my8"
    rbdash.turnexchange(actualSpeaker, nextSpeaker, nextSpeakerName, slowPace, organic,  explicit)
    end = time.time()
    print("TE " + str(explicit) + str(end-begin))

    begin = time.time()
    print("turn 1 -> 3 ")
    actualSpeaker = 1
    nextSpeaker = 3
    nextSpeakerName = "my10"
    rbdash.turnexchange(actualSpeaker, nextSpeaker, nextSpeakerName, slowPace, organic, explicit)
    end = time.time()
    print("TE " + str(explicit) + str(end-begin))

    begin = time.time()
    print("turn 3 -> 1 ")
    actualSpeaker = 3
    nextSpeaker = 1
    nextSpeakerName = "my8"
    rbdash.turnexchange(actualSpeaker, nextSpeaker, nextSpeakerName, slowPace, organic, explicit)
    end = time.time()
    print("TE " + str(explicit) + str(end-begin))


def FollowingTest (rbdash, numBehav=1, explicit=False, slowPace = False):

    begin = time.time()


    print("hear 1 -> suggested 1 ")
    actualSpeaker = 1
    suggestedSpeaker = 1
    rbdash.following(suggestedSpeaker, actualSpeaker, explicit)
    end = time.time()
    print("duration follow " + str(end-begin))
    begin = time.time()
    print("hear 1 -> suggested 1 (2) ")
    actualSpeaker = 1
    suggestedSpeaker = 1
    rbdash.following(suggestedSpeaker, actualSpeaker, explicit)
    end = time.time()
    print("duration follow 2 " + str(end-begin))
    time.sleep (3)
    print("hear 2 -> suggested 1 ")
    begin = time.time()
    actualSpeaker = 2
    suggestedSpeaker = 1
    rbdash.following(suggestedSpeaker, actualSpeaker, explicit)

    end = time.time()

    print("duration following 3 " + str(end-begin))

    begin = time.time()
    print("hear 3 -> suggested 1 ")
    actualSpeaker = 3
    suggestedSpeaker = 1
    rbdash.following(suggestedSpeaker, actualSpeaker, explicit)
    end = time.time()
    print("duration follow " + str(end-begin))


    """
    begin = time.time()
    print("TE 1 -> 2 ")
    nextSpeaker = 2
    nextSpeakerName = "my9"
    rbdash.turnexchange(actualSpeaker, nextSpeaker, nextSpeakerName, slowPace, explicit)

    end = time.time()
    print("duration TE " + str(end-begin))

    print("hear 2 -> suggested 2 ")
    actualSpeaker = 2
    suggestedSpeaker = 2
    rbdash.following(suggestedSpeaker, actualSpeaker, explicit)

    print("hear 3 -> suggested 2 ")
    actualSpeaker = 3
    suggestedSpeaker = 2
    rbdash.following(suggestedSpeaker, actualSpeaker, explicit)

    print("hear 1 -> suggested 2 ")
    actualSpeaker = 1
    suggestedSpeaker = 2
    rbdash.following(suggestedSpeaker, actualSpeaker, explicit)

    print("TE 2 -> 3 ")
    nextSpeaker = 3
    actualSpeaker = 2
    nextSpeakerName = "my8"
    rbdash.turnexchange(actualSpeaker, nextSpeaker, nextSpeakerName, slowPace, explicit)

    print("hear 1 -> suggested 3 ")
    actualSpeaker = 1
    suggestedSpeaker = 3
    rbdash.following(suggestedSpeaker, actualSpeaker,  explicit)

    print("hear 2 -> suggested 3 ")
    actualSpeaker = 2
    suggestedSpeaker = 3
    rbdash.following(suggestedSpeaker, actualSpeaker, explicit)

    print("hear 3 -> suggested 3 ")
    actualSpeaker = 3
    suggestedSpeaker = 3
    rbdash.following(suggestedSpeaker, actualSpeaker,  explicit)
    """

def EncourageTest (rbdash, numBehav=1, explicit=False, slowPace = False):

    print("Encourage 1")

    #print("TE 3 -> 1 ")
    #nextSpeaker = 1
    #actualSpeaker = 3
    #nextSpeakerName = "my10"
    # rbdash.turnexchange(actualSpeaker, nextSpeaker, nextSpeakerName, slowPace, explicit)

    print ("encourage 1 (speaker 2) ")
    #actualSpeaker = 2
    #suggestedSpeaker = 1
    #suggestedSpeakerName = "my10"
    #rbdash.encourage(suggestedSpeaker, suggestedSpeakerName, actualSpeaker, explicit)

    begin = time.time()

    print ("encourage 1 (speaker 1) ")
    actualSpeaker = 1
    suggestedSpeaker = 1
    suggestedSpeakerName = "my10"

    rbdash.encourage(suggestedSpeaker, suggestedSpeakerName, actualSpeaker, explicit)
    end = time.time()
    print("duration encourage " + str(end-begin))


def EngageTest (rbdash, explicit=False, slowPace = False):

    print("engage 1")

    begin = time.time()
    actualSpeaker = 1
    suggestedSpeaker = 1
    suggestedSpeakerName = "my10"
    rbdash.engage(suggestedSpeaker)
    end = time.time()
    print("duration engage " + str(end-begin))

"""
def FollowTest (rbdash, explicit=False, slowPace = False):

    print("Following 1")

    print ("following 1 (speaker 2) ")
    #actualSpeaker = 2
    #suggestedSpeaker = 1
    #suggestedSpeakerName = "my10"

    begin = time.time()
    print ("following 1 (speaker 1) ")
    actualSpeaker = 1
    suggestedSpeaker = 1
    suggestedSpeakerName = "my10"
    rbdash.following(suggestedSpeaker, suggestedSpeakerName, actualSpeaker, explicit)
    end = time.time()
    print("duration follow " + str(end-begin))

"""


def FlencTest (rbdash, explicit=False, slowPace = False):

    print("Following 1")

    print ("following 1 (speaker 2) ")
    #actualSpeaker = 2
    #suggestedSpeaker = 1
    #suggestedSpeakerName = "my10"

    begin = time.time()
    print ("following 1 (speaker 1) ")
    actualSpeaker = 1
    suggestedSpeaker = 1
    suggestedSpeakerName = "my10"
    rbdash.flwencourage (suggestedSpeaker, suggestedSpeakerName, actualSpeaker, explicit)
    end = time.time()
    print("duration flw encourage " + str(end-begin))

def main():
    print ("começa")

    StartTime = time.time()
    rbdash= robot(StartTime)
    print(rbdash.dash.address)
    print(rbdash.dash.device)
    print(rbdash.dash.is_connected)

    if rbdash.dash.is_connected:
        rbdash.dash.name()

        """
        DashSoundTest(rbdash.dash,  "huh")
        DashSoundTest(rbdash.dash,  "my5")
        DashSoundTest(rbdash.dash, "yawn")
        DashSoundTest(rbdash.dash, "confused8")
        DashSoundTest(rbdash.dash, "okay")
        """

        #DashSoundTest (rbdash, sound = "ALL"  )
        """
        print("first speaker TEST EXPLICIT (1) ")
        begin = time.time()
        rbdash.firstspeaker(1, "my10", True)

        end = time.time()
        print("duration first speaker explicit " + str(end-begin))
        print("first speaker TEST IMPLICIT (1) ")
        begin = time.time()
        rbdash.firstspeaker(1, "my8", False)

        end = time.time()
        print("duration first speaker implicit " + str(end-begin))

        rbdash.firstspeaker(1, "my8", False)

        """
        print("TE TEST EXPLICIT (1) ")

        TETest(rbdash, True, False, True)

        print("TE TEST IMPLICIT (2) ")

        TETest(rbdash, False, False, True)

        print("TE Organic  TEST IMLICIT (1) ")

        TETest(rbdash, False, True, True)

        print("TE Organic TEST EXPLICIT (2) ")

        TETest(rbdash, True, True, True)
        """
        print("following TEST (3) ")


        FollowingTest(rbdash, 1, True, False)

        print("encourage TEST EXPLICIT (2) ")

        EncourageTest (rbdash, 1, True, False)

        print("encourage TEST IMPLICIT (2) ")

        EncourageTest (rbdash, 1, False, False)



        print("follow TEST EXPLICIT (2) ")

        FollowingTest (rbdash, True, False)

        print("follow TEST IMPLICIT (2) ")

        FollowingTest (rbdash, False, False)


        print("flw enc TEST EXPLICIT (2) ")

        FlencTest (rbdash, True, False)

        FlencTest (rbdash, True, False)

        print("follow TEST IMPLICIT (2) ")

        FlencTest (rbdash, False, False)

        print("engage TEST IMPLICIT (2) ")

        EngageTest (rbdash, False, False)

        print("middle TEST  ")

        begin = time.time()
        ### rbdash.middle(1, 0, "my8", False, True, False)


        end = time.time()
        print("duration middle implicit " + str(end-begin))
        time.sleep(5)

        print("end TEST  ")

        begin = time.time()
        rbdash.end(1, 2, 3, True)

        end = time.time()
        print("duration end " + str(end-begin))


        begin = time.time()

        rbdash.lastminute()

        end = time.time()
        print("duration lastminute " + str(end-begin))

        begin = time.time()
        rbdash.startsession()
        end = time.time()
        print("duration start  " + str(end-begin))

        print ("close")
        rbdash.dash.closeDash()

"""

if __name__ == '__main__':
    main()
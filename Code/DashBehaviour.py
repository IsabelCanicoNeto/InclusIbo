from robot import *

#===============================================================================
#
#                              ROBOT Behaviours
#
#===============================================================================

'''
************************************ First speaker  **************************************
'''

def firstspeaker(dash, dist, speed, actualSpeaker, nameSpeaker):


    color = checkColor(dash,actualSpeaker)

    firstspeaker_lights(dash, True, actualSpeaker, color)
    time.sleep(0.5)
    firstspeaker_mov(dash, dist, speed, "my2",nameSpeaker, color)
    time.sleep(0.1)
    firstspeaker_lights(dash, False, actualSpeaker, color)

def firstspeaker_lights(dash, firstTime, actualSpeaker, color):

    if firstTime :
        dash.stop()
        time.sleep(0.5)
        dash.reset(4)
        time.sleep(0.5)
        dash.all_color("black")
        time.sleep(0.5)

    dash.eye_brightness(255)
    dash.tail_brightness(255)
    dash.eye(0b1010101010101)
    #time.sleep(0.1)
    dash.all_color(color)
    #time.sleep(0.1)
    dash.eye(8191)
    #time.sleep(0.1)




def firstspeaker_mov(dash, dist, speed, phrase, name, color):

    dash.move(200,200)
    #time.sleep(0.5)
    dash.say(phrase)
    time.sleep(1.5)
    dash.say(name)
    time.sleep(1)



'''
******************************** turnexchange **************************************
'''


def turnexchange(dash, actualSpeaker, nextSpeaker, nextSpeakerName, slowPace = False, phrase="my2", explicit=True):

    turnexchange_lights(dash, True, actualSpeaker, nextSpeaker)
    time.sleep(1)
    turnexchange_mov(dash, actualSpeaker, nextSpeaker, nextSpeakerName, slowPace, "my2", explicit)
    time.sleep(2)
    turnexchange_lights(dash, False, actualSpeaker, nextSpeaker)

def turnexchange_lights(dash, firstTime, actualSpeaker, nextSpeaker):

    #colorActual = checkColor(dash,actualSpeaker)
    colorNext = checkColor(dash,nextSpeaker)

    if firstTime: dash.all_color("black")
    #dash.eye_brightness(0)
    #dash.tail_brightness(0)

    dash.eye(0b1010101010101)
    time.sleep(0.5)
    dash.eye(0b1101010101010)
    time.sleep(0.5)
    dash.all_color(colorNext)
    time.sleep(0.5)
    if not firstTime: dash.eye(8191)
    time.sleep(0.5)


def turnexchange_mov(dash, actualSpeaker, nextSpeaker, name, slowPace, phrase, explicit):

    driveDist, driveSpeed, angle = checkTurnmovement(actualSpeaker, nextSpeaker, slowPace)

    dash.move(-driveDist, driveSpeed)
    time.sleep(2)

    dash.turn(angle)
    time.sleep(0.5)

    dash.move(driveDist, driveSpeed)
    time.sleep(2)

    if explicit :
        dash.say(phrase)
        time.sleep(1.5)
        dash.say(name)
        time.sleep(1)
    else:
        dash.head_pitch(3)
        time.sleep(2)

def hearing(dash, suggestedSpeaker, actualSpeaker, explicit=True):

    hearing_mov(dash, suggestedSpeaker, actualSpeaker, explicit)
    time.sleep(1)

def hearing_mov(dash, suggestedSpeaker, actualSpeaker, explicit):

    i = 0

    if suggestedSpeaker == actualSpeaker:
        while i < 4:
            dash.head_pitch(-2)
            #time.sleep(0.2)
            dash.head_pitch(2)
            time.sleep(0.2)
            i += 1

        #time.sleep(0.5)
        if explicit :
            dash.say ("ayayay")
            time.sleep(1.5)
        # "huh", "ayayay" backchanneling
        dash.head_pitch(0)
        time.sleep(0.5)
    else:
        angle = checkHeadmovement(suggestedSpeaker, actualSpeaker)
        dash.head_yaw(angle)
        time.sleep(0.2)
        while i < 8:
            dash.head_pitch(-1)
            #time.sleep(0.2)
            dash.head_pitch(1)
            time.sleep(0.2)
            i += 1

        angle = 0
        dash.head_yaw(angle)
        time.sleep(2)





def checkColor(dash, speaker):
    speakerID1 = 1
    speakerID2 = 2
    speakerID3 = 3
    if speaker == speakerID1: # red
        return "red"
    if speaker == speakerID2: # yellow
        return "yellow"
    if speaker == speakerID3: # blue
        return "blue"


def checkTurnmovement (actualSpeaker, nextSpeaker, slowPace):
    speakerID1 = 1
    speakerID2 = 2
    speakerID3 = 3

    angle = 120

    if slowPace :  # slower pace, inclusive configuration
        driveDist = 200
        driveSpeed = 100
    else :
        driveDist = 200
        driveSpeed = 200

    if (actualSpeaker == speakerID1):
        if (nextSpeaker == speakerID3):

            return driveDist, driveSpeed,angle
        else:
            angle = -1*angle
            return driveDist, driveSpeed,angle

    if (actualSpeaker == speakerID2) :
        if (nextSpeaker == speakerID1):
            return driveDist, driveSpeed,angle
        else:
            angle = -1*angle
            return driveDist, driveSpeed,angle

    if (actualSpeaker == speakerID3) :
        if (nextSpeaker == speakerID2):
            return driveDist, driveSpeed,angle
        else:
            angle = -1*angle
            return driveDist, driveSpeed,angle

def checkHeadmovement (suggestedSpeaker, actualSpeaker):
    speakerID1 = 1
    speakerID2 = 2
    speakerID3 = 3

    angle = 50

    if (suggestedSpeaker == actualSpeaker):
        angle = 0
        return angle

    if (suggestedSpeaker == speakerID1):
        if (actualSpeaker == speakerID3):
            return angle
        else:
            angle = -1*angle
            return angle

    if (suggestedSpeaker == speakerID2) :
        if (actualSpeaker == speakerID1):
            return angle
        else:
            angle = -1*angle
            return angle

    if (suggestedSpeaker == speakerID3) :
        if (actualSpeaker == speakerID2):
            return angle
        else:
            angle = -1*angle
            return angle
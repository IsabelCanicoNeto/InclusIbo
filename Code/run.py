import argparse
import pathlib
from random import getrandbits
import matplotlib.pyplot as plt

from vadSpeech import *
from activityRobotAll import *
import numpy as np



def handle_int(sig, chunk):
    global leave, got_a_sentence
    leave = True
    got_a_sentence = True

# ############ #
# Presentation #
# ############ #



def plotmic(timeline, mic1_logs, mic2_logs, mic3_logs, ylabel, name):
    plt.clf()
    plt.xlabel('Microphones')
    plt.ylabel(ylabel)
    plt.plot(timeline, mic1_logs)
    plt.plot(timeline, mic1_logs)
    plt.plot(timeline, mic1_logs)
    plt.title(name)
    plt.savefig('%s.pdf' % name, bbox_inches='tight')
    plt.close()


def plotactivity(timeline, activty_logs, robot_log,  ylabel, name):
    plt.clf()
    plt.xlabel('Activity')
    plt.ylabel(ylabel)
    plt.plot(timeline, activty_logs, robot_log)
    plt.title(name)
    plt.savefig('%s.pdf' % name, bbox_inches='tight')
    plt.close()


def  plotrobotactivity(robot_log, ylabel, name):
    plt.clf()
    plt.xlabel('Robot Expression ')
    plt.ylabel(ylabel)
    plt.plot(timeline, robot_logs)
    plt.title(name)
    plt.savefig('%s.pdf' % name, bbox_inches='tight')
    plt.close()

#===============================================================================
#
#                                   MAIN
#
#===============================================================================


# signal.signal(signal.SIGINT, handle_int)
def main():


    # ####################
    # 1 - Configuration  #
    # ####################

    parser = argparse.ArgumentParser()

    parser.add_argument('condition', choices=[
        'encouragedriven',
        'control',
        "baseline",
        "followdriven"

    ], help="Which condition should the activity run?", default='encouragedriven')

    parser.add_argument('-numspeakers', help="Number of children speaking", type=int, default=3)
    parser.add_argument('-sessionDuration', help="Maximimum duration time (s) ", type=int, default=210) #1200 20m 600 10m

    # VAD configurations
    #parser.add_argument('-deviceIDs', help="Mics IDs used.", nargs="+", default=[1, 2, 3])
    parser.add_argument('-numdevices', help="Number of input mics in PC ", type=int, default=5)
    parser.add_argument('-silenceDb', help="Max db allowed to assume nonspeaking per speaker", nargs="+", default=[40.0, 40.0, 40.0])
#    parser.add_argument('-speakerTolerance', help="Number of padding to assume a speaker change (s) ", type=int, default=15)
#    parser.add_argument('-overlapTolerance', help="Number of chunks to assume an overlap (s)", type=int, default=10)

    # Robot Parameters
    parser.add_argument('-cID', help="id the child ", nargs="+", default=[1, 2, 3])
    parser.add_argument('-grpID', help="id of the group ", type=int, default=1)
    parser.add_argument('-name', help="sound with name of the child for explicit reference", nargs="+", default=["my8", "my9", "my10"])
    #parser.add_argument('-idleTime', type=float, help="Time to maintain idle stage (s)", default=5.0)
    #parser.add_argument('-mixedupTime', type=float, help="Time to maintain mixedup stage (s)", default=10.0)
    #parser.add_argument('-confusedTime', type=float, help="Time to maintain confused stage (s)", default=10.0)
    #parser.add_argument('-maxspeechTime', type=float, help="Max time to maintain speechTime per user (s)", default=150.0) # 2.5 minutos



    # Miscellaneous
    parser.add_argument('-save_logs', default = True , help='Whether or not to log activity ')
    parser.add_argument('-debug_active', default = True , help='Whether or not to debug activity ')

    opt = parser.parse_args()

    # study condition
    condition = opt.condition

    endSession = False


    # init robot
    StartTime = time.time()
    activity = activityRobot(start_time = StartTime,
                             condition=condition,
                             speakerID1 = 1,
                             speakerID2 = 2,
                             speakerID3 = 3,
                             name1 = opt.name[0],
                             name2 = opt.name[1],
                             name3 = opt.name[2],
                             cID1 = opt.cID[0],
                             cID2 = opt.cID[1],
                             cID3 = opt.cID[2],
                             grpID = opt.grpID,
                             state="empty",
                             p = opt.debug_active)
    # init microphones
    print ("StartTime")
    print (StartTime)
    print (datetime.datetime.now())
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    print(f"Current Time {current_time}")
    print(f"silence db  {opt.silenceDb[0]}")

    result_directory = f"results/{opt.condition}/{opt.grpID}"
    pathlib.Path(result_directory).mkdir(parents=True, exist_ok=True)
    speakersfile1 = f"{result_directory}/{opt.grpID}_{StartTime}{opt.condition}{opt.cID[0]}"
    speakersfile2 = f"{result_directory}/{opt.grpID}_{StartTime}{opt.condition}{opt.cID[1]}"
    speakersfile3 = f"{result_directory}/{opt.grpID}_{StartTime}{opt.condition}{opt.cID[2]}"
    #create Vad objects - mics
    mic1 = vadSpeech(numdevices=5, micID = 1, micIDname="Red", start_time=StartTime, silenceDb=opt.silenceDb[0], filename_wave=speakersfile1, activity=activity, condition= condition)
    mic2 = vadSpeech(numdevices=5, micID = 2, micIDname="Yellow", start_time=StartTime, silenceDb=opt.silenceDb[1], filename_wave=speakersfile2, activity=activity, condition= condition)
    mic3 = vadSpeech(numdevices=5, micID = 3, micIDname="Blue",  start_time=StartTime, silenceDb=opt.silenceDb[2], filename_wave=speakersfile3, activity=activity, condition= condition)


    # update diferent mics . one per child
    mic1.other_mic1 = mic2
    mic1.other_mic2 = mic3
    mic1.other_mic1ID = 2
    mic1.other_mic2ID = 3
    mic2.other_mic1 = mic1
    mic2.other_mic2 = mic3
    mic2.other_mic1ID = 1
    mic2.other_mic2ID = 3
    mic3.other_mic1 = mic1
    mic3.other_mic2 = mic2
    mic3.other_mic1ID = 1
    mic3.other_mic2ID = 2




    if  condition != "baseline" and not activity.robot.dash.is_connected :
        print ("\n robot disconnected")
        endSession = True

    else :
        endSession = False
        #start detecting sound
        if  condition != "baseline" and activity.robot.dash.is_connected :
            activity.warningstart()
            if not activity.organicspeech : activity.func("firstspeaker")
            #activity.firstround = False
            #StartTime = time.time()

    print ("detect thread")
    mic1.detect_background()
    mic2.detect_background()
    mic3.detect_background()




    # end detecting sound

    endWsession = False
    while not endSession :

        sessionRealDur = time.time() - StartTime
        #if (sessionRealDur >= (opt.sessionDuration - 10)) and not endWsession:
        #    endWsession = True
        #    activity.func("goodbye")
        if sessionRealDur >= opt.sessionDuration:
            endSession = True
            print("stop detecting")
            mic1.leave = True
            mic2.leave = True
            mic3.leave = True
        else :
            if condition != "baseline":
                if (activity.lastround == False ) and (sessionRealDur >= (opt.sessionDuration - 60)): # todo config time for last minute
                       print("ACT: START LAST MINUTE ")
                       activity.lastround = True
                       activity.warninglastminute()

            #mic1.leave = True
            #mic2.leave = True
            #mic3.leave = True


    mic1.stop_detecting()
    mic2.stop_detecting()
    mic3.stop_detecting()
    time.sleep(5)

    if condition != "baseline" and activity.robot.dash.is_connected : activity.func("end")


    EndTime = time.time()
    print (datetime.datetime.now())
    t = time.localtime()
    endcurrent_time = time.strftime("%H:%M:%S", t)
    print(f"End Time {endcurrent_time}")


    # print speech metrics

    if opt.debug_active:
        mic1.printMicMetrics()
        mic2.printMicMetrics()
        mic3.printMicMetrics()
        activity.printActMetrics()
    if opt.save_logs :
        mic1_logs = []
        mic2_logs = []
        mic3_logs = []
        activity_logs = []
        robot_logs = []
        mic1_logsdb = []
        mic2_logsdb =[]
        mic3_logsdb = []
        mic1_logslist = []
        mic2_logslist =[]
        mic3_logslist = []
        mic1_logs, mic1_logslist, mic1_logsdb = mic1.logMicMetrics()
        mic2_logs, mic2_logslist, mic2_logsdb = mic2.logMicMetrics()
        mic3_logs, mic3_logslist, mic3_logsdb = mic3.logMicMetrics()
        activity_logs = activity.logActMetrics()


    # ############### #
    # 4 - Plot & Save #
    # ############### #

    if opt.save_logs:

        unique_id = getrandbits(64)

        print(f"*** Plotting and saving activity logs ***", end="", flush=True)
        # todo : if there is an additional condition add to the directory // add robot information
        plot_directory = f"plots/{opt.condition}/{opt.condition}/{opt.grpID}/"
        pathlib.Path(plot_directory).mkdir(parents=True, exist_ok=True)

        # todo : plots // add robot information
        # plotmic(timeline, mic1_logs, mic2_logs, mic3_logs, ylabel='Microphone', name=f"{plot_directory}/microphone_{unique_id}")
        # plotactivity(timeline, activity_logs, activity.robot_log, ylabel='Activity', name=f"{plot_directory}/activity_{unique_id}")
        # plotrobotactivity(timeline, activity.robot_log, ylabel='Robot Expression', name=f"{plot_directory}/activityrobot_{unique_id}")

        result_directory = f"results/{opt.condition}/{opt.grpID}/"
        pathlib.Path(result_directory).mkdir(parents=True, exist_ok=True)

        with open(f"{result_directory}/final_logs_{opt.condition}{opt.grpID}_{StartTime}.txt", "w") as text_file:
            text_file.write(f"{opt.condition},{current_time},{endcurrent_time},{opt.grpID},{opt.cID[0]},{opt.cID[1]},{opt.cID [2]}, {StartTime} - {EndTime}  ")

        print ("data frames ")
        print (mic1_logs)
        print (mic2_logs)
        print (mic3_logs)
        print (activity_logs)
        print (activity.robot_log)


        np.savetxt(result_directory + f"/mic1_logs_{opt.grpID}_{StartTime}.csv", mic1_logs,delimiter=',', fmt = '%s')
        np.savetxt(result_directory + f"/mic2_logs_{opt.grpID}_{StartTime}.csv", mic2_logs,delimiter=',', fmt = '%s')
        np.savetxt(result_directory + f"/mic3_logs_{opt.grpID}_{StartTime}.csv", mic3_logs,delimiter=',', fmt = '%s')
        np.savetxt(result_directory + f"/mic1_logsspeech_{opt.grpID}_{StartTime}.csv", mic1_logslist,delimiter=',', fmt = '%s')
        np.savetxt(result_directory + f"/mic2_logsspeech_{opt.grpID}_{StartTime}.csv", mic2_logslist,delimiter=',', fmt = '%s')
        np.savetxt(result_directory + f"/mic3_logsspeech_{opt.grpID}_{StartTime}.csv", mic3_logslist,delimiter=',', fmt = '%s')
        np.savetxt(result_directory + f"/mic1_logsdb_{opt.grpID}_{StartTime}.csv", mic1_logsdb ,delimiter=',', fmt = '%s')
        np.savetxt(result_directory + f"/mic2_logsdb_{opt.grpID}_{StartTime}.csv", mic2_logsdb ,delimiter=',', fmt = '%s')
        np.savetxt(result_directory + f"/mic3_logsdb_{opt.grpID}_{StartTime}.csv", mic3_logsdb ,delimiter=',', fmt = '%s')
        #np.save(result_directory + f"/mic2_logs_{StartTime}.npy", np.array(mic2_logs, dtype=object))
        #np.save(result_directory + f"/mic3_logs_{StartTime}.npy", np.array(mic3_logs, dtype=object))
        np.savetxt(result_directory + f"/activity_logs_{opt.grpID}_{StartTime}.csv", activity_logs,delimiter=',', fmt = '%s')
        if condition != "baseline" :
            np.savetxt(result_directory + f"/SSflowrobot_logs_{opt.grpID}_{StartTime}.csv", activity.robot_log[1],delimiter=',', fmt = '%s')
            np.savetxt(result_directory + f"/Stateflowrobot_logs_{opt.grpID}_{StartTime}.csv", activity.robot_log[2],delimiter=',', fmt = '%s')
            np.savetxt(result_directory + f"/Expressionsrobot_logs_{opt.grpID}_{StartTime}.csv", activity.robot_log[3],delimiter=',', fmt = '%s')

        if not opt.debug_active : print(" (Done)\n", flush=True)



if __name__ == '__main__':
    main()
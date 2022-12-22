import os
import fnmatch
import pandas as pd
import time
from datetime import datetime
import numpy as np

column_names_c = ['Group', 'ChildID', 'Condition',

                  'RoleBystanderN_B', 'RoleBystanderT_B', 'RoleBystanderN_NORM_B', 'RoleBystanderT_NORM_B',
                  'RoleAdresseeN_B', 'RoleAdresseeT_B', 'RoleAdresseeN_NORM_B', 'RoleAdresseeT_NORM_B',
                  'RoleSpeakerN_B', 'RoleSpeakerT_B', 'RoleSpeakerN_NORM_B', 'RoleSpeakerT_NORM_B',
                  'RoleDecision makerN_B', 'RoleDecision makerT_B', 'RoleDecision makerN_NORM_B', 'RoleDecision makerT_NORM_B',

                  'IdeasownershipCreatorN_B',  'IdeasCreatedN_NORM_B',
                  'IdeasownershipFollowerN_B',  'IdeasFollowerN_NORM_B',
                  'IdeasownershipCo-creatorN_B', 'IdeasCo-creatorN_NORM_B',
                  'IdeasownershipOpposerN_B','IdeasOpposerN_NORM_B',
                  'IdeasownershipNegotiateN_B', 'IdeasNegotiateN_NORM_B',
                  'IdeasownershipCCreatorN_B', 'IdeasCCreatedN_NORM_B',
                  'Decisionownership_B',

                  'EngagementL2RobotN_B', 'EngagementL2RobotT_B', 'EngagementL2RobotN_NORM_B', 'EngagementL2RobotT_NORM_B',
                  'EngagementL2OtherN_B', 'EngagementL2OtherT_B', 'EngagementL2OtherN_NORM_B', 'EngagementL2OtherT_NORM_B',
                  'EngagementL2GroupN_B', 'EngagementL2GroupT_B', 'EngagementL2GroupN_NORM_B', 'EngagementL2GroupT_NORM_B',
                  'EngagementL2SpeakerN_B', 'EngagementL2SpeakerT_B', 'EngagementL2SpeakerN_NORM_B',
                  'EngagementL2SpeakerT_NORM_B',
                  'EngagementL2BystanderN_B', 'EngagementL2BystanderT_B', 'EngagementL2BystanderN_NORM_B',
                  'EngagementL2BystanderT_NORM_B',
                  'EngagementL2AdresseeN_B', 'EngagementL2AdresseeT_B', 'EngagementL2AdresseeN_NORM_B',
                  'EngagementL2AdresseeT_NORM_B',

                  'GazeMVAL2VIN_B', 'GazeMVAL2VIT_B', 'GazeMVAL2VIN_NORM_B', 'GazeMVAL2VIT_NORM_B',
                  'GazeMVAL2OtherN_B', 'GazeMVAL2OtherT_B', 'GazeMVAL2OtherN_NORM_B', 'GazeMVAL2OtherT_NORM_B',
                  'GazeMVAL2RobotN_B', 'GazeMVAL2RobotT_B', 'GazeMVAL2RobotN_NORM_B', 'GazeMVAL2RobotT_NORM_B',
                  'GazeMVAL2NVIN_B', 'GazeMVAL2NVIT_B', 'GazeMVAL2NVIN_NORM_B', 'GazeMVAL2NVIT_NORM_B',
                  'GazeMVAL2GroupN_B', 'GazeMVAL2GroupT_B', 'GazeMVAL2GroupN_NORM_B', 'GazeMVAL2GroupT_NORM_B',

                  'ChildBehaviourAlonePN_B', 'ChildBehaviourAlonePT_B', 'ChildBehaviourAlonePN_NORM_B',
                  'ChildBehaviourAlonePT_NORM_B',
                  'ChildBehaviourAloneOffTaskN_B', 'ChildBehaviourAloneOffTaskT_B', 'ChildBehaviourAloneOffTaskN_NORM_B',
                  'ChildBehaviourAloneOffTaskT_NORM_B',
                  'ChildBehaviourPositeReinfN_B', 'ChildBehaviourPositeReinfT_B', 'ChildBehaviourPositeReinfN_NORM_B',
                  'ChildBehaviourPositeReinfT_NORM_B',
                  'ChildBehaviourNegativeReinfN_B', 'ChildBehaviourNegativeReinfT_B', 'ChildBehaviourNegativeReinfN_NORM_B',
                  'ChildBehaviourNegativeReinfT_NORM_B',
                  'ChildBehaviourRPositeReinfN_B', 'ChildBehaviourRPositeReinfT_B', 'ChildBehaviourRPositeReinfN_NORM_B',
                  'ChildBehaviourRPositeReinfT_NORM_B',
                  'ChildBehaviourRNegativeRN_B', 'ChildBehaviourRNegativeRT_B', 'ChildBehaviourRNegativeRN_NORM_B',
                  'ChildBehaviourRNegativeRT_NORM_B',
                  'ChildBehaviourEntryN_B', 'ChildBehaviourEntryT_B', 'ChildBehaviourEntryN_NORM_B',
                  'ChildBehaviourEntryT_NORM_B',
                  'ChildBehaviourPeerInterN_B', 'ChildBehaviourPeerInterT_B', 'ChildBehaviourPeerInterN_NORM_B',
                  'ChildBehaviourPeerInterT_NORM_B',
                  'ChildBehaviourOverlapN_B', 'ChildBehaviourOverlapT_B', 'ChildBehaviourOverlapN_NORM_B',
                  'ChildBehaviourOverlapT_NORM_B',
                  'ChildBehaviourRobotInterN_B', 'ChildBehaviourRobotInterT_B', 'ChildBehaviourRobotInterN_NORM_B',
                  'ChildBehaviourRobotInterT_NORM_B',
                  'ChildBehaviourFocusedRN_B', 'ChildBehaviourFocusedRT_B', 'ChildBehaviourFocusedRN_NORM_B',
                  'ChildBehaviourFocusedRT_NORM_B',
                  'ChildBehaviourMediatorN_B', 'ChildBehaviourMediatorT_B', 'ChildBehaviourMediatorN_NORM_B',
                  'ChildBehaviourMediatorT_NORM_B',


                  'SpeakT_DistMean_B',
                  'SpeakN_DistMean_B',
                  'IdeasCreatedN_DistMean_B',
                  'IdeasAcceptedN_DistMean_B',
                  'PraiseN_DistMean_B',
                  'CriticizeN_DistMean_B',
                  'MediatorN_DistMean_B',
                  'EngagementT_DistMean_B',
                  'OverlapT_DistMean_B',
                  'ActiveEngageT_DistMean_B',
                  'EngageRobotT_DistMean_B',
                  'DisEngageT_DistMean_B',
                  'RoleBystanderN_DistMean_B',
                  'RoleAdresseeN_DistMean_B',


                  'GazeRobotN_DistMean_B',
                  'GazeOtherN_DistMean_B',
                  'GazeGroupN_DistMean_B',
                  'GazeSpeakerN_DistMean_B',
                  'GazeBystanderN_DistMean_B',
                  'GazeAdresseeN_DistMean_B',
                  'SpeakerT_PERC_B',
                    'GazeMVAL2VIN_PERC',
                  'GazeMVAL2VIT_PERC',
                  'GazeMVAL2NVIN_PERC',
                  'GazeMVAL2NVIT_PERC',

                  'GazeMVAL2GroupN_PERC',
                  'GazeMVAL2GroupT_PERC',

                  'GazeMVAL2OtherN_PERC',
                  'GazeMVAL2OtherT_PERC',
                  'ActiveEngageT_NORM_B',
                  'EngagementChildT_NORM_B',
                  'SilenceT_NORM_B',
                  'IdeasCreatedT_NORM_B',
                  'IdeasCreatedT_DistMean_B',
                  'RoleBystanderT_DistMean_B',
                  'RoleAdresseeT_DistMean_B',
                  'RPraiseN_DistMean_B'

                  ]


column_names_g = ['Group', 'Condition',

                            'RobotInfluencesConvTEN_B',	'RobotInfluencesConvTET_B',
                            'RobotInfluencesConvTimeKeeperN_B',	'RobotInfluencesConvTimeKeeperT_B',
                            'RobotIgnoredN_B',	'RobotIgnoredT_B',
                            'RobotPlayNoDistractionN_B',	'RobotPlayNoDistractionT_B',
                            'RobotNoImpactN_B',	'RobotNoImpactT_B',
                            'RobotAuthorityN_B',	'RobotAuthorityT_B',
                            'RobotAsaDistractionN_B',	'RobotAsaDistractionT_B',
                            'RobotPerceivedUnFairN_B',	'RobotPerceivedUnFairT_B',
                            'RobotPerceivedFairN_B',	'RobotPerceivedFairT_B',

                            'GrpAutonomyResearcherDrivenN_B', 'GrpAutonomyResearcherDrivenT_B',
                            'GrpAutonomyChildrenDrivenN_B', 'GrpAutonomyChildrenDrivenT_B',
                            'GrpAutonomyRobotDrivenN_B', 'GrpAutonomyRobotDrivenT_B',

                            'DecisionCollectiveN_B', 'DecisionCollectiveT_B',
                            'DecisionIndividualN_B', 'DecisionIndividualT_B',
                            'DecisionNoDecisionN_B', 'DecisionNoDecisionT_B',
                            'DecisionNotenoughttimeN_B', 'DecisionNotenoughttimeT_B',


                            'SpeakT_Total_gr_B' , 'SpeakT_Mean_gr_B', 'SpeakT_DistMean_gr_B',
                            'SpeakN_Total_gr_B' , 'SpeakN_Mean_gr_B', 'SpeakN_DistMean_gr_B',

                            'IdeasCreatedN_Total_gr_B', 'IdeasCreatedN_Mean_gr_B', 'IdeasCreatedN_DistMean_gr_B',
                            'IdeasAcceptedN_Total_gr_B', 'IdeasAcceptedN_Mean_gr_B' , 'IdeasAcceptedN_DistMean_gr_B' ,

                            'PraiseN_Total_gr_B', 'PraiseN_Mean_gr_B' ,  'PraiseN_DistMean_gr_B',

                            'EngagementT_Total_gr_B', 'EngagementT_Mean_gr_B', 'EngagementT_DistMean_gr_B',

                            'OverlapT_Total_gr_B', 'OverlapT_Mean_gr_B', 'OverlapT_DistMean_gr_B',

                            'CriticizeN_Total_gr_B', 'CriticizeN_Mean_gr_B' ,'CriticizeN_DistMean_gr_B',
                           'MediatorN_Total_gr_B', 'MediatorN_Mean_gr_B', 'MediatorN_DistMean_gr_B',
                             'ActiveEngageT_Total_gr_B', 'ActiveEngageT_Mean_gr_B', 'ActiveEngageT_DistMean_gr_B',
                  'EngageRobotT_Total_gr_B', 'EngageRobotT_Mean_gr_B', 'EngageRobotT_DistMean_gr_B',
                  'DisEngageT_Total_gr_B', 'DisEngageT_Mean_gr_B', 'DisEngageT_DistMean_gr_B',
                  'RoleBystanderN_Total_gr_B', 'RoleBystanderN_Mean_gr_B', 'RoleBystanderN_DistMean_gr_B',
                  'RoleAdresseeN_Total_gr_B', 'RoleAdresseeN_Mean_gr_B', 'RoleAdresseeN_DistMean_gr_B',
                  'GazeRobotN_Total_gr_B', 'GazeRobotN_Mean_gr_B', 'GazeRobotN_DistMean_gr_B',
                  'GazeOtherN_Total_gr_B', 'GazeOtherN_Mean_gr_B', 'GazeOtherN_DistMean_gr_B',
                  'GazeGroupN_Total_gr_B', 'GazeGroupN_Mean_gr_B', 'GazeGroupN_DistMean_gr_B',
                  'GazeSpeakerN_Total_gr_B', 'GazeSpeakerN_Mean_gr_B', 'GazeSpeakerN_DistMean_gr_B',
                  'GazeBystanderN_Total_gr_B', 'GazeBystanderN_Mean_gr_B', 'GazeBystanderN_DistMean_gr_B',
                  'GazeAdresseeN_Total_gr_B', 'GazeAdresseeN_Mean_gr_B', 'GazeAdresseeN_DistMean_gr_B',



                  'DecisionDurT_B', 'NGrpAutonomy_B',

                  'GrpAutonomyResearcherDrivenN_NORM_B', 'GrpAutonomyRobotDrivenN_NORM_B', 'GrpAutonomyChildrenDrivenN_NORM_B',
                  'GrpAutonomyChildrenDrivenT_NORM_B', 'GrpAutonomyResearcherDrivenT_NORM_B', 'GrpAutonomyRobotDrivenT_NORM_B',


                  'RobotInfluencesConvTEN_NORM_B',
                 'RobotInfluencesConvTET_NORM_B',

            'RobotInfluencesConvTimeKeeperN_NORM_B',
            'RobotInfluencesConvTimeKeeperT_NORM_B',

            'RobotIgnoredN_NORM_B',
            'RobotIgnoredT_NORM_B',

            'RobotPlayNoDistractionN_NORM_B',
            'RobotPlayNoDistractionT_NORM_B',

            'RobotNoImpactN_NORM_B',
            'RobotNoImpactT_NORM_B',

            'RobotAuthorityN_NORM_B',
            'RobotAuthorityT_NORM_B',

            'RobotAsaDistractionN_NORM_B',
            'RobotAsaDistractionT_NORM_B',

            'RobotPerceivedUnFairnesMsN_NORM_B',
            'RobotPerceivedUnFairnessT_NORM_B',

            'RobotPerceivedFairN_NORM_B',
            'RobotPerceivedFairT_NORM_B',

            'EngagementT_NORM_gr_B',
            'ActiveEngageT_NORM_gr_B',
            'PraiseN_NORM_gr_B',
            'PeerInterN_NORM_gr_B',
            'RobotActiveEngageT_NORM_gr_B',
            'SilenceT_Total_gr_B',

            'TEN_gr_B',
            'TEOrgN_gr_B',
            'TEManN_gr_B',
            'TEN_NORM_gr_B',
            'TEOrgN_NORM_gr_B',
            'TEManN_NORM_gr_B',

            'TEFairN_gr_B',
            'TEUnFairN_gr_B',
            'TEFairOutN_gr_B',

            'TEFairN_NORM_gr_B',
            'TEUnFairN_NORM_gr_B',
            'TEFairOutN_NORM_gr_B',

            'RIgnoreReasonN_gr_B',
            'RDistractionN_gr_B',
            'RUnfairN_gr_B',
            'RFluidSpeechN_gr_B',
            'ROtherN_gr_B',
            'RNotIgnoredN_gr_B',
            'RShyN_gr_B',

            'RIgnoreReasonN_NORM_gr_B',
            'RDistractionN_NORM_gr_B',
            'RUnfairN_NORM_gr_B',
            'FluidSpeechN_NORM_gr_B',
            'ROtherN_NORM_gr_B',
            'RNotIgnoredN_NORM_gr_B',
            'RShyN_NORM_gr_B',
            'IdeasCreatedT_Total_gr_B', 'IdeasCreatedT_Mean_gr_B', 'IdeasCreatedT_DistMean_gr_B',
                  'RoleBystanderT_Total_gr_B', 'RoleBystanderT_Mean_gr_B', 'RoleBystanderT_DistMean_gr_B',
                  'RoleAdresseeT_Total_gr_B', 'RoleAdresseeT_Mean_gr_B', 'RoleAdresseeT_DistMean_gr_B',
                   'RPraiseN_Total_gr_B', 'RPraiseN_Mean_gr_B', 'RPraiseN_DistMean_gr_B'

                  ]

df_c_B = pd.DataFrame(column_names_c)  # dataframe child
df_g_B = pd.DataFrame(column_names_g)  # dataframe group

df_c_E = pd.DataFrame(pd.Series(column_names_c).str.replace('_B', '_E'))
df_g_E = pd.DataFrame(pd.Series(column_names_g).str.replace('_B', '_E'))

df_c_F = pd.DataFrame(pd.Series(column_names_c).str.replace('_B', '_F'))
df_g_F = pd.DataFrame(pd.Series(column_names_g).str.replace('_B', '_F'))

global baseline
global encourage
global follow

global SpeakT_Total_gr
global SilenceT_Total_gr
global SpeakT_Mean_gr
global SpeakN_Total_gr
global SpeakN_Mean_gr
global IdeasCreatedN_Total_gr
global IdeasFollowerN_Total_gr
global IdeasOpposerN_Total_gr
global IdeasNegotiateN_Total_gr
global IdeasCreatedN_Mean_gr
global IdeasAcceptedN_Total_gr
global IdeasAcceptedN_Mean_gr

global PraiseN_Total_gr
global PraiseN_Mean_gr
global SpeakT_DistMean_gr
global SpeakN_DistMean_gr
global IdeasCreatedN_DistMean_gr
global IdeasAcceptedN_DistMean_gr
global PraiseN_DistMean_gr
global EngagementT_Total_gr
global EngagementT_Mean_gr
global EngagementT_DistMean_gr
global OverlapT_DistMean_gr
global OverlapT_Mean_gr
global OverlapT_Total_gr
global IdeasCreatedT_DistMean_gr
global RoleBystanderT_DistMean_gr
global RoleAdresseeT_DistMean_gr
global IdeasCreatedT_Total_gr
global RoleBystanderT_Total_gr
global RoleAdresseeT_Total_gr
global RPraiseN_Total_gr
global RPraiseN_Mean_gr
global RPraiseN_DistMean_gr

global IdeasCreatedT_Mean_gr
global RoleBystanderT_Mean_gr
global RoleAdresseeT_Mean_gr

global CriticizeN_DistMean_gr
global MediatorN_DistMean_gr
global ActiveEngageT_DistMean_gr
global EngageRobotT_DistMean_gr
global DisEngageT_DistMean_gr
global RoleBystanderN_DistMean_gr
global RoleAdresseeN_DistMean_gr

global GazeRobotN_DistMean_gr
global GazeOtherN_DistMean_gr
global GazeGroupN_DistMean_gr
global GazeSpeakerN_DistMean_gr
global GazeBystanderN_DistMean_gr
global GazeAdresseeN_DistMean_gr

global CriticizeN_Mean_gr
global MediatorN_Mean_gr
global ActiveEngageT_Mean_gr
global EngageRobotT_Mean_gr
global DisEngageT_Mean_gr
global RoleBystanderN_Mean_gr
global RoleAdresseeN_Mean_gr

global GazeRobotN_Mean_gr
global GazeOtherN_Mean_gr
global GazeGroupN_Mean_gr
global GazeSpeakerN_Mean_gr
global GazeBystanderN_Mean_gr
global GazeAdresseeN_Mean_gr

global CriticizeN_Total_gr
global MediatorN_Total_gr
global ActiveEngageT_Total_gr
global RobotActiveEngageT_Total_gr
global EngageRobotT_Total_gr
global DisEngageT_Total_gr
global RoleBystanderN_Total_gr
global RoleAdresseeN_Total_gr

global GazeRobotN_Total_gr
global GazeOtherN_Total_gr
global GazeGroupN_Total_gr
global GazeSpeakerN_Total_gr
global GazeBystanderN_Total_gr
global GazeAdresseeN_Total_gr

global SessionDur

global EngagementT_NORM_gr
global ActiveEngageT_NORM_gr
global RobotActiveEngageT_NORM
global PraiseN_NORM_gr
global PeerInterN_NORM_gr


global TEN_gr
global TEOrgN_gr
global TEManN_gr


global TEN_NORM_gr
global TEOrgN_NORM_gr
global TEManN_NORM_gr

global TEFairN_gr
global TEUnFairN_gr
global TEFairOutN_gr

global TEFairN_NORM_gr
global TEUnFairN_NORM_gr
global TEFairOutN_NORM_gr

global RIgnoreReasonN_gr
global RDistractionN_gr
global RUnfairN_gr
global RFluidSpeechN_gr
global ROtherN_gr
global RNotIgnoredN_gr
global RShyN_gr

global RIgnoreReasonN_NORM_gr
global RDistractionN_NORM_gr
global RUnfairN_NORM_gr
global FluidSpeechN_NORM_gr
global ROtherN_NORM_gr
global RNotIgnoredN_NORM_gr
global RShyN_NORM_gr




def pandaFile (filename, Grp, Condition):
    #df = pd.read_table(filename,header=None,sep=" ", encoding='windows-1252')
    #dateparse = lambda x: pd.datetime.strptime(x, '%H:%M:%S').time()
    # dateparse = lambda x: pd.datetime.strptime(x, '%H:%M:%S').time()
    temp_df=pd.read_csv(filename, sep='\s+', skipinitialspace = True) #, parse_dates=['time'],                 date_parser=dateparse)
    time_conv = temp_df['time']
    new_timelist = []
    for ind in time_conv.index:
        secs = time_conv[ind][6:11]
        mins = time_conv[ind][3:5]
        new_timelist.append(float(secs)+float(mins)*60)
    temp_df ['time'] = pd.Series(new_timelist) #in seconds
    if "Nave" in filename:
        activitynave = True
    else : activitynave = False
    #print (temp_df)
    ComputeGroupBalanceMetrics (Grp, 1, Condition, temp_df, activitynave)
    updateDataFrameChild (Grp, 1, Condition, temp_df, activitynave) #DataFrame df_c child 1
    updateDataFrameChild(Grp, 2, Condition, temp_df, activitynave)  # DataFrame df_c child 2
    updateDataFrameChild(Grp, 3, Condition, temp_df, activitynave)  # DataFrame df_c child 3
    updateDataFrameGrp(Grp, Condition, temp_df)  # DataFrame df_c child 3
    #c2 = getDataFrame(Grp, 2, True, Condition, temp_db)  # DataFrame df_c child 1
    #c3 = getDataFrame(Grp, 3, True, Condition, temp_db)  # DataFrame df_c child 1
    #group = getDataFrame (Grp, 0, False Condition, temp_db)   # DataFrame df_c child 1
    #print (temp_df)

    #print(df_c_B)
    #print(df_g_B)

    #print(df_c_E)
    #print(df_g_E)

    #print(df_c_F)
    #print(df_g_F)



def ComputeGroupBalanceMetrics (Group, ChildID, Condition, temp_df, activitynave):
    global SpeakT_Total_gr
    global SilenceT_Total_gr
    global SpeakT_Mean_gr
    global SpeakN_Total_gr
    global SpeakN_Mean_gr
    global IdeasCreatedN_Total_gr
    global IdeasFollowerN_Total_gr
    global IdeasOpposerN_Total_gr
    global IdeasNegotiateN_Total_gr
    global IdeasCreatedN_Mean_gr
    global IdeasAcceptedN_Total_gr
    global IdeasAcceptedN_Mean_gr

    global PraiseN_Total_gr
    global PraiseN_Mean_gr
    global SpeakT_DistMean_gr
    global SpeakN_DistMean_gr
    global IdeasCreatedN_DistMean_gr
    global IdeasAcceptedN_DistMean_gr
    global PraiseN_DistMean_gr
    global EngagementT_Total_gr
    global EngagementT_Mean_gr
    global EngagementT_DistMean_gr
    global OverlapT_DistMean_gr
    global OverlapT_Mean_gr
    global OverlapT_Total_gr
    global IdeasCreatedT_DistMean_gr
    global RoleBystanderT_DistMean_gr
    global RoleAdresseeT_DistMean_gr
    global IdeasCreatedT_Total_gr
    global RoleBystanderT_Total_gr
    global RoleAdresseeT_Total_gr

    global IdeasCreatedT_Mean_gr
    global RoleBystanderT_Mean_gr
    global RoleAdresseeT_Mean_gr
    global RPraiseN_Total_gr
    global RPraiseN_Mean_gr
    global RPraiseN_DistMean_gr

    global CriticizeN_DistMean_gr
    global MediatorN_DistMean_gr
    global ActiveEngageT_DistMean_gr
    global EngageRobotT_DistMean_gr
    global DisEngageT_DistMean_gr
    global RoleBystanderN_DistMean_gr
    global RoleAdresseeN_DistMean_gr

    global GazeRobotN_DistMean_gr
    global GazeOtherN_DistMean_gr
    global GazeGroupN_DistMean_gr
    global GazeSpeakerN_DistMean_gr
    global GazeBystanderN_DistMean_gr
    global GazeAdresseeN_DistMean_gr

    global CriticizeN_Mean_gr
    global MediatorN_Mean_gr
    global ActiveEngageT_Mean_gr
    global EngageRobotT_Mean_gr
    global DisEngageT_Mean_gr
    global RoleBystanderN_Mean_gr
    global RoleAdresseeN_Mean_gr

    global GazeRobotN_Mean_gr
    global GazeOtherN_Mean_gr
    global GazeGroupN_Mean_gr
    global GazeSpeakerN_Mean_gr
    global GazeBystanderN_Mean_gr
    global GazeAdresseeN_Mean_gr

    global CriticizeN_Total_gr
    global MediatorN_Total_gr
    global ActiveEngageT_Total_gr
    global RobotActiveEngageT_Total_gr
    global EngageRobotT_Total_gr
    global DisEngageT_Total_gr
    global RoleBystanderN_Total_gr
    global RoleAdresseeN_Total_gr

    global GazeRobotN_Total_gr
    global GazeOtherN_Total_gr
    global GazeGroupN_Total_gr
    global GazeSpeakerN_Total_gr
    global GazeBystanderN_Total_gr
    global GazeAdresseeN_Total_gr

    global SessionDur

    global EngagementT_NORM_gr
    global ActiveEngageT_NORM_gr
    global RobotActiveENgageT_NORM
    global PraiseN_NORM_gr
    global PeerInterN_NORM_gr

    DecisionCollectiveN = \
        temp_df[(temp_df.value == "CollectiveDecision")].count()['value']
    DecisionCollectiveT = \
        temp_df[(temp_df.value == "CollectiveDecision")].sum()['time']

    DecisionIndividualN = \
        temp_df[(temp_df.value == "IndividualDecision")].count()['value']
    DecisionIndividualT = \
        temp_df[(temp_df.value == "IndividualDecision")].sum()['time']

    DecisionNoDecisionN = \
        temp_df[(temp_df.value == "NoDecision")].count()['value']
    DecisionNoDecisionT = \
        temp_df[(temp_df.value == "NoDecision")].sum()['time']

    DecisionNotenoughttimeN = \
        temp_df[(temp_df.value == "Notenoughttimetodecide")].count()['value']
    DecisionNotenoughttimeT = \
        temp_df[(temp_df.value == "Notenoughttimetodecide")].sum()['time']

    SessionDur = max(DecisionCollectiveT, DecisionIndividualT, DecisionNoDecisionT, DecisionNotenoughttimeT)


    if temp_df[(temp_df.code == "CR(1)-ChildData")].any(axis=None) :
        viChild = str(1)
    elif temp_df[(temp_df.code == "CY(2)-ChildData")].any(axis=None) :\
        viChild = str(2)
    else: viChild = str(3)

    print (f"viChild {viChild}")


    SpeakT_Total_gr = float(temp_df[temp_df.value == "Speaker"].sum()['time'])
    SpeakT_Mean_gr = SpeakT_Total_gr / 3
    SilenceT_Total_gr = 0.0

    print (f"SpeakT_Total_gr {SpeakT_Total_gr} {SpeakT_Mean_gr}")

    SpeakN_Total_gr = float(temp_df[temp_df.value == "Speaker"].count()['value'])
    SpeakN_Mean_gr = SpeakN_Total_gr / 3

    print(f"SpeakN_Total_gr {SpeakN_Total_gr} {SpeakN_Mean_gr}")

    IdeasCreatedN_Total_gr = float(temp_df[(temp_df.value == "Creator")].count()['value'])
    IdeasCreatedT_Total_gr = float(
        temp_df[(temp_df.value == "Creator") ].sum()['time'])

    IdeasFollowerN_Total_gr = float(temp_df[(temp_df.value == "Follower")].count()['value'])
    IdeasOpposerN_Total_gr = float(temp_df[(temp_df.value == "Opposer")].count()['value'])
    IdeasNegotiateN_Total_gr = float(temp_df[(temp_df.value == "Negotiate")].count()['value'])

    #IdeasCreatedN_Total_gr += float(temp_df["Creator" in temp_df.value].count()['value'])
    IdeasCreatedN_Mean_gr = IdeasCreatedN_Total_gr / 3
    IdeasCreatedT_Mean_gr = IdeasCreatedT_Total_gr / 3

    print(f"Ideas created group {IdeasCreatedN_Total_gr} {IdeasCreatedN_Mean_gr}")



    IdeasAcceptedN_Total_gr =  float(temp_df[(temp_df.code == "CY(2)-Decisionownership")].iloc[0]['value'])

    IdeasAcceptedN_Total_gr += float(temp_df[temp_df.code == "CV(1)-Decisionownership"].iloc[0]['value'])
    IdeasAcceptedN_Total_gr += float(temp_df[temp_df.code == "CB(3)-Decisionownership"].iloc[0]['value'])

    if activitynave:
        IdeasAcceptedN_Total_gr = IdeasAcceptedN_Total_gr / 5

    IdeasAcceptedN_Mean_gr = IdeasAcceptedN_Total_gr / 3

    print (f"Ideas accepted group {IdeasAcceptedN_Total_gr} {IdeasAcceptedN_Mean_gr}"  )

    """
    GazeVIF_Total_gr = temp_df[(gaze in temp_df.code) & (temp_df.value == "L2VI") & (viChild not in temp_df.code)].count()['value']
    GazeNVIF_Total_gr = \
    temp_df[(gaze in temp_df.code) & (temp_df.value == "L2NVI") & (viChild not in temp_df.code)].count()['value']

    GazeVIF_Mean_gr = GazeVIF_Total / 2 # 2 nv children
    GazeNVIF_Mean_gr = GazeNVIF_Total / 2

    GazeVIT_Total_gr = \
    temp_df[(gaze in temp_df.code) & (temp_df.value == "L2VI") & (viChild not in temp_df.code)].sum()['time']
    GazeNVIT_Total_gr = \
        temp_df[(gaze in temp_df.code) & (temp_df.value == "L2NVI") & (viChild not in temp_df.code)].sum()['time']

    GazeVIT_Mean_gr = GazeVIT_Total / 2  # 2 nv children
    GazeNVIT_Mean_gr = GazeNVIT_Total / 2

    """

    PraiseN_Total_gr =  temp_df[(temp_df.value == "PositiveReinforce")].count()['value']
    PraiseN_Mean_gr = PraiseN_Total_gr / 3

    RPraiseN_Total_gr = temp_df[(temp_df.value == "ReceivePositiveReinforce")].count()['value']
    RPraiseN_Mean_gr = RPraiseN_Total_gr / 3

    EngagementT_Total_gr = temp_df[(temp_df.value == "AlonePositive") | (temp_df.value == "EntryBehaviour") | (temp_df.value == "PeerInteractionNeutral")  | (temp_df.value == "Mediator")  ].sum()['time']
    EngagementT_Mean_gr = EngagementT_Total_gr / 3

    OverlapT_Total_gr = temp_df[(temp_df.value == "Overlap")].sum()['time']
    OverlapT_Mean_gr = OverlapT_Total_gr / 3

    CriticizeN_Total_gr =  temp_df[(temp_df.value == "NegativeReinforce")].count()['value']
    CriticizeN_Mean_gr = CriticizeN_Total_gr / 3


    MediatorN_Total_gr = temp_df[(temp_df.value == "Mediator")].count()['value']
    MediatorN_Mean_gr = MediatorN_Total_gr / 3

    ActiveEngageT_Total_gr = temp_df[(temp_df.value == "EntryBehaviour") | (
                temp_df.value == "PeerInteractionNeutral") | (temp_df.value == "Mediator")].sum()['time']
    ActiveEngageT_Mean_gr = ActiveEngageT_Total_gr / 3

    RobotActiveEngageT_Total_gr = temp_df[(temp_df.value == "EntryBehaviour") | (
            temp_df.value == "PeerInteractionNeutral") | (temp_df.value == "Mediator") | (temp_df.value == "Focusedonrobot") ].sum()['time']


    EngageRobotT_Total_gr = float(temp_df[(temp_df.value == "Robotinteraction") | (
            temp_df.value == "Focusedonrobot") ].sum()['time'])
    EngageRobotT_Mean_gr = EngageRobotT_Total_gr / 3

    DisEngageT_Total_gr = float(temp_df[(temp_df.value == "Robotinteraction") | (temp_df.value == "AloneOffTask") | (
            temp_df.value == "Focusedonrobot")].sum()['time'])
    DisEngageT_Mean_gr = DisEngageT_Total_gr / 3


    RoleBystanderN_Total_gr = temp_df[(temp_df.value == "Bystander")].count()['value']
    RoleBystanderN_Mean_gr = RoleBystanderN_Total_gr / 3

    RoleAdresseeN_Total_gr = temp_df[(temp_df.value == "Adressee")].count()['value']
    RoleAdresseeN_Mean_gr = RoleAdresseeN_Total_gr / 3

    RoleBystanderT_Total_gr = temp_df[(temp_df.value == "Bystander")].sum()['time']
    RoleBystanderT_Mean_gr = RoleBystanderT_Total_gr / 3

    RoleAdresseeT_Total_gr = temp_df[(temp_df.value == "Adressee")].sum()['time']
    RoleAdresseeT_Mean_gr = RoleAdresseeN_Total_gr / 3

    GazeRobotN_Total_gr = temp_df[(temp_df.code == "CY(2)-Engagement") & (temp_df.value == "L2Robot")].count()['value']
    GazeRobotN_Total_gr += temp_df[(temp_df.code == "CR(1)-Engagement") & (temp_df.value == "L2Robot")].count()['value']
    GazeRobotN_Total_gr += temp_df[(temp_df.code == "CB(3)-Engagement") & (temp_df.value == "L2Robot")].count()['value']
    GazeRobotN_Mean_gr = GazeRobotN_Total_gr /3

    GazeOtherN_Total_gr = temp_df[(temp_df.code == "CY(2)-Engagement") & (temp_df.value == "L2Other")].count()['value']
    GazeOtherN_Total_gr += temp_df[(temp_df.code == "CR(1)-Engagement") & (temp_df.value == "L2Other")].count()['value']
    GazeOtherN_Total_gr += temp_df[(temp_df.code == "CB(3)-Engagement") & (temp_df.value == "L2Other")].count()['value']
    GazeOtherN_Mean_gr = GazeOtherN_Total_gr / 3

    GazeSpeakerN_Total_gr = temp_df[(temp_df.code == "CY(2)-Engagement") & (temp_df.value == "L2Speaker")].count()[
        'value']
    GazeSpeakerN_Total_gr += temp_df[(temp_df.code == "CR(1)-Engagement") & (temp_df.value == "L2Speaker")].count()[
        'value']
    GazeSpeakerN_Total_gr += temp_df[(temp_df.code == "CB(3)-Engagement") & (temp_df.value == "L2Speaker")].count()[
        'value']
    GazeSpeakerN_Mean_gr = GazeSpeakerN_Total_gr / 3

    GazeGroupN_Total_gr = temp_df[(temp_df.code == "CY(2)-Engagement") & (temp_df.value == "L2Group")].count()['value']
    GazeGroupN_Total_gr += temp_df[(temp_df.code == "CR(1)-Engagement") & (temp_df.value == "L2Group")].count()[
        'value']
    GazeGroupN_Total_gr += temp_df[(temp_df.code == "CB(3)-Engagement") & (temp_df.value == "L2Group")].count()[
        'value']
    GazeGroupN_Mean_gr = GazeGroupN_Total_gr / 3

    GazeBystanderN_Total_gr = temp_df[(temp_df.code == "CY(2)-Engagement") & (temp_df.value == "L2Bystander")].count()['value']
    GazeBystanderN_Total_gr += temp_df[(temp_df.code == "CR(1)-Engagement") & (temp_df.value == "L2Bystander")].count()['value']
    GazeBystanderN_Total_gr += temp_df[(temp_df.code == "CB(3)-Engagement") & (temp_df.value == "L2Bystander")].count()['value']
    GazeBystanderN_Mean_gr = GazeBystanderN_Total_gr / 3

    GazeAdresseeN_Total_gr = temp_df[(temp_df.code == "CY(2)-Engagement") & (temp_df.value == "L2Adressee")].count()[
        'value']
    GazeAdresseeN_Total_gr += temp_df[(temp_df.code == "CR(1)-Engagement") & (temp_df.value == "L2Adressee")].count()[
        'value']
    GazeAdresseeN_Total_gr += temp_df[(temp_df.code == "CB(3)-Engagement") & (temp_df.value == "L2Adressee")].count()[
        'value']
    GazeAdresseeN_Mean_gr = GazeAdresseeN_Total_gr / 3

    print(f"Praise group {PraiseN_Total_gr} {PraiseN_Mean_gr}")

    SpeakT_DistMean_gr = 0.0

    SpeakN_DistMean_gr = 0.0

    IdeasCreatedN_DistMean_gr = 0.0

    RPraiseN_DistMean_gr = 0.0

    IdeasAcceptedN_DistMean_gr = 0.0

    PraiseN_DistMean_gr = 0.0

    EngagementT_DistMean_gr = 0.0

    OverlapT_DistMean_gr = 0.0

    CriticizeN_DistMean_gr = 0.0
    MediatorN_DistMean_gr = 0.0
    ActiveEngageT_DistMean_gr = 0.0
    EngageRobotT_DistMean_gr = 0.0
    DisEngageT_DistMean_gr = 0.0
    RoleBystanderN_DistMean_gr = 0.0
    RoleAdresseeN_DistMean_gr = 0.0

    GazeRobotN_DistMean_gr = 0.0
    GazeOtherN_DistMean_gr = 0.0
    GazeGroupN_DistMean_gr = 0.0
    GazeSpeakerN_DistMean_gr = 0.0
    GazeBystanderN_DistMean_gr = 0.0
    GazeAdresseeN_DistMean_gr = 0.0

    EngagementT_NORM_gr = 0.0
    ActiveEngageT_NORM_gr = 0.0
    RobotActiveEngageT_NORM = 0.0
    PraiseN_NORM_gr = 0.0
    PeerInterN_NORM_gr = 0.0

    IdeasCreatedT_DistMean_gr = 0.0
    RoleBystanderT_DistMean_gr = 0.0
    RoleAdresseeT_DistMean_gr = 0.0
    RPraiseN_DistMean_gr = 0,0



def updateDataFrameChild (Group, ChildID, Condition, temp_df, activitynave):
    global SpeakT_Total_gr
    global SilenceT_Total_gr
    global SpeakT_Mean_gr
    global SpeakN_Total_gr
    global SpeakN_Mean_gr
    global IdeasCreatedN_Total_gr
    global IdeasFollowerN_Total_gr
    global IdeasOpposerN_Total_gr
    global IdeasNegotiateN_Total_gr
    global IdeasCreatedN_Mean_gr
    global IdeasAcceptedN_Total_gr
    global IdeasAcceptedN_Mean_gr

    global PraiseN_Total_gr
    global PraiseN_Mean_gr
    global SpeakT_DistMean_gr
    global SpeakN_DistMean_gr
    global IdeasCreatedN_DistMean_gr
    global IdeasAcceptedN_DistMean_gr
    global PraiseN_DistMean_gr
    global EngagementT_Total_gr
    global EngagementT_Mean_gr
    global EngagementT_DistMean_gr
    global OverlapT_DistMean_gr
    global OverlapT_Mean_gr
    global OverlapT_Total_gr
    global IdeasCreatedT_DistMean_gr
    global RoleBystanderT_DistMean_gr
    global RoleAdresseeT_DistMean_gr
    global IdeasCreatedT_Total_gr
    global RoleBystanderT_Total_gr
    global RoleAdresseeT_Total_gr
    global RPraiseN_Total_gr
    global RPraiseN_Mean_gr
    global RPraiseN_DistMean_gr

    global IdeasCreatedT_Mean_gr
    global RoleBystanderT_Mean_gr
    global RoleAdresseeT_Mean_gr

    global CriticizeN_DistMean_gr
    global MediatorN_DistMean_gr
    global ActiveEngageT_DistMean_gr
    global EngageRobotT_DistMean_gr
    global DisEngageT_DistMean_gr
    global RoleBystanderN_DistMean_gr
    global RoleAdresseeN_DistMean_gr

    global GazeRobotN_DistMean_gr
    global GazeOtherN_DistMean_gr
    global GazeGroupN_DistMean_gr
    global GazeSpeakerN_DistMean_gr
    global GazeBystanderN_DistMean_gr
    global GazeAdresseeN_DistMean_gr

    global CriticizeN_Mean_gr
    global MediatorN_Mean_gr
    global ActiveEngageT_Mean_gr
    global EngageRobotT_Mean_gr
    global DisEngageT_Mean_gr
    global RoleBystanderN_Mean_gr
    global RoleAdresseeN_Mean_gr

    global GazeRobotN_Mean_gr
    global GazeOtherN_Mean_gr
    global GazeGroupN_Mean_gr
    global GazeSpeakerN_Mean_gr
    global GazeBystanderN_Mean_gr
    global GazeAdresseeN_Mean_gr

    global CriticizeN_Total_gr
    global MediatorN_Total_gr
    global ActiveEngageT_Total_gr
    global EngageRobotT_Total_gr
    global DisEngageT_Total_gr
    global RoleBystanderN_Total_gr
    global RoleAdresseeN_Total_gr

    global GazeRobotN_Total_gr
    global GazeOtherN_Total_gr
    global GazeGroupN_Total_gr
    global GazeSpeakerN_Total_gr
    global GazeBystanderN_Total_gr
    global GazeAdresseeN_Total_gr

    global SessionDur
    global PeerInterN_NORM_gr


    if ChildID == 1 :
        role = "CR(1)-Role"
        ideas = "CR(1)-Ideas"
        engagement = "CR(1)-Engagement"
        gaze = "CR(1)-Gaze"
        behaviour= "CR(1)-Behaviour"
        owner= "CV(1)-Decisionownership"


    elif ChildID == 2:
        role = "CY(2)-Role"
        ideas = "CY(2)-Ideas"
        engagement = "CY(2)-Engagement"
        gaze = "CY(2)-Gaze"
        behaviour= "CY(2)-Behaviour"
        owner = "CY(2)-Decisionownership"
    else:
        role = "CB(3)-Role"
        ideas = "CB(3)-Ideas"
        engagement = "CB(3)-Engagement"
        gaze = "CB(3)-Gaze"
        behaviour = "CB(3)-Behaviour"
        owner= "CB(3)-Decisionownership"

    Decisionownership = float(temp_df[(temp_df.code == owner)].iloc[0]['value'])
    if activitynave :
          Decisionownership = Decisionownership / 5

    # T normal based on session duration; N normal based on role group
    RoleBystanderN=temp_df[(temp_df.code == role) & (temp_df.value == "Bystander")].count()['value']  # 'RoleBystanderN_B''RoleBystanderN_B'
    RoleBystanderT=temp_df[(temp_df.code == role) & (temp_df.value == "Bystander")].sum()['time']
    RoleBystanderN_NORM=   RoleBystanderN / RoleBystanderN_Total_gr
    RoleBystanderT_NORM=  RoleBystanderT / SessionDur

    RoleAdresseeN=temp_df[(temp_df.code == role) & (temp_df.value == "Adressee")].count()['value']
    RoleAdresseeT=temp_df[(temp_df.code == role) & (temp_df.value == "Adressee")].sum()['time']
    RoleAdresseeN_NORM=  RoleAdresseeN / RoleAdresseeN_Total_gr
    RoleAdresseeT_NORM =  RoleAdresseeT / SessionDur

    RoleSpeakerN = temp_df[(temp_df.code == role) & (temp_df.value == "Speaker")].count()['value']
    RoleSpeakerT = temp_df[(temp_df.code == role) & (temp_df.value == "Speaker")].sum()['time']
    RoleSpeakerN_NORM = RoleSpeakerN / SessionDur
    RoleSpeakerT_NORM = RoleSpeakerT / SessionDur
    SilenceTimeT_NORM = (SessionDur - RoleSpeakerT) / SessionDur



    # T normal based on session duration; N normal based on role group
    RoleDecisionmakerN = temp_df[(temp_df.code == role) & (temp_df.value == "Decisionmaker")].count()['value']
    RoleDecisionmakerT = temp_df[(temp_df.code == role) & (temp_df.value == "Decisionmaker")].sum()['time']
    RoleDecisionmakerN_NORM = 999.0
    RoleDecisionmakerT_NORM = RoleDecisionmakerT / SessionDur

    IdeasownershipCreatorN = temp_df[(temp_df.code == ideas) & (temp_df.value == "Creator")].count()['value']
    IdeasownershipFollowerN = temp_df[(temp_df.code == ideas) & (temp_df.value == "Follower")].count()['value']
    IdeasownershipCocreatorN = temp_df[(temp_df.code == ideas) & (temp_df.value == "Co-creator")].count()['value']
    IdeasownershipOpposerN = temp_df[(temp_df.code == ideas) & (temp_df.value == "Opposer")].count()['value']
    IdeasownershipNegotiateN = temp_df[(temp_df.code == ideas) & (temp_df.value == "Negotiate")].count()['value']
    IdeasownershipCreatorT = temp_df[(temp_df.code == ideas) & (temp_df.value == "Creator")].sum()['time']
    IdeasownershipCreatorT += temp_df[(temp_df.code == ideas) & (temp_df.value == "Co-creator")].sum()['time']
    # normal based on session duration
    IdeasCreatedN_NORM =  IdeasownershipCreatorN/ SessionDur
    IdeasFollowerN_NORM = IdeasownershipFollowerN/ SessionDur
    IdeasCocreatorN_NORM = IdeasownershipCocreatorN / SessionDur
    IdeasOpposerN_NORM = IdeasownershipOpposerN / SessionDur
    IdeasNegotiateN_NORM = IdeasownershipNegotiateN / SessionDur
    IdeasCCreatorN_NORM = (IdeasownershipCocreatorN + IdeasownershipCreatorN) / SessionDur

    IdeasCreatedT_NORM = IdeasownershipCreatorT / SessionDur


    # normal based on session duration
    EngagementL2RobotN = temp_df[(temp_df.code == engagement) & (temp_df.value == "L2Robot")].count()['value']
    EngagementL2RobotT = temp_df[(temp_df.code == engagement) & (temp_df.value == "L2Robot")].sum()['time']
    EngagementL2RobotN_NORM = EngagementL2RobotN / SessionDur
    EngagementL2RobotT_NORM = EngagementL2RobotT / SessionDur

    EngagementL2OtherN = temp_df[(temp_df.code == engagement) & (temp_df.value == "L2Other")].count()['value']
    EngagementL2OtherT = temp_df[(temp_df.code == engagement) & (temp_df.value == "L2Other")].sum()['time']
    EngagementL2OtherN_NORM = EngagementL2OtherN/ SessionDur
    EngagementL2OtherT_NORM = EngagementL2OtherT / SessionDur

    EngagementL2GroupN = temp_df[(temp_df.code == engagement) & (temp_df.value == "L2Group")].count()['value']
    EngagementL2GroupT = temp_df[(temp_df.code == engagement) & (temp_df.value == "L2Group")].sum()['time']
    EngagementL2GroupN_NORM = EngagementL2GroupN/ SessionDur
    EngagementL2GroupT_NORM= EngagementL2GroupT/ SessionDur

    EngagementL2SpeakerN = temp_df[(temp_df.code == engagement) & (temp_df.value == "L2Speaker")].count()['value']
    EngagementL2SpeakerT = temp_df[(temp_df.code == engagement) & (temp_df.value == "L2Speaker")].sum()['time']
    EngagementL2SpeakerN_NORM = EngagementL2SpeakerN/ SessionDur
    EngagementL2SpeakerT_NORM = EngagementL2SpeakerT/ SessionDur

    EngagementL2BystanderN = temp_df[(temp_df.code == engagement) & (temp_df.value == "L2Bystander")].count()['value']
    EngagementL2BystanderT = temp_df[(temp_df.code == engagement) & (temp_df.value == "L2Bystander")].sum()['time']
    EngagementL2BystanderN_NORM = EngagementL2BystanderN/ SessionDur
    EngagementL2BystanderT_NORM= EngagementL2BystanderT/ SessionDur

    EngagementL2AdresseeN = temp_df[(temp_df.code == engagement) & (temp_df.value == "L2Adressee")].count()['value']
    EngagementL2AdresseeT = temp_df[(temp_df.code == engagement) & (temp_df.value == "L2Adressee")].sum()['time']
    EngagementL2AdresseeN_NORM = EngagementL2AdresseeN/ SessionDur
    EngagementL2AdresseeT_NORM = EngagementL2AdresseeT/ SessionDur

    # norm based on duration

    GazeMVAL2VIN = float(temp_df[(temp_df.code == gaze) & (temp_df.value == "L2VI")].count()['value'])
    GazeMVAL2VIT= temp_df[(temp_df.code == gaze) & (temp_df.value == "L2VI")].sum()['time']
    GazeMVAL2VIN_NORM = GazeMVAL2VIN / SessionDur
    GazeMVAL2VIT_NORM = GazeMVAL2VIT /SessionDur

    GazeMVAL2OtherN = temp_df[(temp_df.code == gaze) & (temp_df.value == "L2Other")].count()['value']
    GazeMVAL2OtherT = temp_df[(temp_df.code == gaze) & (temp_df.value == "L2Other")].sum()['time']
    GazeMVAL2OtherN_NORM = GazeMVAL2OtherN / SessionDur
    GazeMVAL2OtherT_NORM = GazeMVAL2OtherT / SessionDur


    GazeMVAL2RobotN = temp_df[(temp_df.code == gaze) & (temp_df.value == "L2Robot")].count()['value']
    GazeMVAL2RobotT = temp_df[(temp_df.code == gaze) & (temp_df.value == "L2Robot")].sum()['time']
    GazeMVAL2RobotN_NORM = GazeMVAL2RobotN / SessionDur
    GazeMVAL2RobotT_NORM =  GazeMVAL2RobotT/ SessionDur

    GazeMVAL2NVIN = temp_df[(temp_df.code == gaze) & (temp_df.value == "L2NVI")].count()['value']
    GazeMVAL2NVIT = temp_df[(temp_df.code == gaze) & (temp_df.value == "L2NVI")].sum()['time']
    GazeMVAL2NVIN_NORM = GazeMVAL2NVIN / SessionDur
    GazeMVAL2NVIT_NORM = GazeMVAL2NVIN / SessionDur

    GazeMVAL2GroupN = temp_df[(temp_df.code == gaze) & (temp_df.value == "L2Group")].count()['value']
    GazeMVAL2GroupT = temp_df[(temp_df.code == gaze) & (temp_df.value == "L2Group")].sum()['time']
    GazeMVAL2GroupN_NORM = (GazeMVAL2GroupN +  GazeMVAL2VIN + GazeMVAL2NVIN) / SessionDur
    GazeMVAL2GroupT_NORM = (GazeMVAL2GroupT +  GazeMVAL2VIT + GazeMVAL2NVIT) / SessionDur



    # norm based on sessionDur

    ChildBehaviourAlonePN = temp_df[(temp_df.code == behaviour) & (temp_df.value == "AlonePositive")].count()['value']
    ChildBehaviourAlonePT = temp_df[(temp_df.code == behaviour) & (temp_df.value == "AlonePositive")].sum()['time']
    ChildBehaviourAlonePN_NORM = ChildBehaviourAlonePN/ SessionDur
    ChildBehaviourAlonePT_NORM = ChildBehaviourAlonePT/ SessionDur
    
    ChildBehaviourAloneOffTaskN = temp_df[(temp_df.code == behaviour) & (temp_df.value == "AloneOffTask")].count()[
        'value']
    ChildBehaviourAloneOffTaskT = temp_df[(temp_df.code == behaviour) & (temp_df.value == "AloneOffTask")].sum()['time']
    ChildBehaviourAloneOffTaskN_NORM = ChildBehaviourAloneOffTaskN/ SessionDur
    ChildBehaviourAloneOffTaskT_NORM = ChildBehaviourAloneOffTaskT/ SessionDur
    
    ChildBehaviourPositeReinfN = temp_df[(temp_df.code == behaviour) & (temp_df.value == "PositiveReinforce")].count()[
        'value']
    ChildBehaviourPositeReinfT = temp_df[(temp_df.code == behaviour) & (temp_df.value == "PositiveReinforce")].sum()[
        'time']
    ChildBehaviourPositeReinfN_NORM = ChildBehaviourPositeReinfN/ SessionDur
    ChildBehaviourPositeReinfT_NORM = ChildBehaviourPositeReinfT/ SessionDur
    
    ChildBehaviourNegativeReinfN = temp_df[(temp_df.code == behaviour) & (temp_df.value == "NegativeReinforce")].count()[
        'value']
    ChildBehaviourNegativeReinfT = temp_df[(temp_df.code == behaviour) & (temp_df.value == "NegativeReinforce")].sum()[
        'time']
    ChildBehaviourNegativeReinfN_NORM = ChildBehaviourNegativeReinfN/ SessionDur
    ChildBehaviourNegativeReinfT_NORM = ChildBehaviourNegativeReinfT/ SessionDur
    
    ChildBehaviourRPositeReinfN = \
    temp_df[(temp_df.code == behaviour) & (temp_df.value == "ReceivePositiveReinforce")].count()[
        'value']
    ChildBehaviourRPositeReinfT = \
    temp_df[(temp_df.code == behaviour) & (temp_df.value == "ReceivePositiveReinforce")].sum()[
        'time']
    ChildBehaviourRPositeReinfN_NORM = ChildBehaviourRPositeReinfN / SessionDur
    ChildBehaviourRPositeReinfT_NORM = ChildBehaviourRPositeReinfT/ SessionDur
    
    ChildBehaviourRNegativeRN = \
    temp_df[(temp_df.code == behaviour) & (temp_df.value == "ReceiveNegativeReinforce")].count()[
        'value']
    ChildBehaviourRNegativeRT = temp_df[(temp_df.code == behaviour) & (temp_df.value == "ReceiveNegativeReinforce")].sum()[
        'time']
    ChildBehaviourRNegativeRN_NORM = ChildBehaviourRNegativeRN/ SessionDur
    ChildBehaviourRNegativeRT_NORM = ChildBehaviourRNegativeRT/ SessionDur
    
    ChildBehaviourEntryN = \
        temp_df[(temp_df.code == behaviour) & (temp_df.value == "EntryBehaviour")].count()[
            'value']
    ChildBehaviourEntryT = \
        temp_df[(temp_df.code == behaviour) & (temp_df.value == "EntryBehaviour")].sum()[
            'time']
    ChildBehaviourEntryN_NORM = ChildBehaviourEntryN/ SessionDur
    ChildBehaviourEntryT_NORM = ChildBehaviourEntryT/ SessionDur
    
    ChildBehaviourPeerInterN = \
        temp_df[(temp_df.code == behaviour) & (temp_df.value == "PeerInteractionNeutral")].count()[
            'value']
    ChildBehaviourPeerInterT = \
        temp_df[(temp_df.code == behaviour) & (temp_df.value == "PeerInteractionNeutral")].sum()[
            'time']
    ChildBehaviourPeerInterN_NORM = ChildBehaviourPeerInterN / SessionDur
    ChildBehaviourPeerInterT_NORM = ChildBehaviourPeerInterT/ SessionDur

    PeerInterN_NORM_gr += ChildBehaviourPeerInterN_NORM
    
    ChildBehaviourOverlapN = \
        temp_df[(temp_df.code == behaviour) & (temp_df.value == "Overlap")].count()[
            'value']
    ChildBehaviourOverlapT = \
        temp_df[(temp_df.code == behaviour) & (temp_df.value == "Overlap")].sum()[
            'time']
    ChildBehaviourOverlapN_NORM = ChildBehaviourOverlapN/ SessionDur
    ChildBehaviourOverlapT_NORM = ChildBehaviourOverlapT/ SessionDur
    
    ChildBehaviourRobotInterN = \
        temp_df[(temp_df.code == behaviour) & (temp_df.value == "Robotinteraction")].count()[
            'value']
    ChildBehaviourRobotInterT = \
        temp_df[(temp_df.code == behaviour) & (temp_df.value == "Robotinteraction")].sum()[
            'time']
    ChildBehaviourRobotInterN_NORM = ChildBehaviourRobotInterN/ SessionDur
    ChildBehaviourRobotInterT_NORM = ChildBehaviourRobotInterT/ SessionDur
    
    ChildBehaviourFocusedRN = \
        temp_df[(temp_df.code == behaviour) & (temp_df.value == "Focusedonrobot")].count()[
            'value']
    ChildBehaviourFocusedRT = \
        temp_df[(temp_df.code == behaviour) & (temp_df.value == "Focusedonrobot")].sum()[
            'time']
    ChildBehaviourFocusedRN_NORM = ChildBehaviourFocusedRN/ SessionDur
    ChildBehaviourFocusedRT_NORM = ChildBehaviourFocusedRT/ SessionDur
    
    ChildBehaviourMediatorN = \
        temp_df[(temp_df.code == behaviour) & (temp_df.value == "Mediator")].count()[
            'value']
    ChildBehaviourMediatorT = \
        temp_df[(temp_df.code == behaviour) & (temp_df.value == "Mediator")].sum()[
            'time']
    ChildBehaviourMediatorN_NORM = ChildBehaviourMediatorN/ SessionDur
    ChildBehaviourMediatorT_NORM = ChildBehaviourMediatorT/ SessionDur

    EngagementChildT = ChildBehaviourMediatorT + ChildBehaviourAlonePT + ChildBehaviourEntryT + ChildBehaviourPeerInterT

    # Percentagem  por criança do tpo de gaze
    TotalGAZEN = GazeMVAL2NVIN + GazeMVAL2VIN + GazeMVAL2GroupN + GazeMVAL2OtherN + GazeMVAL2RobotN
    TotalGAZET = GazeMVAL2NVIT + GazeMVAL2VIT + GazeMVAL2GroupT + GazeMVAL2OtherT + GazeMVAL2RobotT

    GazeMVAL2VIN_PERC = GazeMVAL2VIN / TotalGAZEN
    GazeMVAL2VIT_PERC = GazeMVAL2VIT / (GazeMVAL2NVIT + GazeMVAL2VIT)

    GazeMVAL2NVIN_PERC = GazeMVAL2NVIN / TotalGAZEN
    GazeMVAL2NVIT_PERC = GazeMVAL2NVIN / TotalGAZET

    GazeMVAL2GroupN_PERC = GazeMVAL2GroupN / TotalGAZEN
    GazeMVAL2GroupT_PERC = GazeMVAL2GroupT / TotalGAZET

    GazeMVAL2OtherN_PERC = GazeMVAL2OtherN / TotalGAZEN
    GazeMVAL2OtherT_PERC = GazeMVAL2OtherT / TotalGAZET

    # Percentage of time , he is a speaker
    SpeakerT_PERC = RoleSpeakerT / SpeakT_Total_gr



    IdeasownershipCCreatedN = (IdeasownershipCreatorN +  IdeasownershipCocreatorN)
    IdeasCCreatedN_NORM = (IdeasownershipCCreatedN - IdeasCreatedN_Mean_gr) / IdeasCreatedN_Total_gr

    if IdeasFollowerN_Total_gr == 0.0:
        IdeasFollowerN_NORM = 0.0
    else : IdeasFollowerN_NORM = IdeasownershipFollowerN / IdeasFollowerN_Total_gr
    if IdeasOpposerN_Total_gr == 0.0:
        IdeasOpposerN_NORM = 0.0
    else:    IdeasOpposerN_NORM = IdeasownershipOpposerN / IdeasOpposerN_Total_gr
    if IdeasNegotiateN_Total_gr != 0.0 : IdeasNegotiateN_NORM = IdeasownershipNegotiateN / IdeasNegotiateN_Total_gr


    SpeakT_DistMean =  (RoleSpeakerT - SpeakT_Mean_gr)/ SpeakT_Total_gr
    SpeakN_DistMean = (RoleSpeakerN - SpeakN_Mean_gr)/ SpeakN_Total_gr

    SpeakT_DistMean_gr += abs(SpeakT_DistMean)
    SpeakN_DistMean_gr += abs(SpeakN_DistMean)

    # Dist Mean based on Total ideas from createor and co-creator
    IdeasCreatedN_DistMean = (IdeasownershipCCreatedN - IdeasCreatedN_Mean_gr) / IdeasCreatedN_Total_gr
    IdeasCreatedN_DistMean_gr += abs(IdeasCreatedN_DistMean)

    IdeasCreatedT_DistMean = (IdeasownershipCreatorT - IdeasCreatedT_Mean_gr) / IdeasCreatedT_Total_gr
    IdeasCreatedT_DistMean_gr += abs(IdeasCreatedT_DistMean)


    if IdeasAcceptedN_Total_gr != 0.0 :
        IdeasAcceptedN_DistMean =  (Decisionownership - IdeasAcceptedN_Mean_gr)/ IdeasAcceptedN_Total_gr
    else: IdeasAcceptedN_DistMean = 0.0
    IdeasAcceptedN_DistMean_gr  += abs(IdeasAcceptedN_DistMean)

    PraiseN_DistMean = (ChildBehaviourPositeReinfN - PraiseN_Mean_gr) / PraiseN_Total_gr
    PraiseN_DistMean_gr += abs(PraiseN_DistMean)


    RPraiseN_DistMean = (ChildBehaviourRPositeReinfN - RPraiseN_Mean_gr) / RPraiseN_Total_gr
    RPraiseN_DistMean_gr += abs(RPraiseN_DistMean)


    if  CriticizeN_Total_gr == 0.0 :
        CriticizeN_DistMean = 0.0
    else:
        CriticizeN_DistMean = (ChildBehaviourNegativeReinfN - CriticizeN_Mean_gr) / CriticizeN_Total_gr
    CriticizeN_DistMean_gr += abs (CriticizeN_DistMean)
    
    if MediatorN_Total_gr == 0.0:
        MediatorN_DistMean = 0.0
    else:
        MediatorN_DistMean = (ChildBehaviourMediatorN - MediatorN_Mean_gr) / MediatorN_Total_gr
    MediatorN_DistMean_gr += abs (MediatorN_DistMean)

    if OverlapT_Total_gr != 0.0:
        OverlapT_DistMean = (ChildBehaviourOverlapT - OverlapT_Mean_gr) / OverlapT_Total_gr
    else: OverlapT_DistMean = 0.0
    OverlapT_DistMean_gr += abs(OverlapT_DistMean)

    print (f"Overlap {OverlapT_DistMean_gr} {OverlapT_DistMean} ")

    # Participation inclui Alone PT 
    EngagementChildT = ChildBehaviourAlonePT + ChildBehaviourEntryT + ChildBehaviourPeerInterT + ChildBehaviourMediatorT
    EngagementT_DistMean = ( EngagementChildT - EngagementT_Mean_gr) / EngagementT_Total_gr
    EngagementT_DistMean_gr += abs(EngagementT_DistMean)
    EngagementChildT_NORM = EngagementChildT / SessionDur

    # Active participation 
    ActiveEngageChildT = ChildBehaviourEntryT + ChildBehaviourPeerInterT + ChildBehaviourMediatorT
    ActiveEngageT_DistMean = (ActiveEngageChildT - ActiveEngageT_Mean_gr ) / ActiveEngageT_Total_gr
    ActiveEngageT_DistMean_gr += abs (ActiveEngageT_DistMean)
    ActiveEngageT_NORM = ActiveEngageChildT  / SessionDur
    RobotActiveEngageT_NORM = (ActiveEngageChildT + ChildBehaviourRobotInterT) / SessionDur
    
    # Robot Interaction or Focus 
    EngageRobotChildT = ChildBehaviourRobotInterT + ChildBehaviourFocusedRT
    if EngageRobotT_Total_gr == 0.0:
        EngageRobotT_DistMean = (EngageRobotChildT - EngageRobotT_Mean_gr) / EngageRobotT_Total_gr
    else : EngageRobotT_DistMean = 0.0
    EngageRobotT_DistMean_gr += abs ( EngageRobotT_DistMean)

    # Alone Offtasks and  interacting with robot  
    DisEngageChildT = ChildBehaviourAloneOffTaskN + ChildBehaviourRobotInterN  + ChildBehaviourFocusedRT
    DisEngageT_DistMean=  (DisEngageChildT - DisEngageT_Mean_gr) / DisEngageT_Total_gr
    DisEngageT_DistMean_gr += abs (DisEngageT_DistMean)
    
    # distMean role 
    
    RoleBystanderN_DistMean =  (RoleBystanderN- RoleBystanderN_Mean_gr) / RoleBystanderN_Total_gr
    RoleBystanderN_DistMean_gr += abs(RoleBystanderN_DistMean)

    RoleAdresseeN_DistMean = (RoleAdresseeN - RoleAdresseeN_Mean_gr) / RoleAdresseeN_Total_gr
    RoleAdresseeN_DistMean_gr += abs(RoleAdresseeN_DistMean)

    RoleBystanderT_DistMean = (RoleBystanderT - RoleBystanderT_Mean_gr) / RoleBystanderT_Total_gr
    RoleBystanderT_DistMean_gr += abs(RoleBystanderT_DistMean)

    RoleAdresseeT_DistMean = (RoleAdresseeT - RoleAdresseeT_Mean_gr) / RoleAdresseeT_Total_gr
    RoleAdresseeT_DistMean_gr += abs(RoleAdresseeT_DistMean)

    
    # dist Mean gaze 
    GazeRobotN_DistMean = (EngagementL2RobotN - GazeRobotN_Mean_gr) / GazeRobotN_Total_gr
    GazeRobotN_DistMean_gr += abs(GazeRobotN_DistMean)
    
    GazeOtherN_DistMean = (EngagementL2OtherN - GazeOtherN_Mean_gr) / GazeOtherN_Total_gr
    GazeOtherN_DistMean_gr += abs(GazeOtherN_DistMean)
    
    GazeGroupN_DistMean= (EngagementL2GroupN - GazeGroupN_Mean_gr) / GazeGroupN_Total_gr
    GazeGroupN_DistMean_gr += abs(GazeGroupN_DistMean)
    
    GazeSpeakerN_DistMean= (EngagementL2SpeakerN - GazeSpeakerN_Mean_gr) / GazeSpeakerN_Total_gr
    GazeSpeakerN_DistMean_gr += abs(GazeSpeakerN_DistMean)

    GazeBystanderN_DistMean = (EngagementL2BystanderN - GazeBystanderN_Mean_gr) / GazeBystanderN_Total_gr
    GazeBystanderN_DistMean_gr += abs(GazeBystanderN_DistMean)

    GazeAdresseeN_DistMean = (EngagementL2AdresseeN - GazeAdresseeN_Mean_gr) / GazeAdresseeN_Total_gr
    GazeAdresseeN_DistMean_gr += abs(GazeAdresseeN_DistMean)



    df_temp = [ Group, ChildID, Condition,

                  RoleBystanderN, RoleBystanderT, RoleBystanderN_NORM, RoleBystanderT_NORM,
                  RoleAdresseeN, RoleAdresseeT, RoleAdresseeN_NORM, RoleAdresseeT_NORM,
                  RoleSpeakerN, RoleSpeakerT, RoleSpeakerN_NORM, RoleSpeakerT_NORM,
                  RoleDecisionmakerN, RoleDecisionmakerT, RoleDecisionmakerN_NORM, RoleDecisionmakerT_NORM,

                  IdeasownershipCreatorN,  IdeasCreatedN_NORM,
                  IdeasownershipFollowerN,  IdeasFollowerN_NORM,
                  IdeasownershipCocreatorN, IdeasCocreatorN_NORM,
                  IdeasownershipOpposerN,IdeasOpposerN_NORM,
                  IdeasownershipNegotiateN, IdeasNegotiateN_NORM,
                  IdeasownershipCCreatedN, IdeasCCreatedN_NORM,
                  Decisionownership,

                  EngagementL2RobotN, EngagementL2RobotT, EngagementL2RobotN_NORM, EngagementL2RobotT_NORM,
                  EngagementL2OtherN, EngagementL2OtherT, EngagementL2OtherN_NORM, EngagementL2OtherT_NORM,
                  EngagementL2GroupN, EngagementL2GroupT, EngagementL2GroupN_NORM, EngagementL2GroupT_NORM,
                  EngagementL2SpeakerN, EngagementL2SpeakerT, EngagementL2SpeakerN_NORM,
                  EngagementL2SpeakerT_NORM,
                  EngagementL2BystanderN, EngagementL2BystanderT, EngagementL2BystanderN_NORM,
                  EngagementL2BystanderT_NORM,
                  EngagementL2AdresseeN, EngagementL2AdresseeT, EngagementL2AdresseeN_NORM,
                  EngagementL2AdresseeT_NORM,

                  GazeMVAL2VIN, GazeMVAL2VIT, GazeMVAL2VIN_NORM, GazeMVAL2VIT_NORM,
                  GazeMVAL2OtherN, GazeMVAL2OtherT, GazeMVAL2OtherN_NORM, GazeMVAL2OtherT_NORM,
                  GazeMVAL2RobotN, GazeMVAL2RobotT, GazeMVAL2RobotN_NORM, GazeMVAL2RobotT_NORM,
                  GazeMVAL2NVIN, GazeMVAL2NVIT, GazeMVAL2NVIN_NORM, GazeMVAL2NVIT_NORM,
                  GazeMVAL2GroupN, GazeMVAL2GroupT, GazeMVAL2GroupN_NORM, GazeMVAL2GroupT_NORM,

                  ChildBehaviourAlonePN, ChildBehaviourAlonePT, ChildBehaviourAlonePN_NORM,
                  ChildBehaviourAlonePT_NORM,
                  ChildBehaviourAloneOffTaskN, ChildBehaviourAloneOffTaskT, ChildBehaviourAloneOffTaskN_NORM,
                  ChildBehaviourAloneOffTaskT_NORM,
                  ChildBehaviourPositeReinfN, ChildBehaviourPositeReinfT, ChildBehaviourPositeReinfN_NORM,
                  ChildBehaviourPositeReinfT_NORM,
                  ChildBehaviourNegativeReinfN, ChildBehaviourNegativeReinfT, ChildBehaviourNegativeReinfN_NORM,
                  ChildBehaviourNegativeReinfT_NORM,
                  ChildBehaviourRPositeReinfN, ChildBehaviourRPositeReinfT, ChildBehaviourRPositeReinfN_NORM,
                  ChildBehaviourRPositeReinfT_NORM,
                  ChildBehaviourRNegativeRN, ChildBehaviourRNegativeRT, ChildBehaviourRNegativeRN_NORM,
                  ChildBehaviourRNegativeRT_NORM,
                  ChildBehaviourEntryN, ChildBehaviourEntryT, ChildBehaviourEntryN_NORM,
                  ChildBehaviourEntryT_NORM,
                  ChildBehaviourPeerInterN, ChildBehaviourPeerInterT, ChildBehaviourPeerInterN_NORM,
                  ChildBehaviourPeerInterT_NORM,
                  ChildBehaviourOverlapN, ChildBehaviourOverlapT, ChildBehaviourOverlapN_NORM,
                  ChildBehaviourOverlapT_NORM,
                  ChildBehaviourRobotInterN, ChildBehaviourRobotInterT, ChildBehaviourRobotInterN_NORM,
                  ChildBehaviourRobotInterT_NORM,
                  ChildBehaviourFocusedRN, ChildBehaviourFocusedRT, ChildBehaviourFocusedRN_NORM,
                  ChildBehaviourFocusedRT_NORM,
                  ChildBehaviourMediatorN, ChildBehaviourMediatorT, ChildBehaviourMediatorN_NORM,
                  ChildBehaviourMediatorT_NORM,


                  SpeakT_DistMean,
                  SpeakN_DistMean,
                  IdeasCreatedN_DistMean,
                  IdeasAcceptedN_DistMean,
                  PraiseN_DistMean,
                  CriticizeN_DistMean,
                  MediatorN_DistMean,
                  EngagementT_DistMean,
                  OverlapT_DistMean,
                  ActiveEngageT_DistMean,
                  EngageRobotT_DistMean,
                  DisEngageT_DistMean,
                  RoleBystanderN_DistMean,
                  RoleAdresseeN_DistMean,


                  GazeRobotN_DistMean,
                  GazeOtherN_DistMean,
                  GazeGroupN_DistMean,
                  GazeSpeakerN_DistMean,
                  GazeBystanderN_DistMean,
                  GazeAdresseeN_DistMean,
                
                  SpeakerT_PERC,
                  GazeMVAL2VIN_PERC,
                  GazeMVAL2VIT_PERC,
                  GazeMVAL2NVIN_PERC,
                  GazeMVAL2NVIT_PERC,


                  GazeMVAL2GroupN_PERC,
                  GazeMVAL2GroupT_PERC,

                  GazeMVAL2OtherN_PERC,
                  GazeMVAL2OtherT_PERC,
                    ActiveEngageT_NORM,
                EngagementChildT_NORM,
                RobotActiveEngageT_NORM,
                SilenceTimeT_NORM,
                IdeasCreatedT_NORM,
                IdeasCreatedT_DistMean,
                RoleBystanderT_DistMean,
                RoleAdresseeT_DistMean,
                RPraiseN_DistMean
                ]


    if Condition == "B":
        df_c_B[str(str(Group)+str(ChildID))] = pd.Series(df_temp).copy()
        #df_c_B.set_index(0,inplace=True)
        print (df_c_B)
        #baseline = df_c_B.T.copy()


    elif Condition == "E":
        df_c_E[str(str(Group)+str(ChildID))] = pd.Series(df_temp).copy()
        #df_c_E.set_index(0, inplace=True)
        print(df_c_E)
        #encourage = df_c_E.T.copy()

    else:
        df_c_F[str(str(Group)+str(ChildID))] = pd.Series(df_temp).copy()
        #df_c_F.set_index(0, inplace=True)
        print(df_c_F)
        #follow = df_c_E.T.copy()



def updateDataFrameGrp (Group, Condition, temp_df):
    global SpeakT_Total_gr
    global SilenceT_Total_gr
    global SpeakT_Mean_gr
    global SpeakN_Total_gr
    global SpeakN_Mean_gr
    global IdeasCreatedN_Total_gr
    global IdeasFollowerN_Total_gr
    global IdeasOpposerN_Total_gr
    global IdeasNegotiateN_Total_gr
    global IdeasCreatedN_Mean_gr
    global IdeasAcceptedN_Total_gr
    global IdeasAcceptedN_Mean_gr

    global PraiseN_Total_gr
    global PraiseN_Mean_gr
    global SpeakT_DistMean_gr
    global SpeakN_DistMean_gr
    global IdeasCreatedN_DistMean_gr
    global IdeasAcceptedN_DistMean_gr
    global PraiseN_DistMean_gr
    global EngagementT_Total_gr
    global EngagementT_Mean_gr
    global EngagementT_DistMean_gr
    global OverlapT_DistMean_gr
    global OverlapT_Mean_gr
    global OverlapT_Total_gr

    global CriticizeN_DistMean_gr
    global MediatorN_DistMean_gr
    global ActiveEngageT_DistMean_gr
    global EngageRobotT_DistMean_gr
    global DisEngageT_DistMean_gr
    global RoleBystanderN_DistMean_gr
    global RoleAdresseeN_DistMean_gr

    global GazeRobotN_DistMean_gr
    global GazeOtherN_DistMean_gr
    global GazeGroupN_DistMean_gr
    global GazeSpeakerN_DistMean_gr
    global GazeBystanderN_DistMean_gr
    global GazeAdresseeN_DistMean_gr

    global CriticizeN_Mean_gr
    global MediatorN_Mean_gr
    global ActiveEngageT_Mean_gr
    global EngageRobotT_Mean_gr
    global DisEngageT_Mean_gr
    global RoleBystanderN_Mean_gr
    global RoleAdresseeN_Mean_gr

    global GazeRobotN_Mean_gr
    global GazeOtherN_Mean_gr
    global GazeGroupN_Mean_gr
    global GazeSpeakerN_Mean_gr
    global GazeBystanderN_Mean_gr
    global GazeAdresseeN_Mean_gr

    global CriticizeN_Total_gr
    global MediatorN_Total_gr
    global ActiveEngageT_Total_gr
    global EngageRobotT_Total_gr
    global DisEngageT_Total_gr
    global RoleBystanderN_Total_gr
    global RoleAdresseeN_Total_gr

    global GazeRobotN_Total_gr
    global GazeOtherN_Total_gr
    global GazeGroupN_Total_gr
    global GazeSpeakerN_Total_gr
    global GazeBystanderN_Total_gr
    global GazeAdresseeN_Total_gr

    global SessionDur

    global TEN_gr
    global TEOrgN_gr
    global TEManN_gr

    global TEN_NORM_gr
    global TEOrgN_NORM_gr
    global TEManN_NORM_gr

    global TEFairN_gr
    global TEUnFairN_gr
    global TEFairOutN_gr

    global TEFairN_NORM_gr
    global TEUnFairN_NORM_gr
    global TEFairOutN_NORM_gr

    global RIgnoreReasonN_gr
    global RDistractionN_gr
    global RUnfairN_gr
    global RFluidSpeechN_gr
    global ROtherN_gr
    global RNotIgnoredN_gr
    global RShyN_gr

    global RIgnoreReasonN_NORM_gr
    global RDistractionN_NORM_gr
    global RUnfairN_NORM_gr
    global FluidSpeechN_NORM_gr
    global ROtherN_NORM_gr
    global RNotIgnoredN_NORM_gr
    global RShyN_NORM_gr

    RobotInfluencesConvTEN=temp_df[(temp_df.code == "R-RobotImpact") & (temp_df.value == "RobotInfluencesConvTE")].count()['value']
    RobotInfluencesConvTET = \
    temp_df[(temp_df.code == "R-RobotImpact") & (temp_df.value == "RobotInfluencesConvTE")].sum()['time']

    RobotInfluencesConvTimeKeeperN = \
    temp_df[(temp_df.code == "R-RobotImpact") & (temp_df.value == "RobotInfluencesConvTimeKeeper")].count()['value']
    RobotInfluencesConvTimeKeeperT = \
        temp_df[(temp_df.code == "R-RobotImpact") & (temp_df.value == "RobotInfluencesConvTimeKeeper")].sum()['time']

    RobotIgnoredN = \
        temp_df[(temp_df.code == "R-RobotImpact") & (temp_df.value == "RobotIgnored")].count()['value']
    RobotIgnoredT = \
        temp_df[(temp_df.code == "R-RobotImpact") & (temp_df.value == "RobotIgnored")].sum()['time']

    RobotPlayNoDistractionN = \
        temp_df[(temp_df.code == "R-RobotImpact") & (temp_df.value == "RobotPlayNoDistraction")].count()['value']
    RobotPlayNoDistractionT = \
        temp_df[(temp_df.code == "R-RobotImpact") & (temp_df.value == "RobotPlayNoDistraction")].sum()['time']

    RobotNoImpactN = \
        temp_df[(temp_df.code == "R-RobotImpact") & (temp_df.value == "RobotNoImpact")].count()['value']
    RobotNoImpactT = \
        temp_df[(temp_df.code == "R-RobotImpact") & (temp_df.value == "RobotNoImpact")].sum()['time']

    RobotAuthorityN = \
        temp_df[(temp_df.code == "R-RobotImpact") & (temp_df.value == "RobotAuthority")].count()['value']
    RobotAuthorityT = \
        temp_df[(temp_df.code == "R-RobotImpact") & (temp_df.value == "RobotAuthority")].sum()['time']

    RobotAsaDistractionN = \
        temp_df[(temp_df.code == "R-RobotImpact") & (temp_df.value == "RobotAsaDistraction")].count()['value']
    RobotAsaDistractionT = \
        temp_df[(temp_df.code == "R-RobotImpact") & (temp_df.value == "RobotAsaDistraction")].sum()['time']

    RobotPerceivedUnFairnessN = \
        temp_df[(temp_df.code == "R-RobotImpact") & (temp_df.value == "RobotPerceivedUnFairness")].count()['value']
    RobotPerceivedUnFairnessT = \
        temp_df[(temp_df.code == "R-RobotImpact") & (temp_df.value == "RobotPerceivedUnFairness")].sum()['time']

    RobotPerceivedFairN = \
        temp_df[(temp_df.code == "R-RobotImpact") & (temp_df.value == "RobotPerceivedFair")].count()['value']
    RobotPerceivedFairT = \
        temp_df[(temp_df.code == "R-RobotImpact") & (temp_df.value == "RobotPerceivedFair")].sum()['time']

    GrpAutonomyResearcherDrivenN = \
        temp_df[(temp_df.value == "ResearcherDriven")].count()['value']
    GrpAutonomyResearcherDrivenT = \
        temp_df[(temp_df.value == "ResearcherDriven")].sum()['time']

    GrpAutonomyChildrenDrivenN = \
        temp_df[(temp_df.value == "ChildrenDriven")].count()['value']
    GrpAutonomyChildrenDrivenT = \
        temp_df[(temp_df.value == "ChildrenDriven")].sum()['time']

    GrpAutonomyRobotDrivenN = \
        temp_df[(temp_df.value == "RobotDriven")].count()['value']
    GrpAutonomyRobotDrivenT = \
        temp_df[(temp_df.value == "RobotDriven")].sum()['time']

    DecisionCollectiveN = \
        temp_df[(temp_df.value == "CollectiveDecision")].count()['value']
    DecisionCollectiveT = \
        temp_df[(temp_df.value == "CollectiveDecision")].sum()['time']

    DecisionIndividualN = \
        temp_df[(temp_df.value == "IndividualDecision")].count()['value']
    DecisionIndividualT = \
        temp_df[(temp_df.value == "IndividualDecision")].sum()['time']

    DecisionNoDecisionN = \
        temp_df[(temp_df.value == "NoDecision")].count()['value']
    DecisionNoDecisionT = \
        temp_df[(temp_df.value == "NoDecision")].sum()['time']

    DecisionNotenoughttimeN = \
        temp_df[(temp_df.value == "Notenoughttimetodecide")].count()['value']
    DecisionNotenoughttimeT = \
        temp_df[(temp_df.value == "Notenoughttimetodecide")].sum()['time']

    DecisionDurT = max(DecisionCollectiveT, DecisionIndividualT, DecisionNoDecisionT, DecisionNotenoughttimeT )

    NGrpAutonomy = GrpAutonomyResearcherDrivenN + GrpAutonomyRobotDrivenN + GrpAutonomyChildrenDrivenN

    TEN_gr =  temp_df[(temp_df.value == "TE")].count()['value']
    TEOrgN_gr =  temp_df[(temp_df.value == "TEOrg")].count()['value']
    TEManN_gr =  temp_df[(temp_df.value == "TEManual")].count()['value']

    TEN_NORM_gr = TEN_gr / SessionDur
    TEOrgN_NORM_gr = TEOrgN_gr / SessionDur
    TEManN_NORM_gr = TEManN_gr / SessionDur

    TEFairN_gr = temp_df[(temp_df.value == "Fair")].count()['value']
    TEUnFairN_gr = temp_df[(temp_df.value == "Unfair")].count()['value']
    TEFairOutN_gr = temp_df[(temp_df.value == "FairOut")].count()['value']
    TEFairN_gr += TEFairOutN_gr

    TEFairN_NORM_gr = TEFairN_gr  / TEN_gr
    TEUnFairN_NORM_gr = TEUnFairN_gr  / TEN_gr
    TEFairOutN_NORM_gr = TEFairOutN_gr  / TEN_gr


    RDistractionN_gr = temp_df[(temp_df.value == "Distraction")].count()['value']
    RUnfairN_gr = temp_df[(temp_df.value == "Unfair")].count()['value']
    RFluidSpeechN_gr = temp_df[(temp_df.value == "Inthemiddleofaconversation") | (temp_df.value == "FluidSpeech") ].count()['value']
    ROtherN_gr = temp_df[(temp_df.code== "RobotIgnoredReason") & (temp_df.value == "Other")].count()['value']
    RNotIgnoredN_gr =temp_df[(temp_df.value == "NotIgnored")].count()['value']
    RShyN_gr =temp_df[(temp_df.value == "Shy")].count()['value']

    RIgnoreReasonN_gr = RDistractionN_gr + RUnfairN_gr +  RFluidSpeechN_gr +  ROtherN_gr


    RDistractionN_NORM_gr = RDistractionN_gr / TEN_gr
    RUnfairN_NORM_gr = RUnfairN_gr / TEN_gr
    RFluidSpeechN_NORM_gr = RFluidSpeechN_gr / TEN_gr
    ROtherN_NORM_gr = ROtherN_gr / TEN_gr
    RNotIgnoredN_NORM_gr = RNotIgnoredN_gr / TEN_gr
    RIgnoreReasonN_NORM_gr = (1 - RNotIgnoredN_NORM_gr)
    RShyN_NORM_gr = RShyN_gr / TEN_gr

    TGrpAutonomy = GrpAutonomyResearcherDrivenT + GrpAutonomyRobotDrivenT + GrpAutonomyChildrenDrivenT

    NRobotImpact = RobotNoImpactN + RobotIgnoredN + RobotAsaDistractionN + RobotAuthorityN + RobotPlayNoDistractionN + RobotInfluencesConvTEN + RobotInfluencesConvTimeKeeperN + RobotPerceivedFairN + RobotPerceivedUnFairnessN

    TRobotImpact = RobotNoImpactT+ RobotIgnoredT + RobotAsaDistractionT + RobotAuthorityT + RobotPlayNoDistractionT + RobotInfluencesConvTET + RobotInfluencesConvTimeKeeperT + RobotPerceivedFairT + RobotPerceivedUnFairnessT

    # todo avaliar se decisiondurT ou  TGrpAutonomy
    GrpAutonomyChildrenDrivenT_NORM = GrpAutonomyChildrenDrivenT /  DecisionDurT
    GrpAutonomyResearcherDrivenT_NORM = GrpAutonomyResearcherDrivenT / DecisionDurT
    GrpAutonomyRobotDrivenT_NORM = GrpAutonomyRobotDrivenT / DecisionDurT
    # todo avaliar se decisiondur T ou NGrpAutonomy
    GrpAutonomyChildrenDrivenN_NORM = GrpAutonomyChildrenDrivenN / NGrpAutonomy
    GrpAutonomyResearcherDrivenN_NORM = GrpAutonomyResearcherDrivenN / NGrpAutonomy
    GrpAutonomyRobotDrivenN_NORM = GrpAutonomyRobotDrivenN / NGrpAutonomy

    EngagementT_NORM = EngagementT_Total_gr / SessionDur
    ActiveEngageT_NORM = ActiveEngageT_Total_gr / SessionDur
    RobotActiveEngageT_NORM = RobotActiveEngageT_Total_gr / SessionDur
    PraiseN_NORM = PraiseN_Total_gr / SessionDur



    # todo avaliar se decisiondurT ou TRobotImpact  ou NRobotImpact
    RobotInfluencesConvTEN_NORM=RobotInfluencesConvTEN /  NRobotImpact
    RobotInfluencesConvTET_NORM = RobotInfluencesConvTET / DecisionDurT

    # todo avaliar se decisiondurT ou TRobotImpact  ou NRobotImpact
    RobotInfluencesConvTimeKeeperN_NORM = RobotInfluencesConvTimeKeeperN /  NRobotImpact
    RobotInfluencesConvTimeKeeperT_NORM = RobotInfluencesConvTimeKeeperT / DecisionDurT

    # todo avaliar se decisiondurT ou TRobotImpact  ou NRobotImpact
    RobotIgnoredN_NORM = RobotIgnoredN /  NRobotImpact
    RobotIgnoredT_NORM = RobotIgnoredT / DecisionDurT

    # todo avaliar se decisiondurT ou TRobotImpact  ou NRobotImpact
    RobotPlayNoDistractionN_NORM = RobotPlayNoDistractionN /  NRobotImpact
    RobotPlayNoDistractionT_NORM = RobotPlayNoDistractionT / DecisionDurT

    # todo avaliar se decisiondurT ou TRobotImpact  ou NRobotImpact
    RobotNoImpactN_NORM = RobotNoImpactN /  NRobotImpact
    RobotNoImpactT_NORM = RobotNoImpactT / DecisionDurT

    # todo avaliar se decisiondurT ou TRobotImpact  ou NRobotImpact
    RobotAuthorityN_NORM = RobotAuthorityN /  NRobotImpact
    RobotAuthorityT_NORM = RobotAuthorityT / DecisionDurT

    # todo avaliar se decisiondurT ou TRobotImpact  ou NRobotImpact
    RobotAsaDistractionN_NORM = RobotAsaDistractionN /  NRobotImpact
    RobotAsaDistractionT_NORM = RobotAsaDistractionT / DecisionDurT

    # todo avaliar se decisiondurT ou TRobotImpact  ou NRobotImpact
    RobotPerceivedUnFairnessN_NORM =  RobotPerceivedUnFairnessN /  NRobotImpact
    RobotPerceivedUnFairnessT_NORM =  RobotPerceivedUnFairnessT / DecisionDurT


    RobotPerceivedFairN_NORM = RobotPerceivedFairN /  NRobotImpact
    RobotPerceivedFairT_NORM = RobotPerceivedFairT / DecisionDurT

    SilenceT_Total_gr += (DecisionDurT - SpeakT_Total_gr)

    df_temp = [Group, Condition,      RobotInfluencesConvTEN  ,	 RobotInfluencesConvTET  ,
        RobotInfluencesConvTimeKeeperN  ,	 RobotInfluencesConvTimeKeeperT  ,
                             RobotIgnoredN,	 RobotIgnoredT,
                             RobotPlayNoDistractionN  ,	 RobotPlayNoDistractionT  ,
                             RobotNoImpactN  ,	 RobotNoImpactT  ,
                             RobotAuthorityN  ,	 RobotAuthorityT  ,
                             RobotAsaDistractionN  ,	 RobotAsaDistractionT  ,
                             RobotPerceivedUnFairnessN  ,	 RobotPerceivedUnFairnessT  ,
                              RobotPerceivedFairN  ,	 RobotPerceivedFairT  ,

                             GrpAutonomyResearcherDrivenN  ,  GrpAutonomyResearcherDrivenT  ,
                             GrpAutonomyChildrenDrivenN  ,  GrpAutonomyChildrenDrivenT  ,
                             GrpAutonomyRobotDrivenN  ,  GrpAutonomyRobotDrivenT  ,

                             DecisionCollectiveN  ,  DecisionCollectiveT  ,
                             DecisionIndividualN  ,  DecisionIndividualT  ,
                             DecisionNoDecisionN  ,  DecisionNoDecisionT  ,
                             DecisionNotenoughttimeN  ,  DecisionNotenoughttimeT,

                       SpeakT_Total_gr, SpeakT_Mean_gr, SpeakT_DistMean_gr,
                       SpeakN_Total_gr, SpeakN_Mean_gr, SpeakN_DistMean_gr,

                       IdeasCreatedN_Total_gr, IdeasCreatedN_Mean_gr, IdeasCreatedN_DistMean_gr,
                       IdeasAcceptedN_Total_gr, IdeasAcceptedN_Mean_gr, IdeasAcceptedN_DistMean_gr,

                       #GazeNVIT_Total_gr, GazeNVIT_Mean_gr_B, GazeNVIT_DistMean_gr_B,
                       #GazeVIT_Total_gr_B, GazeVIT_Mean_gr_B, GazeVIT_DistMean_gr_B,

                       PraiseN_Total_gr, PraiseN_Mean_gr, PraiseN_DistMean_gr,

                        EngagementT_Total_gr, EngagementT_Mean_gr, EngagementT_DistMean_gr,
                        OverlapT_Total_gr, OverlapT_Mean_gr, OverlapT_DistMean_gr,

               CriticizeN_Total_gr, CriticizeN_Mean_gr, CriticizeN_DistMean_gr,
               MediatorN_Total_gr, MediatorN_Mean_gr, MediatorN_DistMean_gr,
               ActiveEngageT_Total_gr, ActiveEngageT_Mean_gr, ActiveEngageT_DistMean_gr,
               EngageRobotT_Total_gr, EngageRobotT_Mean_gr, EngageRobotT_DistMean_gr,
               DisEngageT_Total_gr, DisEngageT_Mean_gr, DisEngageT_DistMean_gr,
               RoleBystanderN_Total_gr, RoleBystanderN_Mean_gr, RoleBystanderN_DistMean_gr,
               RoleAdresseeN_Total_gr, RoleAdresseeN_Mean_gr, RoleAdresseeN_DistMean_gr,
               GazeRobotN_Total_gr, GazeRobotN_Mean_gr, GazeRobotN_DistMean_gr,
               GazeOtherN_Total_gr, GazeOtherN_Mean_gr, GazeOtherN_DistMean_gr,
               GazeGroupN_Total_gr, GazeGroupN_Mean_gr, GazeGroupN_DistMean_gr,
               GazeSpeakerN_Total_gr, GazeSpeakerN_Mean_gr, GazeSpeakerN_DistMean_gr,
               GazeBystanderN_Total_gr, GazeBystanderN_Mean_gr, GazeBystanderN_DistMean_gr,
               GazeAdresseeN_Total_gr, GazeAdresseeN_Mean_gr, GazeAdresseeN_DistMean_gr,

               DecisionDurT, NGrpAutonomy,
                        GrpAutonomyResearcherDrivenN_NORM , GrpAutonomyRobotDrivenN_NORM,  GrpAutonomyChildrenDrivenN_NORM,
                        GrpAutonomyChildrenDrivenT_NORM , GrpAutonomyResearcherDrivenT_NORM, GrpAutonomyRobotDrivenT_NORM,

                        RobotInfluencesConvTEN_NORM,
                        RobotInfluencesConvTET_NORM,

                        RobotInfluencesConvTimeKeeperN_NORM,
                        RobotInfluencesConvTimeKeeperT_NORM,

                        RobotIgnoredN_NORM,
                        RobotIgnoredT_NORM,

                        RobotPlayNoDistractionN_NORM,
                        RobotPlayNoDistractionT_NORM,

                        RobotNoImpactN_NORM,
                        RobotNoImpactT_NORM,

                        RobotAuthorityN_NORM,
                        RobotAuthorityT_NORM,

                        RobotAsaDistractionN_NORM,
                        RobotAsaDistractionT_NORM,

                        RobotPerceivedUnFairnessN_NORM,
                        RobotPerceivedUnFairnessT_NORM,

                        RobotPerceivedFairN_NORM,
                        RobotPerceivedFairT_NORM,
                        EngagementT_NORM,
                        ActiveEngageT_NORM,
                        PraiseN_NORM,
                        PeerInterN_NORM_gr,
                        RobotActiveEngageT_NORM,
                        SilenceT_Total_gr,
                       TEN_gr,
                       TEOrgN_gr,
                       TEManN_gr,
                       TEN_NORM_gr,
                       TEOrgN_NORM_gr,
                       TEManN_NORM_gr,

                       TEFairN_gr,
                       TEUnFairN_gr,
                       TEFairOutN_gr,

                       TEFairN_NORM_gr,
                       TEUnFairN_NORM_gr,
                       TEFairOutN_NORM_gr,

                       RIgnoreReasonN_gr,
                       RDistractionN_gr,
                       RUnfairN_gr,
                       RFluidSpeechN_gr,
                       ROtherN_gr,
                       RNotIgnoredN_gr,
                       RShyN_gr,

                       RIgnoreReasonN_NORM_gr,
                       RDistractionN_NORM_gr,
                       RUnfairN_NORM_gr,
                       RFluidSpeechN_NORM_gr,
                       ROtherN_NORM_gr,
                       RNotIgnoredN_NORM_gr,
                       RShyN_NORM_gr,
                       IdeasCreatedT_Total_gr, IdeasCreatedT_Mean_gr, IdeasCreatedT_DistMean_gr,
               RoleBystanderT_Total_gr, RoleBystanderT_Mean_gr, RoleBystanderT_DistMean_gr,
               RoleAdresseeT_Total_gr, RoleAdresseeT_Mean_gr, RoleAdresseeT_DistMean_gr,
               RPraiseN_Total_gr, RPraiseN_Mean_gr, RPraiseN_DistMean_gr
               ]

    if Condition == "B":
        df_g_B[str(Group)] = pd.Series(df_temp).copy()
        # df_c_B.set_index(0,inplace=True)
        print(df_g_B)
        baselineg = df_g_B.T.copy()
    elif Condition == "E":
        df_g_E[str(Group)] = pd.Series(df_temp).copy()
        # df_c_B.set_index(0,inplace=True)
        print(df_g_E)
        encourageg = df_g_E.T.copy()
    else:
        df_g_F[str(Group)] = pd.Series(df_temp).copy()
        # df_c_B.set_index(0,inplace=True)
        print(df_g_F)
        followg = df_g_F.T.copy()


def parseLine(line, Grp, Condition):
    print (line)

    if line[0:1] == "S": return
    if "Child Data" in line :
        print ("ignorar Child Data")
        return
    if "Role" in line :
        child = line[3_4]
        print (f"Child number {child}")
        parseeachCLine (line, child)

def parseeachCLine (line, child):

    parseCh1 = append ((Grp, child, condition, ))




for file_name in os.listdir('coding/'):
    if fnmatch.fnmatch(file_name, '*.txt'):
        print(file_name)
        print("Group", {file_name[22:24]})
        print("Condition", {file_name[31:32]})
        Grp =  file_name[22:24]
        Condition = file_name[31:32]
        filename = "coding/"+file_name
        #readfileCod (filename, Grp, Condition)
        pandaFile(filename, Grp, Condition)

df_c_B.set_index(0,inplace=True)
df_c_E.set_index(0,inplace=True)
df_c_F.set_index(0,inplace=True)
df_g_B.set_index(0,inplace=True)
df_g_E.set_index(0,inplace=True)
df_g_F.set_index(0,inplace=True)
baseline = df_c_B.T.copy()
encourage = df_c_E.T.copy()
follow =  df_c_F.T.copy()
groupdf_b = df_g_B.T.copy()
groupdf_e =  df_g_E.T.copy()
groupdf_f =  df_g_F.T.copy()
tablec = pd.concat([baseline, encourage, follow], axis = 1)
tableg = pd.concat([groupdf_b, groupdf_e, groupdf_f], axis = 1)

t = time.time()
#current_time = time.strftime("%H:%M:%S", t)
"""
outputfilename = f"coding/outputfile/baseline_{t}.txt"
baseline.to_csv (outputfilename)
outputfilename = f"coding/outputfile/encourage_{t}.txt"
encourage.to_csv (outputfilename)
outputfilename = f"coding/outputfile/follow_{t}.txt"
follow.to_csv (outputfilename)
outputfilename = f"coding/outputfile/baselinegr_{t}.txt"
groupdf_b.to_csv (outputfilename)
outputfilename = f"coding/outputfile/encouragegr_{t}.txt"
groupdf_e.to_csv (outputfilename)
outputfilename = f"coding/outputfile/followgr_{t}.txt"

groupdf_f.to_csv (outputfilename)
"""
outputfilename = f"coding/outputfile/tabelacon_c_{t}.txt"
tablec.to_csv (outputfilename)
outputfilename = f"coding/outputfile/tabelacon_g_{t}.txt"
tableg.to_csv (outputfilename)




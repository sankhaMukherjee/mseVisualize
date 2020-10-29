import pgIO
import os, pickle
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection

import matplotlib as mpl
mpl.rcParams['mathtext.fontset'] = 'cm'


mseLableHeaders = [
    ('Abnormal or psychotic thoughts', 'no issues'),
    ('Abnormal or psychotic thoughts', 'experiencing delusions/abnormal thoughts (grandure)'),
    ('Abnormal or psychotic thoughts', 'experiencing delusions/abnormal thoughts (persecution)'),
    ('Abnormal or psychotic thoughts', 'experiencing delusions/abnromal thoughts (religious)'),
    ('Abnormal or psychotic thoughts', 'experiencing hallucinations (auditory)'),
    ('Abnormal or psychotic thoughts', 'experiencing hallucinations (visual)'),
    ('Abnormal or psychotic thoughts', 'experiencing hallucinations (tactile)'),
    ('Abnormal or psychotic thoughts', 'History of delusions/abnormal thoughts'),
    ('Abnormal or psychotic thoughts', 'History of hallucinations'),
    ('Abnormal or psychotic thoughts', 'neutral/unable to categorize'),
    ('Abnormal or psychotic thoughts', 'experiencing delusions (not specified)'),
    ('Abnormal or psychotic thoughts', 'experiencing hallucinations (not specified)'),
    ('Abnormal or psychotic thoughts', 'experiencing delusions/abnormal thoughts (obsessions)'),
    ('Abnormal or psychotic thoughts', 'experiencing delusions/abnormal thoughts (paranoia)'),
    ('Abnormal or psychotic thoughts', 'experiencing hallucinations (olfactory)'),
    ('Abnormal or psychotic thoughts', 'responding to internal stimuli'),
    ('Abnormal or psychotic thoughts', 'experiencing delusions/abnormal thoughts (sexual)'),
    ('Affect', 'no issues/appropriate affect'),
    ('Affect', 'neutral/unable to categorize'),
    ('Affect', 'aggressive'),
    ('Affect', 'reactive'),
    ('Affect', 'irritable/angry'),
    ('Affect', 'improved from last visit'),
    ('Affect', 'issues with cognition'),
    ('Affect', 'loss of energy/tiredness'),
    ('Affect', 'blunted/restricted'),
    ('Affect', 'anxious/fearful'),
    ('Affect', 'tearful/depressed/sad'),
    ('Affect', 'bright/positive'),
    ('Affect', 'labile'),
    ('Affect', 'intense'),
    ('Affect', 'expansive/overly animated'),
    ('Affect', 'generally odd or out of the oridnary/inappropriate'),
    ('Affect', 'flooded'),
    ('Appearance', 'Issues with  Affect'),
    ('Appearance', 'Sleep/Bed'),
    ('Appearance', 'Issues with Eye Contact'),
    ('Appearance', 'Not age appropriate'),
    ('Appearance', 'Issues with general Health'),
    ('Appearance', 'Issues with Behavior'),
    ('Appearance', 'Positive Affect'),
    ('Appearance', 'Postivie Grooming/Hygiene'),
    ('Appearance', 'Issues with Grooming/Hygiene'),
    ('Appearance', 'Positive Health'),
    ('Appearance', 'Issues with Weight'),
    ('Appearance', 'Normal/no issues'),
    ('Appearance', 'Hospital attire'),
    ('Appearance', 'Positive dress'),
    ('Appearance', 'Issues with dress'),
    ('Appearance', 'Neutral'),
    ('Appearance', 'Positive eye contact'),
    ('Appearance', 'Appropriate Age'),
    ('Appearance', 'Positive Behavior'),
    ('Association', 'intact/no issues'),
    ('Association', 'neutral/unable to categorize'),
    ('Association', 'circumstantial'),
    ('Association', 'loose'),
    ('Association', 'tangential'),
    ('Association', 'age appropriate'),
    ('Association', 'improved'),
    ('Association', 'declined'),
    ('Association', 'disorganized'),
    ('Association', 'general issues'),
    ('Attention/Concentration', 'intact/no issues'),
    ('Attention/Concentration', 'neutral/unable to categorize'),
    ('Attention/Concentration', 'general issues'),
    ('Attention/Concentration', 'improved'),
    ('Attention/Concentration', 'declined'),
    ('Attention/Concentration', 'age appropriate'),
    ('Attention/Concentration', 'issues due to MH'),
    ('Attention/Concentration', 'issues due to DD'),
    ('Attention/Concentration', 'varrying'),
    ('Attitude', 'positive/appropriate'),
    ('Attitude', 'neutral/unable to categorize'),
    ('Attitude', 'age appropriate'),
    ('Attitude', 'not age appropriate'),
    ('Attitude', 'negative/inappropriate'),
    ('Attitude', 'improved'),
    ('Attitude', 'declined'),
    ('Cognition', 'normal/no issues'),
    ('Cognition', 'neutral/unable to categorize'),
    ('Cognition', 'issues with concentration'),
    ('Cognition', 'positive concentration'),
    ('Cognition', 'issues with fund of knowledge'),
    ('Cognition', 'positive fund of knowledge'),
    ('Cognition', 'issues with attention'),
    ('Cognition', 'positive attention'),
    ('Cognition', 'general issues'),
    ('Executive Functioning', 'in tact/noissues'),
    ('Executive Functioning', 'neutral/unable to categorize'),
    ('Executive Functioning', 'some impairment'),
    ('Executive Functioning', 'much impairment'),
    ('Executive Functioning', 'improved since last session'),
    ('Executive Functioning', 'declined since last session'),
    ('Executive Functioning', 'age appropriate'),
    ('Executive Functioning', 'below age level'),
    ('Executive Functioning', 'impaired (due to DD)'),
    ('Executive Functioning', 'impaired (due to TBI)'),
    ('Executive Functioning', 'impaired (due to other MH issue)'),
    ('Fund of knowledge', 'intact/no issues'),
    ('Fund of knowledge', 'neutral/unable to categorize'),
    ('Fund of knowledge', 'positive vocabulary'),
    ('Fund of knowledge', 'issues with vocabulary'),
    ('Fund of knowledge', 'positive history'),
    ('Fund of knowledge', 'issues with history'),
    ('Fund of knowledge', 'average'),
    ('Fund of knowledge', 'above average'),
    ('Fund of knowledge', 'below average'),
    ('Fund of knowledge', 'positive current events'),
    ('Fund of knowledge', 'issues with current events'),
    ('Fund of knowledge', 'generally limited/issues'),
    ('Fund of knowledge', 'declined'),
    ('Fund of knowledge', 'improved'),
    ('Gait and station', 'normal/no issues'),
    ('Gait and station', 'neutral/unable to categorize'),
    ('Gait and station', 'non-ambulatory'),
    ('Gait and station', 'issues with gait/station'),
    ('Gait and station', 'assistive device needed'),
    ('Homicidal', 'not present'),
    ('Homicidal', 'neutral'),
    ('Homicidal', 'present'),
    ('Impulse control', 'good/no issues'),
    ('Impulse control', 'neutral/unable to categorize'),
    ('Impulse control', 'limited/some issues'),
    ('Impulse control', 'poor/serious issues'),
    ('Impulse control', 'age appropriate'),
    ('Impulse control', 'not age appropriate'),
    ('Insight', 'no issues with insight'),
    ('Insight', 'issues with insight'),
    ('Insight', 'neutral/unable to categorize'),
    ('Intelligence', 'normal/no issues with intelligence'),
    ('Intelligence', 'issues with intelligence'),
    ('Intelligence', 'neutral/unable to categorize'),
    ('Judgment', 'no issues with judgement'),
    ('Judgment', 'issues with judgement'),
    ('Judgment', 'neutral/unable to categorize'),
    ('Language', 'intact'),
    ('Language', 'neutral/unable to categorize'),
    ('Language', 'repetition intact'),
    ('Language', 'issues with repetition'),
    ('Language', 'object naming intact'),
    ('Language', 'issues with object naming'),
    ('Language', 'impaired'),
    ('Language', 'non-verbal/mute'),
    ('Language', 'minimally verbal'),
    ('Language', 'issues related to DD'),
    ('Level of consciousness', 'normal; no issues notes'),
    ('Level of consciousness', 'neutral; unable to categorize'),
    ('Level of consciousness', 'sleepy/drowsy'),
    ('Level of consciousness', 'clouded'),
    ('Level of consciousness', 'issues verbally'),
    ('Level of consciousness', 'misc. issues'),
    ('Level of consciousness', 'impaired due to DD/MI'),
    ('Memory', 'no issues/memory unimpaired'),
    ('Memory', 'issues/memory impaired'),
    ('Memory', 'neutral/unable to categorize'),
    ('Mood', 'Normal; no issues'),
    ('Mood', 'neutral; unable to categorize'),
    ('Mood', 'anxious, tense'),
    ('Mood', 'depressed, sad, despondent'),
    ('Mood', 'irritable, angry'),
    ('Mood', 'improved'),
    ('Mood', 'declined'),
    ('Mood', 'elevated, manic'),
    ('Mood', 'labile'),
    ('Mood', 'misc. issues'),
    ('Mood', 'suicidal'),
    ('Orientation', 'no orientation issues'),
    ('Orientation', 'issues with orientation to person'),
    ('Orientation', 'issues with orientation to place'),
    ('Orientation', 'issues with orientation to time/date'),
    ('Orientation', 'issues with orientation to situation'),
    ('Orientation', 'neutral/unable to categorize'),
    ('Orientation', 'general orientation issues'),
    ('Psychomotor', 'normal; no issues'),
    ('Psychomotor', 'neutral; unable to categorize'),
    ('Psychomotor', 'retarded; slowed'),
    ('Psychomotor', 'agitated; tense; restless'),
    ('Psychomotor', 'improved'),
    ('Psychomotor', 'declined'),
    ('Psychomotor', 'constricted'),
    ('Psychomotor', 'tremors'),
    ('Psychomotor', 'tics'),
    ('Psychomotor', 'involuntary movements'),
    ('Psychomotor', 'misc. issues'),
    ('Psychomotor', 'catatonic'),
    ('Reasoning', 'normal; no issues'),
    ('Reasoning', 'neutral; unable to categorize'),
    ('Reasoning', 'impaired; poor'),
    ('Reasoning', 'impaired due to DD/cognitive issues'),
    ('Reasoning', 'impaired due to MI'),
    ('Reasoning', 'concrete'),
    ('Reasoning', 'abstract'),
    ('Reasoning', 'improved'),
    ('Reasoning', 'misc. issues'),
    ('Sensorium', 'normal; no issues'),
    ('Sensorium', 'neutral; unable to categorize'),
    ('Sensorium', 'clouded; sedate'),
    ('Sensorium', 'impaired'),
    ('Sensorium', 'fluctuating'),
    ('Sensorium', 'impaired due to medications/drugs/alcohol'),
    ('Sensorium', 'sleepy; lethargic'),
    ('Sleep', 'normal, no issues'),
    ('Sleep', 'neutral, unable to categorize'),
    ('Sleep', "maintenance issues (can't stay asleep)"),
    ('Sleep', 'onset issues (unable to fall asleep)'),
    ('Sleep', 'nightmares'),
    ('Sleep', 'insomnia'),
    ('Sleep', 'hypersomnia'),
    ('Sleep', 'misc. issues related to sleep'),
    ('Speech', 'normal, no issues'),
    ('Speech', 'neutral, unable to categorize'),
    ('Speech', 'issues with rate'),
    ('Speech', 'issues with tone'),
    ('Speech', 'issues with volume'),
    ('Speech', 'stutter or lisp'),
    ('Speech', 'misc. issues'),
    ('Speech', 'impoverished'),
    ('Speech', 'improved'),
    ('Speech', 'unintelligible'),
    ('Speech', 'mute, non-verbal'),
    ('Suicidal', 'normal, no issues, not present'),
    ('Suicidal', 'neutral, unable to categorize'),
    ('Suicidal', 'suicidal ideation'),
    ('Suicidal', 'suicidal with intent'),
    ('Suicidal', 'suicidal with plan'),
    ('Suicidal', 'suicide attempt'),
    ('Suicidal', 'history of ideation'),
    ('Suicidal', 'history of attempt'),
    ('Suicidal', 'self-injurious'),
    ('Suicidal', 'history of self injury'),
    ('Suicidal', 'suicidal ideation with means'),
    ('Violent Thoughts', 'normal, no issues'),
    ('Violent Thoughts', 'neutral, unable to categorize'),
    ('Violent Thoughts', 'present'),
    ('Violent Thoughts', 'present, with intent'),
    ('Violent Thoughts', 'present with plan'),
    ('Violent Thoughts', 'present with means'),
    ('Violent Thoughts', 'history of violent thoughts'),
    ('Violent Thoughts', 'history of violent behaviors'),
    ('Violent Thoughts', 'violent/aggressive behavior'),]

def getData(userId):

    try:

        fileName = f'data/{userId}_userData.pkl'

        if os.path.exists(fileName):
            userData = pickle.load( open(fileName, 'rb') )
            return userData

        userData = {}
        print('Getting MSE data')
        data = pgIO.getAllData('''
            select 
                category_mapped, sign_val,
                array_agg( distinct visit_start_date ) 
            from
                ds_internal_otsuka.mse_raw_data mrd 
            where
                upid = %s
            group by
                category_mapped, sign_val
            order by 1,2;''', (userId,))

        userData['mseData'] = data

        print('Getting meds data')
        data = pgIO.getAllData('''
            select 
                * 
            from 
                ds_internal_otsuka.patients_rexulti_dates
            where
                person_id = %s''', (userId,))

        _, start, stop, _ = data[0]

        userData['rexultiStart'] = start
        userData['rexultiStop']  = stop

        with open( fileName, 'wb' ) as fOut:
            pickle.dump( userData, fOut )

    except Exception as e:
        print(f'Unable to get user data: {e}')
        return None

    return userData

def getMSElabels(userId):

    try:
        fileName = f'data/{userId}_labels.pkl'

        if os.path.exists(fileName):
            mseLabels = pickle.load( open(fileName, 'rb') )
            return mseLabels

        data = pgIO.getAllData('''
            select * from r20r1_dcdm.derived_mse
            where
                person_id = %s
        ''', (userId, ))

        data  = list(zip(*data))
        dates = data[1]
        labels = []
        for i in range(241):
            labels.append( list(data[3+i]) )
        labels = np.array(labels)

        mseLabels = {
            'dates'  : dates,
            'labels' : labels }

        with open(fileName, 'wb') as fOut:
            pickle.dump( mseLabels, fOut )

        return mseLabels

    except Exception as e:
        print(f'Unable to get mse data: {e}')
        return None

    return mseLabels


def plot(xData, yData, rawData, yTickPos, yTickLabels, title, start, stop, userId):

    fPath      = '/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf'
    fPath      = '/usr/local/share/fonts/NeueEinstellung-Regular.otf'
    prop       = fm.FontProperties(fname=fPath, size='large')
    propSmall  = fm.FontProperties(fname=fPath, size=8)
    bgColor    = (224/255, 228/255, 237/255)
    hmuskBlue  = (25/255, 45/255, 91/255)
    hmuskGrey  = (151/255, 165/255,194/255)

    n = len(xData)
    delY = 0.2 #inches
    yStartPos = 1/( 2 + delY*n )
    yEndPos   = (delY*n)/( 2 + delY*n )
    yFrac     = (delY*n)/( 2 + delY*n )

    p = plt.figure(figsize=(11.5, 2+delY*n ), facecolor=bgColor)
    ax = plt.axes([0.3, yStartPos, 0.69, yEndPos], facecolor='None')

    for x, y, r in zip(xData, yData, rawData):
        
        if r: 
            mec = hmuskGrey
        else:
            mec = hmuskBlue

        plt.plot(x, y, '|', mec=mec)

    plt.axhline(y=sum(rawData), color='k', lw=1)
    plt.ylim([-0.5, n+0.5])
    plt.yticks( yTickPos, yTickLabels, fontproperties=prop, fontsize=10 )

    titleYPos = (1.5 + delY*n)/( 2 + delY*n )
    plt.figtext( 0.3 + 0.69/2, titleYPos, title, fontproperties=prop, fontsize=14 )

    plt.axvline(start, ls = '--', color='grey')
    plt.axvline(stop,  ls = '--', color='grey')

    plt.xlabel('Date', fontproperties=prop, fontsize=10)
    plt.xticks(fontproperties=prop, fontsize=10)

    title = title.lower()
    title = title.replace(' ', '-').replace('/', '-')
    plt.savefig( os.path.join(
            'results',
            f'{userId}_{title}.png'), 
            dpi=300, facecolor=bgColor  )

    return

def plotData(userData, mseLabels, userId):

    categories = sorted(list(set([c for c, _, _ in userData['mseData']])))
    print(categories)

    mseDates = mseLabels['dates']

    for mmm, c in enumerate(categories):

        m1 = m2 = 0
        yVals = []
        yTicks = []

        xData = []
        yData = []
        yTickPos, yTickLabels = [], []
        rawData = []
        

        print(f'\n----[{c}]-----')
        
        for c1, s, dates in userData['mseData']:
            if c1 != c: continue
            print( f'{s}[{len(dates)}]', end=', ' )

            xData.append( dates )
            yData.append( [m1]*len(dates) )
            yTickPos.append( m1 )
            yTickLabels.append(s)
            rawData.append(True)

            m1 += 1

        print()


        for i, (c1, s) in enumerate(mseLableHeaders):
            if c1 != c: continue

            labels = mseLabels['labels'][i, :]
            count = sum(labels)
            if count == 0: continue 
            
            print( f'{s} -> {count}', end=', ' )
            dates1 = [d for j, d in enumerate(mseDates) if labels[j]==1]

            xData.append( dates1 )
            yData.append( [m1+m2+1]*len(dates1) )
            yTickPos.append(m1+m2+1)
            yTickLabels.append( f'{s} [{i:03}]' )
            rawData.append( False )

            m2 += 1

        plot(xData, yData, rawData, yTickPos, yTickLabels, c, userData['rexultiStart'], userData['rexultiStop'], userId)
        print()
    
    plt.show()
            

    return 

def main():

    userId = 3010019
    userData  = getData(userId)
    mseLabels = getMSElabels(userId)

    plotData(userData, mseLabels, userId)

    if True and mseLabels is not None:
        print(len(mseLabels['dates']))
        print(mseLabels['labels'].shape)

    if False and userData is not None:
        print(userData['rexultiStart'])
        print(userData['rexultiStop'])
        for category, sign, dates in userData['mseData']:
            print( f'[{category:>30s}]:{sign:30s} | {len(dates)}' )


    return

if __name__ == "__main__":
    main()


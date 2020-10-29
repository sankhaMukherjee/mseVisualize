import pgIO
import os, pickle
import numpy as np



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

def main():

    userId = 3010019
    userData  = getData(userId)
    mseLabels = getMSElabels(userId)

    if mseLabels is not None:
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


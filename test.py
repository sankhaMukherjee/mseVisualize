import pgIO
import os, pickle



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



def main():

    userId = 3010019
    userData = getData(userId)

    if userData is not None:
        print(userData['rexultiStart'])
        print(userData['rexultiStop'])
        for category, sign, dates in userData['mseData']:
            print( f'[{category:>30s}]:{sign:30s} | {len(dates)}' )


    return

if __name__ == "__main__":
    main()


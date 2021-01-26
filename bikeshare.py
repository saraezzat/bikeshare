"""
student: Sara Ezzat
email: sara.ezzat.abdelhamid@gmail.com

"""
import time
import pandas as pd
import numpy as np
import tabulate as tabulate

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun']
DAYS = ['saturday','sunday','monday','tuesday',
        'wednesday','thursday','friday']
FILTERS = ['day','month','both','none']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter
        (str) day - name of the day of week to filter
        
    if the user enters the wrong data the program returns to the previous step
    """
    print('_'*60)
    print('\nHello! Let\'s explore some US bikeshare data!')
    city=''
    month='all'
    day='all'
    filters=''
    # get user input for city (chicago, new york city, washington).
    while True:
        city = input('Which of these cities would you like to view: Chicago, New York City or Washington? ').lower()
        if city not in CITY_DATA: 
            #handles random input, loops back to getting city
            print("\nPlease choose one of the listed cities and make sure your spelling is correct!")
            print('='*60+'\n')
            continue
        else:
            #getting the user's desired filter 
            while True:
                filters = input('Would you like to filter your data with day, month, both or none: ').lower()
                if filters not in FILTERS: 
                    #handels random input, loops back to getting filter
                    print('Please enter valid information!')
                    print('choose one of the four options')
                    print('(day, month, both or none)')
                    print('='*60)
                    continue
                elif filters=='both':
                    month = input('Please choose a month: (Jan,Feb,Mar,Apr,May,Jun) \t').lower()
                    day= input("Please choose the day: (Saturday, Sunday,...)\t").lower()
                    if month not in MONTHS or day not in DAYS: 
                        #handles wrong input from user, loops back to choosing a filter and resets variables
                        print('We dont\'t have data for that!')
                        print('Choose one of the listed months and make sure your spelling is correct!')
                        print('='*60)
                        month,day='all','all'
                        continue
                elif filters == 'day':
                    day= input("Please choose the day: (Saturday, Sunday,...)\t").lower()
                    if day not in DAYS: 
                        #handles wrong input from user
                        print('Please type the day as suggested!\n(Saturday, Sunday,...)')
                        print('='*60)
                        day='all'
                        continue
                elif filters == 'month':
                    month = input('Please choose a month: (Jan,Feb,Mar,Apr,May,Jun) \t').lower()
                    if month not in MONTHS: 
                        #handles wrong input from user
                        print('We dont\'t have data for that! Choose one of the listed months!')
                        print('='*60)
                        month='all'
                        continue
                elif filters == 'none':
                    print('OK, let\'s get all the data for {}!'.format(city))
                break
        break

    print('-'*40)
    return city, month, day

    
def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour']=df['Start Time'].dt.hour
    
    # filter by month if applicable
    if month != 'all': 
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    return df
    


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print("The most common month: ", df['month'].mode()[0])
    # display the most common day of week
    print("The most common day: ",df['day_of_week'].mode()[0])
    # display the most common start hour
    print("The most common start hour: ",df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
     
    df['trip']=df["Start Station"]+df['End Station']
    
    # display most commonly used start station
    print("Most common START station: ", df['Start Station'].mode()[0])
    # display most commonly used end station
    print("Most common END station: ", df['End Station'].mode()[0])
    # display most frequent combination of start station and end station trip
    print("\nMost frequent trip is {}!".format(df['trip'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    #calculatiing the travel time in a new column
    df['travel_time'] = pd.to_datetime(df['End Time']) - pd.to_datetime(df["Start Time"])
    # display total travel time
    print("Total travel time: ", df['travel_time'].sum() )
    # display mean travel time
    print("The mean travel time: ",df['travel_time'].mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def user_stats(df):
    """Displays statistics on bikeshare users."""
    
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('User type values:\n', df['User Type'].value_counts())
    # Display counts of each gender if it's available in the dataframe
    if "Gender" in df.columns:
        print('\nUser gender:\n',df['Gender'].value_counts())
    # Display earliest, most recent, and most common year of birth if available in the dataframe
    if "Birth Year"in df.columns:
        print('\nEarliest year of birth: ', int(df['Birth Year'].min()))
        print('Most recent year of birth: ', int(df['Birth Year'].max()))
        print('Most common year of birth: ', int(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    
def dispaly_raw_data(df):
    """
    Asks user whether to choose to see raw data or not
       
    """
    while True:
        raw_data=input('Would you like to see a sample of the data? Enter yes or no.\n' ).lower()
        if raw_data=='yes': 
            print(df.sample(n=5))
            print('-'*40)
        else:
             break
def display_raw_data_modified(df):
    while True:
        display_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        if display_data.lower() != 'yes':
            break
        print(tabulate(df_default.iloc[np.arange(0+i,5+i)], headers ="keys"))
        i+=5
    
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        dispaly_raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
if __name__ == "__main__":
	main() 
print("\n\t END OF PROGRAM!\nThank you for stopping by!")
